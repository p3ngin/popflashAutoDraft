#!/usr/bin/python3
from itertools import combinations
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import sys

#Create list of arguments passed while running script
#List will contain all user IDs needed to build URL for player profiles
playerArgs = list(sys.argv[1:])

#Create Data Frame and global variables
columns_teamCombos = ['ratingDiff', 'team1_rating', 'team2_rating','team1_p0', 'team1_p1', 'team1_p2', 'team1_p3', 'team1_p4' ,'team2_p0', 'team2_p1', 'team2_p2', 'team2_p3', 'team2_p4']

teamCombos = pd.DataFrame(columns=columns_teamCombos)

ratingDiff = 0
team1_rating = 0
team2_rating = 0
team1_final = ()
team2_final = ()
team1_p0 = ''
team1_p1 = ''
team1_p2 = ''
team1_p3 = ''
team1_p4 = ''
team2_p0 = ''
team2_p1 = ''
team2_p2 = ''
team2_p3 = ''
team2_p4 = ''
playerURL = ''
players = {}

playerList = set(players.keys())

#Gathering playerdata from popflash profiles
def buildURL(playerArgs):
    for p in playerArgs:
        playerURL = 'https://popflash.site/user/' + str(p)
        scrapeData(playerURL)

def scrapeData(playerURL):
    page = requests.get(playerURL)
    soup = BeautifulSoup(page.text, 'html.parser')

    nameScrape = soup.find_all('span')[2].get_text()
    ratingScrape = float(soup.find_all(class_ = 'stat')[0].get_text())
    
    playerData(nameScrape, ratingScrape)

def playerData(nameScrape, ratingScrape):
    players[nameScrape] = ratingScrape


#Team build algorithm --------------------------------------

def buildTeams(players):
    """ Iterates through player list and produces all possible team combinations of 5
            For each team combination, assign player to each team and calculate average HLTV rating per team combination
            Calculates rating difference between teams for giving combination.
            Appends combination into a dataframe """

    playerList = set(players.keys())

    for team1 in list(combinations(players.keys(), 5)):
        team1_final = set(team1)
        team2_final = playerList - team1_final

        team1_rating = sum([players[x] for x in team1_final])/5
        team2_rating = sum([players[x] for x in team2_final])/5

        ratingDiff = abs(team1_rating - team2_rating)

        team1_list = list(team1_final)
        team2_list = list(team2_final)

        team1_p0, team1_p1, team1_p2, team1_p3, team1_p4 = [team1_list[i] for i in (0, 1, 2, 3, 4)]

        #assign players to team specific variables - TEAM 2
        team2_p0, team2_p1, team2_p2, team2_p3, team2_p4 = [team2_list[i] for i in (0, 1, 2, 3, 4)]

        appendTeam(ratingDiff, team1_rating, team2_rating, team1_p0, team1_p1, team1_p2, team1_p3, team1_p4, team2_p0, team2_p1, team2_p2, team2_p3, team2_p4)
        #return ratingDiff, team1_rating, team2_rating, team1_p0, team1_p1, team1_p2, team1_p3, team1_p4, team2_p0, team2_p1, team2_p2, team2_p3, team2_p4        
 

def appendTeam(ratingDiff, team1_rating, team2_rating, team1_p0, team1_p1, team1_p2, team1_p3, team1_p4, team2_p0, team2_p1, team2_p2, team2_p3, team2_p4):
    #Function to append each team combination to data frame
    appendData = [ratingDiff, team1_rating, team2_rating, team1_p0, team1_p1, team1_p2, team1_p3, team1_p4, team2_p0, team2_p1, team2_p2, team2_p3, team2_p4]
    teamCombos.loc[len(teamCombos.index)] =  appendData


c = 1

while c < 10:
    buildURL(playerArgs)
    if c == 10:
        buildTeams(players)
        break
    c += 1
buildTeams(players)

#print the top 3 rows in data set with lowest rating difference. This will provide the 3 most ideal combinations for a fair game

print(teamCombos.nsmallest(3, ['ratingDiff']))
