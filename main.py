import random, accessDB
import copy

#rrr, run rate, last 7 balls of player

def doToss(pace, spin, outfield, secondInnDew, pitchDetoriate, typeOfPitch):
	battingLikely = 0.45
	if(secondInnDew):
		battingLikely = battingLikely - random.uniform(0.09, 0.2)
	if(pitchDetoriate):
		battingLikely = battingLikely + random.uniform(0.09, 0.2)
	if(typeOfPitch == "dead"):
		battingLikely = battingLikely - random.uniform(0.05, 0.15)
	if(typeOfPitch == "green"):
		battingLikely = battingLikely + random.uniform(0.05, 0.15)
	if(typeOfPitch == "dusty"):
		battingLikely = battingLikely + random.uniform(0.04, 0.1)

	toss = random.randint(0, 1)
	# print(toss, battingLikely)
	if(toss == 0):
		outcome = random.uniform(0, 1)
		if(outcome > battingLikely):
			return(1)
		else:
			return(0)

	else:
		outcome = random.uniform(0,1)
		if(outcome > battingLikely):
			return(0)
		else:
			return(1)


def pitchInfo(venue, typeOfPitch):
	if(typeOfPitch == "dusty"):
		pace = 1 + 0.5*(random.random() * (random.random()-random.random())) #how good the pitch is for pace. 0.75-1.25, lower is better for bowling
		spin = 1 + 0.5*(random.random() * (random.random()-random.random())) #how good the pitch is for spin. 0.75-1.25, lower is better for bowling
		spin = spin - random.uniform(0.1, 0.16)
		outfield = 1 + 0.5*(random.random() * (random.random()-random.random())) #how good the outfield is. 0.75-1.25, lower is better for bowling
	elif(typeOfPitch == "green"):
		pace = 1 + 0.5*(random.random() * (random.random()-random.random())) #how good the pitch is for pace. 0.75-1.25, lower is better for bowling
		pace = pace - random.uniform(0.1, 0.16)
		spin = 1 + 0.5*(random.random() * (random.random()-random.random())) #how good the pitch is for spin. 0.75-1.25, lower is better for bowling
		outfield = 1 + 0.5*(random.random() * (random.random()-random.random())) #how good the outfield is. 0.75-1.25, lower is better for bowling
	elif(typeOfPitch == "dead"):
		pace = 1 + 0.5*(random.random() * (random.random()-random.random())) #how good the pitch is for pace. 0.75-1.25, lower is better for bowling
		spin = 1 + 0.5*(random.random() * (random.random()-random.random())) #how good the pitch is for spin. 0.75-1.25, lower is better for bowling
		outfield = 1 + 0.5*(random.random() * (random.random()-random.random())) #how good the outfield is. 0.75-1.25, lower is better for bowling

	return [pace, spin, outfield]

def innings(batting, bowling, battingName, bowlingName, pace, spin, outfield, dew, detoriate):
	# print(battingName, bowlingName, pace, spin, outfield, dew, detoriate)
	bowlerTracker = {}
	batterTracker = {}
	battingOrder = []
	catchingOrder = []

	runs = 0
	balls = 0
	#break or spin; medium or fast

	def delivery(bowler, batter, over):
		nonlocal runs
		batInfo = None
		bowlInfo = None
		wideRate = bowler['bowlWideRate']
		noballRate = bowler['bowlNoballRate']

		if(bowler['bowlStyle'] in batter['player']['byBowler']):
			batInfo = batter['player']['byBowler'][bowler['bowlStyle']]

		else:
			batInfo = batter['player']


		if(batter['player']['batStyle'] in bowler['byBatsman']):
			bowlInfo = bowler['byBatsman'][batter['player']['batStyle']]

		else:
			bowlInfo = bowler

		if('break' or 'spin' in bowler['bowlStyle']): #Increase effect and divide from negative things for bowler to positive (W, 1, 0)
			effect = (1.0 - spin)/2
			# print("effect:", effect, "original:", spin)
			bowlInfo['bowlOutsRate'] += (effect *0.2)
			bowlInfo['bowlRunDenominationsObject']['0'] += (effect * 0.45)
			bowlInfo['bowlRunDenominationsObject']['1'] += (effect * 0.25)
			bowlInfo['bowlRunDenominationsObject']['4'] -= (effect *0.4)
			bowlInfo['bowlRunDenominationsObject']['6'] -= (effect *0.3)
		elif('medium' or 'fast' in bowler['bowlStyle']):
			effect = (1.0 - fast)/2
			# print("effect:", effect, "original:", fast)
			bowlInfo['bowlOutsRate'] += (effect *0.2)
			bowlInfo['bowlRunDenominationsObject']['0'] += (effect * 0.45)
			bowlInfo['bowlRunDenominationsObject']['1'] += (effect * 0.25)
			bowlInfo['bowlRunDenominationsObject']['4'] -= (effect *0.4)
			bowlInfo['bowlRunDenominationsObject']['6'] -= (effect *0.3)

		# print(batInfo)
		denAvg = {}
		outAvg = (batInfo['batOutsRate'] + bowlInfo['bowlOutsRate']) / 2

		for batKey in batInfo['batRunDenominationsObject']:
			denAvg[batKey] = (batInfo['batRunDenominationsObject'][batKey] + bowlInfo['bowlRunDenominationsObject'][batKey])/2

		runRate = 0

		def getOutcome(den, out):
			nonlocal runs
			# print(den)
			total = 0
			for denom in den:
				total += den[denom]

			last = 0
			denominationProbabilties = []
			for denom in den:
				denomObj = {"denomination": denom, "start": last, "end":  last + den[denom] }
				denominationProbabilties.append(denomObj)
				last += den[denom]

			decider = random.uniform(0, total)
			for prob in denominationProbabilties:
				if(prob['start'] <= decider and prob['end'] > decider):
					if(prob['denomination'] != '0'):
						print(prob['denomination'])	
					runs += int(prob['denomination']) #Next - add wicket types, extras, bowler rotation, new batsman, innings change, aggression changes based on over number and rr, and based on last 10 ball player form
					if(prob['denomination'] == '0'):
						probOut = outAvg*(total/den['0'])
						outDecider = random.uniform(0,1)
						# print(outDecider)
						if(probOut > outDecider):
							print("W")
						else:
							print(prob['denomination'])

		if(balls > 0):
			runRate = (runs/balls)*6

		if(balls < 12):
			sixAdjustment = random.uniform(0.02, 0.05)
			if(outAvg < 0.04):
				outAvg = 0.01
			else:
				outAvg = outAvg - 0.04

			if(sixAdjustment > denAvg['6']):
				sixAdjustment = denAvg['6']

			denAvg['6'] -= sixAdjustment
			denAvg['0'] += sixAdjustment * (1/3)
			denAvg['1'] += sixAdjustment * (2/3)
			getOutcome(denAvg, outAvg)

		

	#Deciding batting order
	for i in batting:
		runObj = {}
		outObj = {}
		i['batBallsTotal'] += 1
		for run in i['batRunDenominations']:
			runObj[run] = i['batRunDenominations'][run] / i['batBallsTotal']
		i['batRunDenominationsObject'] = runObj

		for out in i['batOutTypes']:
			outObj[out] = i['batOutTypes'][out] / i['batBallsTotal']
		i['batOutTypesObject'] = outObj

		for styles in i['byBowler']:

			runObj2 = {}
			outObj2 = {}
			batOutsRate = i['byBowler'][styles]['batOutsTotal'] / i['byBowler'][styles]['batBallsTotal']
			i['byBowler'][styles]['batOutsRate'] = batOutsRate
			for run in i['byBowler'][styles]['batRunDenominations']:
				runObj2[run] = i['byBowler'][styles]['batRunDenominations'][run] / i['byBowler'][styles]['batBallsTotal']
			i['byBowler'][styles]['batRunDenominationsObject'] = runObj2
			for out in i['byBowler'][styles]['batOutTypes']:
				outObj2[out] = i['byBowler'][styles]['batOutTypes'][out] / i['byBowler'][styles]['batBallsTotal']
			i['byBowler'][styles]['batOutTypesObject'] = outObj2

		i['batOutsRate'] = i['batOutsTotal'] / i['batBallsTotal']

		newPos = []
		for p in i['position']:
			if(p != "null"):
				newPos.append(p)
		posTotal = sum(newPos)
		if(len(newPos) != 0):			
			posAvg = posTotal/len(newPos)
		else:
			posAvg = 9.0
		battingOrder.append({"posAvg": posAvg, "player": i})

	battingOrder = sorted(battingOrder, key=lambda k: k['posAvg']) 
	catchingOrder = sorted(catchingOrder, key=lambda k:k['catchRate'])

	for i in bowling:
		runObj = {}
		outObj = {}
		i['catchRate'] = i['catches'] / i['matches']
		i['bowlWideRate'] = i['bowlWides'] / i['matches']
		i['bowlNoballRate'] = i['bowlNoballs'] / i['matches']
		i['bowlBallsTotal'] += 1
		for run in i['bowlRunDenominations']:
			runObj[run] = i['bowlRunDenominations'][run] / i['bowlBallsTotal']
		i['bowlRunDenominationsObject'] = runObj

		for out in i['bowlOutTypes']:
			outObj[out] = i['bowlOutTypes'][out] / i['bowlBallsTotal']
		i['bowlOutTypesObject'] = outObj

		for styles in i['byBatsman']:
			runObj2 = {}
			outObj2 = {}
			bowlOutsRate = i['byBatsman'][styles]['bowlOutsTotal'] / i['byBatsman'][styles]['bowlBallsTotal']
			i['byBatsman'][styles]['bowlOutsRate'] = batOutsRate
			for run in i['byBatsman'][styles]['bowlRunDenominations']:
				runObj2[run] = i['byBatsman'][styles]['bowlRunDenominations'][run] / i['byBatsman'][styles]['bowlBallsTotal']
			i['byBatsman'][styles]['bowlRunDenominationsObject'] = runObj2
			for out in i['byBatsman'][styles]['bowlOutTypes']:
				outObj2[out] = i['byBatsman'][styles]['bowlOutTypes'][out] / i['byBatsman'][styles]['bowlBallsTotal']
			i['byBatsman'][styles]['bowlOutTypesObject'] = outObj2


		i['bowlOutsRate'] = i['bowlOutsTotal'] / i['bowlBallsTotal']

		obj = {"20":0,"1":0, "2":0, "3":0, "4":0,"5":0,"6":0,"7":0,"8":0,"9":0,"10":0,"11":0,"12":0,"13":0,"14":0,"15":0,"16":0,"17":0,"18":0,"19":0}
		for over in i['overNumbers']:
			obj[over] += 1
		for keys in obj:
			if(i['matches'] != 0):
				avg = obj[keys]/i['matches']
			else:
				avg = -1
			obj[keys] = avg
		i['overNumbersObject'] = obj

	bowlingOpening = sorted(bowling, key=lambda k:k['overNumbersObject']['1'])
	bowlingOpening.reverse()
	batter1 = battingOrder[0]
	batter2 = battingOrder[1]
	for i in range(20):
		if(i == 0):
			overBowler = bowlingOpening[0]
			for i in range(6):
				# print(overBowler['byBatsman']['right-hand bat']['bowlRunDenominationsObject']['4'])
				delivery(copy.deepcopy(overBowler), copy.deepcopy(batter1), i)

	

def game():
	f = open("teams/match.txt", "r")
	team1 = None
	team2 = None
	venue = None
	toss = None

	secondInnDew = False
	#for 1st
	dew = False
	pitchDetoriate = True
	#for 1st
	detoriate = False

	paceFactor = None
	spinFactor = None
	outfield = None
	typeOfPitch = "dusty"

	team1Players = []
	team2Players = []

	team1Info = []
	team2Info = []

	#spin, pace factor -> 0.0 - 1.0
	for l in f:
		l = l.replace("\n", "")
		if("XVENUE" in l):
			venue = l.split("-")[1]
			# print(venue)

		elif("XTEAM" in l):
			if(team1 == None):
				team1 = l.split("-")[1]
			else:
				team2 = l.split("-")[1]

		elif(l != ''):
			if(team2 == None):
				team1Players.append(l)
			else:
				team2Players.append(l)

	for player in team1Players:
		obj = accessDB.getPlayerInfo(player)
		team1Info.append(obj)

	for player in team2Players:
		obj = accessDB.getPlayerInfo(player)
		team2Info.append(obj)

	pitchInfo_ = pitchInfo(venue, typeOfPitch)
	paceFactor, spinFactor, outfield = pitchInfo_[0], pitchInfo_[1], pitchInfo_[2]
	battingFirst = doToss(paceFactor, spinFactor, outfield, secondInnDew,pitchDetoriate,typeOfPitch)
	# print(paceFactor, spinFactor, outfield)

	def getBatting():
		if(battingFirst == 0):
			return [team1Info, team2Info, team1, team2]
		else:
			return [team2Info, team1Info, team2, team1]

	innings(getBatting()[0], getBatting()[1], getBatting()[2], getBatting()[3], paceFactor, spinFactor, outfield, dew, detoriate)

game()

