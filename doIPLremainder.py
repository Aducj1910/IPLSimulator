from mainconnect import game
from tabulate import tabulate
import sys,os

rel = os.getcwd().replace("\\", "/")
dir = rel + '/scores'

for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))

teams = ['dc', 'csk', 'rcb', 'mi', 'kkr', 'pbks', 'rr', 'srh']
alreadyDone = {"mivrcb", "cskvdc", "kkrvsrh", "pbksvrr",
"mivkkr", "rcbvsrh", "dcvrr", "pbksvcsk", "mivsrh", "rcbvkkr",
"pbksvdc", "cskvrr", "mivdc", "pbksvsrh", "cskvkkr",
"rrvrcb", "mivpbks", "kkrvrr", "cskvrcb", "dcvsrh", 
"pbksvkkr", "rcbvdc", "srhvcsk",  "rrvmi", "kkrvdc", 
"pbksvrcb", "cskvmi", "rrvsrh", "dcvpbks"
    
}
points = {}

battingInfo = {}
bowlingInfo = {}
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

                bat1, bat2, bowl1, bowl2 = resList[9],resList[10],resList[11],resList[12]
            # print(bat2)
                for bat in bat1:
                    if(bat not in battingInfo):
                        battingInfo[bat] = bat1[bat]
                        battingInfo[bat]['innings'] = 1
                        battingInfo[bat]['scoresArray'] = [int(battingInfo[bat]['runs'])]
                    else:
                        battingInfo[bat]['balls'] += bat1[bat]['balls']
                        battingInfo[bat]['runs'] += bat1[bat]['runs']
                        battingInfo[bat]['ballLog'] += bat1[bat]['ballLog']
                        battingInfo[bat]['innings'] += 1
                        battingInfo[bat]['scoresArray'] +=[int(bat1[bat]['runs'])]

                for bat in bat2:
                    if(bat not in battingInfo):
                        battingInfo[bat] = bat2[bat]
                        battingInfo[bat]['innings'] = 1
                        battingInfo[bat]['scoresArray'] = [int(battingInfo[bat]['runs'])]
                    else:
                        battingInfo[bat]['balls'] += bat2[bat]['balls']
                        battingInfo[bat]['runs'] += bat2[bat]['runs']
                        battingInfo[bat]['ballLog'] += bat2[bat]['ballLog']
                        battingInfo[bat]['innings'] += 1
                        battingInfo[bat]['scoresArray'] +=[int(bat2[bat]['runs'])]

                for bowl in bowl1:
                    if(bowl not in bowlingInfo):
                        bowlingInfo[bowl] = bowl1[bowl]
                        bowlingInfo[bowl]['matches'] = 1
                    else:
                        bowlingInfo[bowl]['balls'] += bowl1[bowl]['balls']
                        bowlingInfo[bowl]['runs'] += bowl1[bowl]['runs']
                        bowlingInfo[bowl]['ballLog'] += bowl1[bowl]['ballLog']
                        bowlingInfo[bowl]['wickets'] += bowl1[bowl]['wickets']
                        bowlingInfo[bowl]['matches'] += 1

                for bowl in bowl2:
                    if(bowl not in bowlingInfo):
                        bowlingInfo[bowl] = bowl2[bowl]
                        bowlingInfo[bowl]['matches'] = 1

                    else:
                        bowlingInfo[bowl]['balls'] += bowl2[bowl]['balls']
                        bowlingInfo[bowl]['runs'] += bowl2[bowl]['runs']
                        bowlingInfo[bowl]['ballLog'] += bowl2[bowl]['ballLog']
                        bowlingInfo[bowl]['wickets'] += bowl2[bowl]['wickets']
                        bowlingInfo[bowl]['matches'] += 1

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
#Playoffs
final = []
elim = [pointsTabulate[2][0], pointsTabulate[3][0]]
q1 = [pointsTabulate[0][0], pointsTabulate[1][0]]
q2 = []

def playoffs(reslist, team1, team2):
    print(resList[0])
    print(resList[2])
    winner = resList[-1].upper()
    innings1Balls = 120
    innings2Balls = resList[5]
    innings1Runs = resList[6]
    innings2Runs = resList[7]

    innings1Bat = resList[-3]
    innings2Bat = resList[-2]
    winMsg = resList[8]

    loser = team1.upper()
    if(team1.upper() == winner):
        loser = team2.upper()

    print(winMsg.upper())

    bat1, bat2, bowl1, bowl2 = resList[9],resList[10],resList[11],resList[12]
    # print(bat2)
    for bat in bat1:
        if(bat not in battingInfo):
            battingInfo[bat] = bat1[bat]
            battingInfo[bat]['innings'] = 1
            battingInfo[bat]['scoresArray'] = [int(battingInfo[bat]['runs'])]
        else:
            battingInfo[bat]['balls'] += bat1[bat]['balls']
            battingInfo[bat]['runs'] += bat1[bat]['runs']
            battingInfo[bat]['ballLog'] += bat1[bat]['ballLog']
            battingInfo[bat]['innings'] += 1
            battingInfo[bat]['scoresArray'] +=[int(bat1[bat]['runs'])]

    for bat in bat2:
        if(bat not in battingInfo):
            battingInfo[bat] = bat2[bat]
            battingInfo[bat]['innings'] = 1
            battingInfo[bat]['scoresArray'] = [int(battingInfo[bat]['runs'])]
        else:
            battingInfo[bat]['balls'] += bat2[bat]['balls']
            battingInfo[bat]['runs'] += bat2[bat]['runs']
            battingInfo[bat]['ballLog'] += bat2[bat]['ballLog']
            battingInfo[bat]['innings'] += 1
            battingInfo[bat]['scoresArray'] +=[int(bat2[bat]['runs'])]

    for bowl in bowl1:
        if(bowl not in bowlingInfo):
            bowlingInfo[bowl] = bowl1[bowl]
            bowlingInfo[bowl]['matches'] = 1
        else:
            bowlingInfo[bowl]['balls'] += bowl1[bowl]['balls']
            bowlingInfo[bowl]['runs'] += bowl1[bowl]['runs']
            bowlingInfo[bowl]['ballLog'] += bowl1[bowl]['ballLog']
            bowlingInfo[bowl]['wickets'] += bowl1[bowl]['wickets']
            bowlingInfo[bowl]['matches'] += 1

    for bowl in bowl2:
        if(bowl not in bowlingInfo):
            bowlingInfo[bowl] = bowl2[bowl]
            bowlingInfo[bowl]['matches'] = 1

        else:
            bowlingInfo[bowl]['balls'] += bowl2[bowl]['balls']
            bowlingInfo[bowl]['runs'] += bowl2[bowl]['runs']
            bowlingInfo[bowl]['ballLog'] += bowl2[bowl]['ballLog']
            bowlingInfo[bowl]['wickets'] += bowl2[bowl]['wickets']
            bowlingInfo[bowl]['matches'] += 1

    return {'win': winner, 'lose': loser}


print(f"Qualifier 1 {q1[0]} vs {q1[1]}")
resList = game(False, q1[0], q1[1], "q1")
dict = playoffs(resList, q1[0], q1[1])
final.append(dict['win'])
q2.append(dict['lose'])

print(f"Eliminator {elim[0]} vs {elim[1]}")
resList = game(False, elim[0], elim[1], "eliminator")
dict = playoffs(resList, elim[0], elim[1])
q2.append(dict['win'])

print(f"Qualifier 2 {q2[0]} vs {q2[1]}")
resList = game(False, q2[0], q2[1], "q2")
dict = playoffs(resList, q2[0], q2[1])
final.append(dict['win'])

print(f"Final {final[0]} vs {final[1]}")
resList = game(False, final[0], final[1], "final")
dict = playoffs(resList, final[0], final[1])
print(f"{dict['win'].upper()} WINS THE IPL!!!")


#End
battingTabulate = []
for b in battingInfo:
    c = battingInfo[b]
    l = [b, c['innings'], c['runs']]
    outs = 0
    for bl in c['ballLog']:
        if("W" in bl):
            outs += 1

    avg = "NA"
    if(outs != 0):
        avg = c['runs'] / outs
        avg = str(round(avg, 2))
    sr = "NA"

    if(c['balls'] != 0):
        sr = c['runs'] / c['balls']
        sr = sr * 100
        sr = str(round(sr, 2))

    l += [avg, max(c['scoresArray']), sr ,c['balls']]
    battingTabulate.append(l)

bowlingTabulate = []
for b in bowlingInfo:
    c = bowlingInfo[b]
    l = [b, c['wickets']]

    if(c['balls'] != 0):
        overs_ =f"{str(c['balls'] // 6)}.{str(c['balls'] % 6)}"
        l += [overs_, c['runs']]
        l.append(str(round((((c['runs']/c['balls'])*6) - 0.5), 2))) #-0.5 REMOVE LATER --IMPORTANT
    else:
        l += [0, c['runs'], "NA"]

    bowlingTabulate.append(l)

battingTabulate = sorted(battingTabulate, key=lambda x:(x[2]))
battingTabulate.reverse()
bowlingTabulate = sorted(bowlingTabulate, key=lambda x:(x[1]))
bowlingTabulate.reverse()

stdoutOrigin=sys.stdout 
sys.stdout = open(f"scores/batStats.txt", "w")

print(tabulate(battingTabulate, ["Player", "Innings", "Runs", "Average", "Highest","SR" ,"Balls"], tablefmt="grid"))

sys.stdout.close()
sys.stdout=stdoutOrigin

stdoutOrigin=sys.stdout 
sys.stdout = open(f"scores/bowlStats.txt", "w")

print(tabulate(bowlingTabulate, ["Player", "Wickets", "Overs", "Runs Conceded" ,"Economy"], tablefmt="grid"))

sys.stdout.close()
sys.stdout=stdoutOrigin


print("bat", battingf, "bowl", bowlingf)