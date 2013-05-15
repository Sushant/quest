import json
import pymongo


def cache_suggest(func):
  def __cache(*args, **kwargs):
    response = {'result': []}
    try:
      _conn = pymongo.MongoClient()
      _db = _conn['quest']
    except:
      pass

    callback = kwargs.get('callback', None)
    if callback:
      del kwargs['callback']

    try:
      query = kwargs.get('query', None)
      if query and _db:
        response = _db['suggest'].find_one({'_id': query.lower()})['matches']
    except:
      response = func(*args, **kwargs)
      if query and response != {'result': []}:
        try:
          doc = {'_id': query.lower(), 'matches': response}
          _db['suggest'].save(doc)
        except:
          pass

    if callback:
      return callback + '('+ json.dumps(response) + ')'
    return json.dumps(response)
  return __cache


def cache_results(tag):
  def cache_wrapper(func):
    def __cache(*args):
      response = {}
      try:
        query = args[1]
      except:
        query = None

      try:
        _conn = pymongo.MongoClient()
        _db = _conn['quest']
      except:
        pass

      try:
        if query and tag and _db:
          response = _db['results'].find_one({'_id': query.lower(), 'tag': tag})['matches']
          print 'Cache hit for', query, ' and ', tag
      except:
        response = func(*args)
        if query and tag and response:
          try:
            doc = {'_id': query.lower(), 'tag': tag, 'matches': response}
            _db['results'].save(doc)
            print 'Saved: ', doc
          except:
            pass

      return response
    return __cache
  return cache_wrapper
