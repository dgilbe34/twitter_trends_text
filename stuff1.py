# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 19:31:21 2016

@author: Drew Gilbertson
"""

from twilio.rest import TwilioRestClient 
import tweepy
import googlemaps

def send_text(sms_body):
    # put your own credentials here 
    ACCOUNT_SID = "ACb11e191cec67bbd230b2933735af2c41" 
    AUTH_TOKEN = "2ac54df4b2ac1a8749460481aee74a72" 
     
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
     
    client.messages.create(
        to="+12026049770", 
        from_="+13012653336", 
        body=sms_body, 
        #media_url="http://farm2.static.flickr.com/1075/1404618563_3ed9a44a3a.jpg", 
    )
def find_coords():
    # Replace the API key below with a valid API key.
    gmaps = googlemaps.Client(key='AIzaSyA0U0dksUA7lN4kzXOixJEljqLposzu-6M')
    location = input("Please enter your current location: ")
    # Geocoding and address
    geocode_result = gmaps.geocode(location)
    lat_lng = geocode_result[0]['geometry']['location']
    return lat_lng
    """
    # Request directions via public transit
    now = datetime.now()
    directions_result = gmaps.directions("Sydney Town Hall",
                                         "Parramatta, NSW",
                                         mode="transit",
                                         departure_time=now)
    """

def get_trends(coords):
    auth = tweepy.OAuthHandler("VGMmGmqsSCm7urqc2GPBMGrhu", "kpsOx3peDVniaIzsqlXaYrVbeu9ul7UtC3mpQMWdTxtuniaTm9")
    auth.set_access_token("316935684-UNjkigZOsU217X4t7GqOkGzU1v2Z2LEFI5g0suvE", "tfttvUnKFhHgrOm2rAcegEofWhq6vL7vWZ5Jd3MYFrYPz")
    
    api = tweepy.API(auth)
    
    retrieve_woeid = api.trends_closest(coords['lat'],coords['lng'])[0]
    #print(retrieve_woeid)
    
    trends=api.trends_place(retrieve_woeid['woeid'])
    trends=trends[0]['trends']
    
    #woeid=retrieve_woeid[0]['woeid']
    sms_body = "The closest location with trendng data is " + retrieve_woeid['name']+". Here are the current trends..."
    for index, trend_info in enumerate(trends):
        if index < 10:
            sms_body += "\n"+ str(index+1) + ". "+trend_info['name'] 
    return sms_body
    

def main():
    
    coords = find_coords()
    sms_body = get_trends(coords)
    send_text(sms_body)
    
main()
