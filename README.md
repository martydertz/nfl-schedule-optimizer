# nfl-schedule-optimizer
Creates a proxy-rating for game popularity then maximizes given scheduling constraints

##Requirements/Dependencies
1. csv file with each match-up for the upcoming NSF season
2. Python and Gurobi for Python
3. A proxy-rating for the popularity of each NSF match-up. NSF uses proprietary Nielsen ratings. When I implemented this last year I used a function of fantasy football points from the previous season and playoff wins.

##How It Works
The optimization problem is broken down into chunks. Each chunk is a file named 'Enhancement' (ie EnhancementOne) with procedures to make the core model then ad each constraint. Constraints go from basic -- beginning with 'each game occurs once in the season' -- to more complex -- a team can't play a Monday night game immediately after a Thursday night game.

##Soft vs Hard Constraints
Hard constraints, like each team plays once a week, are unbreakable. Soft constraints, like no rematches within 8 weeks, can be broken but when they are deduct a penalty cost from the model score. 'Hard' and 'soft' are used in the contraint procedures to make it clear what each is. 
