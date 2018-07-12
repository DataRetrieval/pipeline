#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =============================================================================

import json

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# =============================================================================

class SSLProxies(object):
    """Extract proxies from sslproxies.org"""

    BASE_URL = 'https://www.sslproxies.org/'

    @classmethod
    def fetch(cls, user_agent='Mozilla/5.0'):
        """Extract list of proxies"""
        headers = {'User-Agent': user_agent}
        response = requests.get(cls.BASE_URL, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.select('#proxylisttable > tbody > tr')
        proxies = set()
        for row in rows:
            cells = row.find_all('td')
            ip_address = cells[0].get_text()
            port = cells[1].get_text()

            proxy = '{ip}:{port}'.format(ip=ip_address, port=port)
            proxies.add(proxy)
        return proxies

# -----------------------------------------------------------------------------

class USProxy(object):
    """Extract proxies from us-proxy.org"""

    BASE_URL = 'https://www.us-proxy.org/'

    @classmethod
    def fetch(cls, user_agent='Mozilla/5.0'):
        """Extract list of proxies"""
        headers = {'User-Agent': user_agent}
        response = requests.get(cls.BASE_URL, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.select('#proxylisttable > tbody > tr')
        proxies = set()
        for row in rows:
            cells = row.find_all('td')
            ip_address = cells[0].get_text()
            port = cells[1].get_text()

            proxy = '{ip}:{port}'.format(ip=ip_address, port=port)
            proxies.add(proxy)
        return proxies
        
# -----------------------------------------------------------------------------

class FreeProxyList(object):
    """Extract proxies from free-proxy-list.net"""

    BASE_URL = 'https://www.free-proxy-list.net/'

    @classmethod
    def fetch(cls, user_agent='Mozilla/5.0'):
        """Extract list of proxies"""
        headers = {'User-Agent': user_agent}
        response = requests.get(cls.BASE_URL, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.select('#proxylisttable > tbody > tr')
        proxies = set()
        for row in rows:
            cells = row.find_all('td')
            ip_address = cells[0].get_text()
            port = cells[1].get_text()

            proxy = '{ip}:{port}'.format(ip=ip_address, port=port)
            proxies.add(proxy)
        return proxies
        
# =============================================================================

def main():
    """Entry-point"""
    ua = UserAgent()
    providers = [SSLProxies, USProxy, FreeProxyList]
    proxies = set()
    for provider in providers:
        proxies |= provider.fetch(ua.random)
    print(json.dumps({'proxies': list(proxies)}))

# -----------------------------------------------------------------------------

if __name__ == '__main__':
    main()

# END =========================================================================
