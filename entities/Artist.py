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

from lib import params

USERNAME = 'tnahsus'
PASSWORD = 'sdb.xtc'

class Artist(Entity):
  def __init__(self):
    self.lastfm = pylast.LastFMNetwork(api_key=params.***REMOVED***,
                    api_secret=params.***REMOVED***,
                    username=USERNAME,
                    password_hash=pylast.md5(PASSWORD))
    config.ECHO_NEST_API_KEY = params.***REMOVED***

  def get_results(self, query):
    results = {}
    try:
      artist = self.lastfm.get_artist(query)
    except Exception as e:
      return None
    infobox = self.get_facts(artist)
    if infobox:
      results['infobox'] = infobox
    results['lists'] = []
    albums = self.get_top_albums(artist)
    if albums:
      results['lists'].append(albums)
    tracks = self.get_top_tracks(artist)
    if tracks:
      results['lists'].append(tracks)
    artists = self.get_similar_artists(artist)
    if artists:
      results['lists'].append(artists)

    return results


  def get_facts(self, lf_artist):
    infobox = {}
    try:
      image = lf_artist.get_cover_image()
      name = lf_artist.name
      infobox['title'] = name
      infobox['image'] = image
    except Exception as e:
      print 'Failed to get facts from Last.fm'


    try:
      infobox['basic_info'] = {}
      echonest_artist = artist.Artist(lf_artist.name)
      years = echonest_artist.years_active
      active_years = ''
      for streak in years:
        for k, v in streak.iteritems():
          if active_years:
            active_years += ', '
          active_years += str(k) + ': ' + str(v)
      infobox['basic_info']['Active from'] = active_years
      biographies = echonest_artist.biographies
      infobox['summary'] = []
      for b in biographies:
        if b['site'] == 'wikipedia':
          infobox['summary'].append(b['text'][:500] + '...Read more on <a href="' + b['url'] + '">Wikipedia</a>')
    except Exception as e:
      import traceback
      print 'Failed to get facts from Echonest', str(e), traceback.format_exc()
    return infobox


  def get_top_albums(self, artist):
    top_albums = {'title': 'Top Albums'}

    try:
      albums = artist.get_top_albums()
      albums = albums[:10]
    except Exception as e:
      return None

    album_items = []
    for a in albums:
      try:
        image = a.item.get_cover_image()
        title = a.item.title
        quest_url = '/search/?query=' + title + '&tag=album'
        album_items.append({'title': title, 'url': quest_url, 'image': image})
      except:
        continue
    top_albums['items'] = album_items
    return top_albums


  def get_top_tracks(self, artist):
    top_tracks = {'title': 'Top Tracks'}

    try:
      tracks = artist.get_top_tracks()
      tracks = tracks[:10]
    except Exception as e:
      return None

    track_items = []
    for t in tracks:
      try:
        title = t.item.title
        quest_url = '/search/?query=' + title + '&tag=track'
        track_items.append({'title': title, 'url': quest_url})
      except:
        continue
    top_tracks['items'] = track_items
    return top_tracks


  def get_similar_artists(self, artist):
    similar_artists = {'title': 'Similar Artists'}

    try:
      artists = artist.get_similar()
      artists = artists[:10]
    except Exception as e:
      return None

    artist_items = []
    for a in artists:
      try:
        title = a.item.name
        image = a.item.get_cover_image()
        quest_url = '/search/?query=' + title + '&tag=artist'
        artist_items.append({'title': title, 'url': quest_url, 'image': image})
      except:
        continue
    similar_artists['items'] = artist_items
    return similar_artists


if __name__ == '__main__':
  a = Artist()
  import pprint
  pp = pprint.PrettyPrinter(indent=2)
  pp.pprint(a.get_results('Can'))
