import os, json, time

with open('teams/teams.json') as f:
  data = json.load(f)

for filename in os.listdir('teams'):
	time.sleep(0.5)
	filenameToPass = filename.replace(".txt", "")
	filenameToPassUpper = filenameToPass.upper()
	if("json" not in filenameToPass):	
		f = open(f"teams/{filenameToPass}.txt", "r")
		data[filenameToPass] = []
		for l in f:
			if("XTEAM" not in l):
				l = l.replace("\n", "")
				data[filenameToPass].append(l)


with open('teams/teams.json', 'w') as json_file:
  json.dump(data, json_file)

