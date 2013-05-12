from Entity import Entity
import wolframalpha
import imdb

class Actor(Entity):
	""" Entity representation for Entity called Actor. """
	def get_results(self,query):
		result = self.get_facts(query);
		print result;
		#self.get_list_of_movies(query);

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

	def get_list_of_movies(self,query):
		ia = imdb.IMDb();
		person = ia.search_person(query);
		required_person = ia.get_person(person[0].personID);
		titles = required_person.get_titlesRefs();
		for title in titles:
			print title;