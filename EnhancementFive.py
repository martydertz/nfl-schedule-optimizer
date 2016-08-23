#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      NSFUSER
#
# Created:     05/05/2015
# Copyright:   (c) NSFUSER 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from gurobipy import *

def hard_min_one_thurs_night_per_team(nfl, x, hardConstrDict, gamesDict):
    for t in teamLst:
        constName=str(t)+"_minimum_one_thurs_night_game"
        hardConstrDict[t,"min_one_thurs_night_year"]=nfl.addConstr(quicksum(x[t,h,w,'ThurN']
                                                +x[t,h,w,'ThurE']+x[t,h,w,'ThurL']
                                                for h in gamesDict['Away'][t]
                                                for w in W)
                                                +quicksum(x[a,t,w,'ThurN']+x[a,t,w,'ThurE']
                                                +x[a,t,w,'ThurL']
                                                for a in gamesDict['Home'][t]
                                                for w in W)>=1,
                                                name=constName)
    nfl.update()
    return nfl, x, hardConstrDict

def hard_monday_games_no_follow_thursday(nfl,x,hardConstrDict,teamLst, timeSlotDict, gamesDict):
    W=range(1,17)
    for t in teamLst:
        for w in W:
            constName=str(t)+"_monday_games_after_thursday_game_"+str(w)
            hardConstrDict[t,w,constName]=nfl.addConstr(
                                        quicksum(x[a,t,w,s]+x[t,h,w,s]
                                                for s in timeSlotDict['MON']
                                                for a in gamesDict['Home'][t]
                                                for h in gamesDict['Away'][t]) # sum of all monday games for team 't' in wk 'w'

                                                +                               # PLUS

                                                quicksum(x[a,t,w+1,s]+x[t,h,w+1,s]
                                                for a in gamesDict['Home'][t]
                                                for h in gamesDict['Away'][t] # sum of all thursday games played by team 't' in wk '(w+1)'
                                                for s in timeSlotDict['THU'])
                                                <=1,                            # less than or eql to 1
                                                name=constName)
    nfl.update()
    return nfl, x, hardConstrDict

def hard_no_games_on_blackout_dates(nfl,x,teamLst,timeSlotDict, gamesDict, blackoutDict):
# Teams do not play at home on blackout dates
    for t in teamLst:
        if t in blackoutDict:
            for tpl in blackoutDict[t]:
                w=tpl[0] # blacked out week
                day=tpl[1] # blacked out day of the week
                slots=timeSlotDict[day] # blacked out timeslots
                for s in slots:
                    for a in gamesDict['Home'][t]:
                        if a != 'BYE':
                            x[a,t,w,s].setAttr("ub",0.0)

    nfl.update()
    return nfl, x
def hard_max_five_prime_in_season(nfl,x, teamLst, gamesDict, hardConstrDict):
    W=range(1,18)
    prime=["SunN","MonN1","MonN2","ThurE","ThurL","ThurN"]
    for t in teamLst:
        constName= "max_five_prime_per_season_"+str(t)
        hardConstrDict[t,constName]=nfl.addConstr(quicksum(x[t,h,w,s]
                                                    for w in W
                                                    for h in gamesDict['Away'][t]
                                                    for s in prime)
                                                    +quicksum(x[a,t,w,s]
                                                    for w in W
                                                    for a in gamesDict['Home'][t]
                                                    for s in prime)<=5, name=constName)
    nfl.update()
    return nfl, x, hardConstrDict

def hard_superbowl_winner_opens_thursday(nfl,x, gamesLst, timeSlot, timeSlotDict):
# NE won 2014/2015 superbowl therefore NE opens 2015/2016 season on Thurs night
# equivalent to setting upper bound for all NE non thursday night home games in
# week one to zero
    for a,h in gamesLst:
        w=1
        if a=='NE':
            for s in timeSlot:
                x[a,h,w,s].setAttr("ub",0.0)
        if h=='NE':
            for s in timeSlot:
                if not s in timeSlotDict['THU']:
                    x[a,h,w,s].setAttr("ub",0.0)
    nfl.update()
    return nfl, x
def soft_new_york_teams_avoid_jewish_holidays(nfl, x, softConstrDict,gamesDict, timeSlotDict):
    ny_game_on_jewish_holidays_var={}
    nyjHome=gamesDict['Home']['NYG']
    nyjAway=gamesDict['Away']['NYG']
    nygHome=gamesDict['Home']['NYJ']
    nygAway=gamesDict['Away']['NYJ']
    for w in [1,3,4]:
        for s in timeSlotDict['MON']:
            for t in ['NYJ','NYG']:
                ny_game_on_jewish_holidays_var[t,w,s]=nfl.addVar(vtype=GRB.BINARY, obj=-2000,
                                                    name= s+"_"+t+"_jewish_conflic_week_"+str(w))

    for t in ['NYJ','NYG']:
        w=13
        for s in timeSlotDict['MON']:
            ny_game_on_jewish_holidays_var[t,w,s]=nfl.addVar(vtype=GRB.BINARY, obj=-2000,
                                                    name= s+"_"+t+"_jewish_conflic_week_"+str(w))
    nfl.update()
    for w in [1,3,4]:
        for s in ['MonN1', 'MonN2']:
            for t in ['NYJ','NYG']:
                softConstrDict[t,w,s]=nfl.addConstr(quicksum(x[t,h,w,s] for h in gamesDict['Away'][t])+
                        quicksum(x[a,t,w,s] for a in gamesDict['Home'][t])==
                        ny_game_on_jewish_holidays_var[t,w,s],
                        name="jewish_holiday_conflict_"+t+"_"+s+"_week_"+str(w))

    for t in ['NYJ','NYG']:
        w=13
        softConstrDict[t,w, 'jewish_holiday_constr']=nfl.addConstr(quicksum(x[t,h,w,s]
                                                for h in gamesDict['Away'][t]
                                                for s in timeSlotDict['MON'])+
                                                quicksum(x[a,t,w,s]
                                                for a in gamesDict['Home'][t]
                                                for s in timeSlotDict['MON'])==
                                                quicksum(ny_game_on_jewish_holidays_var[t,w,s]
                                                for s in timeSlotDict['MON']),
                                                name="jewish_holiday_conflict_"+t+"_"+"_week_"+str(w))
    nfl.update()
    return nfl, x, softConstrDict, ny_game_on_jewish_holidays_var

def soft_florida_no_home_weeks_one_to_three(nfl,x,softConstrDict, gamesDict,timeSlotDict):
# add soft contraint - florida teams don't play home games in September (weeks 1-3)
    florida_teams_no_sunday_home_games_september_var={}
    for t in ['JAX','TB','MIA']:
        for w in [1,2,3]:
            for s in timeSlotDict['SUN']:
                florida_teams_no_sunday_home_games_september_var[t,w,s]=nfl.addVar(vtype=GRB.BINARY, obj=-1500, name=t+ "_"
                                            +s+ "_week_" + str(w) +"_sept_var")

    nfl.update()
    for t in ['JAX','TB','MIA']:
        for w in [1,2,3]:
            for s in timeSlotDict['SUN']:
                softConstrDict[t,w,s,'florida_no_sunday_home_sept']=nfl.addConstr(florida_teams_no_sunday_home_games_september_var[t,w,s]
                                            ==quicksum(x[a,t,w,s] for a in gamesDict['Home'][t])
                                            +quicksum(x[t,h,w,s] for h in gamesDict['Away'][t]),
                                            name=s+"_week_"+str(w)+"_"+t+"_september_early_var_const")
    nfl.update()
    return nfl, x, softConstrDict, florida_teams_no_sunday_home_games_september_var

def soft_thursday_night_within_one_timezone(nfl,x,softConstrDict, timeDict, gamesLst, timeSlotDict):
# No team playing a Thursday night game should travel more than one time zone from home
# add soft constraint - no traveling more than 1 timezone on Thursday nights
# create list of games in which opponents are 2 timezones apart
# add variable for each a,h,w that is 1 if game happens on wednesday night
    W=range(1,18)
    twoTimeZoneGames=[]
    for a,h in gamesLst:
        for zone in timeDict:
            if a in timeDict[zone]:
                atz=zone
            if h in timeDict[zone]:
                htz=zone
        if abs(atz-htz>1):
             twoTimeZoneGames.append(tuple([a,h]))
    two_time_zone_game_vars={}
    for a,h in twoTimeZoneGames:
        for w in W:
            varName=a +"_"+h+"_thurs_night_game_week_"+str(w)
            two_time_zone_game_vars[a,h,w]=nfl.addVar(vtype=GRB.BINARY, obj=-583,
                                        name=varName)
    nfl.update()
    for w in W:
        for a,h in twoTimeZoneGames:
            constName=a+"_"+h +"_two_time_zone_var_one_if_thurs_game_wk_"+str(w)
            softConstrDict[a,h,w,constName]=nfl.addConstr(quicksum(x[a,h,w,s] for s in timeSlotDict['THU'])==
                            two_time_zone_game_vars[a,h,w], name=constName)

    nfl.update()
    return nfl, x, two_time_zone_game_vars, softConstrDict
if __name__ == '__main__':
    main()
