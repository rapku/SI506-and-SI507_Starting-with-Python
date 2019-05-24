import tweepy
import nltk
import json
import sys

a = sys.argv
if len(a) != 3:
	usertocheck = input('Input a username\n')
	tweetstocheck = input('Input number of tweets to be analyzed\n')
	a = [a[0], usertocheck, tweetstocheck]

#Authentication thing
consumerkey = ''
consumersecret = ''
accesskey = ''
accesssecret = ''
auth = tweepy.OAuthHandler(consumerkey, consumersecret)
auth.set_access_token(accesskey, accesssecret)
api = tweepy.API(auth)

webheader = ['http', 'https', 'RT']

#Converts tweet object (Status) into a string (to remove issues w/ emojis)
#Also does the NLTK things: separates to words, filters 3 indicated common Twitter things and non-alpha tokens, and tags them
def tweet2taggedtokens(tweet):
	dumping = json.dumps(tweet.text)
	tokenfilter = [f.lower() for f in nltk.word_tokenize(dumping) if f.isalpha() and f not in webheader]
	c = nltk.pos_tag(tokenfilter)
	return c

#Check if person even exists in Twitter
try:
	tweetstore = api.user_timeline(a[1], count=int(a[2]))
except Exception:
	print('User may not exist, please check in Twitter')
	sys.exit()

#Finding original tweet information only
original_tweet_data = {'count':0, 'favorite':0, 'retweeted':0}
text_collection = []

for x in tweetstore:
	for tagtuple in (tweet2taggedtokens(x)):
		text_collection.append(tagtuple)
	try:
		x.retweeted_status
	except Exception:
		original_tweet_data['count'] +=1
		original_tweet_data['favorite'] += x.favorite_count
		original_tweet_data['retweeted'] += x.retweet_count


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

if len(tweetstore) < int(a[2]):
	print('This user only has {0} tweets available.\nTWEETS ANALYZED: {0}'.format(len(tweetstore)), '\n')
else:
	print('TWEETS ANALYZED: {0}'.format(int(a[2])), '\n')
	
print('Most frequent verbs:\n', fivewordprinter(verbs), sep='')
print('Most frequent nouns:\n', fivewordprinter(nouns), sep='')
print('Most frequent adjectives:\n', fivewordprinter(adjectives),'\n', sep='')


print('Original tweets: {}'.format(original_tweet_data['count']))
print('Times Favorited (original tweets): {}'.format(original_tweet_data['favorite']))
print('Times Retweeted (original tweets): {}'.format(original_tweet_data['retweeted']))

