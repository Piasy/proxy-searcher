#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.http import HttpResponse
import service.api

def api_available(request):
	return HttpResponse(service.api.get_proxy())

def hello(request):
	return HttpResponse("Hello world!")