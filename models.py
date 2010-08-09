from google.appengine.ext import db

class Page(db.Model):
  title = db.StringProperty(required=True)
  path = db.StringProperty(required=True)
  
  def by_path(path, default_title='Pagina in allestimento'):
    pages = Page.all().filter('path = ', path).fetch(1)
    if len(pages) < 1:
      Page(path = path, title = default_title).put()
    pages = Page.all().filter('path = ', path).fetch(1)
    page = pages[0]
    return pages[0]

  by_path = staticmethod(by_path)
