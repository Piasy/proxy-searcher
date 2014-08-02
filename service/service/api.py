#!/usr/bin/env python
#-*- coding: utf-8 -*-
import service.dynamic_proxy
import json, time, thread

def get_proxy():
    flog = open('service/log.json', 'r')
    log = json.loads(flog.read())
    flog.close()
    if (not log) or time.time() - log["lastupdate"] > 3600:
        thread.start_new_thread(service.dynamic_proxy.get_proxies, ())
    fpro = open('service/proxies.json', 'r')
    ret = fpro.read()
    fpro.close()
    return ret

if __name__ == "__main__":
    print get_proxy()
    
