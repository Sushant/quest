import json
import beanstalkc

class Entity:
  """ Entity class that woyld be inherited by all entites. """
  wolframalpha_key = '4QGGQ9-8XH4X85PUH'
  freebase_key = 'AIzaSyBANswxSoGmIqHpU3-I_sihTKZtKHwLVg8';

  def __init__(self):
    try:
      self._queue = beanstalkc.Connection()
    except:
      self._queue = None


  def get_results(self,query):
   print "Implement this method!"


  def extract(self, query, tag):
    if self._queue:
      try:
        job = json.dumps({'query': query, 'tag': tag})
        self._queue.put(job)
        print 'Added: ', job
      except:
        print 'Failed to add %s to extractor' %(str(query))
