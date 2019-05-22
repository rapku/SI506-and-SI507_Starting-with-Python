SI 506 SAMPLE README

Your readme should include ALL of the following in order to earn full points for it.

You should include these README instructions and fill in your answers below/beside the questions.

You may submit this .txt file edited, or a .PDF if you want to format it more (just like the project plan).


* In ~2-3 sentences, what does your project do?

e.g. "If you fill out secret_data.py with your Facebook information as instructed below, and run the program, the project will find the most common word in your last 25 FB posts and create a CSV file of songs from a search on iTunes that comes from that word."

You should not say "Option 1" or "Option 2" -- tell us what YOUR project does, whatever that is.

Project description:
The user must fill out the information required in finalprojectkeys.py.
The program will need a string, then search the New York Times for 10 articles using the string provided, check which has the most tags connected to each article, and get the longest word for each of the top five articles with the most tags.
For each of these 5 words, the program will search Flickr for 20 photos and place them in a CSV file.


* What files (by name) are included in your submission? List them all! MAKE SURE YOU INCLUDE EVERY SINGLE FILE YOUR PROGRAM NEEDS TO RUN, as well as a sample of its output file.
SI506_finalproject.py
finalprojectkeys.py
SI506finalproject_cache.json
sample_photooutput.csv
SI506final_README.txt

* What Python modules must be pip installed in order to run your submission? List them ALL (e.g. including requests, requests_oauthlib... anything someone running it will need!). Note that your project must run in Python 3.
Modules required:
requests, json, csv, time, string, sys

* Explain SPECIFICALLY how to run your code. We should very easily know, after reading this:
    - What file to run (e.g. python SI506_finalproject.py). That's what we expect -- but tell us specifically, just in case.

    - Anything else (e.g. "There will be a prompt asking you to enter a word. You'll definitely get good data if you enter the word 'mountains', but you can try anything", or "You need to fill out secret_data.py with the Facebook key and secret" -- if you have to do something like this, you should include the FULL INSTRUCTIONS, just like we did. Not enough to say "just like PS9". Provide text or a link to tell someone exactly what to do to fill out a file they need to include.

    - Anything someone should know in order to understand what's happening in your program as it runs

    - If your project requires secret data of YOUR OWN, and won't work with OURS (e.g. if you are analyzing data from a private group that is just yours and not ours), you must include the secret data we need in a file for us and explain that you are doing that. (We don't expect this to happen, but if it does, we still need to be able to run your program in order to grade it.)

Running the code:
1. Assure all files in submission are in the same folder
2. Open finalprojectkeys.py (included in submission), input API keys for the New York Times and Flickr, and save.
3. Run the following in bash: python SI506_finalproject.py <a string you want to search>
	If mac, may need to use python3 instead
	If you don't put a string after .py, there will be an input prompt afterwards.
4. Upon running the file, there will be a text prompt for a word:
	Testing the sample cache: use the word 'alpine'

Notes:
Program can get an error on the step requesting for individual photo information in Flickr. If an error happens, run the program again until it displays the 'CSV file produced, check folder' prompt.

If the program is running without cached data, running the program will take a while due to the following:
	Because the New York Times API has a rate limit of 5 requests per second, there is a time delay set for each page request
	There are a large number of requests for the information per photo ID (default 100 requests made)

* Where can we find all of the project technical requirements in your code? Fill in with the requirements list below.
-- NOTE: You should list (approximately) every single line on which you can find a requirement. If you have requirements written in different files, you should also specify which filename it is in! For example, ("Class definition: 26" -- if you begin a class definition on line 26 of your Python file)
It's ok to be off by a line or 2 but you do need to give us 100% of this information -- it makes grading much easier!

REQUIREMENTS LIST:
* Get and cache data from 2 REST APIs (list the lines where the functions to get & cache data begin and where they are invoked):
    * If you relied upon FB data and did not cache it, say so here:
* Define at least 2 classes, each of which fulfill the listed requirements:
* Create at least 1 instance of each class:
* Invoke the methods of the classes on class instances:
* At least one sort with a key parameter:
* Define at least 2 functions outside a class (list the lines where function definitions begin):
* Invocations of functions you define:
* Create a readable file:
END REQUIREMENTS LIST
----------------------------------------------------------------------------------------------------------------------------------------------------------
Requirement List:
Retrieving and caching from 2 REST APIs:
	1. New York Times:
		Function: nyt_get (Lines 105-128)
		Invocation: Line 188
	2. Flickr:
		Function 1: flickr_search_idgen (Lines 148-166)
		Invocation: Line 195

		Function 2: flickrid_info (Lines 169-191)
		Invocation: Line 199

2 Classes:
	1. Article
		Definition: Lines 40-66
		Instances: Line 187 (list of articles as result of article_converter function)
		Method invocation - Article.longestword(): Line 190
			Removes all punctuation found in the snippet of an article, uses .split() to break into a list, and finds the longest word. 
			In this case, Article.longestword() invoked as part of list comprehension iterating over 5 articles found in variable articlelist

	2. Photo
		Definition: Lines 68-93
		Instances: Line 199 (Photo instances generated then included as part of a list)
		Method invocation - Photo.tagstring(): Line 207-208
			Used to create a string of all tags, for easier writing into a CSV file. 
			In this case, Photo.tagstring() invoked as part of a for loop iterating over a list of Photo objects

Sorting:
	1. 	Photolist (Line 211)
		This list is sorted using key parameter [lambda x: x.tagnum()]
		x.tagnum() is a class method designed to provide the number of tags the Photo has
		Sorting is in descending order, Photo objects with the most tags come first

Functions outside class:
	1. jsondumps_shortcut()
		Definition: Lines 98-102
		Invocation: Line 127, 165, 186
		Does the necessary conversion of the cache dictionary into a string, and writes it into a .json file, used by all request-based functions

	2. article_converter(dictionary)
		Definition: Lines 131-145
		Invocation: Line 201
		Turns the JSON formatted information from nyt_get into a list of Articles. Set up is due to the NYT only displaying pages, rather than number of results
----------------------------------------------------------------------------------------------------------------------------------------------------------

* Put any citations you need below. If you borrowed code from a 506 problem set directly, or from the textbook directly, note that. If you borrowed code from a friend/classmate or worked in depth with a friend/classmate, note that. If you borrowed code from someone else's examples on a website, note that.

Line 8 and 57: Found code from StackOverflow thread (https://stackoverflow.com/questions/34293875/how-to-remove-punctuation-marks-from-a-string-in-python-3-x-using-translate/34294398)

* Explain in a couple sentences what should happen as a RESULT of your code running: what CSV or text file will it create? What information does it contain? What should we expect from it in terms of how many lines, how many columns, which headers...?
It will use the 5 words found as the longest in their respective articles, and searches for 20 photos each, getting their ID first, then grabbing the information for each ID. 

Finally, after that, the program produces a CSV file with a header row, and 100 rows of photo data. 
	Headers: Photo title, Username, List of tags, Number of tags
	Per row represents information from 1 Photo: photo title, username, a string of all tags, number of tags

* Make sure you include a SAMPLE version of the file this project outputs (this should be in your list of submitted files above!).

* Is there anything else we need to know or that you want us to know about your project? Include that here!
