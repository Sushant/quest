import os
import sys
import pylast
from pyechonest import config
from pyechonest import artist
from Entity import Entity
CWD = os.path.dirname(__file__)

path = os.path.abspath(os.path.join(CWD, '..'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

from lib import cache
from lib import params
from lib import threadpool

USERNAME = 'USERNAME'
PASSWORD = 'PASSWORD'

class Album(Entity):
  def __init__(self):
    Entity.__init__(self)
    self.lastfm = pylast.LastFMNetwork(api_key=params.LASTFM_API_KEY,
                    api_secret=params.LASTFM_API_SECRET,
                    username=USERNAME,
                    password_hash=pylast.md5(PASSWORD))
    config.ECHO_NEST_API_KEY = params.ECHONEST_API_KEY


  @cache.cache_results('album')
  def get_results(self, query):
    results = {}
    infobox = {}
    tracks = {}
    try:
      artist, album_name = query.split('|')
      album = self.lastfm.get_album(artist, album_name)
    except Exception as e:
      return None

    pool = threadpool.ThreadPool(4)
    pool.add_task(self.get_facts, album, infobox)
    pool.add_task(self.get_tracks, album, tracks)
    pool.wait_completion()
    if infobox:
      results['infobox'] = infobox
    results['lists'] = []
    if tracks:
      results['lists'].append(tracks)
    return results


  def get_facts(self, lf_album, infobox):
    try:
      image = lf_album.get_cover_image()
      name = lf_album.title
      infobox['title'] = name + ' by ' + lf_album.artist.name
      infobox['image'] = image
    except Exception as e:
      print 'Failed to get facts from Last.fm' + str(e)


    try:
      infobox['basic_info'] = {'Release date': lf_album.get_release_date()}
      infobox['summary'] = [lf_album.get_wiki_summary()]
    except Exception as e:
      import traceback
      print 'Failed to get facts from Last.fm', str(e), traceback.format_exc()
    return infobox


  def get_tracks(self, album, al_tracks):
    al_tracks['title'] = 'Album Tracks'

    try:
      tracks = album.get_tracks()
    except Exception as e:
      return str(e)

    track_items = []
    for t in tracks:
      try:
        title = t.title
        quest_url = '/search/?query=' + album.artist.name + '|' + title + '&tag=track'
        track_items.append({'title': title, 'url': quest_url})
      except:
        continue
    al_tracks['items'] = track_items
    return al_tracks


if __name__ == '__main__':
  a = Album()
  import pprint
  pp = pprint.PrettyPrinter(indent=2)
  pp.pprint(a.get_results('Blur|Parklife'))
