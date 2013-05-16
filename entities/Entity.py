import wolframalpha
import imdb
import json
import urllib

class Entity:
 	""" Entity class that woyld be inherited by all entites. """
 	wolframalpha_key = '4QGGQ9-8XH4X85PUH'
 	freebase_key = 'AIzaSyBANswxSoGmIqHpU3-I_sihTKZtKHwLVg8'

 	def get_results(self,query):
 		print "Implement this method!"

 	## Provides link to fetch image
	def get_image(self,query):
  		modified_query = query.lower().split()
  		modified_query = '_'.join(modified_query)
  		service_url = 'https://www.googleapis.com/freebase/v1/topic/en/' + modified_query
  		params = {
      		'filter': '/common/topic/image',
      		'limit': 1,
      		'key': self.freebase_key
  		}
  		url = service_url + '?' + urllib.urlencode(params)
  		try:
  			response = urllib.urlopen(url).read()
  			response = json.loads(response.encode('utf8'))
  		except:
  			response = None

  		image_link = ""
  		try:
  			if response and response['id']:
  				image_link = 'https://usercontent.googleapis.com/freebase/v1/image'+ response['id']
  		except Exception as e:
  			print 'Failed to get image from freebase'
		return image_link


