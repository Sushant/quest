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

USERNAME = 'tnahsus'
PASSWORD = 'sdb.xtc'

class Track(Entity):
  def __init__(self):
    Entity.__init__(self)
    self.lastfm = pylast.LastFMNetwork(api_key=params.***REMOVED***,
                    api_secret=params.***REMOVED***,
                    username=USERNAME,
                    password_hash=pylast.md5(PASSWORD))


  @cache.cache_results('album')
  def get_results(self, query):
    results = {}
    infobox = {}
    tracks = {}
    try:
      artist, track_name = query.split('|')
      track = self.lastfm.get_track(artist, track_name)
    except Exception as e:
      return None

    pool = threadpool.ThreadPool(4)
    pool.add_task(self.get_facts, track, infobox)
    pool.add_task(self.get_similar_tracks, track, tracks)
    pool.wait_completion()
    if infobox:
      results['infobox'] = infobox
    results['lists'] = []
    if tracks:
      results['lists'].append(tracks)

    return results


  def get_facts(self, track, infobox):
    album_name = 'N/A'
    try:
      name = track.title + ' by ' + track.artist.name
      album = track.get_album()
      album_name = album.get_title()
      image = album.get_cover_image()
      infobox['title'] = name
      infobox['image'] = image
    except Exception as e:
      import traceback
      print 'Failed to get facts from Last.fm' + str(e) + traceback.format_exc()


    try:
      infobox['basic_info'] = {
          'Album': album_name,
          'Duration': str(track.get_duration() / 1000 / 60) + ' mins'
      }
      infobox['summary'] = [track.get_wiki_summary()]
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


  def get_similar_tracks(self, track, similar_tracks):
    similar_tracks['title'] = 'Similar Tracks'

    try:
      tracks = track.get_similar()
      tracks = tracks[:10]
    except Exception as e:
      return None

    track_items = []
    for t in tracks:
      try:
        title = t.item.title
        artist = t.item.artist.name
        quest_url = '/search/?query=' + artist + '|' + title + '&tag=track'
        #self.extract(artist + '|' + title, 'track')
        track_items.append({'title': title, 'url': quest_url})
      except:
        continue
    similar_tracks['items'] = track_items
    return similar_tracks


if __name__ == '__main__':
  t = Track()
  import pprint
  pp = pprint.PrettyPrinter(indent=2)
  pp.pprint(t.get_results('Blur|Parklife'))
