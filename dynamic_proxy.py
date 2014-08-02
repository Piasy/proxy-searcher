import sgmllib, sys, os, string
import urllib, urllib2, json
import re

class MyHTMLParser(sgmllib.SGMLParser):
    field = "NONE"
    wanted = False
    proxies = []

    def handle_data(self, data):
        #handle data in the current field
        if self.field == "P" and self.wanted:
            p1 = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} \d{1,5}')
            p2 = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}')
            res1 = re.findall(p1, data)
            res2 = re.findall(p2, data)
            if res1:
                ss = res1[0].split(' ')
                self.proxies.append((ss[0], ss[1]))
            elif res2:
                ss = res2[0].split(':')
                self.proxies.append((ss[0], ss[1]))

    def start_div(self, attrs):
        #get in the td field
        self.field = "DIV"
        for name, value in attrs:
            if name == "id" and value == "NEW_INFO_LIST":
                self.wanted = True
                
    def end_div(self):
        #get out the td field
        self.field = "NONE"
        self.wanted = False

    def start_p(self, attrs):
        #
        self.field = "P"
        
    def end_p(self):
        #
        self.field = "NONE"

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
    ava_pro = []
    parser = MyHTMLParser()
    html = urllib2.urlopen('http://www.itmop.com/proxy/').read() #get html
    MyHTMLParser().feed(html)
    urllib2.socket.setdefaulttimeout(20)
    for ip, port in parser.proxies:
        if available(ip, port):
            print "ava: " + ip + ":" + port
            ava_pro.append((ip, port))
        else:
            print "none ava: " + ip + ":" + port
    return ava_pro

if __name__ == "__main__":
    print get_proxies()
