from django import template
from google.appengine.ext.webapp import template as app_template
import os
import re
import tokenize
import StringIO

register = template.Library()

def do_item(parser, token):
    tag_name, menupath, title = map(strip, token.split_contents())
    assert menupath[0] == "/", "Menu path must begin with / but was '%s'" % menupath
    assert menupath == '/' or menupath[-5:] == ".html", "Menu path must end with .html but was '%s'" %  menupath[-5:]
    bits = menupath.split('/')[1:]
    level = len(bits)
    return MenuNode("menu.html", { 'menupath': menupath, 'title': title, 
        'bits': bits,'level': level})

def strip(header):
  if header[0] == header[-1] == '"':
    header = header.strip('"')
  if header[0] == header[-1] == '\'':
    header = header.strip('\'')
  return header
 
def parent(url):
  bits =  url.split('/')
  if len(bits)>2:
    return bits[1]
  return None

def is_child(menu, current):
  #current /escursioni
  #menu /escursioni/trekking.html
  menu = menu.replace('.html', '') 
  current = current.replace('.html', '') 
  bits = menu.split('/');
  if(bits[-2] == current[1:]):
    return True
  return False

def is_ancestor(menu, current):
  #current /escursioni/trekking
  #menu /escursioni
  menu = menu.replace('.html', '') 
  current = current.replace('.html', '') 
  bits = menu.split('/');
  return current.find(menu) == 0

def is_sibling(menu, current):
  #current /escursioni/camminare.html
  #menu /escursioni/trekking.html
  if(parent(menu) == parent(current)):
    return True
  return False

class MenuNode(template.Node):
  
  def __init__(self, template_name, context):
    self.template_name = template_name
    self.context = context

  def render(self, context):
    context.update(self.context)
    path = context['path'];
    menupath = context['menupath'];
    if(path == '/index.html'):
      context['path'] = '/'
    if(context['level'] == 1 or 
        is_child(menupath, path) or 
        is_sibling(menupath, path) 
        ):
      context['visible'] = True
    else:
      context['visible'] = False
    if menupath != '/' and is_ancestor(menupath, path):
      context['anchorClass'] = "navPath"
    else:
      context['anchorClass'] = "nav"

    return app_template.render(os.path.join(os.path.dirname(__file__), 
      self.template_name), context)

register.tag('menuitem', do_item)
