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
