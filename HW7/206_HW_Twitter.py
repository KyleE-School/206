import unittest
import tweepy
import requests
import json
import twitter_info

## SI 206 - HW
## COMMENT WITH: Kyle Essenmacher 
## Your section day/time: Thurs 8:30 AM
## Any names of people you worked with on this assignment: Michele, Aaron, Priscilla, Imaan

## Write code that uses the tweepy library to search for tweets with three different phrases of the
## user's choice (should use the Python input function), and prints out the Tweet text and the
## created_at value (note that this will be in GMT time) of the first FIVE tweets with at least
## 1 blank line in between each of them, e.g.


## You should cache all of the data from this exercise in a file, and submit the cache file
## along with your assignment.

## So, for example, if you submit your assignment files, and you have already searched for tweets
## about "rock climbing", when we run your code, the code should use CACHED data, and should not
## need to make any new request to the Twitter API.  But if, for instance, you have never
## searched for "bicycles" before you submitted your final files, then if we enter "bicycles"
## when we run your code, it _should_ make a request to the Twitter API.

## Because it is dependent on user input, there are no unit tests for this -- we will
## run your assignments in a batch to grade them!

## We've provided some starter code below, like what is in the class tweepy examples.

##SAMPLE OUTPUT
## See: https://docs.google.com/a/umich.edu/document/d/1o8CWsdO2aRT7iUz9okiCHCVgU5x_FyZkabu2l9qwkf8/edit?usp=sharing



## **** For extra credit, create another file called twitter_info.py that
## contains your consumer_key, consumer_secret, access_token, and access_token_secret,
## import that file here.  Do NOT add and commit that file to a public GitHub repository.

## **** If you choose not to do that, we strongly advise using authentication information
## for an 'extra' Twitter account you make just for this class, and not your personal
## account, because it's not ideal to share your authentication information for a real
## account that you use frequently.

## Get your secret values to authenticate to Twitter. You may replace each of these
## with variables rather than filling in the empty strings if you choose to do the secure way
## for EC points
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
## Set up your authentication to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
# Set up library to grab stuff from twitter with your authentication, and
# return it in a JSON-formatted way

api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

## Write the rest of your code here!

#### Recommended order of tasks: ####
## 1. Set up the caching pattern start -- the dictionary and the try/except
## 		statement shown in class.
xyz = "twitter_results.json" #calls twitter results xyz 

try:
	Cache_file = open("xyz", 'r') #read data from file
	Cache_contents = Cache_file.read() #if data is there put it into a string
	Cache_diction = json.loads(Cache_contents) #put into dictionary
	Cache_file.close() #close
except:
	Cache_diction = {}


## 2. Write a function to get twitter data that works with the caching pattern,
## 		so it either gets new data or caches data, depending upon what the input
##		to search for is.
def get_tweet(search_term):
    if search_term in Cache_diction: #The code runs the cache file and will look for a term.
        print("using cache") #If the searches term has been cached then it will be returned.
        return Cache_diction[search_term]
    else:
        print("fetching") #If not, it pulls from Twitter
        results = api.search(search_term)
        try:
            Cache_diction[search_term] = json.dumps(results)
            dumped_json_cache = json.dumps(Cache_diction)
            fw = open(xyz, 'w')
            fw.write(dumped_json_cache)
            fw.close()
            return Cache_diction[search_term]
        except:
            print("Wasn't in cache and wasn't in search either") #If there was nothing in cached or twitter
            return None


## 3. Using a loop, invoke your function, save the return value in a variable, and explore the
##		data you got back!
c = 0
while c < 3: #enter tweet key word three times
    tweet_term = input('Enter Tweet term: ') #Asks user for a search term
    if len(tweet_term) < 1: break
    data = get_tweet(tweet_term) #Data is a dictionary
    c += 1
    data_dict = json.loads(data)

## 4. With what you learn from the data -- e.g. how exactly to find the
##		text of each tweet in the big nested structure -- write code to print out
## 		content from 5 tweets, as shown in the linked example.
    for tweet in data_dict['statuses'][0:5]: #Print content from 5 tweets
        text = tweet['text']
        created_at = tweet['created_at']
        print('TEXT:', text) #Print out text
        print('CREATED AT:', created_at) #Print when the tweet was created
        print('\n')








