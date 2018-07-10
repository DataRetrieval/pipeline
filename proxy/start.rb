#!/usr/bin/env ruby

# frozen_string_literal: true

require 'erb'
require 'socksify/http'
require 'logger'

$logger = Logger.new(STDOUT, Logger::DEBUG)

module Service
  class Base
    attr_reader :host
    attr_reader :port

    def self.spawn(*args)
      $logger.debug "Running: #{args.join(' ')}"
      child = Process.fork { exec args.join(" ") }
      Process.detach(child)
    end
    
    def initialize(host, port)
      @host = host
      @port = port
    end

    def name
      self.class.name.downcase.split('::').last
    end

    def start
      ensure_directories
      $logger.info "Starting #{name}: #{host}:#{port} ..."
    end
    
    def stop
      $logger.info "Stopping #{name}: #{host}:#{port} ..."
      if File.exists?(pid_file)
        pid = File.read(pid_file).strip.to_i
        begin
          Process.kill('SIGINT', pid)
        rescue => error
          $logger.warn "Failed to kill #{name} on #{host}:#{port}: #{error.message}"
        end
      else
          $logger.info "#{name} on #{host}:#{port} is not running."
      end
    end
    
    def restart
      stop
      sleep 5
      start
    end

    def ensure_directories
      %w{lib run log}.each do |dir|
        path = "/var/#{dir}/#{name}"
        Dir.mkdir(path) unless Dir.exists?(path)
      end
    end

    def data_directory
      "/var/lib/#{name}"
    end

    def pid_file
      "/var/run/#{name}/#{port}.pid"
    end

    def executable
      `which #{name}`.strip
    end
    
    def compile_config(template, output)
      template = File.read(template)
      File.write(output, ERB.new(template).result(binding))
    end
  end


  class Tor < Base
    attr_reader :new_circuit_period
    attr_reader :max_circuit_dirtiness
    attr_reader :circuit_build_timeout

    def initialize(host: '127.0.0.1', port: 9050)
      @host = host
      @port = port
      
      @new_circuit_period = ENV['NEW_CIRCUIT_PERIOD'] || 120
      @max_circuit_dirtiness = ENV['MAX_CIRCUIT_DIRTINESS'] || 600
      @circuit_build_timeout = ENV['CIRCUIT_BUILD_TIMEOUT'] || 60
    end

    def data_directory
      "#{super}/#{port}"
    end

    def start
      super
      compile_config('/etc/tor/torrc.erb', "/etc/tor/torrc.#{port}")
      self.class.spawn(executable, "-f /etc/tor/torrc.#{port}")
    end
    
    def working?
      uri = URI.parse('http://icanhazip.com')
      Net::HTTP.SOCKSProxy(host, port).start(uri.host, uri.port) do |http|
        http.get(uri.path).code == 200
      end
    rescue
      false
    end
  end

  class HAProxy < Base
    attr_reader :backends
    attr_reader :monitor_port
    attr_reader :monitor_username
    attr_reader :monitor_password

    def initialize(host: '127.0.0.1', port: 5566)
      @host = ENV['HAPROXY_HOST'] || host
      @port = ENV['HAPROXY_PORT'] || port
      
      @monitor_port = ENV['HAPROXY_MONITOR_PORT'] || 2090
      @monitor_username = ENV['HAPROXY_MONITOR_USERNAME'] || 'admin'
      @monitor_password = ENV['HAPROXY_MONITOR_PASSWORD'] || 'admin'

      @backends = []
    end

    def start
      super
      compile_config('/etc/haproxy/haproxy.cfg.erb', '/etc/haproxy/haproxy.cfg')
      self.class.spawn(executable, '-f /etc/haproxy/haproxy.cfg')
    end

    def add_backend(backend)
      @backends << {
        name: "#{backend.host}:#{backend.port}", 
        host: backend.host, 
        port: backend.port
      }
    end
  end

  class Privoxy < Base
    attr_reader :socks_proxies

    def initialize(host: '0.0.0.0', port: 8118)
      @host = ENV['PRIVOXY_HOST'] || host
      @port = ENV['PRIVOXY_PORT'] || port

      @socks_proxies = []
    end

    def start
      super
      compile_config('/etc/privoxy/privoxy.cfg.erb', '/etc/privoxy/privoxy.cfg')
      self.class.spawn(executable, "--no-daemon", '/etc/privoxy/privoxy.cfg')
    end
    
    def add_socks_proxy(socks_proxy)
      @socks_proxies << {
        host: socks_proxy.host, 
        port: socks_proxy.port
      }
    end
  end
end

proxies = []

haproxy = Service::HAProxy.new
tor_instances = Integer(ENV['TOR_INSTANCES'] || 20)
1000.upto(1000 + tor_instances) do |port|
  proxy = Service::Tor.new(host: '127.0.0.1', port: port)
  haproxy.add_backend(proxy)
  proxy.start
  proxies << proxy
end
haproxy.start

privoxy = Service::Privoxy.new
privoxy.add_socks_proxy(haproxy)
privoxy.start

healthcheck_timeout = Integer(ENV['HEALTHCHECK_TIMOUT'] || 60)
sleep healthcheck_timeout
loop do
  $logger.info "Testing proxies ..."
  proxies.each do |proxy|
    $logger.info "Testing proxy #{proxy.host}:#{proxy.port} ..."
    proxy.restart unless proxy.working?
    $logger.info "Sleeping for #{tor_instances} seconds ..."
    sleep tor_instances
  end

  $logger.info "Sleeping for #{healthcheck_timeout} seconds ..."
  sleep healthcheck_timeout
end
