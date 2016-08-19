#-------------------------------------------------------------------------------
# Name:        Martin Dertz
# Purpose:      Add Enhancement three to NFL model
#
#-------------------------------------------------------------------------------
from gurobipy import *

def hard_thanksgiving_afc_nfc(nfl, x, hardConstrDict, gamesLst, teamConf, gamesDict):
#  One of the Thanksgiving day games will have an AFC team visiting
#  One of the Thanksgiving day games will have an NFC team visiting
    t1='DAL'
    t2 ='DET'
    constName='hard_thanksgiving_one_afc_visiting'
    w=12
    hardConstrDict[constName]=nfl.addConstr(quicksum(x[a,t1,w,"ThurL"] for a in gamesDict['Home'][t1]
                                                if a !='BYE' and teamConf[a] =='AFC') +
                                                quicksum(x[a,t2,w,'ThurE'] for a in gamesDict['Home'][t2]
                                                if a !='BYE' and teamConf[a] in ['AFC'])==1,
                                                 name=constName)
    constName='hard_thanksgiving_one_nfc_visiting'
    w=12
    hardConstrDict[constName]=nfl.addConstr(quicksum(x[a,h,w,"ThurL"] for a,h in gamesLst
                                                if a !='BYE' and teamConf[a] in ['NFC']) +
                                                quicksum(x[a,h,w,'ThurE'] for a,h in gamesLst
                                                if a !='BYE' and teamConf[a] in ['NFC'])>=1,
                                                 name=constName)
    nfl.update()

    return nfl, x, hardConstrDict


def soft_no_team_opens_with_two_away(nfl, x, gamesDict, teamLst, timeSlot):
# each team plays at least one home game in the first two weeks
# add binary variable to objective fns for each team that is binary with negative
# coefficient; then constrain var for each team such that it is one iff team 't' opens
# the season with 2 away games
    softConstrDict={}
    first_two_away={}
    for t in teamLst:
        varName=str(t)+"_first_two_games_away_var"
        first_two_away[t]=nfl.addVar(vtype=GRB.BINARY,obj=-2000,name=varName)
    nfl.update()
    for t in teamLst:
        softConstrDict[t]=nfl.addConstr(quicksum(x[a,t,1,s]+x[a,t,2,s]
                                        for a in gamesDict['Home'][t]
                                        for s in timeSlot)+first_two_away[t]>=1,
                                        name="soft_"+str(t)+"_home_game_in_first_two_wks")

    nfl.update()
    return nfl, x, first_two_away, softConstrDict

def soft_no_rematch_within_eight_weeks(nfl, x, softConstrDict, gamesLst, timeSlot):
# it is undesirable for teams a,h to play twice in less than 8 weeks
# add binary variables for whether teams meet within every 8,7,6 and 5 weeks
    every_eight_weeks={}
    for w in range(1,11):
        for a,h in gamesLst:
            if (h,a) in gamesLst:
                varName= str(a)+"_"+str(h) +"_play_within_eight_weeks_"+str(w)+"_to_"+str(w+7)
                every_eight_weeks[a,h,w]=nfl.addVar(vtype=GRB.BINARY, obj=-1000,
                                            name=varName)
    nfl.update()
    every_seven_weeks={}
    for w in range(1,12):
        for a,h in gamesLst:
            if (h,a) in gamesLst:
                varName= str(a)+"_"+str(h) +"_play_within_seven_weeks_"+str(w)+"_to_"+str(w+6)
                every_seven_weeks[a,h,w]=nfl.addVar(vtype=GRB.BINARY, obj=-2000,
                                            name=varName)
    nfl.update()
    every_six_weeks={}
    for w in range(1,13):
        for a,h in gamesLst:
            if (h,a) in gamesLst:
                varName= str(a)+"_"+str(h) +"_play_within_six_weeks_"+str(w)+"_to_"+str(w+5)
                every_six_weeks[a,h,w]=nfl.addVar(vtype=GRB.BINARY, obj=-3000,
                                            name=varName)
    nfl.update()
    every_five_weeks={}
    for w in range(1,14):
        for a,h in gamesLst:
            if (h,a) in gamesLst:
                varName= str(a)+"_"+str(h) +"_play_within_five_weeks_"+str(w)+"_to_"+str(w+4)
                every_five_weeks[a,h,w]=nfl.addVar(vtype=GRB.BINARY, obj=-3500,
                                            name=varName)
    nfl.update()
# Add constraint to games within 8 weeks of each other that makes every_eight var
# eql one if teams meet within 8 wks
    I=range(1,8)
    for a,h in gamesLst:
        if (h,a) in gamesLst:
            for w in range(1,11):
                constName=a+"_"+h+"_play_no_game_within_eight_weeks_"+str(w)+"_"+str(w+7)
                softConstrDict[a,h,constName]=nfl.addConstr(quicksum(x[a,h,w,s]+x[h,a,w,s]
                                        for s in timeSlot)
                                        +quicksum(x[h,a,w+i,s] for i in I
                                        for s in timeSlot)+quicksum(x[a,h,(w+i),s]
                                        for i in I for s in timeSlot)
                                        -every_eight_weeks[a,h,w]<=1,
                                        name=constName)

    nfl.update()
# Add constraint to games within 7 weeks of each other
    I=range(1,7)
    for a,h in gamesLst:
        if (h,a) in gamesLst:
            for w in range(1,12):
                constName=a+"_"+h+"_play_no_game_within_seven_weeks_"+str(w)+"_"+str(w+6)
                softConstrDict[a,h,constName]=nfl.addConstr(quicksum(x[a,h,w,s]+x[h,a,w,s]
                                        for s in timeSlot)+quicksum(x[h,a,w+i,s] for i in I
                                        for s in timeSlot)
                                        +quicksum(x[a,h,(w+i),s] for i in I for s in timeSlot)
                                        -every_seven_weeks[a,h,w]<=1,
                                        name=constName)

    nfl.update()
# Add constraint to games within 6 weeks of each other
    I=range(1,6)
    for a,h in gamesLst:
        if (h,a) in gamesLst:
            for w in range(1,13):
                constName=a+"_"+h+"_play_no_game_within_six_weeks_"+str(w)+"_"+str(w+5)
                softConstrDict[a,h,constName]= nfl.addConstr(quicksum(x[a,h,w,s]+x[h,a,w,s]
                                        for s in timeSlot)+quicksum(x[h,a,w+i,s] for i in I
                                        for s in timeSlot)
                                        +quicksum(x[a,h,(w+i),s] for i in I for s in timeSlot)
                                        -every_six_weeks[a,h,w]<=1,
                                        name=constName)
    nfl.update()

# Add constraint to games within 5 weeks of each other
    I=range(1,5)
    for a,h in gamesLst:
        if (h,a) in gamesLst:
            for w in range(1,14):
                constName=a+"_"+h+"_play_no_game_within_seven_weeks_"+str(w)+"_"+str(w+4)
                softConstrDict[a,h,constName]= nfl.addConstr(quicksum(x[a,h,w,s]+x[h,a,w,s]
                                        for s in timeSlot)+quicksum(x[h,a,w+i,s] for i in I
                                        for s in timeSlot)
                                        +quicksum(x[a,h,(w+i),s] for i in I for s in timeSlot)
                                        -every_five_weeks[a,h,w]<=1,
                                        name=constName)
    nfl.update()
    return nfl, x, softConstrDict, every_eight_weeks, every_seven_weeks, every_six_weeks, every_five_weeks

def hard_no_rematch_within_three(nfl,x, gamesLst,timeSlot,hardConstrDict):

    for a,h in gamesLst:
        if (h,a) in gamesLst:
            for w in range(1,15):
                constName="hard_"+ a+h+"_no_rematch_within_four_weeks_"+str(w)+"_"+str(w+1)
                hardConstrDict[a,h,'no_rematch_within_four']=nfl.addConstr(quicksum(x[a,h,w,s]
                                                        +x[h,a,w,s] for s in timeSlot)
                                                        +quicksum(x[a,h,w,s] +x[h,a,w,s]
                                                        for s in timeSlot for i in range(1,3))<=1,
                                                        name=constName)
    nfl.update()

    return nfl, x, hardConstrDict

if __name__ == '__main__':
    main()
