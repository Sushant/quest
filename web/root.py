import os
import sys
import json
import urllib
import cherrypy


CWD = os.path.dirname(__file__)

path = os.path.abspath(os.path.join(CWD, '..'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

from lib import suggest
from lib import params
from lib import templates
from lib import cache

class Root:

  def __init__(self):
    self.load_entities()


  def load_entities(self):
    sys.path.insert(1, params.ENTITIES_DIR)
    #library_list = []
    #print 'Loading entities...'

    #for f in os.listdir(params.ENTITIES_DIR):
    #  module_name, ext = os.path.splitext(f) # Handles no-extension files, etc.
    #  print module_name, ext
    #  if ext == '.py': # Important, ignore .pyc/other files.
    #    if module_name != '__init__':
    #      print 'imported module: %s' % (module_name)
    #      module = __import__(module_name)
    #      library_list.append(module)

    #return library_list

  @cherrypy.expose
  def index(self):
    template = templates.get('index.html')
    return template.render()


  @cherrypy.expose
  @cache.cache_suggest
  def suggest(self, *args, **kwargs):
    query = kwargs.get('query', None)
    if query:
      response = suggest.freebase(query)
      if not response:
        response = suggest.dbpedia(query)
      if response:
        return {'result': response}
    return {'result': []}

  @cherrypy.expose
  def search(self, *args, **kwargs):
    query = kwargs.get('query', None)
    tag = kwargs.get('tag', None)
    if tag == "Film Director":
      tag = "Director"

    try:
      module = __import__(tag.capitalize())
      _class = getattr(module, tag.capitalize())
      entity = _class()
      results = entity.get_results(query)
      results['query'] = query
      results['tag'] = tag
      template = templates.get('results.html')
      return template.render({'results': results})
    except Exception as e:
      print 'Error: ', e
      return None


if __name__ == '__main__':

  config = {
    'global': {
      'server.socket_host': "0.0.0.0",
            'server.socket_port': params.WEB_PORT,
            'server.thread_pool': 10,
            'engine.autoreload_on':False,
        },
        '/': {
            'tools.staticdir.root': params.WEB_DIR,
            'tools.sessions.on': True,
            'tools.sessions.timeout': 300,
            'tools.gzip.on': True,
        },
        '/images': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': "images",
        },
        '/css': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': "css",
        },
        '/js': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': "js",
        }
  }

  cherrypy.config.update(config['global'])
  app = cherrypy.tree.mount(Root(), config=config)


  try:
    cherrypy.engine.start()
    print 'Successfully started the Quest Panel'
    cherrypy.engine.block()
  except socket.error, fault:
    print 'Unable to start Quest Panel: ', fault
