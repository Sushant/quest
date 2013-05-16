import os
import sys
import json
import beanstalkc


import params
sys.path.insert(1, params.ENTITIES_DIR)


class Extractor:
  def __init__(self):
    self._init_queue()

  def _init_queue(self):
    try:
      self._queue = beanstalkc.Connection()
    except:
      print 'Failed to connect to queue'
      sys.exit(1)


  def run(self):
    while True:
      job = self.get_next_job()
      if job:
        response = self.process_job(job)


  def get_next_job(self):
    try:
      job = self._queue.reserve()
      if job:
        job_body_str = job.body
        job.delete()
        job_dict = json.loads(job_body_str)
        return job_dict
    except Exception as e:
      print 'Connection to beanstalk failed', str(e)


  def process_job(self, job):
    query = job['query']
    tag = job['tag']
    print 'Processing query: ', query, ' tag: ', tag
    module = __import__(tag.capitalize())
    _class = getattr(module, tag.capitalize())
    entity = _class()
    entity.get_results(query)


if __name__ == '__main__':
  extractor = Extractor()
  extractor.run()
