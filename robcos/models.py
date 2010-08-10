from appengine_django import models
from google.appengine.ext import db

class Page(models.BaseModel):
  path = db.StringProperty(required=True)
  title = db.StringProperty(required=False)
  description = db.StringProperty(required=False)
  keywords = db.StringProperty(required=False)
  
  def by_path(path):
    pages = Page.all().filter('path = ', path).fetch(1)
    if len(pages) < 1:
        page = Page(path = path)
        page.put()
        return page
    return pages[0]

  by_path = staticmethod(by_path)
