# Script to parse json data from Apple App Store API
# Liam Goudge August 2018

import urllib
import json
import re
import sys # for exception handling

fname = '/Users/username/Desktop/output.csv' # whatever path you want for the output file
fh = open(fname,'w')

headlines = ("AppName", "AppID", "Artist", "ArtistID", "URL", "Rating", "RatingCount",'\n')
sep = "^" # this is the character that will separate fields in the output CSV file. Set Excel to parse on this character.
fh.write(sep.join(headlines))

#term = 'Health+%26+Fitness'
term = 'glucose' # this is the term that you want to search on the App Store. Can be an app or 
limit = '50' # max number of returns is currently 200
entity = 'software'
country = 'us'

myurl = 'https://itunes.apple.com/search?term='+term+'&country='+country+'&entity='+entity+'&limit='+limit
    
print 'Retrieving', myurl
uh = urllib.urlopen(myurl)
data = uh.read()
print 'Retrieved',len(data),'characters'
	
try: js = json.loads(str(data))
except Exception, e:
    print >> sys.stderr, "Exception: %s" % str(e)
    sys.exit(1)

myArray = js["results"]

if myArray:
	for app in myArray:
		name = app["trackName"]
		trackID = app["trackId"]
		genre = app["primaryGenreName"]
		genreIDs = app["genreIds"]
		primaryGenre = app["primaryGenreId"]
		seller = app["sellerName"]
		artistName = app["artistName"]
		artistID = app["artistId"]
		bundleID = app["bundleId"]
	
		try: sellerURL = app["sellerUrl"] # not every app has this field
		except: sellerURL = None
	
		try: rating = app["averageUserRating"] # not every app has this field
		except: rating = None

		try: allTimeRatingCount = app["userRatingCount"] # not every app has this field
		except: allTimeRatingCount = None
	
		try: currentVersionRatingCount = app["userRatingCountForCurrentVersion"] # not every app has this field
		except: currentVersionRatingCount = None
	
		released = app["releaseDate"]
		price = app["price"]
		descr = app["description"]
		devices = app["supportedDevices"]
	
		result = (name, str(trackID), artistName, str(artistID), str(sellerURL), str(rating), str(allTimeRatingCount), str(currentVersionRatingCount), '\n')

		lineData = sep.join(result)
		clean = re.sub('[^\x00-\x7e]','*',lineData) # pull out all the weird characters that stop a write
	
		try: fh.write(clean)
		except: print "Couldn't write " + clean

else:
	print "No data returned from App Store"


fh.close()
