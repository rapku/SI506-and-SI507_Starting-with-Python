import tweepy
import nltk
import json
import sys

a = sys.argv
if len(a) != 3:
	usertocheck = input('Input a username\n')
	tweetstocheck = input('Input number of tweets to be analyzed\n')
	a = [a[0], usertocheck, tweetstocheck]

#CACHING FORMULA
CACHE = 'twittercache.json'
try:
	cache = open(CACHE, 'r')
	cache_reader = cache.read()
	TWEET_CACHE = json.loads(cache_reader)
	cache.close()
except Exception:
	TWEET_CACHE = {}

#API things
consumerkey = ''
consumersecret = ''
accesskey = ''
accesssecret = ''
auth = tweepy.OAuthHandler(consumerkey, consumersecret)
auth.set_access_token(accesskey, accesssecret)
api = tweepy.API(auth)

ident = '{1}_{2}'.format(*a)
webheader = ['http', 'https', 'RT']

#CACHING FORMULA
def grab_tweets(user, tweets):
	userparam = {}
	if ident in TWEET_CACHE:
		print('Retrieved from cache')
		return TWEET_CACHE[ident]
	else:
		twy = api.user_timeline(user,count=tweets)
		twy_json = []
		for x in range(len(twy)):
			twy_json.append(twy[x]._json)
		TWEET_CACHE[ident] = twy_json
		dump = json.dumps(TWEET_CACHE)
		cachewrite = open(CACHE, 'w')
		cachewrite.write(dump)
		cachewrite.close()
		return TWEET_CACHE[ident]

#Converts tweet object (Status) into a string (to remove issues w/ emojis)
#Also does the NLTK things: separates to words, filters 3 indicated common Twitter things and non-alpha tokens, and tags them
def tweet2taggedtokens(tweet):
	dumping = json.dumps(tweet['text'])
	tokenfilter = [f.lower() for f in nltk.word_tokenize(dumping) if f.isalpha() and f not in webheader]
	c = nltk.pos_tag(tokenfilter)
	return c


#check if user exists
try:
	targettweets = grab_tweets(a[1],int(a[2]))
except Exception:
	print('User may not exist, please check in Twitter')
	sys.exit()


#Finding original tweet information only
original_tweet_data = {'count':0, 'favorite':0, 'retweeted':0}
text_collection = []
for x in targettweets:
	for tagtuple in (tweet2taggedtokens(x)):
		text_collection.append(tagtuple)
	try:
		x['retweeted_status']
	except Exception:
		original_tweet_data['count'] +=1
		original_tweet_data['favorite'] += x['favorite_count']
		original_tweet_data['retweeted'] += x['retweet_count']

#text analysis
frequency = nltk.FreqDist(text_collection).most_common()
nouns = sorted([(tups[0][0], tups[1]) for tups in frequency if 'NN' in tups[0][1]], key= lambda x: x[1], reverse=True)[:5]
verbs = sorted([(tups[0][0], tups[1]) for tups in frequency if 'VB' in tups[0][1]], key= lambda x: x[1], reverse=True)[:5]
adjectives = sorted([(tups[0][0], tups[1]) for tups in frequency if 'JJ' in tups[0][1]], key= lambda x: x[1], reverse=True)[:5]

def fivewordprinter(lst):
	word = ''
	for x in lst:
		word += ' {}({})'.format(*x)
	return word

# Print statements
print('User: {}'.format(a[1]))

if len(targettweets) < int(a[2]):
	print('This user only has {0} tweets available.\nTWEETS ANALYZED: {0}'.format(len(targettweets)), '\n')
else:
	print('TWEETS ANALYZED: {0}'.format(int(a[2])), '\n')

print('Most frequent verbs:\n', fivewordprinter(verbs), sep='')
print('Most frequent nouns:\n', fivewordprinter(nouns), sep='')
print('Most frequent adjectives:\n', fivewordprinter(adjectives),'\n', sep='')


print('Original tweets: {}'.format(original_tweet_data['count']))
print('Times Favorited (original tweets): {}'.format(original_tweet_data['favorite']))
print('Times Retweeted (original tweets): {}'.format(original_tweet_data['retweeted']))

