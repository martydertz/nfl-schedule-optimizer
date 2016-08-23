#-------------------------------------------------------------------------------
# Name:        ENHANCEMENT IV
# Purpose:
#
# Author:      MDERTZ

#-------------------------------------------------------------------------------
from gurobipy import *

def hard_eliminate_games(nfl, x, gamesLst, hardConstrDict):
    W=range(1,18)
    for w in range(2,17):
        hardConstrDict['one_monday_night',w]=nfl.addConstr(quicksum(x[a,h,w,s]
                                                    for a,h in gamesLst for s in ['MonN1','MonN2'])
                                                    <=1, name = "monday_night_one_per_week_"+str(w))
        hardConstrDict['one_thursday_night',w]=nfl.addConstr(quicksum(x[a,h,w,'ThurN']
                                                    for a,h in gamesLst)
                                                    <=1, name = "thursday_night_one_per_week_"+str(w))
# One sunday marque game per week
    for w in W:
        nfl.addConstr(quicksum(x[a,h,w,'SunM'] for a,h in gamesLst)<=1,name="_eqauls_one_week_"+str(w))

# one saturday early and one saturday late
        if w == 16:
            hardConstrDict[w,'one_sate_satl_game']=nfl.addConstr(quicksum(x[a,h,w,'SatL'] for a,h in gamesLst)==1,
                                                        name="one_sat_late_wk_"+str(w))
            hardConstrDict[w,'one_sate_sate_game']=nfl.addConstr(quicksum(x[a,h,w,'SatE'] for a,h in gamesLst)==1,
                                                        name="one_sat_early_wk_"+str(w))

    nfl.update()

    for a,h in gamesLst:
        for w in W:
            if w ==17:
                x[a,h,w,'ThurN'].setAttr("ub",0.0) # no thurs night games wk 17
                x[a,h,w,'MonN1'].setAttr("ub",0.0) # no monday games wk 17
                x[a,h,w,'MonN2'].setAttr("ub",0.0) # no monday games wk 17
            if w != 12:
                x[a,h,w,'ThurE'].setAttr("ub",0.0) # no thursday day games outside wk 12
                x[a,h,w,'ThurL'].setAttr("ub", 0.0)
            if w!=16:
                x[a,h,w,'SatE'].setAttr("ub",0.0) # no saturday day games outside wk 16
                x[a,h,w,'SatL'].setAttr("ub",0.0)


    nfl.update()

    return nfl, x, hardConstrDict
if __name__ == '__main__':
    hard_eliminate_games(nfl, x, gamesLst, hardConstrDict)
