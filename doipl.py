from main import game
from tabulate import tabulate

teams = ['dc', 'csk', 'rcb', 'mi', 'kkr', 'pbks', 'rr', 'srh']
points = {}
for i in teams:
	points[i] = {"P": 0, "W": 0, "L": 0, "T": 0, "runsScored": 0, "ballsFaced": 0, "runsConceded": 0, "ballsBowled": 0, "pts": 0}

battingf = 0
bowlingf = 0

for i in teams:
	team1 = i
	for j in teams:
		if(i != j):
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


pointsTabulate = sorted(pointsTabulate, key=lambda x: (x[6], -x[5]))
pointsTabulate.reverse()

print(tabulate(pointsTabulate, ["Team", "Played", "Won", "Lost" ,"Tied", "NRR", "Points"], tablefmt="grid"))
print("bat", battingf, "bowl", bowlingf)


