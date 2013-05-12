import os
import sys
import json
import urllib
import requests
import cherrypy
import traceback


CWD = os.path.dirname(__file__)

path = os.path.abspath(os.path.join(CWD, '..'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

from lib import params
from lib import templates

class Root:

  @cherrypy.expose
  def index(self):
    template = templates.get('index.html')
    return template.render()


  @cherrypy.expose
  def suggest(self, *args, **kwargs):
    query = kwargs.get('query')
    callback = kwargs.get('callback', None)
    response = self.suggest_freebase(query)
    if not response:
      response = self.suggest_dbpedia(query)
    if response:
      response = {'result': response}
      if callback:
        return callback + '('+ json.dumps(response) + ')'
      return json.dumps(response)
    else:
      response = {'result': []}
      if callback:
        return callback + '('+ json.dumps(response) + ')'
      return json.dumps(response)


  def suggest_freebase(self, query):
    url = params.FREEBASE_SUGGEST_URL + urllib.quote(query)
    try:
      response = requests.get(url)
      results = json.loads(response.text)
      if results['status'] == '200 OK':
        results = results['result']
        resp = []
        results = sorted(results, key=lambda k: k['score'], reverse=True)
        results = results[:4]
        for r in results:
          try:
            #if r['name'].lower() == query.lower():
              resp.append({
                  'name': r['name'],
                  'tag': r['notable']['name'],
                  'score': r['score']
               })
          except:
            continue
        # Remove duplicate dicts
        resp = [dict(t) for t in set([tuple(d.items()) for d in resp])]
        resp = sorted(resp, key=lambda k: k['score'], reverse=True)
        return resp
    except Exception as e:
      print traceback.format_exc()
    return None


  def suggest_dbpedia(self, query):
    url = params.DBPEDIA_SUGGEST_URL + urllib.quote(query)
    try:
      header = {'accept': 'application/json'}
      response = requests.get(url, headers=header)
      results = json.loads(response.text)['results']
      resp = []
      for r in results:
        try:
          if r['label'].lower() == query.lower():
            resp.append({
                'name': r['label'],
                'tag': r['classes'][0]['label'].capitalize(),
                'score': 0
             })
        except:
          continue
      resp = [dict(t) for t in set([tuple(d.items()) for d in resp])]
      return resp
    except Exception as e:
      print traceback.format_exc()
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
