#!/usr/bin/env python
#-*- coding: utf-8 -*-
import urllib2
import re, json, time, parsers

def get_self_ip():
    try:
        data = urllib2.urlopen('http://20140507.ip138.com/ic.asp').read()
        pp = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        res = re.findall(pp, data)
        if res:
            return res[0]
    except Exception,ex:
        return "0.0.0.0"

def available(ip, port):
    org = get_self_ip()
    proxy = urllib2.ProxyHandler({'http':'http://' + ip + ':' + port + '/'})
    opener = urllib2.build_opener(proxy)
    changed = org
    try:
        data = opener.open('http://20140507.ip138.com/ic.asp').read()
        pp = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        res = re.findall(pp, data)
        if res:
            changed = res[0]
    except Exception,ex:
        changed = org
    return changed != org

def get_proxies():
    pros = []
    ava_pro = []
    #itmop
    try:
        html = urllib2.urlopen('http://www.itmop.com/proxy/').read()
        pros += parsers.parse_itmop(html)
    except Exception,ex:
        print Exception, ":", ex

    """
    #proxylists
    for i in range(1, 11):
        url = 'http://www.freeproxylists.net/zh/?pr=HTTP&u=80&page=' + str(i)
        html = urllib2.urlopen(url).read()
        pros += parsers.parse_itmop(html)
        time.sleep(2)
    """

    #kunpeng
    try:
        html = urllib2.urlopen('http://www.site-digger.com/html/articles/20110516/proxieslist.html').read()
        pros += parsers.parse_kunpeng(html)
    except Exception,ex:
        print Exception, ":", ex

    #comru 3464
    html = urllib2.urlopen('http://www.3464.com/data/Proxy/http/').read()
    pros += parsers.parse_comru_3464(html)
    for i in range(1, 9):
        try:
            url = 'http://proxy.com.ru/list_' + str(i) + '.html'
            html = urllib2.urlopen(url).read()
            pros += parsers.parse_comru_3464(html)
            time.sleep(2)
        except Exception,ex:
            print Exception, ":", ex

    urllib2.socket.setdefaulttimeout(20)
    for ip, port in pros:
        if available(ip, port):
            print "ava: " + ip + ":" + port
            one = {}
            one['ip'] = ip
            one['port'] = port
            ava_pro.append(one)
        #else:
        #    print "none ava: " + ip + ":" + port
    print len(ava_pro)
    fpro = open('service/service/proxies.json', 'w')
    fpro.write(json.dumps(ava_pro))
    fpro.close()

    flog = open('service/service/log.json', 'w')
    nlog = {}
    nlog["lastupdate"] = time.time()
    flog.write(json.dumps(nlog))
    flog.close()

if __name__ == "__main__":
    print get_proxies()
