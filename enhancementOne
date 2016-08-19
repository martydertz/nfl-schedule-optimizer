#-------------------------------------------------------------------------------
# Name:        Enhancement One
# Purpose:
#
# Author:      MDERTZ
#
# Created:     25/04/2015
# 4)   No team plays three consecutive home/away games between Weeks 1-5 and 15-17.
# 5)   Each team must play at least two home/away games every 6 weeks.
# 6)   Each team must play at least four home/away games every 10 weeks.
# 7)   No team can play four consecutive home/away games.
# 12) Jets and Giants cannot play at home on the same weekend.
#-------------------------------------------------------------------------------

import os
os.chdir("C:\GMU_Courses\OR_604\NFLSchedule")
from gurobipy import *

#dbName = '2015NFLInformation.db'
#sys.path.append("C:\GMU_Courses\OR_604\NFLSchedule")
# Create Indexes (all)
#gamesDict, gamesLst, ratingDict = NFLTeamParser.buildGamesData(dbName)
#teamLst, teamDict, teamConf, teamDiv, timeDict = NFLTeamParser.buildTeamDataStructure(dbName)
#timeSlot,timeSlotDict=NFLTeamParser.buildTimeSlots()
#blackoutDict,blackouts=CreateBlackoutDatesTable.createBlackoutDict(dbName)
# no team plays threeconsecutive home games in weeks 1-6/15-17
def hard_three_in_a_row_home_away(nfl, x, gamesDict, timeSlot,teamLst):
    hardConstrDict={}
# HARD CONSTRAINT: No team plays three consecutive home/away games between Weeks 1-5 and 15-17
# FOR HOME GAMES:
    for t in teamLst:
       for w in [1,2,3,15]:
            hardConstrDict[t,w]=nfl.addConstr(quicksum(x[a,t,w,s] for a in gamesDict['Home'][t]
                                            for s in timeSlot)
                                            + quicksum(x[a,t,(w+1),s] for a in gamesDict['Home'][t]
                                            for s in timeSlot)
                                            + quicksum(x[a,t,(w+2),s] for a in gamesDict['Home'][t]
                                            for s in timeSlot) <=2,
                                            name= "hard_consec_home_" + str(t) +"_wk_" + str(w))

    nfl.update()
# FOR AWAY GAMES
    for t in teamLst:
        for w in [1,2,3,15]:
            w1=w+1
            w2=w+2
            hardConstrDict[t,w]=nfl.addConstr(quicksum(x[t,h,w,s] for h in gamesDict['Away'][t]
                                            for s in timeSlot)
                                     + quicksum(x[t,h,w1,s] for h in gamesDict['Away'][t]
                                     for s in timeSlot)
                                    +quicksum(x[t,h,w2,s] for h in gamesDict['Away'][t]
                                    for s in timeSlot) <=2,
                                    name= "hard_consec_away_"+str(t)+"_wk_"+str(w))

    nfl.update()
    return nfl, x, hardConstrDict
def hard_two_home_per_six_weeks(nfl,x,hardConstrDict, gamesDict, timeSlot, teamLst):
# each team plays at least 2 home games every 6 weeks
    for w in range(1,11):
        for t in teamLst:
            hardConstrDict[t,w,'two_home_per_6_weeks']=nfl.addConstr(quicksum(x[a,t,w,s]+
                                        x[a,t,(w+1),s]+x[a,t,(w+2),s]+
                                        x[a,t,(w+3),s]+x[a,t,(w+4),s]+x[a,t,(w+5),s]
                                        for a in gamesDict['Home'][t]
                                        for s in timeSlot)>=2,
                                        name = "hard_min_2_home_per_6_wks_" +str(t)+
                                        "_wks_"  + str(w) + "_to_"+str(w+5))
    nfl.update()
# each team plays at least 2 away games every 6 weeks
    for w in range(1,11):
        for t in teamLst:
            hardConstrDict[t,w,'two_away_per_6_weeks']=nfl.addConstr(quicksum(x[t,h,w,s]+
                                        x[t,h,(w+1),s]+x[t,h,(w+2),s]+x[t,h,(w+3),s]+
                                        x[t,h,(w+4),s]+x[t,h,(w+5),s]
                                        for s in timeSlot
                                        for h in gamesDict['Away'][t])>=2,
                                        name="hard_min_2_away_per_6_wks_"+str(t)+
                                        "_wks_"+str(w)+"_to_"+str(w+5))
    nfl.update()
    return nfl, x, hardConstrDict
# HARD CONSTRAINT (6)   Each team must play at least four home/away games every 10 weeks.
def hard_four_home_four_away_per_ten_weeks(nfl, x, hardConstrDict, gamesDict, timeSlot, teamLst):
# four home games every ten weeks - ie sum over all timeslots and away opponents
# in ten wk period for team t is >=4
    for w in range(1,9):
        for t in teamLst:
            hardConstrDict[t,w,'four_home_every_ten']=nfl.addConstr(quicksum(x[a,t,w,s]+
                                        x[a,t,(w+1),s]+x[a,t,(w+2),s]+
                                        x[a,t,(w+3),s]+x[a,t,(w+4),s]+x[a,t,(w+5),s]+
                                        x[a,t,(w+6),s]+x[a,t,(w+7),s]+x[a,t,(w+7),s]+
                                        x[a,t,(w+8),s]+x[a,t,(w+9),s]
                                        for a in gamesDict['Home'][t]
                                        for s in timeSlot)>=4,
                                        name = "hard_min_4_home_per_10_wks_" +str(t)+
                                        "_wks_"  + str(w) + "_to_"+str(w+9))
    nfl.update()
# for away gamessum over all timeslots and home opponents
# in ten wk period for team t is >=4
    for w in range(1,9):
        for t in teamLst:
            hardConstrDict[t,w,'four_home_every_ten']=nfl.addConstr(quicksum(x[t,h,w,s]+
                                        x[t,h,(w+1),s]+x[t,h,(w+2),s]+x[t,h,(w+3),s]+
                                        x[t,h,(w+4),s]+x[t,h,(w+5),s]+
                                        x[t,h,(w+6),s]+x[t,h,(w+7),s]+x[t,h,(w+8),s]+
                                        x[t,h,(w+9),s]
                                        for h in gamesDict['Away'][t]
                                        for s in timeSlot)>=4,
                                        name="hard_min_4_away_per_10_wks_"+str(t)+
                                        "_wks_"+str(w)+"_to_"+str(w+9))
    nfl.update()
    return nfl, x, hardConstrDict

def hard_no_four_consecutive_home(nfl,x,hardConstrDict,gamesDict, timeSlot, teamLst):
# no team plays four consecutive home/away games
# for home games for team t, this means the sum of its games for 'Home' in
# w, w+1, w+2 and w+3 must be < 4
    for w in range(1,14):
        for t in teamLst:
            hardConstrDict[t,w,'no_4_consec_home']=nfl.addConstr(quicksum(x[a,t,w,s]+
                                        x[a,t,(w+1),s]+x[a,t,(w+2),s]+
                                        x[a,t,(w+3),s]
                                        for a in gamesDict['Home'][t]
                                        for s in timeSlot)<=3,
                                        name="hard_no_4_consec_home_"+str(t)+"_wks_"
                                          +str(w)+"_to_"+str(w+3))
    nfl.update()
    for w in range(1,14):
            for t in teamLst:
                hardConstrDict[t,w,'no_4_consec_away']=nfl.addConstr(quicksum(x[t,h,w,s]+
                                                x[t,h,(w+1),s]+x[t,h,(w+2),s]+
                                                x[t,h,(w+3),s]
                                                for h in gamesDict['Away'][t]
                                                for s in timeSlot)<=3,
                                                name="hard_no_4_consec_away_"+str(t)
                                                +"_wks_"+str(w)+"_to_"+str(w+3))
    nfl.update()
    return nfl, x, hardConstrDict

def hard_jets_giants_home(nfl, x, hardConstrDict, gamesDict, timeSlot, teamLst):
    # Jets/Giants cannot play at home in same week
    nyjClean=[]
    nygClean=[]
    t1='NYG'
    t2='NYJ'
    nyjHome=gamesDict['Home'][t2]
    nygHome=gamesDict['Home'][t1]
    for t in nygHome:
        nygClean.append(str(t))
    for t in nyjHome:
        nyjClean.append(str(t))
    nyjClean.remove('BYE')
    nygClean.remove('BYE')
    for w in range(1,17):
        constName = "hard_week_"+str(w)+ "_NY_Home_"
        hardConstrDict[t1,t2,w,"NY_Home"]=nfl.addConstr(quicksum(x[a,t1,w,s] for a in nygClean
                                        for s in timeSlot) +
                                        quicksum(x[a,t2,w,s] for a in nyjClean
                                        for s in timeSlot)<=1,
                                        name=constName)
    nfl.update()
    return nfl, x, hardConstrDict

if __name__ == '__main__':
    three_in_a_row_home()
