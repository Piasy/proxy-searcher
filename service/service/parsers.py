#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sgmllib, re, urllib

class ITMOPParser(sgmllib.SGMLParser):
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
        self.field = "P"
        
    def end_p(self):
        self.field = "NONE"

class ComRuParser(sgmllib.SGMLParser):
    field = "NONE"
    wanted = False
    inner_html = ""
    proxies = []

    def handle_data(self, data):
        #handle data in the current field
        if self.field == "TD" and self.wanted:
            self.inner_html += data + " "

    def start_tr(self, attrs):
        #get in the td field
        self.field = "TR"
        self.wanted = True
                
    def end_tr(self):
        #get out the td field
        self.field = "NONE"
        self.wanted = False
        pp = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} \d{1,5}')
        res = re.findall(pp, self.inner_html)
        if res:
            ss = res[0].split(' ')
            self.proxies.append((ss[0], ss[1]))
        #print self.inner_html
        self.inner_html = ""

    def start_td(self, attrs):
        self.field = "TD"
        
    def end_td(self):
        self.field = "NONE"

def parse_kunpeng(html):
    ret = []
    pp = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}')
    res = re.findall(pp, html)
    if res:
        for addr in res:
            ss = addr.split(':')
            ret.append((ss[0], ss[1]))
    return ret

def parse_proxy_lists(html):
    ret = []
    pp = re.compile(r'(IPDecode\(")(.*)("\)</script></td><td align="center">)(\d{1,5})')
    res = re.findall(pp, html)
    if res:
        for addr in res:
            ret.append((urllib.unquote(addr[1]), addr[3]))
    return ret

def parse_itmop(html):
    parser = ITMOPParser()
    parser.feed(html)
    return parser.proxies

def parse_comru_3464(html):
    parser = ComRuParser()
    parser.feed(html)
    return parser.proxies

if __name__ == "__main__":
    print parse_comru_3464(open('testdata/3464.htm').read())
