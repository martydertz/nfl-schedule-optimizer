#-------------------------------------------------------------------------------
# Name:        Enhancement Two
# Author:       Martin Dertz
#
#-------------------------------------------------------------------------------
from gurobipy import *
import os
os.chdir("C:\GMU_Courses\OR_604\NFLSchedule")


def hard_no_bye_first_four_last_five(nfl, x, teamLst, timeSlot):
# Bye games do not occur in first 4 weeks nor last 5 weeks
    a='BYE'
    wks=range(1,5)+range(12,18)
    for t in teamLst:
        for w in wks:
            for s in timeSlot:
                x[a,t,w,s].setAttr("ub",0.0)

    nfl.update()
    return nfl, x

def hard_early_bye_previous_year(nfl, x, timeSlot):
    # ARI, CIN, CLE, DEN, MIA, OAK, STL, SEA had week 4 or 5 bye games in 2014
# so cannot have early byes in 2015. For each early by team, for every timeslot
# for both w in {4,5}, the games variable upper bound is 0
    noEarlyByeTeams= ['ARI', 'CIN', 'CLE', 'DEN', 'MIA', 'OAK', 'STL', 'SEA']
    for t in noEarlyByeTeams:
        for s in timeSlot:
            b='BYE'
            x[b,t,4,s].setAttr("ub", 0.0)
            x[b,t,5,s].setAttr("ub", 0.0)
    nfl.update()
    return nfl, x

def hard_one_three_consecutive_away_home(nfl, x, hardConstrDict, gamesDict, teamLst, timeSlot):
    # Teams may play a maximum of one set of three consecutive home/away games
# during Weeks 4-16  but it is undesirable for this to occur
    three_consec_home_var={}
    three_consec_away_var={}
# add binary variable 'Hw' and 'Aw' for each team t, for each w in {4:16},
# which eqls 1 iff
# team t plays home games in each of weeks i,(i+1),(i+2) for Hi and/or
# away games in each of weeks i, (i+1),(i+2) for Ai
    for w in range(4,17):
        for t in teamLst:
           three_consec_home_var[t,w]= nfl.addVar(vtype=GRB.BINARY, obj=-2500, name="hard_"+str(t) +"_3_cons_home_wks_"+str(w)
                                                                    +"_to_"+str(w+2))

           three_consec_away_var[t,w]=nfl.addVar(vtype=GRB.BINARY, obj=-5000, name="hard_"+str(t) +"3_cons_away_wks_"+str(w)
                                                                +"_to_"+str(w+2))
    nfl.update()
# for each team t, for each w in {4:13}, add constraint for home games which
# requires the 'Hi' variable to be eql 1 if there are 3 homegames in weeks
# w, (w+1), (w+2). Do the same for the 'Ai' variable and consecutive Away games
# for team t

    for t in teamLst:
        for w in range(4,14):
            constName= "hard_"+str(t) +"_three_consec_away_wks_" +str(w)+"_to_"+str(w+2)
            hardConstrDict[t,w,"three_consecutive_away"]=nfl.addConstr(quicksum(x[t,h,w,s]+ x[t,h,(w+1),s]
                                            +x[t,h,(w+2),s]
                                            for h in gamesDict['Away'][t]
                                            for s in timeSlot)
                                                -three_consec_away_var[t,w]<=2, name=constName)

            constName="hard_"+str(t) +"_three_consec_home_wks_" +str(w)+"_to_"+str(w+2)
            hardConstrDict[t,w, "three_consecutive_home"]=nfl.addConstr(quicksum(x[a,t,w,s]+x[a,t,(w+1),s]+
                                                x[a,t,(w+2),s] for a in gamesDict['Home'][t]
                                                for s in timeSlot)
                                                -three_consec_home_var[t,w]<=2,name=constName)


    nfl.update()

# for each team t, constrain 'Ai' and 'Hi' variables such that it can only
# one of them can be eql 1.
    for t in teamLst:
        hardConstrDict[t,w, "max_one_three_consec_away"]=nfl.addConstr(quicksum(three_consec_away_var[t,w]
                                                for w in range (4,17)) <=1,
                                                name="hard_"+str(t) + "_three_consec_away_var_wk_"
                                                +str(w)+ "_to_"+str(w+2))
        hardConstrDict[t,w,"max_one_three_consec_home"]=nfl.addConstr(quicksum(three_consec_home_var[t,w]
                                                for w in range (4,17)) <=1,
                                                name="hard_"+str(t) + "_consec_home_var_wk_"
                                                +str(w))
    nfl.update()
    return nfl, x, hardConstrDict, three_consec_away_var, three_consec_home_var

def hard_week_17_all_divisional(nfl, x, gamesLst, timeSlot, teamConf, teamDiv):
# week 17 is all divisional games, which is the same as setting all
# non-divisional games to 0
    for a,h in gamesLst:
        if not a=='BYE':
            if not teamConf[a]==teamConf[h] or not teamDiv[a]==teamDiv[h]:
                for s in timeSlot:
                    x[a,h,17,s].setAttr("ub",0.0)
    nfl.update()
    return nfl, x


    nfl.update()
    return nfl, x, hardConstrDict
if __name__ == '__main__':
    allTogether()
