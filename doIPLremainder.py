from mainconnect import game
from tabulate import tabulate

teams = ['dc', 'csk', 'rcb', 'mi', 'kkr', 'pbks', 'rr', 'srh']
alreadyDone = {"mivrcb", "cskvdc", "kkrvsrh", "pbksvrr",
"mivkkr", "rcbvsrh", "dcvrr", "pbksvcsk", "mivsrh", "rcbvkkr",
"pbksvdc", "cskvrr", "mivdc", "pbksvsrh", "cskvkkr",
"rrvrcb", "mivpbks", "kkrvrr", "cskvrcb", "dcvsrh", 
"pbksvkkr", "rcbvdc", "srhvcsk",  "rrvmi", "kkrvdc", 
"pbksvrcb", "cskvmi", "rrvsrh", "dcvpbks"
	
}
points = {}
points['dc'] = {"P": 8, "W": 6, "L": 2, "T": 0, "runsScored": 1325, "ballsFaced": 902, "runsConceded": 1320, "ballsBowled": 958, "pts": 12}
points['csk'] = {"P": 7, "W": 5, "L": 2, "T": 0, "runsScored": 1285, "ballsFaced": 805, "runsConceded": 1153, "ballsBowled": 832, "pts": 10}
points['rcb'] = {"P": 7, "W": 5, "L": 2, "T": 0, "runsScored": 1132, "ballsFaced": 819, "runsConceded": 1185, "ballsBowled": 840, "pts": 10}
points['mi'] = {"P": 7, "W": 4, "L": 3, "T": 0, "runsScored": 1120, "ballsFaced": 831, "runsConceded": 1098, "ballsBowled": 821, "pts": 8}
points['rr'] = {"P": 7, "W": 3, "L": 4, "T": 0, "runsScored": 1212, "ballsFaced": 831, "runsConceded": 1207, "ballsBowled": 810, "pts": 6}
points['pbks'] = {"P": 8, "W": 3, "L": 5, "T": 0, "runsScored": 1242, "ballsFaced": 946, "runsConceded": 1212, "ballsBowled": 882, "pts": 6}
points['kkr'] = {"P": 7, "W": 2, "L": 5, "T": 0, "runsScored": 1110, "ballsFaced": 820, "runsConceded": 1166, "ballsBowled": 812, "pts": 4}
points['srh'] = {"P": 7, "W": 1, "L": 6, "T": 0, "runsScored": 1073, "ballsFaced": 820, "runsConceded": 1158, "ballsBowled": 819, "pts": 2}


battingf = 0
bowlingf = 0

for i in teams:
	team1 = i
	for j in teams:
		if(i != j):
			done = False
			for d in alreadyDone:
				if(d == f"{i}v{j}"):
					done = True

			if(not done):
				team2 = j
				print(f"Welcome to {i.upper()} vs {j.upper()}")
				resList = game(False, i, j)
				print(resList[0])
				print(resList[2])
				winner = resList[-1]
				innings1Balls = 120
				innings2Balls = resList[5]
				innings1Runs = resList[6]
				innings2Runs = resList[7]

				innings1Bat = resList[-3]
				innings2Bat = resList[-2]
				winMsg = resList[8]

				loser = i
				if(winner == i):
					loser = j

				print(winMsg)
				if("runs" in winMsg):
					battingf += 1
				else:
					bowlingf += 1
				


				if(winner == "tie"):
					points[i]['P'] += 1
					points[j]['P'] += 1

					points[i]['T'] += 1
					points[j]['T'] += 1

					points[i]['pts'] += 1
					points[j]['pts'] += 1

					points[innings1Bat]['runsScored'] += innings1Runs
					points[innings2Bat]['runsScored'] += innings2Runs

					points[innings1Bat]['runsConceded'] += innings2Runs
					points[innings2Bat]['runsConceded'] += innings1Runs

					points[innings1Bat]['ballsBowled'] += innings2Balls
					points[innings2Bat]['ballsBowled'] += innings1Balls

					points[innings1Bat]['ballsFaced'] += innings1Balls
					points[innings2Bat]['ballsFaced'] += innings2Balls

				else:
					points[i]['P'] += 1
					points[j]['P'] += 1

					points[winner]['W'] += 1
					points[loser]['L'] += 1

					points[winner]['pts'] += 2
					points[innings1Bat]['runsScored'] += innings1Runs
					points[innings2Bat]['runsScored'] += innings2Runs

					points[innings1Bat]['runsConceded'] += innings2Runs
					points[innings2Bat]['runsConceded'] += innings1Runs

					points[innings1Bat]['ballsBowled'] += innings2Balls
					points[innings2Bat]['ballsBowled'] += innings1Balls

					points[innings1Bat]['ballsFaced'] += innings1Balls
					points[innings2Bat]['ballsFaced'] += innings2Balls

pointsTabulate = []

for team in points:
	l = []
	l = [team.upper(), points[team]['P'], points[team]['W'], points[team]['L'], points[team]['T']]

	nrr = 0
	nrr_scored = (points[team]['runsScored'] / points[team]['ballsFaced']) * 6
	nrr_conceded = (points[team]['runsConceded'] / points[team]['ballsBowled']) * 6
	nrr = nrr_scored - nrr_conceded
	l.append(nrr)
	l.append(points[team]['pts'])
	pointsTabulate.append(l)


pointsTabulate = sorted(pointsTabulate, key=lambda x: (x[6], x[5]))
pointsTabulate.reverse()

print(tabulate(pointsTabulate, ["Team", "Played", "Won", "Lost" ,"Tied", "NRR", "Points"], tablefmt="grid"))
print("bat", battingf, "bowl", bowlingf)


