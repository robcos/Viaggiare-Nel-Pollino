from django import template
from google.appengine.ext.webapp import template as app_template
import os
import re
import tokenize
import StringIO

register = template.Library()

def do_local(parser, token):
    nodelist = parser.parse(('endbox',))
    parser.delete_first_token()
    tag_name, title, img, side, orientation = token.split_contents()
    title = strip(title) 
    img = strip(img) 
    side = strip(side) 
    orientation = strip(orientation) 
    if orientation == "vertical":
      height = "240"
      width = "180"
    else:
      height = "180"
      width = "240"
    #img = "http://farm5.static.flickr.com/" + img

    return FlickrNode(nodelist, title, None, img, side, width, height, "local_contentbox.html")


def do_flickr(parser, token):
    nodelist = parser.parse(('endbox',))
    parser.delete_first_token()
    tag_name, title, img, side, orientation = token.split_contents()
    title = strip(title) 
    img = strip(img) 
    side = strip(side) 
    orientation = strip(orientation) 
    photo_id = re.search('.*/(\d*)_.*', img).group(1)
    if orientation == "vertical":
      height = "240"
      width = "180"
    else:
      height = "180"
      width = "240"
    img = "http://farm5.static.flickr.com/" + img
    href = "http://www.flickr.com/photos/pollino/" + photo_id

    return FlickrNode(nodelist, title, href, img, side, width, height)

def do_smallbox(parser, token):
    nodelist = parser.parse(('endbox',))
    tag_name, header = token.contents.split(None,1)

    parser.delete_first_token()
    return SmallBoxNode(nodelist, header, "smallbox.html")

def do_snippet(parser, token):
    bits = token.split_contents()
    tag_name, snippet = bits[:2]
    if len(bits) > 2:
      title = bits[2]
    return SnippetNode(snippet, title=None)

def do_call(parser, token):
   """
   Loads a template and renders it with the current context.

   Example::

       {% call "foo/some_include" %}
       {% call "foo/some_include" with arg1 arg2 ... argn %}
   """
   bits = token.contents.split()
   if 'with' in bits: #has 'with' key
       pos = bits.index('with')
       argslist = bits[pos+1:]
       bits = bits[:pos]
   else:
       argslist = []
   if len(bits) != 2:
       raise template.TemplateSyntaxError, "%r tag takes one argument: the name of the template to be included" % bits[0]
   path = parser.compile_filter(bits[1])
   args = []
   kwargs = {}
   if argslist:
       for i in argslist:
           if '=' in i:
               a, b = i.split('=', 1)
               a = a.strip()
               b = b.strip()
               buf = StringIO.StringIO(a)
               keys = list(tokenize.generate_tokens(buf.readline))
               if keys[0][0] == tokenize.NAME:
                   kwargs[a] = parser.compile_filter(b)
               else:
                   raise template.TemplateSyntaxError, "Argument syntax wrong: should be key=value"
           else:
               args.append(parser.compile_filter(i))
   return SnippetNode(path, *args, **kwargs)




def do_contentbox(parser, token):
    nodelist = parser.parse(('endbox',))
    tag_name, header = token.split_contents()
    header = strip(header)
    parser.delete_first_token()
    return SmallBoxNode(nodelist, header, "contentbox.html")

def strip(header):
  if header[0] == header[-1] == '"':
    header = header.strip('"')
  if header[0] == header[-1] == '\'':
    header = header.strip('\'')
  return header
 
class FlickrNode(template.Node):
  def __init__(self, nodelist, title, href, src, side, width, height, template="flickr_contentbox.html"):
    self.nodelist = nodelist
    self.title = title
    self.href = href
    self.src = src
    self.side = side
    self.width = width
    self.height = height
    self.template = template

  def render(self, context):
    output = self.nodelist.render(context)
    return app_template.render(os.path.join(os.path.dirname(__file__), self.template),
        { "title": self.title, "href": self.href, "src": self.src, 
        "side": self.side, "height": self.height, "width" : self.width,
        "header": self.title, "content": output})

class SnippetNode(template.Node):
  def __init__(self, template_name, *args, **kwargs):
    self.snippet = template_name
    self.args = args
    self.kwargs = kwargs

  def render(self, context):
    d = {}
    args = d['args'] = []
    kwargs = d['kwargs'] = {}
    for i in self.args:
      args.append(i.resolve(context))
    for key, value in self.kwargs.items():
      kwargs[key] = d[key] = value.resolve(context)
    
    context.update(d)

    return app_template.render(os.path.join(os.path.dirname(__file__), 
      self.snippet), context)

class SmallBoxNode(template.Node):
  def __init__(self, nodelist, header, template):
    self.nodelist = nodelist
    self.header = header
    self.template = template

  def render(self, context):
    output = self.nodelist.render(context)
    return app_template.render(os.path.join(os.path.dirname(__file__), 
      self.template), { "header": self.header, "content": output})

register.tag('smallbox', do_smallbox)
register.tag('contentbox', do_contentbox)
register.tag('flickr', do_flickr)
register.tag('local', do_local)
register.tag('snippet', do_call)
