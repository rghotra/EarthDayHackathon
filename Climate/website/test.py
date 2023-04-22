import maps_api

addy1 = {
    'street': '36 Valley Street',
    'city': 'Lake Ronkonkoma',
    'state': 'NY',
    'zipcode': 11797
}

addy2 = {
    'street': '70 Morningside Drive',
    'city': 'New York',
    'state': 'NY',
    'zipcode': 10027
}

src = maps_api.getCoords(addy1)
dst = maps_api.getCoords(addy2)

print("Source: ", src)
print("Destination: ", dst)

response = maps_api.getMapsResponse(src, dst)
print([i['html_instructions'] for i in response[0]['legs'][0]['steps']])
