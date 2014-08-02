#!/usr/bin/env python
#-*- coding: utf-8 -*-
import service.dynamic_proxy
import json

def get_proxy():
	return json.dumps(service.dynamic_proxy.get_proxies())

if __name__ == "__main__":
	print get_proxy()
