# 507WaiverFall2017
Waiver exam for University of Michigan SI 507. You must complete all 3 parts, and the code for each part must be checked in to github with the name specified for that part. Any other filenames will break our grading system and will be rejected.

## Part 1: Create a program to analyze the twitter timeline of a selected user.

FILENAME: part1.py

ARGUMENTS: the program takes two arguments--a twitter username and the number of tweets to analyze.

OUTPUT: the program outputs the following:
* the user name
* the number of tweets analyzed
* the five most frequent verbs that appear in the analyzed tweets
* the five most frequent nouns that appear in the analyzed tweets
* the five most frequent adjectives that appear in the analyzed tweets
* the number of _original_ tweets (i.e., not retweets)
* the number of times that the _original_ tweets in the analyzed set were favorited
* the number of times that the _original_ tweets in the analyzed set were retweeted by others

NOTES: 
* use tweepy for accessing the Twitter API
* Use NLTK for analyzing parts of speech. Use NLTK's default POS tagger and tagset (this will use the [UPenn treebank tagset](https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html))--you do NOT need to install any taggers or tagsets into NLTK.
* stop words: ignore any words that do not start with an alphabetic character `[a-zA-Z`], and also ignore 'http', 'https', and 'RT' (these show up a lot in Twitter)
* a "verb" is anything that is tagged VB*
* a "noun" is anything that is tagged NN*
* an "adjective" is anything that is tagged JJ*
* for the nouns, verbs, and adjectives, don't worry about the fact that there might be words that have the same frequency and will therefore be listed in random order. We'll account for this in our grading.

SAMPLE OUTPUT:

```bash
mwnewman$ python3 get_tweets.py umsi 50
USER: umsi
TWEETS ANALYZED: 50
VERBS: are(4) being(3) is(3) improve(2) Join(2) 
NOUNS: umsi(8) UMSI(8) students(5) Join(5) amp(5) 
ADJECTIVES more(5) umsi(4) doctoral(2) new(2) social(2) 
ORIGINAL TWEETS: 27
TIMES FAVORITED (ORIGINAL TWEETS ONLY): 69
TIMES RETWEETED (ORIGINAL TWEETS ONLY): 18
```
## Part 2: Create a Simple Database application

For part 2, you will create a program to access information in the Northwind database (included in the repository)

FILENAME: part2.py

USAGE: the program does different things based on the arguments passed in.  
**part2.py customers**: prints the list of all cusomters

**part2.py employees**: prints the list of all employees

**part2.py orders cust=&lt;customer id&gt;**: prints the list of _order dates_ for all orders placed for the specified customer. Use the _customer ID_ for this command.

**part2.py orders emp=&lt;employee last name&gt;**: prints the list of _order dates_ for all orders managed by the specified employee. Use the _employee last name_ for this command.

SAMPLE OUTPUT:
The sample output is large, so it's on another page: [Sample Output](https://github.com/numerator/507WaiverFall2017/blob/master/part2_output.md)

NOTES: Use sqlite3.

## Part 3: Scrape the Michigan Daily

FILENAME: part3.py

Finally, in part 3, you will use Beautiful Soup to scrape the Most Read stories from the Michigan Daily site (http://michigandaily.com), and will crawl one level deeper to find the author of each Most Read story.

SAMPLE OUTPUT:
```
dhcp3-213:507waiver2 mwnewman$ python3 part3.py   
Michigan Daily -- MOST READ  
Darkness and the Occult: A brief history of doom metal  
  by Selena Aguilera
UPDATE: University confirms Richard Spencer has requested to speak at 'U'  
  by Kaela Theut
"The white rice was excellent. Followed the directions on the bag perfectly. Way to go."  
  by Hunter Zhao
Schlissel: "I try not to have a personal opinion" on potential C.C. Little renaming, awaiting further review  
  by Alexa St. John
A guide to Michigan's 2018 gubernatorial race
  by Colin Beresford
```
NOTES: If there is more than one reporter, you only need to print the first name on the byline.
