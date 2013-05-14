from Entity import Entity
import wolframalpha
import imdb
import json
import urllib

class Actor(Entity):
  """ Entity representation for Entity called Actor. """

  ## Overriding the get_results method of base class.
  def get_results(self,query):
    results = {};
    print query
    results['Facts'] = self.get_facts(query);
    #results['Movies'] = self.get_list_of_movies(query);
    results['Movies'] = self.get_list_of_movies_from_freebase(query);
    results['Similar Actors'] = self.get_list_of_similar_people(query);
    results['Characters Portrayed'] = self.get_list_of_characters_portrayed(query);
    return results;

  ## API call to wolfram alpha to get facts.
  def get_facts(self,query):
    client = wolframalpha.Client(Entity.wolframalpha_key);
    res = client.query(query);
    result_dictionary = {};
    for s in res:
      if str(s.title) != 'None' and str(s.text) != 'None':
        if str(s.title).lower() == "basic information": 
          temp_data = str(s.text).split('\n');
          temp_dict = {};
          for line in temp_data:
            temp_index = line.split('|');
            temp_dict[temp_index[0]] = temp_index[1];
          result_dictionary[s.title] = temp_dict;
        elif str(s.title).lower() == "notable facts":
          temp_data = str(s.text).replace("...","").split('\n');
          result_dictionary[s.title] = temp_data;
        else:
          result_dictionary[str(s.title)] = str(s.text);
    return result_dictionary;

  ## API call to IMDB for list of movies. Very slow.
  def get_list_of_movies_from_IMDB(self,query):
    ia = imdb.IMDb();
    person = ia.search_person(query);
    required_person = ia.get_person(person[0].personID);
    titles = required_person.get_titlesRefs();
    movie_dictionary = {};
    for title in titles:
      movie_dictionary[str(title)] = "To be encoded!!!!";
    return movie_dictionary;

  ## API call to freebase for list of movies. Response is quicker than IMDB API.
  def get_list_of_movies_from_freebase(self,query):
    service_url = 'https://www.googleapis.com/freebase/v1/search';
    params = {
        'query': query,
        'filter': '(all type:/film/film)',
        'limit': 30,
        'key': Entity.freebase_key
        }
    url = service_url + '?' + urllib.urlencode(params);
    response = json.loads(urllib.urlopen(url).read());
    movie_dictionary = {};
    for result in response['result']:
      movie = str(result['name']);
      movie_dictionary[movie] = "URL To Be Encoded!!!!!";
    return movie_dictionary;

  ## API call to freebase to get list of similar people.
  def get_list_of_similar_people(self,query):
    service_url = 'https://www.googleapis.com/freebase/v1/search';
    params = {
        'query': query,
        'filter': '(all type:/people/person practitioner_of:actor)',
        'limit': 10,
        'key': Entity.freebase_key
        }
    url = service_url + '?' + urllib.urlencode(params);
    response = json.loads(urllib.urlopen(url).read());
    people_dictionary = {};
    for result in response['result']:
      person = str(result['name']);
      people_dictionary[person] = "URL To Be Encoded!!!!!";
    return people_dictionary;

  ## Generating list of characters portrayed.
  def get_list_of_characters_portrayed(self,query):
    service_url = 'https://www.googleapis.com/freebase/v1/search';
    params = {
        'filter': '(all portrayed_by:\"'+query+'\")',
        'limit': 15,
        'key': Entity.freebase_key
        }
    url = service_url + '?' + urllib.urlencode(params);
    response = json.loads(urllib.urlopen(url).read());
    character_dictionary = {};
    for result in response['result']:
      character = str(result['name']);
      character_dictionary[character] = "URL To Be Encoded!!!!!";
    return character_dictionary;
