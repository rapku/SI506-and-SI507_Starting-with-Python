import requests
import json
import csv
import time
import string
import sys
initiate = sys.argv
#Removes punctuation, based off StackOverflow: https://stackoverflow.com/questions/34293875/how-to-remove-punctuation-marks-from-a-string-in-python-3-x-using-translate/34294398
cleaning = str.maketrans('','', string.punctuation)

#-----------------------------------------------------------------------------------------------------------------------------------------------
#	Check for keys
#-----------------------------------------------------------------------------------------------------------------------------------------------
try:
	from finalprojectkeys import NYT, FKey
except Exception:
	NYT = ''
	FKey = ''

keyname = ['New York Times API Key', 'Flickr API Key']
if NYT == '':
	NYT = input('The file for holding API keys may be missing or incomplete. Please input the {} here.'.format(keyname[0]))
if FKey == '':
	NYT = input('The file for holding API keys may be missing or incomplete. Please input the {} here.'.format(keyname[1]))

#-----------------------------------------------------------------------------------------------------------------------------------------------
#	Caching
#-----------------------------------------------------------------------------------------------------------------------------------------------
cachename = 'SI506finalproject_cache.json'
try:
	CACHEFILE = open(cachename, 'r')
	CACHE = json.loads(CACHEFILE.read())
	CACHEFILE.close()
except Exception:
	CACHE = {}

#-----------------------------------------------------------------------------------------------------------------------------------------------
#	Class definitions
#-----------------------------------------------------------------------------------------------------------------------------------------------
class Article(object):
	def __init__(self, dictionary):
		self.id = dictionary['_id']
		self.text = dictionary['snippet']
		self.url = dictionary['web_url']
		self.keywords = dictionary['keywords']


		self.headline = dictionary['headline']['name']
		self.altheadline = dictionary['headline']['main']

	def __str__(self):
		if self.headline == None:
			return self.altheadline
		else:
			return self.headline

	def longestword(self):
		cleaned = self.text.translate(cleaning)
		longestlist = sorted(cleaned.split(), key=lambda x: len(x), reverse=True)
		if len(longestlist) == 0:
			return 'No snippet available'
		else:
			return longestlist[0]

	def keywords_found(self):
		return len(self.keywords)

class Photo(object):
	def __init__(self, dictionary):
		if dictionary['photo']['title']['_content'] == None:
			self.title = ''
		else:	
			self.title = dictionary['photo']['title']['_content']
		self.owner = dictionary['photo']['owner']['username']
		self.tags = [dictionary['photo']['tags']['tag'][x]['raw'] for x in range(len(dictionary['photo']['tags']['tag']))]

	def __str__(self):
		return "{} by {}".format(self.title, self.owner)

	def tagnum(self):
		return len(self.tags)

	def tagstring(self):
		if len(self.tags) == 0:
			return ''
		elif len(self.tags) == 1:
			return self.tags[0]
		else:
			tagstr = ''
			for x in range(len(self.tags)-1):
				tagstr += '{}, '.format(self.tags[x])
			tagstr += '{}'.format(self.tags[-1])
			return tagstr

#-----------------------------------------------------------------------------------------------------------------------------------------------
#	Functions
#-----------------------------------------------------------------------------------------------------------------------------------------------
def jsondumps_shortcut():
	dump = json.dumps(CACHE)
	cachewriter = open(cachename, 'w')
	cachewriter.write(dump)
	cachewriter.close()

#Notes: NYT gets results per page (10 results per page)
def nyt_get(search_term, search_target=10):
	identifier = 'nyt.{}.{}'.format(search_term, search_target)
	nytbase = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'
	params = {}
	params['api-key'] = NYT
	params['q'] = search_term

	if identifier in CACHE:
		print('NYT info retrieved from cache')
		return CACHE[identifier]
	else:
		print('Retrieving New York Times articles')
		dictionarylist = {'results':search_target}
		pages_to_search = int(search_target/10)+1

		for x in range(pages_to_search):
			params['page'] = x
			req = requests.get(nytbase, params)
			dictionarylist[str(x)] = json.loads(req.text)
			time.sleep(1)

		CACHE[identifier] = dictionarylist
		jsondumps_shortcut()
		return CACHE[identifier]

#Converts NYT JSON to articles
def article_converter(dictionary):
	target_number = dictionary['results']
	page = int(target_number/10)+1
	articlelist = []
	for x in range(page):
		pagejson = dictionary[str(x)]
		if target_number % 10 != 0 and x == range(page)[-1]:
			for article in range(target_number % 10):
				articlelist.append(Article(pagejson['response']['docs'][article]))
		elif x != range(page)[-1]:
			for article in range(len(pagejson['response']['docs'])):
				articlelist.append(Article(pagejson['response']['docs'][article]))
		else:
			pass
	return articlelist

#searches for 20 photos and provides the id to use the getInfo API method later
def flickr_search_idgen(term, limit=20):
	identifier = 'flickrids.{}.{}'.format(term, limit)
	base = 'https://api.flickr.com/services/rest/'
	params = {}
	params['api_key'] = FKey
	params['method'] = 'flickr.photos.search'
	params['tags'] = term
	params['format'] = 'json'
	params['per_page'] = limit

	if identifier in CACHE:
		print('Flickr search for term {} retrieved from cache'.format(term))
		return CACHE[identifier]
	else:
		idsearch = requests.get(base, params)
		iddict = json.loads(idsearch.text[14:-1])
		CACHE[identifier] = [iddict['photos']['photo'][x]['id'] for x in range(len(iddict['photos']['photo']))]
		jsondumps_shortcut()
		return CACHE[identifier]

#Calls Flickr API >> Get info per picture using ID
def flickrid_info(flickr_id):
	identifier = 'info.{}'.format(flickr_id)
	base = 'https://api.flickr.com/services/rest/'
	params = {}
	params['api_key'] = FKey
	params['method'] = 'flickr.photos.getInfo'
	params['photo_id'] = flickr_id
	params['format'] = 'json'

	if identifier in CACHE:
		print('{} in cache'.format(flickr_id))
		return CACHE[identifier]
	else:
		print('Retrieving info for photo {}'.format(flickr_id))
		infosearch = requests.get(base, params)
		try:
			CACHE[identifier] =  json.loads(infosearch.text[14:-1])
			jsondumps_shortcut()
			time.sleep(0.5)
			return CACHE[identifier]
		except Exception:
			print('Error, run program again')
			sys.exit
#-----------------------------------------------------------------------------------------------------------------------------------------------
#	Actually doing things online
#-----------------------------------------------------------------------------------------------------------------------------------------------
if len(sys.argv) == 1:
	userinput = input('Hi.\nThis program needs a search term from you.\n\nPlease enter a string on something you want to find\n\n')
else:
	userinput = initiate[1]

NYTsearch = nyt_get(userinput)
articlelist = sorted(article_converter(NYTsearch), key= lambda x: x.keywords_found(), reverse=True)[0:5]
wordsearch = [x.longestword() for x in articlelist]
print('With the term {}, we chose 5 articles with the most number of tags\nPresenting a list of the longest word in each of the 5 articles mentioned: {}'.format(userinput, wordsearch))
idlist = []

for word in wordsearch:
	ids = flickr_search_idgen(word)
	for oneid in ids:
		idlist.append(oneid)

photolist = sorted([Photo(flickrid_info(x)) for x in idlist], key = lambda x: x.tagnum(), reverse=True)

#-----------------------------------------------------------------------------------------------------------------------------------------------
#	Writing CSV file
#-----------------------------------------------------------------------------------------------------------------------------------------------
csvmake = open('photooutput.csv', 'w', newline='')
csvwriter = csv.writer(csvmake)
csvwriter.writerow(('Photo title', 'Username', 'List of tags', 'Number of tags'))
for x in photolist:
	csvwriter.writerow((x.title, x.owner, x.tagstring(), x.tagnum()))
print('CSV file produced, check folder')
csvmake.close()