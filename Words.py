#Charles Kelsey 2/9/22
#a silly program that does random things when a word is entered
#things i learned making this:
#-manipulating strings and lists in a more "pythonic" way
#-installing libraries using pip
#-making calls to an API
#-using JSON objects
#-using sets (as opposed to lists)

import random
import json
import requests

#setup for oxforddictionaries.com api
app_id = "a08cd97d"
app_key = "84e6be224cfb8382bd83270231422854"

endpoint = "entries"
language_code = "en-us"

partsOfSpeech = set(["noun", "pronoun", "verb", "adjective", "adverb", "preposition", "conjunction", "interjection"])

while True:
    print("Enter a word:")

    word = input().lower()
    if word == "exit":
        break

    url = "https://od-api.oxforddictionaries.com/api/v2/" + endpoint + "/" + language_code + "/" + word.lower()
    r = requests.get(url, headers = {"app_id": app_id, "app_key": app_key})

    response = r.json()

    #check that the request returned a valid word
    if("error" in response):
        print("Error: that's not a word.")
        continue

    #print(json.dumps(response, indent=4, sort_keys=True))

    print("Word has an even number of characters:")
    print(len(word) % 2 == 0)

    print("Contains an E:")
    print("e" in word)

    #display first 3 words of definition
    #the structure of the returned JSON doesn't seem to be predictable, so the definition might be in one of several places
    try:
        definition = response["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["definitions"][0]
    except KeyError:
        try:
            definition = response["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["shortDefinitions"][0]
        except KeyError:
            print("Error: unexpected JSON.")
            continue
    
    #split the definition into a list of words, then join the first 3 into a new string with spaces between
    shortdef = " ".join(definition.split(" ")[:3])

    print("First 3 words of definition:")
    print(shortdef)

    #randomly choose one part of speech that this word is *not*
    parts = set()

    for x in response["results"]:
        for y in x["lexicalEntries"]:
            parts.add(y["lexicalCategory"]["id"])

    print("This word is not a " + random.choice(tuple(partsOfSpeech - parts)) + ".")

print("Exiting...")