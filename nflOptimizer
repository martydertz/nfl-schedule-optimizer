import os
import csv
import sqlite3
import sys
from gurobipy import *
#os.chdir("C:\GMU_Courses\OR_604\NFLSchedule")
print os.getcwd()
import NFLTeamParser
import CreateBlackoutDatesTable
import CoreModel
import EnhancementOne, EnhancementTwo, EnhancementThree, EnhancementFour, EnhancementFive, EnhancementSix

#these are all for my own implementaiton so they're commented out
dbName = '2015NFLInformation.db'
softConstrDict={}
# Create Indexes (all)
gamesDict, gamesLst, ratingDict = NFLTeamParser.buildGamesData(dbName)
teamLst, teamDict, teamConf, teamDiv, timeDict = NFLTeamParser.buildTeamDataStructure(dbName)
timeSlot,timeSlotDict=NFLTeamParser.buildTimeSlots()
blackoutDict,blackouts=CreateBlackoutDatesTable.createBlackoutDict(dbName)
# Create model, add game variables w/ quad index x[a,h,w,s], and core constraints
nfl,x, coreConstrDict=CoreModel.makeCoreNFLModel(gamesLst, timeSlot,ratingDict)

# add Enhancement Once - hard constraint dict creation
nfl, x, hardConstrDict = EnhancementOne.hard_three_in_a_row_home_away(nfl, x, gamesDict, timeSlot, teamLst) # no 3 cons home/away wks 1-5 and 5-17

# Enhancement Four - all hard constraints (or variable bounds)
nfl, x, hardConstrDict=EnhancementFour.hard_eliminate_games(nfl, x, gamesLst, hardConstrDict)

# Optimize model
nfl.optimize()

#enhancement one
nfl, x, hardConstrDict = EnhancementOne.hard_two_home_per_six_weeks(nfl,x, hardConstrDict, gamesDict, timeSlot, teamLst)
nfl, x, hardConstrDict = EnhancementOne.hard_three_in_a_row_home_away(nfl, x, gamesDict, timeSlot, teamLst) # no 3 cons home/away wks 1-5 and 5-17
nfl, x, hardConstrDict = EnhancementOne.hard_four_home_four_away_per_ten_weeks(nfl, x, hardConstrDict, gamesDict, timeSlot, teamLst)
nfl, x, hardConstrDict = EnhancementOne.hard_no_four_consecutive_home(nfl,x,hardConstrDict, gamesDict, timeSlot, teamLst)
nfl, x, hardConstrDict = EnhancementOne.hard_jets_giants_home(nfl, x, hardConstrDict, gamesDict, timeSlot, teamLst)

 # Add Enhancement Two - all hard constraints
nfl, x = EnhancementTwo.hard_no_bye_first_four_last_five(nfl, x, teamLst, timeSlot)
nfl, x = EnhancementTwo.hard_early_bye_previous_year(nfl, x, timeSlot)
nfl, x, hardConstrDict, three_consec_home_var, three_consec_away_var = EnhancementTwo.hard_one_three_consecutive_away_home(nfl, x, hardConstrDict, gamesDict, teamLst, timeSlot)
nfl, x = EnhancementTwo.hard_week_17_all_divisional(nfl, x, gamesLst, timeSlot, teamConf, teamDiv)

# Add Enhancement Three - Soft Contraints Constraints
nfl, x, first_two_away, softConstrDict = EnhancementThree.soft_no_team_opens_with_two_away(nfl, x, gamesDict, teamLst, timeSlot)
nfl, x, sofConstDict, every_eight_weeks, every_seven_weeks, every_six_weeks, every_five_weeks = EnhancementThree.soft_no_rematch_within_eight_weeks(nfl, x, softConstrDict, gamesLst, timeSlot)
# Add Enhancement Three - Hard Constraintes
#nfl, x, hardConstrDict=EnhancementThree.hard_thanksgiving_afc_nfc(nfl, x, hardConstrDict, gamesLst, teamConf, gamesDict)
#nfl, x, hardConstrDict=EnhancementThree.hard_no_rematch_within_three(nfl,x,gamesLst,timeSlot,hardConstrDict)

# Enhancement Five - Hard  Constraints
nfl, x, hardConstrDict=EnhancementFive.hard_monday_games_no_follow_thursday(nfl,x,hardConstrDict,teamLst, timeSlotDict, gamesDict)
nfl, x = EnhancementFive.hard_no_games_on_blackout_dates(nfl,x,teamLst,timeSlotDict, gamesDict, blackoutDict)
nfl, x, hardConstrDict=EnhancementFive.hard_max_five_prime_in_season(nfl, x,teamLst,gamesDict, hardConstrDict)
nfl, x = EnhancementFive.hard_superbowl_winner_opens_thursday(nfl,x, gamesLst, timeSlot,timeSlotDict)
# Enhancement Five - Soft Constraints
nfl, x, softConstrDict, ny_game_on_jewish_holidays_var= EnhancementFive.soft_new_york_teams_avoid_jewish_holidays(nfl, x, softConstrDict,gamesDict, timeSlotDict)
nfl, x, softConstrDict, florida_teams_no_sunday_home_games_september_var=EnhancementFive.soft_florida_no_home_weeks_one_to_three(nfl,x,softConstrDict, gamesDict,timeSlotDict)
nfl, x, two_time_zone_game_vars, softConstrDict = EnhancementFive.soft_thursday_night_within_one_timezone(nfl, x, softConstrDict, timeDict,gamesLst, timeSlotDict)

# Enhancement Six - Hard Constraints

nfl, x, hardConstrDict = EnhancementSix.hard_double_header_constraint_family(nfl, x, hardConstrDict, gamesLst, teamConf)
nfl, x, hardConstrDict = EnhancementSix.hard_ny_sf_conflicts(nfl,x,hardConstrDict, teamConf, gamesDict, timeSlot)
nfl, x = EnhancementSix.hard_mountain_west_coast(nfl,x,gamesDict, timeDict)
# Enhancement Six = Soft Constraints
nfl, x, softConstrDict, sundayLatePenalty = EnhancementSix.soft_minimize_sunday_late_games(nfl,x, softConstrDict, gamesLst)

#create a copy to use FeasRelax feature later

nfl1 = nfl.copy()

nfl.setObjective(0.0)

for c in nfl.getConstrs():
    if c.constrName[:4]=='hard':
        sense = c.sense
        if sense != '>':
            nfl.addVar(obj=1.0, name="ArtN_" + c.constrName,
                         column=Column([-1], [c]))
        if sense != '<':
            nfl.addVar(obj=1.0, name="ArtP_" + c.constrName,
                         column=Column([1], [c]))

nfl.update()
nfl.optimize()

nfl1.feasRelaxS(0, True, False, True)
nfl1.optimize()


