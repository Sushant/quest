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

class Film(Entity):
  """ Entity representation for Entity called Film. """

  ## Overriding the get_results method of base class.
  @cache.cache_results('film')
  def get_results(self,query):
    results = {}

    infobox = self.get_facts(query)
    if infobox:
      results['infobox'] = infobox
    results['lists'] = []
    movies = self.get_list_of_similar_movies_from_freebase(query)
    if movies:
      results['lists'].append(movies)

    actors = self.get_list_of_actors(query)
    if actors:
      results['lists'].append(actors)

    return results
    #results['Similar Actors'] = self.get_list_of_similar_people(query)
    #results['Characters Portrayed'] = self.get_list_of_characters_portrayed(query)
    #return results


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
  def get_facts(self,query):
    client = wolframalpha.Client(Entity.wolframalpha_key)
    infobox = {}
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
          elif r.title.lower() == 'Basic movie information'.lower():
            lines = r.text.split('\n')
            basic_info = {}
            for line in lines:
              pair = line.split(' | ')
              basic_info[pair[0]] = pair[1]
            infobox['basic_info'] = basic_info
          elif r.title.lower() == 'Box office performance'.lower():
            lines = r.text.split('\n')
            box_office_info = {}
            for line in lines:
              pair = line.split(' | ')
              box_office_info[pair[0]] = pair[1]
            infobox['box_office_info'] = box_office_info  
          elif r.title.lower() == 'Cast'.lower():
            lines = r.text.split('\n')
            cast_info = {}
            for line in lines:
              pair = line.split(' | ')
              cast_info[pair[0]] = pair[1]
            infobox['cast_info'] = cast_info
          elif r.title.lower() == 'Academy Awards and nominations'.lower():
            lines = r.text.split('\n')
            awards_info = {}
            for line in lines:
              pair = line.split(' | ')
              awards_info[pair[0]] = pair[1]
            infobox['awards_info'] = awards_info
      except Exception as e:
        continue
    return infobox


  ## API call to IMDB for list of movies. Very slow.
  def get_list_of_movies_from_IMDB(self,query):
    ia = imdb.IMDb()
    person = ia.search_person(query)
    required_person = ia.get_person(person[0].personID)
    titles = required_person.get_titlesRefs()
    movie_dictionary = {}
    for title in titles:
      movie_dictionary[str(title)] = "To be encoded!!!!"
    return movie_dictionary


  ## API call to freebase for list of movies. Response is quicker than IMDB API.
  def get_list_of_similar_movies_from_freebase(self, query):
    movies = {'title': 'Similar Movies'}
    service_url = 'https://www.googleapis.com/freebase/v1/search'
    params = {
        'query': query,
        'filter': '(all type:/film/film)',
        'limit': 30,
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
      if image:
        movie_items.append({'title': result['name'], 'url': quest_url, 'image': image})
      else:
        movie_items.append({'title': result['name'], 'url': quest_url})
    movies['items'] = movie_items
    return movies


  ## API call to freebase to get list of similar people.
  def get_list_of_actors(self,query):
    actors = {'title': 'Cast'}
    service_url = 'https://www.googleapis.com/freebase/v1/search'
    params = {
        'query': query,
        'filter': '(all type:/people/person notable:actor)',
        'limit': 20,
        'key': Entity.freebase_key
        }
    url = service_url + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())

    actor_items = []
    for result in response['result']:
      image = self.get_image(result['name'])
      quest_url = '/search?query=' + result['name'] + '&tag=actor'
      if image:
        actor_items.append({'title': result['name'], 'url': quest_url, 'image': image})
      else:
        actor_items.append({'title': result['name'], 'url': quest_url})
    actors['items'] = actor_items
    return actors


if __name__ == '__main__':
  film = Film()
  import pprint
  pp = pprint.PrettyPrinter(indent=2)
  pp.pprint(film.get_results('Lagaan'))
