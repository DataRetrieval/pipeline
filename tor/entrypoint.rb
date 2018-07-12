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
      
      @new_circuit_period = ENV['TOR_NEW_CIRCUIT_PERIOD'] || 120
      @max_circuit_dirtiness = ENV['TOR_MAX_CIRCUIT_DIRTINESS'] || 600
      @circuit_build_timeout = ENV['TOR_CIRCUIT_BUILD_TIMEOUT'] || 60
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
end

proxies = []
tor_host = ENV['TOR_HOST'] || '0.0.0.0'
tor_ports = ENV['TOR_PORT_RANGE'] || '1000-1025'
Range.new(*tor_ports.split('-').map(&:to_i)) do |port|
  proxy = Service::Tor.new(host: tor_host, port: port)
  proxy.start
  proxies << proxy
end

healthcheck_timeout = Integer(ENV['TOR_HEALTHCHECK_TIMOUT'] || 60)
loop do
  sleep healthcheck_timeout
  
  $logger.info "Testing proxies ..."
  proxies.each do |proxy|
    $logger.info "Testing proxy #{proxy.host}:#{proxy.port} ..."
    proxy.restart unless proxy.working?
  end
end
