import json
import urllib
import pymongo
import requests
import traceback

from lib import params

def local_db(query):
  try:
    _conn = pymongo.MongoClient()
    _db = _conn['quest']
  except:
    pass

  try:
    resp = []
    if query and _db:
      response = _db['results'].find({'_id': {'$regex': query.lower()}})
      for r in response:
        resp.append({
          'name': r['matches']['infobox']['title'],
          'tag': r['tag'].capitalize(),
          'score': 0
        })
      return resp
  except:
    pass

def find_entity_locally(query):
  try:
    _conn = pymongo.MongoClient()
    _db = _conn['quest']
  except:
    pass

  try:
    if query and _db:
      response = _db['results'].find_one({'_id': query.lower()})
      return {
        'name': response['matches']['infobox']['title'],
        'tag': response['tag'].capitalize(),
        'score': 0
      }
  except:
    return None


def freebase(query):
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


def dbpedia(query):
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
