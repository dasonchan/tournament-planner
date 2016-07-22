#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def db_execute(query, params=False):
    """Help to execute query.
    Args:
        query: a sql query to be executed
        params: parameters for the query
    """
    conn = connect()
    c = conn.cursor()
    c.execute(query, params)
    conn.commit()
    conn.close()

def deleteMatches(cur=None):
    """Remove all the match records from the database."""
    db_execute("DELETE FROM match;")

def deletePlayers():
    """Remove all the player records from the database."""
    db_execute("DELETE FROM player;")

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM player;")
    output = c.fetchone()[0]
    conn.close()

    return output

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db_execute("insert into player (player_name) values (%s);", (name,))

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
    c = conn.cursor()
    c.execute("SELECT * FROM standings ORDER BY wins DESC, matches ASC;")
    output = c.fetchall()
    conn.close()

    return output

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db_execute("INSERT INTO match (winner, loser) VALUES (%s, %s)", (winner, loser))
 
 
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
    standings = playerStandings()
    num_players = len(standings)
    output = []

    for p in range(0, num_players, 2):
        pair = ((standings[p][0], standings[p][1], standings[p + 1][0], standings[p + 1][1]))
        output.append(pair)

    return output

