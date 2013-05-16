import os
import sys
CWD = os.path.dirname(__file__)

path = os.path.abspath(os.path.join(CWD, '..'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

from lib import cache
from lib import params
from lib import threadpool

from Entity import Entity
import wolframalpha


class Untaggedentity(Entity):

	@cache.cache_results('untaggedentity')
	def get_results(self, query):
		info = self.get_facts(query)
		results ={}
		results['infobox'] = info
		return results

	def get_facts(self,query):
		client = wolframalpha.Client(Entity.wolframalpha_key)
		infobox = {}
		try:
			results = client.query(query)
			for result in results:
				basic_info = {}
				if result.title and result.text:
					if result.title.lower() == "input interpretation" or result.title.lower() == "input":
						infobox['title'] = result.text
					elif result.title.lower() == "result":
						basic_info['result'] = result.text
						infobox['basic_info'] = basic_info
					elif result.title.lower() == "basic information" or result.title.lower() == "typical human computation times":
						lines = result.text.split("|")
            					for line in lines:
              						pair = line.split(' : ')
              						basic_info[pair[0]] = pair[1]
            					infobox['basic_info'] = basic_info
            				elif result.title.lower() == "notable facts":
            					lines = result.text.split('\n')
            					summary = []
            					for line in lines:
            						if line != "...":
            							summary.append(line)
            					infobox['summary'] = summary
       		except Exception as e:
        			print "Failed to fetch data from wolfram|alpha";
        	return infobox







    
			
    	
