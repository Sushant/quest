import os

CWD = os.path.dirname(__file__)

BASE = os.path.abspath(os.path.join(CWD, '..'))

WEB_DIR = BASE
ENTITIES_DIR = os.path.join(BASE, 'entities')
WEB_PORT = 8080
FREEBASE_SUGGEST_URL = 'https://www.googleapis.com/freebase/v1/search?query='
DBPEDIA_SUGGEST_URL = 'http://lookup.dbpedia.org/api/search.asmx/KeywordSearch?QueryString='
