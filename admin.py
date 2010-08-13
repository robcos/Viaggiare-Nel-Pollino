#!/usr/bin/python2.4
#
# Copyright 2010 Google Inc.
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
from django.http import HttpResponseNotFound

# Python
import logging
import os
import re
import datetime
from robcos.models import Page
from robcos.models import Node


def pages(request):
  path = 'pages.html' 
  if request.method == 'POST':
    pages = Page.all();
    for page in pages:
      title = 'title[' + str(page.key()) + ']'
      description = 'description[' + str(page.key()) + ']'
      keywords = 'keywords[' + str(page.key()) + ']'
      page.title = request.POST.get(title)
      page.keywords = request.POST.get(keywords)
      page.description = request.POST.get(description)
      page.put()
    return HttpResponseRedirect('/admin/pages.html')
  else:
    response = shortcuts.render_to_response(path, {'pages': Page.all() })
  return response

def thanks(request):
  return shortcuts.render_to_response('thanks.html', {})

def edit(request):
  nodepath = request.path.replace('/admin/edit', '')
  node = Node.by_path(nodepath)
  if request.method == 'GET':
    return shortcuts.render_to_response('edit.html', {
      'node': node
    })
  if request.method == 'POST':
    node.title = request.POST.get('node.title')
    node.content = request.POST.get('node.content')
    node.put()
    return HttpResponseRedirect(request.path)
