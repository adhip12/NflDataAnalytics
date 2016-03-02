#!/usr/bin/python

from nflgame import nflgame
import pdb
import matplotlib.pyplot as plt
import collections
import csv


years = [2009, 2010, 2011, 2012, 2013, 2014, 2015 ]


class NFLDataAnalysis():
    def __init__():
        years = range( 2009, 2016)
        weeks = range( 1, 18 )

    def unicodeToAscii( string ):
        return string.encode( 'ascii', 'ignore' )


def teamRivalry( team1, team2 ):
    team1HomeGames = []
    team2HomeGames = []
    for year in years:
        games = nflgame.games(year)
        for game in games:
            home = game.home.encode('ascii', 'ignore' )
            away = game.away.encode('ascii', 'ignore' )
            if team1 == home and team2 == away:
                team1HomeGames.append( game )
            if team1 == away and team2 == home:
                team2HomeGames.append( game )

    for game in team1HomeGames:
        winner = game.winner.encode( 'ascii' )
        if team1 == winner:
            team1HomeWin = team1HomeWin + 1
        elif team2 == winner:
            team2AwayWin = team2AwayWin + 1

    for game in team2HomeGames:
        winner = game.winner.encode( 'ascii' )
        if team1 == winner:
            team1AwayWin = team1AwayWin + 1
        elif team2 == winner:
            team2HomeWin = team2HomeWin + 1

    return team1HomeWin, team1AwayWin, team2HomeWin, team2AwayWin


def totalRushYdsPerWeek( year ):
    weekYdsDict = {}
    for week in range(1,18):
        totalYds = 0
        games = nflgame.games( year, week=week )
        players = nflgame.combine_game_stats( games )
        for p in players.rushing():
            totalYds = totalYds + p.rushing_yds

        weekYdsDict[week] = totalYds/len(games)

    return weekYdsDict

def totalPassYdsPerWeek( year ):
    weekYdsDict = {}
    for week in range(1,18):
        totalYds = 0
        games = nflgame.games( year, week=week )
        players = nflgame.combine_game_stats( games )
        for p in players.passing():
            if p.guess_position == u'QB': 
                totalYds = totalYds + p.passing_yds

        weekYdsDict[week] = totalYds/len(games)

    return weekYdsDict

def topRushersPerWeek ( year, minYds=100, topN=5 ):
    top = {} 
    for week in range( 1, 18 ):
        games = nflgame.games( year, week=week )
        players = nflgame.combine_game_stats( games )
        value = 15
        for p in players.rushing().sort('rushing_yds').limit(topN):
            if p.rushing_yds < minYds:
                break
            #What do we call a decent return on a Running back. This is the
            #limit we could set when finding the topN running backs.
            if top.has_key(p.playerid):
                curValCount = top[p.playerid]
                curValCount[0] = curValCount[0] + p.rushing_yds
                curValCount[1] = curValCount[1] + 1
                top[p.playerid] = curValCount
            else:
                #0 = Ruhsing Yards, 1 = Total number of times in the top
                top[p.playerid] = [ p.rushing_yds, 1, p.name ] 

    return topNByYds( top, topN=10 )

def topReceiversPerWeek ( year, minYds=100, topN=10 ):
    top = {}
    for week in range( 1, 18 ):
        games = nflgame.games( year, week=week )
        players = nflgame.combine_game_stats( games )
        for p in players.receiving().sort('receiving_yds').limit(topN):
            #What do we call a decent return on a Running back. minYds is the 
            #limit we could set when finding the topN running backs.
            if p.receiving_yds < minYds:
                break
            if top.has_key( p.playerid ):
                curValCount = top[p.playerid]
                curValCount[0] = curValCount[0] + p.receiving_yds
                curValCount[1] = curValCount[1] + 1
                top[p.playerid] = curValCount
            else:
                #0 = Ruhsing Yards, 1 = Total number of times in the top
                top[p.playerid] = [ p.receiving_yds, 1 , p.name ] 

    return topNByYds( top, topN=10 )

def topNByYds( data, topN=10 ):
    sortedValues = sorted( data.values(), reverse=True )
    sortedNames = sorted( data, key=data.get, reverse=True )
    sortedValues = sortedValues[:topN]
    sortedNames = sortedNames[:topN]
    topPlayers = collections.OrderedDict()

    for player, value in zip( sortedNames, sortedValues ):
        topPlayers[player] = value

    return topPlayers


def plotTotalRushPassPerYear():
    weekPassYdsPerYear = {}
    weekRushYdsPerYear = {}
    rushYds = dict.fromkeys(range(1,17), 0)
    passYds = dict.fromkeys(range(1,17), 0)
    totalRushPassYds = 0

    for year in years:
        weekRushYdsPerYear = totalRushYdsPerWeek( year )
        weekPassYdsPerYear = totalPassYdsPerWeek( year )
        for week in weekRushYdsPerYear.keys(): 
            rushYds[ week ] = rushYds[week] + weekRushYdsPerYear[week]
        for week in weekPassYdsPerYear.keys(): 
            passYds[ week ] = passYds[week] + weekPassYdsPerYear[week]

    pdb.set_trace()
    plt.plot( range(len(rushYds.keys())), rushYds.values() + passYds.values() )
    #plt.plot( range(len(passYds.keys())), passYds.values() )
    plt.show()


def getTopConsistentReceiversYear( year, minYds, topN ):
    topReceivers=topReceiversPerWeek( year, minYds=minYds, topN=topN )
    f = open("topRcvrs-%s-%s-%s.txt" % ( year, minYds, topN ), 'wt')
    writer = csv.writer(f, quoting=csv.QUOTE_NONE )
    for recvrStats in topReceivers.values():
        yds, topNCount, name = recvrStats
        writer.writerow( (name, yds, topNCount) )


getTopConsistentReceiversYear( 2011, 70, 40 )
getTopConsistentReceiversYear( 2011, 70, 30 )
getTopConsistentReceiversYear( 2011, 80, 40 )
getTopConsistentReceiversYear( 2011, 90, 40 )

#topRushersPerWeek( 2015, minYds=80, topN=10 )
#topRushers=topRushersPerWeek( 2013, minYds=70, topN=40 )
#print topRushers.values()
#plotTotalRushPassPerYear()

#plt.xticks( range(len(weekRushYdsPerYear.keys())), weekRushYdsPerYear[year].keys() )
#plt.plot( range(len(weekRushYdsPerYear[year])), weekRushYdsPerYear[year].values() )
#plt.xticks( range(len(weekRushYdsPerYear[year])), weekRushYdsPerYear[year].keys() )
    
#for year in years:
#    weekPassYdsPerYear[year] = totalPassYdsPerWeek( year )
#    plt.plot(range(len(weekPassYdsPerYear[year])), weekPassYdsPerYear[year].values())


