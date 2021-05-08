import json

with open("data/playerInfoProcessed.json") as f:
	data = json.load(f)

def getPlayerInfo(initials):
	# fetch = document.find_one({"playerInitials": initials})
	fetch = data[initials] #may be same for some

	return fetch 