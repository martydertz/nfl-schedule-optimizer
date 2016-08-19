# nfl-schedule-optimizer
Creates a proxy-rating for game popularity then maximizes given scheduling constraints

##Requirements/Dependencies
1. csv file with each match-up for the upcoming NSF season
2. Python and Gurobi for Python
3. A proxy-rating for the popularity of each NSF match-up. NSF uses proprietary Nielsen ratings. When I implemented this last year I used a function of fantasy football points from the previous season and playoff wins.
