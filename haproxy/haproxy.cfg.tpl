#---------------------------------------------------------------------
# Global settings
#---------------------------------------------------------------------
global
    chroot      /var/lib/haproxy
    pidfile     /var/run/haproxy.pid
    maxconn     4000
    user        haproxy
    group       haproxy
    daemon

#---------------------------------------------------------------------
# common defaults that all the 'listen' and 'backend' sections will
# use if not designated in their block
#---------------------------------------------------------------------
defaults
    mode                    http
    option http-server-close
    option                  redispatch
    retries                 3
    timeout http-request    10s
    timeout queue           1m
    timeout connect         10s
    timeout client          1m
    timeout server          1m
    timeout http-keep-alive 10s
    timeout check           10s
    maxconn                 3000

#---------------------------------------------------------------------
# Statistics page
#---------------------------------------------------------------------
listen stats
	bind :{{ HAPROXY_MONITOR_PORT | default(2090) }}
	mode http
	stats enable  # Enable stats page
	stats hide-version  # Hide HAProxy version
	stats realm "HAProxy Statistics"  # Title text for popup window
	stats uri /  # Stats URI
	stats auth {{ HAPROXY_MONITOR_USERNAME | default('admin') }}:{{ HAPROXY_MONITOR_PASSWORD | default('admin') }}  # Authentication credentials
  
#---------------------------------------------------------------------
# main frontend which proxys to the backends
#---------------------------------------------------------------------
frontend main
    bind *:{{ HAPROXY_PORT | default(5566) }}
    {% for backend in (HAPROXY_BACKENDS | from_json).keys() %}
    use_backend {{ backend }}
    {% endfor %}

#---------------------------------------------------------------------
# round robin balancing between the various backends
#---------------------------------------------------------------------
{% for backend, servers in (HAPROXY_BACKENDS | from_json).items() %}
backend {{ backend }}
    balance     {{ HAPROXY_BALANCE_ALGORITHM }}
	{% for server in servers %}
    {% set host, port = server.split(':') %}
    server {{ host }}:{{ port }} {{ host }}:{{ port }} check
	{% endfor %}
{% endfor %}
