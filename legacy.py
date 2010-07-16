#!/usr/bin/python2.4
#
# Copyright 2009 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""A special handler file for rendering template files of various types."""

# AppEngine
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from django.template import TemplateDoesNotExist

import os

from google.appengine.api import users

from google.appengine.ext import db
from google.appengine.ext.db import djangoforms

import django
from django import http
from django import shortcuts
from django.http import HttpResponseRedirect

# Python
import logging
import os
import re
import datetime

def legacy(request):
  path = os.path.join(request.get_full_path()[1:])

  if path == "index.html":
    return HttpResponseRedirect("/")
  if path == "":
    path = "index.html"
  response = shortcuts.render_to_response(path, {})
  
  if re.match(".*\.jpe?g", path):
    response['Content-Type'] = 'image/jpeg'
    cache_headers(response)
  elif re.match(".*\.gif", path):
    response['Content-Type'] = 'image/gif'
    cache_headers(response)
  elif re.match(".*\.xml", path):
    response['Content-Type'] = 'application/atom+xml'
    cache_headers(response)
  elif re.match(".*\.css", path):
    response['Content-Type'] = 'text/css'
    cache_headers(response)
  else:
    response['Content-Type'] = 'text/html'
  return response
  
def cache_headers(response):
    return
    past = datetime.datetime.now() - datetime.timedelta(days=10)
    then = datetime.datetime.now() + datetime.timedelta(days=10)
    response['Last-Modified'] = past.ctime()
    response['Expires'] = then.ctime()
    response['Cache-Control'] = 'max-age=31536000'
