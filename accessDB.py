import pymongo

connection = pymongo.MongoClient('localhost', 27017)

def getPlayerInfo(initials):
	db = connection['cricmanager']
	document = db['playerInfo']

	fetch = document.find_one({"playerInitials": initials})
	return fetch