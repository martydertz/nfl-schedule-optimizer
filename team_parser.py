import os
import csv
import sqlite3
import sys

#these are all for my own implementaiton so they're commented out
#print os.getcwd()
#os.chdir('C:\GMU_Courses\OR_604\NFLSchedule')
#print os.getcwd()
#gameFile ='NFLGames.csv'
#teamFile = 'TeamInfo.csv'
#ratingFile='PopularityIndex.csv'
#dbName = '2015NFLInformation.db'

def createDataBase(dbName):
#establish connection with or create database for NFL 2015 information
    c = sqlite3.connect(dbName)
    mycursor = c.cursor()
#sql string to create games table if not exists

    sqlstring = """
                CREATE TABLE IF NOT EXISTS tblNFLGames
                (homeTeam VARCHAR,
                awayTeam VARCHAR,
                rating REAL);
                """
    mycursor.execute(sqlstring)
# close cursor, commit to memore, and close connection
    mycursor.execute("DELETE FROM tblNFLGames")
    mycursor.close()
    c.commit()
    c.close()

#connect to the database again and create a cursor for the connection
    c=sqlite3.connect(dbName)
    mycursor = c.cursor()
#sql string to create team info table with columns team, conference, division, timezone
    sqlstring = """
                CREATE TABLE IF NOT EXISTS tblTeamInfo
                (team VARCHAR,
                conference VARCHAR,
                division VARCHAR,
                timezone VARINTEGER)"""
#execute string on cursor to creat Team Info table
    mycursor.execute(sqlstring)
    mycursor.execute("DELETE FROM tblTeamInfo")
    mycursor.close()
    c.commit()
    c.close()
    return

def loadData(teamFile, gameFile, ratingFile, dbName):
#connect to database and create cursor
    c = sqlite3.connect(dbName)
    mycursor = c.cursor()

# read rating file
    myFile=open(ratingFile)
    myReader=csv.reader(myFile)
    ratingDict={}
    for row in myReader:
        team=row[0].strip()
        rating=row[1].strip()
        ratingDict[row[0]]=row[1]
    myFile.close()

#read games file
    myFile = open(gameFile)
    myReader = csv.reader(myFile)
#create empty list to populate w/ games (as tuples)
    games = []
    for row in myReader:
        a=row[1].strip()
        h=row[0].strip()
        hr= float(ratingDict[h])
        ar=float(ratingDict[a])
        row.append(ar*hr)
        games.append(tuple(row))
    mycursor.executemany("INSERT INTO tblNFLGames VALUES(?,?,?);", games)

#close connections and commit to memory
    myFile.close()
    mycursor.close()
    c.commit()
    c.close()
#connect to DB again and read to team information file
    c = sqlite3.connect(dbName)
    mycursor = c.cursor()
    myFile = open(teamFile)
    myReader = csv.reader(myFile)
#create empty list to store information from each row as a tuple
    teamInfo = []
    for row in myReader:
        teamInfo.append(tuple(row))
#insert tuples into team info table as rows of data
    mycursor.executemany("INSERT INTO tblTeamInfo VALUES (?,?,?,?);", teamInfo)
#close connections and commit to memory
    myFile.close()
    mycursor.close()
    c.commit()
    c.close()
    return


def buildTeamDataStructure(dbName):
#connect to database with NFL information
    c = sqlite3.connect(dbName)
    mycursor = c.cursor()
#select team, conf and division from team info (don't need timezone for now
    mycursor.execute("SELECT team, conference, division FROM tblTeamInfo")
    conftbl = mycursor.fetchall()
#create teams dict which will {conf1:div1[team1,...team4],div2[team1,...team4],
#                               ...,div4[...]}, conf2{...}}
    teamsDict = {'AFC':{},'NFC':{}}
    teamLst = []
#iterate over table team information
    for row in conftbl:
#    create a string variable for team, div, and conf variable that has white space
#    stripped away
        div=row[2].strip()
        conf=row[1].strip()
        conf=row[1].strip()
        team = row[0].strip()
#  append team list to list of teams
        teamLst.append(team)
# check if division has been entered as a key yet in the teamsDict that will
# be of the form {CONF1:{div1-1:[teamsLst1a],...,div1-4:[teamsLst1,4]},CONF2:{div2-1:[teamsLst2-1],...,div2-4:[teamsLst2-4]}}
        if teamsDict[conf].has_key(div):
# if division is not yet a key, make it a key whose value is a list whose first entry is the team from the row
            teamsDict[conf][div].append(team)
# if division is a key already, append the team to the list of teams the division is mapping to
        else:
            teamsDict[conf][div] = [team]



    mycursor.close()
    c.commit()
    c.close()

    return teamLst, teamsDict

def buildGamesData(dbName):
# connect to database with NFL information and create cursor
    c = sqlite3.connect(dbName)
    mycursor = c.cursor()
    mycursor.execute("SELECT team, conference FROM tblTeamInfo")
    teamTbl=mycursor.fetchall()
    gamesDict = {'Home':{},'Away':{}}
    for t in teamTbl:
        team=t[0].strip()
        gamesDict['Away'][team]=[]
        gamesDict['Home'][team]=[]
    mycursor.close()
    mycursor=c.cursor()
    mycursor.execute("SELECT homeTeam, awayTeam FROM tblNFLGames")
    gamestbl = mycursor.fetchall()
    gamesLst = []

# set up the keys for the dictionary that will map teams to strings of games for home and away
    for game in gamestbl:
# assign home team and away team to 'home' and 'away' variables after stripping away white space
        away = game[0].strip()
        home = game[1].strip()

        gamesLst.append(tuple([away,home]))
        if not away == 'BYE':
            gamesDict['Home'][home].append(away)
            gamesDict['Away'][away].append(home)
        else:
            gamesDict['Home'][home].append(away)


    mycursor.close()
    c.commit()
    c.close()
    return gamesDict, gamesLst
def allTogether():

    dbName = '2015NFLInformation.db'
    teamFile ='TeamInfo.csv' # build the team file name
    gameFile = 'NFLGames.csv'  # build the games file name
    ratingFile='PopularityIndex.csv' # build rating file name
    createDataBase(dbName)
    loadData(teamFile,gameFile,ratingFile, dbName)
    teamLst, teamDict = buildTeamDataStructure(dbName)
    gamesDict, gamesLst = buildGamesData(dbName)

    return

if __name__ == '__main__':
    allTogether()
