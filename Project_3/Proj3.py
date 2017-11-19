# Developer: Kyle Essenmacher 
# Assignment: Project 3 - Twitter Scraping 
# Graduate Student Instructors: Niharika Ved and Chong Li
# Professor: Colleen Van Lent
# Date: 11.19.17

# Collaborated with Aaron Cheng, Michele Gee, Imaan Munir, Priscilla Nunez

##OBJECTIVE:
## In this assignment you will be creating database and loading data
## into database.  You will also be performing SQL queries on the data.
## You will be creating a database file: 206_APIsAndDBs.sqlite

# Import statements
import unittest
import itertools
import collections
import tweepy
import twitter_info # same deal as always...
import json
import sqlite3

# Kyle's Tweepy Authentication
###############
# MAKE SURE TO HAVE YOUR "twitter info.py" folder in this project folder. Code will not run without this. 
###############
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Set up library to grab tweets from my personal twitter. Included authentication, and
# return it in a JSON format
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

# end of Tweepy Authentication

#Resolves unicode error
import sys
def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)

# Task 1 - Gathering data

## Defined a function called get_user_tweets that gets at least 20 Tweets
## from a specific Twitter user's timeline, and uses caching. The function
## should return a Python object representing the data that was retrieved
## from Twitter. (This may sound familiar...) We have provided a
## CACHE_FNAME variable for you for the cache file name, but you must
## write the rest of the code in this file.

CACHE_FNAME = "206_APIsAndDBs_cache.json"
# Put the rest of your caching setup here:
try:
    cache_file = open(CACHE_FNAME,'r')
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION = json.loads(cache_contents)
except:
    CACHE_DICTION = {}


# Define your function get_user_tweets here:
# info here: https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline

def get_user_tweets(user):
#if already in cache
    if user in CACHE_DICTION:
        uprint("using cached data")
#grab data from chache
        twitter_results = CACHE_DICTION[user]
    else:
        uprint("getting data from internet")
        twitter_results = api.user_timeline(user) 
#get it from the internet
#but also, save in the dictionary to cache it
        CACHE_DICTION[user] = twitter_results 
#add it to the dictionary -- new key-val pair
#and then write the whole cache dictionary, now with new info added, to the file, 
#so it'll be there even after you...
        f = open(CACHE_FNAME, 'w') 
#open the cache file for writing
        f.write(json.dumps(CACHE_DICTION)) 
#make the whole dictionary holding data and unique identifiers into a json-format
        f.close()
    return twitter_results 
#return list



# Write an invocation to the function for the "umich" user timeline and
# save the result in a variable called umich_tweets:

umich_tweets = get_user_tweets('@umich')


## Task 2 - Creating database and loading data into database
## You should load into the Users table:
# The umich user, and all of the data about users that are mentioned
# in the umich timeline.
# NOTE: For example, if the user with the "TedXUM" screen name is
# mentioned in the umich timeline, that Twitter user's info should be
# in the Users table, etc.
conn = sqlite3.connect('206_APIsAndDBs.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Users')
cur.execute('CREATE TABLE Users (user_id INTEGER, screen_name VARCHAR, num_favs INTEGER, description TEXT, PRIMARY KEY (user_id))')


users_lst = []
for tweet in umich_tweets:
# print (tweet)
	if tweet['user']['id'] not in users_lst:
		cur.execute('INSERT INTO Users (user_id, screen_name, num_favs, description) VALUES (?,?,?,?)',
		(tweet['user']['id'],
		tweet['user']['screen_name'],
		tweet['user']['favourites_count'],
		tweet['user']['description']))
		users_lst.append(tweet['user']['id'])
	for uIndiv in tweet['entities']['user_mentions']:
		if uIndiv['id'] not in users_lst:
			cur.execute('INSERT INTO Users (user_id, screen_name) VALUES (?,?)',
			(uIndiv['id'],
			uIndiv['screen_name']))
			users_lst.append(uIndiv['id'])


## You should load into the Tweets table:
# Info about all the tweets (at least 20) that you gather from the
# umich timeline.
# NOTE: Be careful that you have the correct user ID reference in
# the user_id column! See below hints.

cur.execute('DROP TABLE IF EXISTS Tweets')
#ask about TEXT PRIMARY KEY reminder to self ****ask GSI or Prof VL
cur.execute('CREATE TABLE Tweets (tweet_id INTEGER, text TEXT, user_posted INTEGER, time_posted DATETIME, retweets INTEGER, PRIMARY KEY (tweet_id), FOREIGN KEY (user_posted) REFERENCES Users(user_id))')
# user_posted foriegn key reminder to self ****ask GSI or Prof VL

tweets_lst = []
for tweet in umich_tweets:
    # uprint(tweet)
    if tweet['id'] not in tweets_lst:
        cur.execute('INSERT INTO Tweets (tweet_id, text, user_posted, time_posted, retweets) VALUES (?,?,?,?,?)',
        (tweet['id'],
        tweet['text'],
        tweet['user']['id'],
        tweet['created_at'],
        tweet['retweet_count'],))
        tweets_lst.append(tweet['id'])

conn.commit()


## HINT: There's a Tweepy method to get user info, so when you have a
## user id or screenname you can find alllll the info you want about
## the user.

## HINT: The users mentioned in each tweet are included in the tweet
## dictionary -- you don't need to do any manipulation of the Tweet
## text to find out which they are! Do some nested data investigation
## on a dictionary that represents 1 tweet to see it!



## Kyle 11.10.17 - Will complete soon!
## Task 3 - Making queries, saving data, fetching data
# helpful: cur.fetchall(), .join()

# All of the following sub-tasks require writing SQL statements
# and executing them using Python.

# Make a query to select all of the records in the Users database.
# Save the list of tuples in a variable called users_info.
users_info = list(cur.execute('SELECT * FROM Users'))

# Make a query to select all of the user screen names from the database.
# Save a resulting list of strings (NOT tuples, the strings inside them!)
# in the variable screen_names. HINT: a list comprehension will make
# this easier to complete!
screen_names = []
for tup in list(cur.execute('SELECT screen_name FROM Users')):
    for string in tup:
        screen_names.append(string)
#uprint(screen_names)  test


# Make a query to select all of the tweets (full rows of tweet information)
# that have been retweeted more than 10 times. Save the result
# (a list of tuples, or an empty list) in a variable called retweets.
retweets = list(cur.execute('SELECT * FROM Tweets WHERE retweets > 10'))



# Make a query to select all the descriptions (descriptions only) of
# the users who have favorited more than 500 tweets. Access all those
# strings, and save them in a variable called favorites,
# which should ultimately be a list of strings.
favorites = []
for tup in list(cur.execute('SELECT description FROM Users WHERE num_favs > 500')):
    for string in tup:
        favorites.append(string)
uprint(favorites)


# Make a query using an INNER JOIN to get a list of tuples with 2
# elements in each tuple: the user screenname and the text of the
# tweet. Save the resulting list of tuples in a variable called joined_data2.
cur.execute('SELECT Users.screen_name, Tweets.text FROM Users join Tweets on Users.user_id = Tweets.user_posted')
# print ((joined_data))  test
# joined_data2 =[]       test
# for x in joined_data:  test
# 	# print (len(x))      test
# 	joined_data2.append(x)  test
# print (type(joined_data2[0])) test
# print (type(("hi","bye")))    test - changed test and still didn't work
joined_data = cur.fetchall()
print('-------------------------') #Chong Li used to test
print(joined_data) #Chong Li used to test

# for tup in list(cur.execute('SELECT screen_name FROM Users')):
# 	joinedD.append(tup[0])   test

# joinedD2 =[]           test
# for tup in list(cur.execute('SELECT text FROM Tweets')):
# 	joinedD2.append(tup[0])
# 	# print (tup[0])
# print (len(joinedD))
# print (len(joinedD2))   test

# Make a query using an INNER JOIN to get a list of tuples with 2
# elements in each tuple: the user screenname and the text of the
# tweet in descending order based on retweets. Save the resulting
# list of tuples in a variable called joined_data2.

joined_data2 = True


### IMPORTANT: MAKE SURE TO CLOSE YOUR DATABASE CONNECTION AT THE END
### OF THE FILE HERE SO YOU DO NOT LOCK YOUR DATABASE (it's fixable,
### but it's a pain). ###
cur.close()

###### TESTS APPEAR BELOW THIS LINE ######
###### Note that the tests are necessary to pass, but not sufficient --
###### must make sure you've followed the instructions accurately!
######
print("\n\nBELOW THIS LINE IS OUTPUT FROM TESTS:\n")


class Task1(unittest.TestCase):
	def test_umich_caching(self):
		fstr = open("206_APIsAndDBs_cache.json","r")
		data = fstr.read()
		fstr.close()
		self.assertTrue("umich" in data)
	def test_get_user_tweets(self):
		res = get_user_tweets("umsi")
		self.assertEqual(type(res),type(["hi",3]))
	def test_umich_tweets(self):
		self.assertEqual(type(umich_tweets),type([]))
	def test_umich_tweets2(self):
		self.assertEqual(type(umich_tweets[18]),type({"hi":3}))
	def test_umich_tweets_function(self):
		self.assertTrue(len(umich_tweets)>=20)

class Task2(unittest.TestCase):
	def test_tweets_1(self):
		conn = sqlite3.connect('206_APIsAndDBs.sqlite')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Tweets');
		result = cur.fetchall()
		self.assertTrue(len(result)>=20, "Testing there are at least 20 records in the Tweets database")
		conn.close()
	def test_tweets_2(self):
		conn = sqlite3.connect('206_APIsAndDBs.sqlite')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Tweets');
		result = cur.fetchall()
		self.assertTrue(len(result[1])==5,"Testing that there are 5 columns in the Tweets table")
		conn.close()
	def test_tweets_3(self):
		conn = sqlite3.connect('206_APIsAndDBs.sqlite')
		cur = conn.cursor()
		cur.execute('SELECT tweet_id FROM Tweets');
		result = cur.fetchall()
		self.assertTrue(result[0][0] != result[19][0], "Testing part of what's expected such that tweets are not being added over and over (tweet id is a primary key properly)...")
		if len(result) > 20:
			self.assertTrue(result[0][0] != result[20][0])
		conn.close()


	def test_users_1(self):
		conn = sqlite3.connect('206_APIsAndDBs.sqlite')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Users');
		result = cur.fetchall()
		self.assertTrue(len(result)>=2,"Testing that there are at least 2 distinct users in the Users table")
		conn.close()
	def test_users_2(self):
		conn = sqlite3.connect('206_APIsAndDBs.sqlite')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Users');
		result = cur.fetchall()
		self.assertTrue(len(result)<20,"Testing that there are fewer than 20 users in the users table -- effectively, that you haven't added duplicate users. If you got hundreds of tweets and are failing this, let's talk. Otherwise, careful that you are ensuring that your user id is a primary key!")
		conn.close()
	def test_users_3(self):
		conn = sqlite3.connect('206_APIsAndDBs.sqlite')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Users');
		result = cur.fetchall()
		self.assertTrue(len(result[0])==4,"Testing that there are 4 columns in the Users database")
		conn.close()

class Task3(unittest.TestCase):
	def test_users_info(self):
		self.assertEqual(type(users_info),type([]),"testing that users_info contains a list")
	def test_users_info2(self):
		self.assertEqual(type(users_info[0]),type(("hi","bye")),"Testing that an element in the users_info list is a tuple")

	def test_track_names(self):
		self.assertEqual(type(screen_names),type([]),"Testing that screen_names is a list")
	def test_track_names2(self):
		self.assertEqual(type(screen_names[0]),type(""),"Testing that an element in screen_names list is a string")

	def test_more_rts(self):
		if len(retweets) >= 1:
			self.assertTrue(len(retweets[0])==5,"Testing that a tuple in retweets has 5 fields of info (one for each of the columns in the Tweet table)")
	def test_more_rts2(self):
		self.assertEqual(type(retweets),type([]),"Testing that retweets is a list")
	def test_more_rts3(self):
		if len(retweets) >= 1:
			self.assertTrue(retweets[1][-1]>10, "Testing that one of the retweet # values in the tweets is greater than 10")

	def test_descriptions_fxn(self):
		self.assertEqual(type(favorites),type([]),"Testing that favorites is a list")
	def test_descriptions_fxn2(self):
		self.assertEqual(type(favorites[0]),type(""),"Testing that at least one of the elements in the favorites list is a string, not a tuple or anything else")
	def test_joined_result(self):

		self.assertEqual(type(joined_data[0]),type(("hi","bye")),"Testing that an element in joined_result is a tuple")



if __name__ == "__main__":
	unittest.main(verbosity=2)