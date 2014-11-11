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

  @cherrypy.expose
  def index(self):
    template = templates.get('index.html')
    return template.render()


  @cherrypy.expose
  @cache.cache_suggest
  def suggest(self, *args, **kwargs):
    query = kwargs.get('query', None)
    if query:
      response = suggest.local_db(query)
      if not response:
        response = suggest.freebase(query)
      if not response:
        response = suggest.dbpedia(query)
      if response:
        return {'result': response}
    return {'result': []}


  @cherrypy.expose
  def search(self, *args, **kwargs):
    query = kwargs.get('query', None)
    tag = kwargs.get('tag', None).lower()
    if not query:
      query = kwargs.get('searchTerm', None)
    if query:
      if tag == "film director":
        tag = "director"
      elif tag == "film actor":
        tag = "actor"
      elif tag in ['musical group', 'guitarist', 'musician', 'film score artist', 'alternative artist']:
        tag = 'Artist'
      elif tag in ['composition', 'cusical Recording']:
        tag = 'Track'
      elif tag in ['musical album', 'musical release']:
        tag = 'Album'
      elif not tag:
        try:
          tag = suggest.find_entity_locally(query)['tag']
        except:
          tag = 'Untaggedentity'
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
      return 'Please specify a query'


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
