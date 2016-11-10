#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    db_cursor = conn.cursor()
    query = "DELETE from matches"
    db_cursor.execute(query)
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    db_cursor = conn.cursor()
    query = "DELETE from players"
    db_cursor.execute(query)
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    db_cursor = conn.cursor()
    query = "Select count(*) from players"
    db_cursor.execute(query)
    rows=db_cursor.fetchone()
    conn.commit()
    conn.close()
    if rows==None:
        return 0
    else:
        return rows[0]


def registerPlayer(name):
    """Adds a player to the tournament database.
      The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    conn = connect()
    db_cursor = conn.cursor()
    query = "INSERT INTO players (name) VALUES (%s);"
    db_cursor.execute(query,(name,))
    conn.commit()
    conn.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    db_cursor = conn.cursor()
    query = """SELECT id,name, COALESCE(wins,0) as wins, COALESCE(wins,0)+COALESCE(countlosses,0) as matches
                from players left join (select winner, count(*) as wins from matches group by winner) w on players.id=w.winner
                left join (select loser,count(*) as countlosses from matches group by loser) l on players.id=loser order by wins desc;"""
    db_cursor.execute(query)
    ranking=db_cursor.fetchall()
    conn.commit()
    conn.close()
    return ranking

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    db_cursor = conn.cursor()
    query = "INSERT INTO matches (winner,loser) VALUES (%s,%s);"
    db_cursor.execute(query,(winner,loser,))
    conn.commit()
    conn.close()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    pairings=[]
    rankings=playerStandings()
    l=len(rankings)
    for i in range(0,l,2):
        newpair=(rankings[i][0],rankings[i][1],rankings[i+1][0],rankings[i+1][1])
        pairings.append(newpair)
    return pairings
