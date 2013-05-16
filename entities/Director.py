from Entity import Entity
import wolframalpha
import imdb
import json
import urllib
import os
import sys
CWD = os.path.dirname(__file__)

path = os.path.abspath(os.path.join(CWD, '..'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

from lib import params
from lib import cache
from lib import threadpool


class Director(Entity):
  """ Entity representation for Entity called Director. """

  ## Overriding the get_results method of base class.
  @cache.cache_results('director')
  def get_results(self,query):
    results = {}
    infobox = {}
    movies = {}
    directors = {}

    pool = threadpool.ThreadPool(3)
    pool.add_task(self.get_facts, query, infobox)
    pool.add_task(self.get_list_of_movies_from_freebase, query, movies)
    pool.add_task(self.get_list_of_similar_people, query, directors)
  
    pool.wait_completion()
    if infobox:
      results['infobox'] = infobox
    results['lists'] = []
    if movies:
      results['lists'].append(movies)
    if directors:
      results['lists'].append(directors)
    return results


  # Return format:
  #'infobox': {
  #       'title': String,
  #       'image': String (url),
  #       'basic_info': [
  #            { 'dob': 'String',
  #               'full name': 'String'}
  #       ],
  #       'summary': ['List of Strings']
  #  }
  def get_facts(self, query, infobox):
    client = wolframalpha.Client(Entity.wolframalpha_key)
    try:
      res = client.query(query)
    except Exception as e:
      print 'Failed to get facts from Wolfram|Alpha', str(e)
      return infobox
    for r in res:
      try:
        if r.title and r.text:
          image = self.get_image(query)
          if image:
            infobox['image'] = image
          if r.title.lower() == 'Input interpretation'.lower():
            infobox['title'] = r.text
          elif r.title.lower() == 'Basic information'.lower():
            lines = r.text.split('\n')
            basic_info = {}
            for line in lines:
              pair = line.split(' | ')
              basic_info[pair[0]] = pair[1]
            infobox['basic_info'] = basic_info
          elif r.title.lower() == 'Notable facts'.lower():
            lines = r.text.split('\n')
            summary = []
            for line in lines:
              if line != '...':
                summary.append(line)
            infobox['summary'] = summary
      except Exception as e:
        continue
    return infobox


  ## API call to IMDB for list of movies. Very slow.
  def get_list_of_movies_from_IMDB(self, query):
    ia = imdb.IMDb()
    person = ia.search_person(query)
    required_person = ia.get_person(person[0].personID)
    titles = required_person.get_titlesRefs()
    movie_dictionary = {}
    for title in titles:
      movie_dictionary[str(title)] = "To be encoded!!!!"
    return movie_dictionary


  ## API call to freebase for list of movies. Response is quicker than IMDB API.
  def get_list_of_movies_from_freebase(self, query, movies):
    movies['title'] = 'Movies'
    service_url = 'https://www.googleapis.com/freebase/v1/search'
    params = {
        'query': query,
        'filter': '(all type:/film/film)',
        'limit': 20,
        'key': Entity.freebase_key
        }
    try:
      url = service_url + '?' + urllib.urlencode(params)
      response = json.loads(urllib.urlopen(url).read())
    except Exception as e:
      return None

    movie_items = []
    for result in response['result']:
      image = self.get_image(result['name'])
      quest_url = '/search?query=' + result['name'] + '&tag=film'
      movie_items.append({'title': result['name'], 'url': quest_url, 'image': image})
      if image:
        movie_items.append({'title': result['name'], 'url': quest_url, 'image': image})
      else:
        movie_items.append({'title': result['name'], 'url': quest_url})
    movies['items'] = movie_items
    return movies


  ## API call to freebase to get list of similar people.
  def get_list_of_similar_people(self, query, directors):
    directors['title'] = 'Similar Directors'
    service_url = 'https://www.googleapis.com/freebase/v1/search'
    params = {
        'query': query,
        'filter': '(all type:/people/person practitioner_of:director)',
        'limit': 10,
        'key': Entity.freebase_key
        }
    try:
      url = service_url + '?' + urllib.urlencode(params)
      response = json.loads(urllib.urlopen(url).read())
    except Exception as e:
      return None

    director_items = []
    for result in response['result']:
      image = self.get_image(result['name'])
      quest_url = '/search?query=' + result['name'] + '&tag=director'
      if image:
        director_items.append({'title': result['name'], 'url': quest_url, 'image': image})
      else:
        director_items.append({'title': result['name'], 'url': quest_url})
    directors['items'] = director_items
    return directors


if __name__ == '__main__':
  director = Director()
  import pprint
  pp = pprint.PrettyPrinter(indent=2)
  pp.pprint(director.get_results('steven spielberg'))
