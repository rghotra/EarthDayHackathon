import openai
import os

import googlemaps
from datetime import datetime

base_url = 'https://routes.googleapis.com/directions/v2:computeRoutes'

with open('gpt_key.txt', 'r') as file:
    openai.api_key = file.readlines()[0]

with open('maps_key.txt', 'r') as file:
    maps_key = file.readlines()[0]

def getCoords(addy):

    strAddy = f"{addy['street'], addy['city'], addy['state'], addy['zipcode']}"
    prompt = f"What are the latitude and longitude coordinates of {strAddy}? Respond with two numbers separated by a space and no other words."


    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    c1, c2 = str(response['choices'][0]['text']).strip('\n').split(" ")

    return float(c1), float(c2)

def getMapsResponse(src, dst, mode='driving', submode=None): #submode = rail or bus

    gmaps = googlemaps.Client(key=maps_key)

    response = gmaps.directions(
        src,
        dst,
        mode=mode, # “driving”, “walking”, “bicycling” or “transit”
        alternatives=False,
        language='en-US',
        units='imperial',
        departure_time=datetime.now(),
        transit_mode=submode,
        traffic_model="best_guess"
    )

    return response

def getSteps(response):

    if not response:
        return []

    steps = []
    for s in response[0]['legs'][0]['steps']:
        speed = s['distance']['value']/s['duration']['value'] # m/s
        speed *= 2.23693629 # mi/h
        steps.append([speed, s['distance']['value']*0.000621371192])

    return steps

def getDirections(response):
    if not response:
        return []
    
    return [i['html_instructions'].strip('%n') for i in response[0]['legs'][0]['steps']]
