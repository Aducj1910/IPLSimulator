import random
import accessDB
import copy

# rrr, run rate, last 7 balls of player

#TO ADD IMPORTANT -> MORE BALLS THE PLAYER PLAYS, CALCULATE CONFIDENCE BASED ON ->
#1.LAST 7 BALLS, STRIKE RATE, NUMBER OF BALLS (like spin & pace factor it will +vely impact, allow player to accelerate)
#Eliminate slow partnership. Also, maybe increase wicket chance in middle overs to balance out,
#reduce out avg when high confidence (probably not)
#at the start slow sr then when, more balls higher sr 
#accelerate if sr is too low after certain number of balls or
#in accordance with rrr

#REDO ENTIRE BALL ALGORITH, LOOK FROM JAMIE001

#Rehaul -> remake entire ball by ball thing, look at past data to analyse 
#run rate worms of teams and correspond to that

#if certain number of wickets fell quickly, play more defensively

#Try to hit more if rr or rrr becomes low or large respectively

#When chasing or at death overs, make decision whether to attack on the ball or not -> attacking means
#6,4,W,0 but not attacking would get 0,1,2 more reliably

#If last x balls going well for entire team, then more attacking, else more defensive to protect wickets, if slow rr in last x balls
#then attack

#As player progresses through innings confidence will increase attacking rate (line 7)
#Batting order -> highest rate at that pos
#Maybe try to average out the denominations and the rest over the course of the innings

#CHASE LOGIC - take rrr into account every ball, importance increases by ball
#Try for certain number of runs (calc. by runs/balls) and try for that
#Add noballs

def doToss(pace, spin, outfield, secondInnDew, pitchDetoriate, typeOfPitch):
    battingLikely =  0.45
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
        outcome = random.uniform(0, 1)
        if(outcome > battingLikely):
            return(0)
        else:
            return(1)


def pitchInfo(venue, typeOfPitch):
    if(typeOfPitch == "dusty"):
        # how good the pitch is for pace. 0.75-1.25, lower is better for bowling
        pace = 1 + 0.5*(random.random() * (random.random()-random.random()))
        # how good the pitch is for spin. 0.75-1.25, lower is better for bowling
        spin = 1 + 0.5*(random.random() * (random.random()-random.random()))
        spin = spin - random.uniform(0.1, 0.16)
        # how good the outfield is. 0.75-1.25, lower is better for bowling
        outfield = 1 + 0.5*(random.random() *
                            (random.random()-random.random()))
    elif(typeOfPitch == "green"):
        # how good the pitch is for pace. 0.75-1.25, lower is better for bowling
        pace = 1 + 0.5*(random.random() * (random.random()-random.random()))
        pace = pace - random.uniform(0.1, 0.16)
        # how good the pitch is for spin. 0.75-1.25, lower is better for bowling
        spin = 1 + 0.5*(random.random() * (random.random()-random.random()))
        # how good the outfield is. 0.75-1.25, lower is better for bowling
        outfield = 1 + 0.5*(random.random() *
                            (random.random()-random.random()))
    elif(typeOfPitch == "dead"):
        # how good the pitch is for pace. 0.75-1.25, lower is better for bowling
        pace = 1 + 0.5*(random.random() * (random.random()-random.random()))
        # how good the pitch is for spin. 0.75-1.25, lower is better for bowling
        spin = 1 + 0.5*(random.random() * (random.random()-random.random()))
        # how good the outfield is. 0.75-1.25, lower is better for bowling
        outfield = 1 + 0.5*(random.random() *
                            (random.random()-random.random()))

    return [pace, spin, outfield]


def innings1(batting, bowling, battingName, bowlingName, pace, spin, outfield, dew, detoriate):
    # print(battingName, bowlingName, pace, spin, outfield, dew, detoriate)
    bowlerTracker = {} #add names of all in innings def
    batterTracker = {} #add names of all in innings def
    battingOrder = []
    catchingOrder = []
    ballLog = []

    runs = 0
    balls = 0
    wickets = 0
    # break or spin; medium or fast

    # Deciding batting order
    for i in batting:
        batterTracker[i['playerInitials']] = {'playerInitials': i['playerInitials'], 'balls': 0, 'runs': 0, 'ballLog': []}
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
            batOutsRate = i['byBowler'][styles]['batOutsTotal'] / \
                i['byBowler'][styles]['batBallsTotal']
            i['byBowler'][styles]['batOutsRate'] = batOutsRate
            for run in i['byBowler'][styles]['batRunDenominations']:
                runObj2[run] = i['byBowler'][styles]['batRunDenominations'][run] / \
                    i['byBowler'][styles]['batBallsTotal']
            i['byBowler'][styles]['batRunDenominationsObject'] = runObj2
            for out in i['byBowler'][styles]['batOutTypes']:
                outObj2[out] = i['byBowler'][styles]['batOutTypes'][out] / \
                    i['byBowler'][styles]['batBallsTotal']
            i['byBowler'][styles]['batOutTypesObject'] = outObj2

        i['batOutsRate'] = i['batOutsTotal'] / i['batBallsTotal']

        newPos = []
        posAvgObj = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7":0,"8": 0, "9":0, "10":0}
        for p in i['position']:
            if(p != "null"):
                newPos.append(p)
        posTotal = sum(newPos)
        for p in newPos:
            if(str(p) in posAvgObj):
                posAvgObj[str(p)] += 1
            else:
                posAvgObj[str(p)] = 1

        for key_p in posAvgObj:
            posAvgObj[key_p] = posAvgObj[key_p]/i['matches'] 

        if(len(newPos) != 0):
            posAvg = posTotal/len(newPos)
        else:
            posAvg = 9.0
        battingOrder.append({"posAvg": posAvg, "player": i, "posAvgsAll": posAvgObj})

    battingOrder = sorted(battingOrder, key=lambda k: k['posAvg'])
    catchingOrder = sorted(catchingOrder, key=lambda k: k['catchRate'])

    for i in bowling:
        i['bowlBallsTotalRate'] = i['bowlBallsTotal'] / i['matches']
        bowlerTracker[i['playerInitials']] = {'playerInitials': i['playerInitials'], 'balls': 0, 
        'runs': 0, 'ballLog': [], 'overs': 0, 'wickets': 0}
        runObj = {}
        outObj = {}
        i['catchRate'] = i['catches'] / i['matches']
        i['bowlWideRate'] = i['bowlWides'] / (i['bowlBallsTotal'] + 1)
        i['bowlNoballRate'] = i['bowlNoballs'] / (i['bowlBallsTotal'] + 1)
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
            bowlOutsRate = i['byBatsman'][styles]['bowlOutsTotal'] / \
                i['byBatsman'][styles]['bowlBallsTotal']
            i['byBatsman'][styles]['bowlOutsRate'] = batOutsRate
            for run in i['byBatsman'][styles]['bowlRunDenominations']:
                runObj2[run] = i['byBatsman'][styles]['bowlRunDenominations'][run] / \
                    i['byBatsman'][styles]['bowlBallsTotal']
            i['byBatsman'][styles]['bowlRunDenominationsObject'] = runObj2
            for out in i['byBatsman'][styles]['bowlOutTypes']:
                outObj2[out] = i['byBatsman'][styles]['bowlOutTypes'][out] / \
                    i['byBatsman'][styles]['bowlBallsTotal']
            i['byBatsman'][styles]['bowlOutTypesObject'] = outObj2

        i['bowlOutsRate'] = i['bowlOutsTotal'] / i['bowlBallsTotal']

        obj = {"20": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0,
               "10": 0, "11": 0, "12": 0, "13": 0, "14": 0, "15": 0, "16": 0, "17": 0, "18": 0, "19": 0}
        for over in i['overNumbers']:
            obj[over] += 1
        for keys in obj:
            if(i['matches'] != 0):
                avg = obj[keys]/i['matches']
            else:
                avg = -1
            obj[keys] = avg
        i['overNumbersObject'] = obj

    bowlingOpening = sorted(bowling, key=lambda k: k['overNumbersObject']['1'])
    bowlingOpening.reverse()
    bowlingDeath = sorted(bowling, key=lambda k: k['overNumbersObject']['19'])
    bowlingDeath.reverse()
    bowlingMiddle = sorted(bowling, key=lambda k: k['overNumbersObject']['10'])
    bowlingMiddle.reverse()
    batter1 = battingOrder[0]
    batter2 = battingOrder[1]
    onStrike = batter1
    bowler1 = bowlingOpening[0]
    bowler2 = bowlingOpening[1]

    lastOver = None


    def playerDismissed(player):
        nonlocal batter1, batter2, onStrike
        # print("OUT", player['player']['playerInitials'])
        if(wickets == 11):
            print("ALL OUT")
        else:
            if(batter1 == player):
                onStrike = battingOrder[wickets + 1]
                batter1 = battingOrder[wickets + 1]
                found = False
                index_l = 0
                while(not found):
                    localBattingOrder = sorted(battingOrder, key=lambda k: k['posAvgsAll'][str(wickets)])
                    localBattingOrder.reverse()
                    if(batterTracker[localBattingOrder[index_l]['player']['playerInitials']]['balls'] == 0):
                        onStrike = localBattingOrder[index_l]
                        batter1 = localBattingOrder[index_l]
                        found = True
                    else:
                        index_l += 1


            else:
                onStrike = battingOrder[wickets + 1]
                batter2 = battingOrder[wickets + 1]
                found = False
                index_l = 0
                while(not found):
                    localBattingOrder = sorted(battingOrder, key=lambda k: k['posAvgsAll'][str(wickets)])
                    localBattingOrder.reverse()
                    if(batterTracker[localBattingOrder[index_l]['player']['playerInitials']]['balls'] == 0):
                        onStrike = localBattingOrder[index_l]
                        batter2 = localBattingOrder[index_l]
                        found = True
                    else:
                        index_l += 1
             
        # print(batter1['player']['playerInitials']) 
        # print(batter2['player']['playerInitials'])

    def delivery(bowler, batter, over):
        nonlocal batterTracker, bowlerTracker, onStrike, ballLog, balls, runs, wickets
        batInfo = None
        bowlInfo = None
        wideRate = bowler['bowlWideRate']
        noballRate = bowler['bowlNoballRate']
        blname = bowler['playerInitials']
        btname = batter['player']['playerInitials']

        # if(bowler['bowlStyle'] in batter['player']['byBowler']):
        #     batInfo = batter['player']['byBowler'][bowler['bowlStyle']]

        # else:
        #     batInfo = batter['player']

        batInfo = batter['player']

        # if(batter['player']['batStyle'] in bowler['byBatsman']):
        #     bowlInfo = bowler['byBatsman'][batter['player']['batStyle']]

        # else:
        #     bowlInfo = bowler

        bowlInfo = bowler


        # Increase effect and divide from negative things for bowler to positive (W, 1, 0)
        if('break' or 'spin' in bowler['bowlStyle']):
            effect = (1.0 - spin)/2
            # print("effect:", effect, "original:", spin)
            bowlInfo['bowlOutsRate'] += (effect * 0.25)
            bowlInfo['bowlRunDenominationsObject']['0'] += (effect * 0.4)
            bowlInfo['bowlRunDenominationsObject']['1'] += (effect * 0.27)
            bowlInfo['bowlRunDenominationsObject']['4'] -= (effect * 0.6)
            bowlInfo['bowlRunDenominationsObject']['6'] -= (effect * 0.5)
        elif('medium' or 'fast' in bowler['bowlStyle']):
            effect = (1.0 - fast)/2
            # print("effect:", effect, "original:", fast)
            bowlInfo['bowlOutsRate'] += (effect * 0.25)
            bowlInfo['bowlRunDenominationsObject']['0'] += (effect * 0.4)
            bowlInfo['bowlRunDenominationsObject']['1'] += (effect * 0.27)
            bowlInfo['bowlRunDenominationsObject']['4'] -= (effect * 0.6)
            bowlInfo['bowlRunDenominationsObject']['6'] -= (effect * 0.5)

        # print(batInfo)
        denAvg = {}
        outAvg = (batInfo['batOutsRate'] + bowlInfo['bowlOutsRate']) / 2
        outTypeAvg = {}
        runoutChance = 0.01
        if(batter['player']['batOutsTotal'] != 0):
            runoutChance = (batter['player']['runnedOut']) / batter['player']['batBallsTotal']

        for batKey in batInfo['batRunDenominationsObject']:
            denAvg[batKey] = (batInfo['batRunDenominationsObject']
                              [batKey] + bowlInfo['bowlRunDenominationsObject'][batKey])/2

        runRate = 0
        for a,b in zip(batInfo['batOutTypesObject'], bowlInfo['bowlOutTypesObject']):
            outTypeAvg[a] = (batInfo['batOutTypesObject'][a] + bowlInfo['bowlOutTypesObject'][b]) / 2
        outTypeAvg['runOut'] = runoutChance
        # print(outTypeAvg)


        def getOutcome(den, out, over):
            nonlocal batterTracker, bowlerTracker, runs, balls, ballLog, wickets, onStrike

            # print(den)
            if(wideRate > random.uniform(0,1)): #add batter tracking & bowler tracking logs, read ln 267 & ln 255
             runs += 1
             print(over, f"{bowler['displayName']} to {batter['player']['displayName']}", "Wide", "Score: " + str(runs) + "/" + str(wickets))
             ballLog.append(f"{str(balls)}:WD")
             bowlerTracker[blname]['runs'] += 1
             bowlerTracker[blname]['ballLog'].append(f"{str(balls)}:WD")
            else:
                total = 0
                for denom in den:
                    total += den[denom]

                last = 0
                balls += 1
                denominationProbabilties = []
                for denom in den:
                    denomObj = {"denomination": denom,
                                "start": last, "end":  last + den[denom]}
                    denominationProbabilties.append(denomObj)
                    last += den[denom]

                decider = random.uniform(0, total)
                for prob in denominationProbabilties:
                    if(prob['start'] <= decider and prob['end'] > decider):
                        # Next - add wicket types, extras, bowler rotation, new batsman, innings change, aggression changes based on over number and rr, and based on last 10 ball player form
                        runs += int(prob['denomination'])
                        if(prob['denomination'] != '0'):
                            print(over, f"{bowler['displayName']} to {batter['player']['displayName']}", prob['denomination'], "Score: " + str(runs) + "/" + str(wickets))
                            ballLog.append(f"{str(balls)}:{prob['denomination']}")
                            bowlerTracker[blname]['runs'] += int(prob['denomination'])
                            bowlerTracker[blname]['ballLog'].append(f"{str(balls)}:{prob['denomination']}")
                            bowlerTracker[blname]['balls'] += 1
                            batterTracker[btname]['runs'] += int(prob['denomination'])
                            batterTracker[btname]['ballLog'].append(f"{str(balls)}:{prob['denomination']}")
                            batterTracker[btname]['balls'] += 1

                            if(int(prob['denomination']) % 2 == 1):
                               if(onStrike == batter1):
                                onStrike = batter2
                               elif(onStrike == batter2):
                                onStrike = batter1

                        if(prob['denomination'] == '0'): #during high rrr or death overs, probability
                        #of boundary & wicket are both higher
                            probOut = outAvg*(total/den['0'])
                            outDecider = random.uniform(0, 1)
                            # print(over, outDecider)
                            if(probOut > outDecider): #change to >
                                wickets += 1
                                out_type = None
                                probs_o = []
                                total_o = 0
                                last_o = 0
                                for out_k in outTypeAvg:
                                    total_o += outTypeAvg[out_k]
                                for out_k in outTypeAvg:
                                    outobj = {"type": out_k, "start": last_o,
                                     "end": last_o + outTypeAvg[out_k]}
                                    probs_o.append(outobj)
                                    last_o += outTypeAvg[out_k]
                                typeDeterminer = random.uniform(0, total_o)
                                for type_ in probs_o:
                                    if(type_['start'] <= typeDeterminer and type_['end'] > typeDeterminer):
                                        out_type = type_['type']
                                # print("OUTTTT", typeDeterminer, probs_o)

                                if(out_type == "runOut"): #dodismissal function
                                    runOutRuns = random.randint(0,2)
                                    runs += runOutRuns
                                    print(over, f"{bowler['displayName']} to {batter['player']['displayName']}", 
                                        "W", "Score: " + str(runs) + "/" + str(wickets), "Run Out!")
                                    ballLog.append(f"{str(balls)}:W")
                                    bowlerTracker[blname]['runs'] += runOutRuns
                                    bowlerTracker[blname]['ballLog'].append(f"{str(balls)}:{runOutRuns}")
                                    bowlerTracker[blname]['balls'] += 1
                                    batterTracker[btname]['runs'] += runOutRuns
                                    batterTracker[btname]['ballLog'].append(f"{str(balls)}:{runOutRuns}")
                                    batterTracker[btname]['balls'] += 1
                                    playerDismissed(onStrike)


                                elif(out_type == "caught"):
                                    # if(random.randint(0,1) == 1):
                                    #    if(onStrike == batter1):
                                    #     onStrike = batter2
                                    #    elif(onStrike == batter2):
                                    #     onStrike = batter1

                                    fTotal = 0
                                    fList = []
                                    catcher = None
                                    for bowlF in bowling:
                                        bowlF['catchRate']
                                        fList.append({'playerInitials': bowlF['playerInitials'],
                                            'displayName': bowlF['displayName'] ,
                                            "start": fTotal, "end": fTotal + bowlF['catchRate']})
                                        fTotal += bowlF['catchRate']
                                    catcherDetermine = random.uniform(0, fTotal)
                                    for fItem in fList:
                                        if(fItem['start'] <= catcherDetermine and fItem['end'] > catcherDetermine):
                                            catcher = {"playerInitials": fItem['playerInitials'],
                                            "displayName": fItem['displayName']}

                                    print(over, f"{bowler['displayName']} to {batter['player']['displayName']}", 
                                        "W", "Score: " + str(runs) + "/" + str(wickets), f"Caught by {catcher['displayName']}")

                                    ballLog.append(f"{str(balls)}:W-CaughtBy-{catcher['playerInitials']}")#add who caught for scorecard reference
                                    bowlerTracker[blname]['runs'] += int(prob['denomination'])
                                    bowlerTracker[blname]['ballLog'].append(f"{str(balls)}:W")
                                    bowlerTracker[blname]['balls'] += 1
                                    batterTracker[btname]['runs'] += int(prob['denomination'])
                                    batterTracker[btname]['ballLog'].append(f"{str(balls)}:W")
                                    batterTracker[btname]['balls'] += 1
                                    playerDismissed(onStrike)

                                elif(out_type == "bowled" or out_type == "lbw" or out_type == "hitwicket" or out_type == "stumped"):
                                    print(over, f"{bowler['displayName']} to {batter['player']['displayName']}", 
                                        "W", "Score: " + str(runs) + "/" + str(wickets), f"{out_type.title()}")
                                    ballLog.append(f"{str(balls)}:W")#add who caught for scorecard reference
                                    bowlerTracker[blname]['runs'] += int(prob['denomination'])
                                    bowlerTracker[blname]['ballLog'].append(f"{str(balls)}:W")
                                    bowlerTracker[blname]['balls'] += 1
                                    batterTracker[btname]['runs'] += int(prob['denomination'])
                                    batterTracker[btname]['ballLog'].append(f"{str(balls)}:W")
                                    batterTracker[btname]['balls'] += 1
                                    playerDismissed(onStrike)

                               
                            else:
                                # Strike Rotation
                                print(over, f"{bowler['displayName']} to {batter['player']['displayName']}", prob['denomination'], "Score: " + str(runs) + "/" + str(wickets))
                                ballLog.append(f"{str(balls)}:{prob['denomination']}")
                                bowlerTracker[blname]['runs'] += int(prob['denomination'])
                                bowlerTracker[blname]['ballLog'].append(f"{str(balls)}:{prob['denomination']}")
                                bowlerTracker[blname]['balls'] += 1
                                batterTracker[btname]['runs'] += int(prob['denomination'])
                                batterTracker[btname]['ballLog'].append(f"{str(balls)}:{prob['denomination']}")
                                batterTracker[btname]['balls'] += 1

        
        sumLast10 = 0
        outsLast10 = 0
        for i in ballLog:
            spl_bl = i.split(":")
            if("W" not in spl_bl[1]):
                sumLast10 += int(spl_bl[1])
            else:
                outsLast10 += 1

        if(balls < 110):
            adjust_last10 = random.uniform(0.02,0.04)
            if(outsLast10 < 2):
                denAvg['0'] -= adjust_last10 * (1/2)
                denAvg['1'] -= adjust_last10 * (1/2)
                denAvg['2'] += adjust_last10 * (1/2)
                denAvg['4'] += adjust_last10 * (1/2)
            else:
                adjust_last10 += 0.018
                denAvg['0'] += adjust_last10 * (1.1/2)
                denAvg['0'] += adjust_last10 * (0.9/2)
                denAvg['4'] -= adjust_last10 * (1/2)
                denAvg['6'] -= adjust_last10 * (1/2)
                outAvg -= 0.02



        if(batterTracker[btname]['balls'] < 8 and balls < 80):
            adjust = random.uniform(-0.01, 0.03)
            outAvg -= 0.015
            denAvg['0'] += adjust * (1.5/3)
            denAvg['1'] += adjust * (1/3)
            denAvg['2'] += adjust * (0.5/3)
            denAvg['4'] -= adjust * (0.5/3)
            denAvg['6'] -= adjust * (1.5/3)

        if(batterTracker[btname]['balls'] > 15 and batterTracker[btname]['balls'] < 30):
            adjust = random.uniform(0.03, 0.07)
            denAvg['0'] -= adjust * (1/3)
            # denAvg['1'] -= adjust *(1/3)
            denAvg['4'] += adjust * (1/3)

        # if(batterTracker[btname]['balls'] > 30):
        #     adjust = random.uniform(0.05, 0.1)
        #     denAvg['0'] -= adjust * (1.5/3)
        #     denAvg['4'] += adjust * (0.75/3)
        #     denAvg['6'] += adjust * (0.75/3)
        #     outAvg += 0.01

        if(batterTracker[btname]['balls'] > 20 and (batterTracker[btname]['runs'] / batterTracker[btname]['balls']) < 110):
            adjust = random.uniform(0.05, 0.08)
            denAvg['0'] += adjust * (1.5/3)
            denAvg['1'] += adjust * (0.5/3)
            denAvg['6'] += adjust * (2/3)
            outAvg += 0.05

        if(batterTracker[btname]['balls'] > 30 and (batterTracker[btname]['runs'] / batterTracker[btname]['balls']) > 145 and (wickets < 5) or balls > 102):
            adjust = random.uniform(0.06, 0.09)
            denAvg['0'] -= adjust * (1/3)
            denAvg['1'] -= adjust * (1.5/3)
            denAvg['4'] += adjust * (1.6/3)
            denAvg['6'] += adjust * (1.9/3)
            outAvg += 0.02


        if(balls > 0):
            runRate = (runs/balls)*6

        if(balls < 12):
            sixAdjustment = random.uniform(0.02, 0.05)
            if(outAvg < 0.07):
                outAvg = 0
            else:
                outAvg = outAvg - 0.07

            if(sixAdjustment > denAvg['6']):
                sixAdjustment = denAvg['6']

            denAvg['6'] -= sixAdjustment
            denAvg['0'] += sixAdjustment * (1/3)
            denAvg['1'] += sixAdjustment * (2/3)
            getOutcome(denAvg, outAvg, over)

        elif(balls >= 12 and balls < 36): #works very well with 120, try to adjust a bit for death and middle but
        #dont tinker too much
            if(wickets == 0):
                defenseAndOneAdjustment = random.uniform(0.05, 0.11)
                denAvg['0'] -= defenseAndOneAdjustment * (2/3)
                denAvg['1'] -= defenseAndOneAdjustment * (1/3)
                denAvg['4'] += defenseAndOneAdjustment * (2/3)
                denAvg['6'] += defenseAndOneAdjustment * (1/3)
                getOutcome(denAvg, outAvg, over)
            else:
                defenseAndOneAdjustment = random.uniform(0.02, 0.08)
                denAvg['0'] -= defenseAndOneAdjustment * (2/3)
                denAvg['1'] -= defenseAndOneAdjustment * (1/3)
                denAvg['4'] += defenseAndOneAdjustment * (2.5/3)
                denAvg['6'] += defenseAndOneAdjustment * (0.5/3)
                outAvg -= 0.03

                getOutcome(denAvg, outAvg, over)

        elif(balls >= 36 and balls < 102): #works very well with 120, try to adjust a bit for death and middle but
        #dont tinker too much
            if(wickets < 3):
                defenseAndOneAdjustment = random.uniform(0.05, 0.11)
                denAvg['0'] -= defenseAndOneAdjustment * (1.5/3)
                denAvg['1'] -= defenseAndOneAdjustment * (1/3)
                denAvg['4'] += defenseAndOneAdjustment * (1.5/3)
                denAvg['6'] += defenseAndOneAdjustment * (1/3)
                getOutcome(denAvg, outAvg, over)
            else:
                defenseAndOneAdjustment = random.uniform(0.02, 0.07)
                denAvg['0'] -= defenseAndOneAdjustment * (1.6/3)
                denAvg['1'] -= defenseAndOneAdjustment * (1.2/3)
                denAvg['4'] += defenseAndOneAdjustment * (2.1/3)
                denAvg['6'] += defenseAndOneAdjustment * (0.9/3)
                outAvg -= 0.03

                getOutcome(denAvg, outAvg, over)

        else: #works very well with 120, try to adjust a bit for death and middle but
        #dont tinker too much
            if(wickets < 7):
                defenseAndOneAdjustment = random.uniform(0.07, 0.1)
                denAvg['0'] += defenseAndOneAdjustment * (2/3)
                denAvg['1'] -= defenseAndOneAdjustment * (1/3)
                denAvg['4'] += defenseAndOneAdjustment * (1.4/3)
                denAvg['6'] += defenseAndOneAdjustment * (1.8/3)
                outAvg += 0.035
                getOutcome(denAvg, outAvg, over)
            else:
                defenseAndOneAdjustment = random.uniform(0.07, 0.09)
                denAvg['0'] -= defenseAndOneAdjustment * (1.2/3)
                denAvg['1'] -= defenseAndOneAdjustment * (1.8/3)
                denAvg['4'] += defenseAndOneAdjustment * (1.5/3)
                denAvg['6'] += defenseAndOneAdjustment * (1.5/3)
                outAvg += 0.03

                getOutcome(denAvg, outAvg, over)

        # elif(balls >= 36 and balls < 102):
        #     if(wickets == 0 or wickets == 1):
        #         defenseAndOneAdjustment = random.uniform(0.07, 0.11)
        #         denAvg['0'] -= defenseAndOneAdjustment * (2/3)
        #         denAvg['1'] -= defenseAndOneAdjustment * (1/3)
        #         denAvg['4'] += defenseAndOneAdjustment * (2/3)
        #         denAvg['6'] += defenseAndOneAdjustment * (1/3)
        #         getOutcome(denAvg, outAvg, over)
        #     else:
        #         # defenseAndOneAdjustment = random.uniform(0.03, 0.08)
        #         denAvg['0'] += 0.03
        #         # denAvg['1'] -= defenseAndOneAdjustment * (1/3)
        #         denAvg['4'] -= 0.03
        #         # denAvg['6'] += defenseAndOneAdjustment * (0.5/3)
        #         outAvg -= 0.06
        #         getOutcome(denAvg, outAvg, over)



        #     if(wickets == 0):
        #         adjust = random.uniform(0.06, 0.11)
        #         denAvg['0'] -= adjust * (1/3)
        #         denAvg['4'] += adjust * (1.5/3)
        #         denAvg['2'] += adjust * (0.5/3)
        #         denAvg['6'] += adjust * (1/3)
        #         outAvg += 0.02
        #         getOutcome(denAvg, outAvg, over)
        #     else:
        #         adjust = random.uniform(0.04, 0.8)
        #         denAvg['1'] += adjust * (1/3) * (wickets / 2)
        #         denAvg['4'] -= adjust * (2/3) * (wickets / 2)
        #         denAvg['6'] -= adjust * (1/3) * (wickets / 2)  
        #         denAvg['2'] += adjust * (1/3) * (wickets / 2)
        #         denAvg['0'] += adjust * (1/3) * (wickets / 2)

        #         outAvg -= adjust * (1/3) * (wickets)
        #         # print(adjust * (1/3) * (wickets/2))
        #         getOutcome(denAvg, outAvg, over)





    for i in range(20):
        #change strike here
        if(i != 0):
            if(onStrike == batter1):
                onStrike = batter2
            else:
                onStrike = batter1
        if(i == 0):
            overBowler = bowler1
            n = 0
            while(balls < 6):
                # print(overBowler['byBatsman']['right-hand bat']['bowlRunDenominationsObject']['4'])
                delivery(copy.deepcopy(overBowler), copy.deepcopy(
                    onStrike), str(i) + "." + str(n + 1))
                n += 1
            lastOver = overBowler['playerInitials']
        elif(i == 1):
            overBowler = bowler2
            n = 0
            while(balls < 12):
                delivery(copy.deepcopy(overBowler), copy.deepcopy(
                    onStrike), str(i) + "." + str(n + 1))
                n += 1
            lastOver = overBowler['playerInitials']

        elif(i < 6):
            def powerplayPick(bowlerInp):
                bowlerDict = bowlerTracker[bowlerInp['playerInitials']]
                bowlerToReturn = bowlerInp
                if(bowlerDict['balls'] > 11 or (bowlerDict['runs'] / bowlerDict['balls']) > 1.7):
                    if(bowlerDict['balls'] > 11 or (bowlerDict['wickets'] / bowlerDict['balls']) < 0.091):
                        valid = False #continue this
                        localBowling = sorted(bowling, key=lambda k: k['overNumbersObject'][str(i)])
                        localBowling.reverse()
                        while(not valid):
                            pick = localBowling[random.randint(0,3)]
                            pickInfo = bowlerTracker[pick['playerInitials']]
                            if(pickInfo['balls'] < 11 and lastOver != pick['playerInitials']):
                                bowlerToReturn = pick
                                valid = True
                            else:
                                pass
                return bowlerToReturn

            overBowler = None
            if(i % 2 == 1):
                bowler2 = powerplayPick(bowler2)
                overBowler = bowler2
            else:
                bowler1 = powerplayPick(bowler1)
                overBowler = bowler1
            # print(bowlingOpening[0])

            n = 0
            while(balls < ((i + 1)*6)): #Add for the case that the team has to save bowler for death (if death bowler certain number of overs then after 2 in pp, save for later)
                delivery(copy.deepcopy(overBowler), copy.deepcopy(onStrike), str(i) + "." + str(n + 1))
                n += 1
            lastOver = overBowler['playerInitials']

        elif(i < 17): #21 for now but 17 later
            #2 death exclude
            def middleOversPick(bowlerInp):
                bowlerDict = bowlerTracker[bowlerInp['playerInitials']]
                bowlerToReturn = bowlerInp
                def inDeathBowlers(bowlerToCheck):
                    if(bowlerToCheck['playerInitials'] == bowlingDeath[0]['playerInitials'] or
                        bowlerToCheck['playerInitials'] == bowlingDeath[1]['playerInitials'] or
                        bowlerToCheck['playerInitials'] == bowlingDeath[2]['playerInitials']):
                        return True
                    else:
                        return False

                if(inDeathBowlers(bowlerInp)):
                    if((bowlerDict['balls'] > 11) or (bowlerDict['runs'] / bowlerDict['balls']) > 1.5):
                        if(bowlerDict['balls'] > 11 or (bowlerDict['runs'] / bowlerDict['balls'] < 0.088)):
                            valid = False
                            loopIndex = 3
                            playersExp = sorted(bowling, key=lambda k: k['bowlBallsTotalRate'])
                            playersExp.reverse()
                            # print(playersExp)
                            expIndex = 0
                            for pexp in playersExp:
                                if(expIndex < 4):
                                    if(not inDeathBowlers(pexp)):
                                        if(bowlerTracker[pexp['playerInitials']]['balls'] < 7 and pexp['playerInitials'] != lastOver):
                                            bowlerToReturn = pexp
                                            valid = True
                                else:
                                    break
                                expIndex += 1

                            while(not valid):
                                pick = bowlingMiddle[random.randint(0,loopIndex)]
                                pickInfo = bowlerTracker[pick['playerInitials']]
                                if(pickInfo['balls'] == 0):
                                    bowlerToReturn = pick
                                    valid = True
                                else:
                                    if(inDeathBowlers(pickInfo)):
                                        if(pickInfo['balls'] < 11 and (pickInfo['runs'] / pickInfo['balls']) < 1.5):
                                            if(pickInfo['playerInitials'] != lastOver):
                                                bowlerToReturn = pick
                                                valid = True
                                        elif(pickInfo['balls'] < 11 and pickInfo['runs'] / pickInfo['balls'] > 0.088):
                                            if(pickInfo['playerInitials'] != lastOver):
                                                bowlerToReturn = pick
                                                valid = True
                                    else:
                                        if(pickInfo['balls'] < 24 and (pickInfo['runs'] / pickInfo['balls']) < 1.5):
                                            if(pickInfo['playerInitials'] != lastOver):
                                                bowlerToReturn = pick
                                                valid = True
                                        elif(pickInfo['balls'] < 11 and pickInfo['runs'] / pickInfo['balls'] > 0.088):
                                            if(pickInfo['playerInitials'] != lastOver):
                                                bowlerToReturn = pick
                                                valid = True
                                loopIndex += 1

                else:
                    if((bowlerDict['balls'] > 19) or (bowlerDict['runs'] / bowlerDict['balls']) > 1.6):
                        if(bowlerDict['balls'] > 19 or (bowlerDict['runs'] / bowlerDict['balls'] < 0.095)):
                            valid = False
                            loopIndex = 3
                            playersExp = sorted(bowling, key=lambda k: k['bowlBallsTotalRate'])
                            playersExp.reverse()        
                            # print(playersExp)
                            expIndex = 0
                            for pexp in playersExp:
                                if(expIndex < 4):
                                    if(not inDeathBowlers(pexp)):
                                        if(bowlerTracker[pexp['playerInitials']]['balls'] < 7):
                                            bowlerToReturn = pexp
                                            valid = True
                                else:
                                    break
                                expIndex += 1
                                expIndex += 1
                            while(not valid):
                                pick = bowlingMiddle[random.randint(0,loopIndex)]
                                pickInfo = bowlerTracker[pick['playerInitials']]
                                if(pickInfo['balls'] == 0):
                                    bowlerToReturn = pick
                                    valid = True
                                else:
                                    if(inDeathBowlers(pickInfo)):
                                        if(pickInfo['balls'] < 11 and ((pickInfo['runs'] / pickInfo['balls']) < 1.7) or
                                            (pickInfo['runs'] / pickInfo['balls']) > 0.088):
                                            if(pickInfo['playerInitials'] != lastOver):
                                                bowlerToReturn = pick
                                                valid = True
                                    else:
                                        if(pickInfo['balls'] < 24 and ((pickInfo['runs'] / pickInfo['balls']) < 1.6) or 
                                            (pickInfo['runs'] / pickInfo['balls'] < 0.1)):
                                            if(pickInfo['playerInitials'] != lastOver):
                                                bowlerToReturn = pick
                                                valid = True
                                loopIndex += 1


                return bowlerToReturn

        
            overBowler = None
            if(i % 2 == 1):
                bowler2 = middleOversPick(bowler2)
                overBowler = bowler2
            else:
                bowler1 = middleOversPick(bowler1)
                overBowler = bowler1

            n = 0
            while(balls < ((i + 1)*6)): #Add for the case that the team has to save bowler for death (if death bowler certain number of overs then after 2 in pp, save for later)         
                delivery(copy.deepcopy(overBowler), copy.deepcopy(onStrike), str(i) + "." + str(n + 1))
                n += 1
            lastOver = overBowler['playerInitials']

        else:
            def deathOversPick(bowlerInp):
                bowlerDict = bowlerTracker[bowlerInp['playerInitials']]
                bowlerToReturn = bowlerInp
                def inDeathBowlers(bowlerToCheck):
                    if(bowlerToCheck['playerInitials'] == bowlingDeath[0]['playerInitials'] or
                        bowlerToCheck['playerInitials'] == bowlingDeath[1]['playerInitials'] or
                        bowlerToCheck['playerInitials'] == bowlingDeath[2]['playerInitials']):
                        return True
                    else:
                        return False

                if(not inDeathBowlers(bowlerInp) or bowlerDict['balls'] > 23):
                    valid = False
                    pickerIndex = 0
                    while(not valid):
                        pick = bowlingDeath[pickerIndex]
                        pickInfo = bowlerTracker[pick['playerInitials']]
                        if(pickInfo['balls'] == 0):
                            bowlerToReturn = pick
                            valid = True
                        else:
                            if(pickInfo['balls'] < 19 and pickInfo['playerInitials'] != lastOver):
                                bowlerToReturn = pick
                                valid = True
                        pickerIndex += 1
                return bowlerToReturn

            overBowler = None
            if(i % 2 == 1):
                bowler2 = deathOversPick(bowler2)
                overBowler = bowler2
            else:
                bowler1 = deathOversPick(bowler1)
                overBowler = bowler1

            n = 0
            while(balls < ((i + 1)*6)): #Add for the case that the team has to save bowler for death (if death bowler certain number of overs then after 2 in pp, save for later)         
                delivery(copy.deepcopy(overBowler), copy.deepcopy(onStrike), str(i) + "." + str(n + 1))
                n += 1
            lastOver = overBowler['playerInitials']


            
    print(batterTracker)
    print(bowlerTracker)


def game():
    f = open("teams/csk_v_rr.txt", "r")
    team1 = None
    team2 = None
    venue = None
    toss = None

    secondInnDew = False
    # for 1st
    dew = False
    pitchDetoriate = True
    # for 1st
    detoriate = False

    paceFactor = None
    spinFactor = None
    outfield = None
    typeOfPitch = "dusty"

    team1Players = []
    team2Players = []

    team1Info = []
    team2Info = []

    # spin, pace factor -> 0.0 - 1.0
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
    paceFactor, spinFactor, outfield = pitchInfo_[
        0], pitchInfo_[1], pitchInfo_[2]
    battingFirst = doToss(paceFactor, spinFactor, outfield,
                          secondInnDew, pitchDetoriate, typeOfPitch)
    # print(paceFactor, spinFactor, outfield)

    def getBatting():
        if(battingFirst == 0):
            return [team1Info, team2Info, team1, team2]
        else:
            return [team2Info, team1Info, team2, team1]

    innings1(getBatting()[0], getBatting()[1], getBatting()[2], getBatting()[
            3], paceFactor, spinFactor, outfield, dew, detoriate)


game()
