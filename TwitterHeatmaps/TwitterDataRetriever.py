import tweepy
from tweepy import OAuthHandler
import ssl
import certifi
from geopy import geocoders
from geopy.exc import GeocoderTimedOut
import config


class TwitterDataRetriever:
    consumer_key = config.twitter_consumer_key
    consumer_secret = config.twitter_consumer_secret
    access_key = config.twitter_access_key
    access_secret = config.twitter_access_secret

    def __init__(self):
        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(self.consumer_key, self.consumer_secret)
            # set access token and secret
            self.auth.set_access_token(self.access_key, self.access_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def get_tweet_locations(self, query='NBA'):
        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q=query, count=100, result_type="recent")
            locations = []

            # parsing tweets one by one
            for tweet in fetched_tweets:
                location = self.get_location(tweet)
                if location is not None:
                     locations.append(self.get_location(tweet))
                print(tweet.text, "\n", tweet.place, "\n", tweet.created_at)
                print("----------")
            return locations

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))

    def get_location(self, tweet):
        place = tweet.place
        if place is not None:
            coords = place.bounding_box.coordinates[0]
            coord0 = coords[0]
            coord1 = coords[1]
            coord2 = coords[2]

            long = (coord0[0] + coord1[0]) / 2.0000
            lat = (coord0[1] + coord2[1]) / 2.0000
            return [lat, long]   #list ex. [-122.419, 37.7793]
        coordinates = tweet.coordinates
        if coordinates is not None:
            return coordinates["coordinates"]   #list ex. [-122.419, 37.7793]
        geo = tweet.geo
        if geo is not None:
            return geo["coordinates"]   #list ex. [37.7793, -122.419]
        user = tweet.user
        user_location = user.location
        if user_location is not None:
            ctx = ssl.create_default_context(cafile=certifi.where())
            geocoders.options.default_ssl_context = ctx
            geocoders.options.default_user_agent = config.nominatim_user_agent
            #password for geonames - mylocator
            gn = geocoders.Nominatim(user_agent=config.nominatim_user_agent, timeout=15)
            try:
                location = gn.geocode(user_location)
            except GeocoderTimedOut as e:
                print("Geocoder timed out trying to retrieve coordinates for: " + user_location)
                return None
            if location is None:
                return None
            lat = location.latitude
            long = location.longitude
            return [lat, long]    #list ex. [37.7793, -122.419]
        else:
            return None