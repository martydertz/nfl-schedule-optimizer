#-------------------------------------------------------------------------------
# Name:        Enhancement VI
# Purpose:
#
# Author:    MDERTZ
#-----------------------------------------------
from gurobipy import *

def hard_double_header_constraint_family(nfl, x, hardConstrDict, gamesLst, teamConf):
    # One network will air a double header  1:00 PM  and  4:25 PM on Sundays
# Away team drives the conference
# CBS gets AFC games sunday afternoon
# Fox NFC games sunday afternoons
# For each week create variable for each CBS game (AFC away team)
    W=range(1,18)
    CBSGames=[]
    for a,h in gamesLst:
        if a!='BYE' and teamConf[a]=='AFC':
            CBSGames.append(tuple([a,h]))
    FOXGames=[]
    for a,h in gamesLst:
        if a!='BYE' and teamConf[a]=='NFC':
            FOXGames.append(tuple([a,h]))
    nfl.update()

# There is at least one Sunday Early game with the visiting team from each conference
# If there is a CBS Game Late, then a FOX game is the Marque game
    double_header_constr={}
    for w in W:
        constName="hard_week_"+str(w)+"_cbs_sunday_early_game"
        hardConstrDict[w, constName]= nfl.addConstr(quicksum(x[a,h,w,'SunE'] for a,h in CBSGames)
                                                        >=1,name=constName)

        constName="hard_week_"+str(w)+"_Fox_sunday_early_game"
        hardConstrDict[w,constName]=nfl.addConstr(quicksum(x[a,h,w,'SunE'] for a,h in FOXGames)
                                                        >=1, name=constName)

        constName="hard_week_"+str(w)+"_cbs_sunday_late_game_IF_Fox_Marquee_game"
        hardConstrDict[w,constName]=nfl.addConstr(quicksum(x[a,h,w,'SunL'] for a,h in CBSGames)
                                                    -quicksum(x[a,h,w,'SunM'] for a,h in FOXGames)
                                                    >=0, name=constName)

        constName="hard_week_"+str(w)+"_fox_sunday_late_game_IF_cbs_Marquee_game"
        hardConstrDict[w,constName]=nfl.addConstr(quicksum(x[a,h,w,'SunL'] for a,h in FOXGames)
                                                    -quicksum(x[a,h,w,'SunM'] for a,h in CBSGames)
                                                    >=1,  name=constName)
    nfl.update()
# now constrain double header (marquee) variable such that each week there can only be one
# double header except in week 17
    for w in range(1,17):
        hardConstrDict[w,'one_marquee']= nfl.addConstr(quicksum(x[a,h,w,'SunM'] for a,h in CBSGames)+quicksum(x[a,h,w,'SunM']
                        for a,h in FOXGames)<=1, name="hard_week_"+str(w)+"_one_Marquee_game")
    nfl.update()

#11c)   Networks each get 8 double headers during weeks 1-16
    hardConstrDict["fox_eight_double_headers"]= nfl.addConstr(quicksum(x[a,h,w,'SunM']
                                    for w in range(1,17) for a,h in FOXGames) ==8,
                                    name="hard_fox_eight_double_headers")
    hardConstrDict["cbs_eight_double_headers"]= nfl.addConstr(quicksum(x[a,h,w,'SunM']
                                    for w in range(1,17) for a,h in CBSGames) ==8,
                                    name="hard_cbs_eight_double_headers")
    nfl.update()

# 11d)  No network can have more than 2 double headers in a row during weeks 1-16
# create a new binary var that is one if cbs has double header
    for w in range(1,15):
        hardConstrDict['fox_two_double_headers_in_a_row']= nfl.addConstr(quicksum(x[a,h,w,'SunM']+x[a,h,(w+1),'SunM']+x[a,h,(w+2),'SunM']
                       for a,h in FOXGames) <=3, name="hard_fox_no_more_than_two_double_headers_in_row_wks_"
                                    +str(w)+"_"+str(w+2))
        hardConstrDict['cbs_two_double_headers_in_a_row'] =nfl.addConstr(quicksum(x[a,h,w,'SunM']+x[a,h,(w+1),'SunM']+x[a,h,(w+2),'SunM']
                       for a,h in CBSGames)<=3, name="hard_cbs_no_more_than_two_double_headers_in_row_wks_"
                                    +str(w)+"_"+str(w+2))
    nfl.update()
# 11g)  One late Sunday game will be designated the ?Marquee game? and broadcast
# to as many markets as possible
    for w in W:
        hardConstrDict[w,'one_marquee_per_week']= nfl.addConstr(quicksum(x[a,h,w,'SunM'] for a,h in gamesLst)==1,name="hard_one_marq_week_"+str(w))
# 11h)  There will be no more than 5 Sunday afternoon games (this includes the Marquee game
    for w in W:
        hardConstrDict[w,'maximum_five_sunday_afternoon_games']= nfl.addConstr(quicksum(x[a,h,w,s]
                                                for a,h in gamesLst for s in ['SunL','SunM'])
                    <=5, "hard_maximum_five_sunday_afternoon_games_week_"+str(w))
    nfl.update()
    return nfl, x, hardConstrDict
def hard_ny_sf_conflicts(nfl,x,hardConstrDict, teamConf, gamesDict, timeSlot):
# 12a-b)  Jets / Giants and Raiders / 49ers cannot play during the same timeslot
# (unless they are playing each other)
    W=range(1,18)
    for w in W:
        for s in timeSlot:
            for pair in [('NYJ','NYG'),('OAK','SF')]:
                 hardConstrDict[pair,s,w]= nfl.addConstr(quicksum(x[a,pair[0],w,s] for a in gamesDict['Home'][pair[0]] if a !='BYE' or pair[1])+
                            quicksum(x[pair[0],h,w,s] for h in gamesDict['Away'][pair[0]] if h != pair[1])+
                            quicksum(x[a,pair[1], w,s] for a in gamesDict['Home'][pair[1]] if a !='BYE' and a!=pair[0])+
                            quicksum(x[pair[1],h,w,s] for h in gamesDict['Away'][pair[1]] if h !=pair[0])<=1,
                            name="hard_week_"+str(w)+"_timeslot_"+s+"_no_"+pair[0]+"_"+pair[1]+"_conflict")
    nfl.update()
# 12c)  Jets (AFC) and Giants (NFC)  and 49ers (NFC) OAK (AFC)
# cannot play on the same network on the same afternoon
# (unless they are playing each other)
# This means for each wk, the sum over all NYG away games over the sunday afternoon
# timeslots (which are broadcasted on NFC) minus the sum over all NYJ home games
# during sunday afternoon timeslots against NFC opponents <=1
    new_york_california_afternoon_network_conflicts={}
    for w in W:
        for pair in [('NYJ','NYG'),('OAK','SF')]:
            constName="hard_"+pair[0]+"_"+pair[1]+"_no_sunday_afternoon__conflicts"
            # NYG/SF away (CBS)
            hardConstrDict[pair,w, 'CBS']=nfl.addConstr(
                                        quicksum(x[a,pair[0],w,s]
                                        for a in gamesDict['Home'][pair[0]] if a!='BYE' and teamConf[a]=='AFC'
                                        for s in ['SunE','SunL','SunM'])
                                        - quicksum(x[pair[1],h,w,s]
                                        for h in gamesDict['Away'][pair[1]]
                                        for s in ['SunE','SunL','SunM'] )<=1,
                                        name=constName)
            constName="hard_"+pair[1] +"_"+pair[0]+"_no_sunday_afternoon_ FOX_conflicts_wk_"+str(w)
            hardConstrDict[pair,w, 'CBS']=nfl.addConstr(
                                    quicksum(x[a,pair[1],w,s]
                                    for a in gamesDict['Home'][pair[1]] if a !='BYE' and teamConf[a]=='NFC'
                                    for s in ['SunE','SunL','SunM'])
                                    -quicksum(x[pair[0],h,w,s] for h in gamesDict['Away'][pair[0]]
                                    for s in ['SunE','SunL','SunM'])<=1,name=constName)

    nfl.update()
    return nfl, x, hardConstrDict
def hard_mountain_west_coast(nfl,x,gamesDict, timeDict):
    W=range(1,18)
    T = timeDict[3]+timeDict[4]
    for w in W:
        for team in T:
            for visitor in gamesDict['Home'][team]:
                if visitor != 'BYE':
                    x[visitor, team,w,'SunE'].setAttr("ub",0.0)
                    x[visitor, team, w, 'SunL'].setAttr("ub",0.0)
    nfl.update()
    return nfl, x

def soft_minimize_sunday_late_games(nfl,x, softConstrDict, gamesLst):
# SOFT: 11g)  Have as few late Sunday afternoon games as possible to improve
# national viewership for the Marquee game - create new variable for each week
# that is then constrained to be eql to the sum of all Sunday late games in that week
    W=range(1,18)
    sundayLatePenalty={}
    for w in W:
        sundayLatePenalty[w]=nfl.addVar(vtype=GRB.CONTINUOUS, obj=-400,
                                                name="sunday_late_penalty_var_"
                                                +"_"+"_week_"+str(w))
    nfl.update()

    for w in W:
        softConstrDict[w,'min_sun_late_games']= nfl.addConstr(quicksum(x[a,h,w,'SunL'] for a,h in gamesLst)-sundayLatePenalty[w]==1,
                                    name="soft_sunday_late_penalty_var_eqls_late_games_played_week_" +str(w))
    nfl.update()
    return nfl, x, softConstrDict, sundayLatePenalty


if __name__ == '__main__':
    main()
