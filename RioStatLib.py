import json

'''
Intended to parse "decoded" files which would be present on a user's computer

Roster args:
- arg == 0 means team0 which is the home team
- arg == 1 means team1 which is the away team
- arg == -1 means all characters (if function allows)
'''


# large info functions

# returns it in int form
def gameID(statJson: dict):
    return int(statJson["GameID"].replace(',', ''), 16)

# should look to convert to unix or some other standard date fmt
def date(statJson: dict):
    return statJson["Date"]

# tells if a game was a ranked game or not
def isRanked(statJson: dict):
    rankedStatus = statJson["Ranked"]
    if rankedStatus == 0:
        return False
    else:
        return True

# reutrns the stadium that was played on
def stadium(statJson: dict):
    return statJson["StadiumID"]

# returns name of player. teamNum == 0 is home team, teamNum == 1 is away team
def player(statJson: dict, teamNum: int):
    __errorCheck_teamNum(teamNum)
    if teamNum == 0:
        return statJson["Home Player"]
    elif teamNum == 1:
        return statJson["Away Player"]
    else:
        __errorCheck_teamNum(teamNum)

# returns final score of said team
def score(statJson: dict, teamNum: int):
    __errorCheck_teamNum(teamNum)
    if teamNum == 0:
        return statJson["Home Score"]
    elif teamNum == 1:
        return statJson["Away Score"]
    else:
        __errorCheck_teamNum(teamNum)

# returns how many innings were selected for the game
def inningsTotal(statJson: dict):
    return statJson["Innings Selected"]

# returns how many innings were played in the game
def inningsPlayed(statJson: dict):
    return statJson["Innings Played"]

# returns if the game ended in a mercy or not
def isMercy(statJson: dict):
    if inningsTotal(statJson) - inningsPlayed(statJson) >= 1 and not wasQuit(statJson):
        return True
    else:
        return False

# returns if the same was quit out early
def wasQuit(statJson: dict):
    if statJson["Quitter Team"] == "":
        return False
    else:
        return True

# returns the name of the quitter if the game was quit. empty string if no quitter
def quitter(statJson: dict):
    return statJson["Quitter Team"]

# returns average ping of the game
def ping(statJson: dict):
    return statJson["Average Ping"]

# returns number of lag spikes in a game
def lagspikes(statJson: dict):
    return statJson["Lag Spikes"]

# returns the full dict of character game stats as shown in the stat file
def characterGameStats(statJson: dict):
    return statJson["Character Game Stats"]

# returns if the game has any superstar characters in it
def isSuperstarGame(statJson: dict):
    isStarred = False
    charStats = characterGameStats(statJson)
    for character in charStats:
        if charStats[character]["Superstar"] == 1:
            isStarred = True
    return isStarred

# TODO: function that tells if no stars, stars, or mixed stars?

# character stats
# (statJson: dict, teamNum: int, rosterNum: int):

# returns name of specified character
# if no roster spot is provided, returns a list of characters on a given team
def characterName(statJson: dict, teamNum: int, rosterNum: int = -1):
    __errorCheck_teamNum(teamNum)
    __errorCheck_rosterNum(rosterNum)
    if rosterNum == -1:
        charList = []
        for x in range(0, 9):
            charList.append(statJson["Character Game Stats"][f"Team {teamNum} Roster {x}"]["CharID"])
        return charList
    else:
        return statJson["Character Game Stats"][f"Team {teamNum} Roster {rosterNum}"]["CharID"]

# returns if a character is starred
# if no arg, returns if any character on the team is starred
def isStarred(statJson: dict, teamNum: int, rosterNum: int = -1):
    __errorCheck_teamNum(teamNum)
    __errorCheck_rosterNum(rosterNum)
    if rosterNum == -1:
        for x in range(0, 9):
            if statJson["Character Game Stats"][f"Team {teamNum} Roster {x}"]["Superstar"] == 1:
                return True
    else:
        if statJson["Character Game Stats"][f"Team {teamNum} Roster {rosterNum}"]["Superstar"] == 1:
            return True
        else:
            return False

# returns name of chatacter who is the captian
def captain(statJson: dict, teamNum: int):
    __errorCheck_teamNum(teamNum)
    captain = ""
    for character in characterGameStats(statJson):
        if character["Captain"] == 1 and int(character["Team"]) == teamNum:
            captain = character["CharID"]
    return captain

# grabs offensive stats of a character as seen in the stat json
# if no roster provided, returns a list of all character's offensive stats
def offensiveStats(statJson: dict, teamNum: int, rosterNum: int = -1):
    __errorCheck_teamNum(teamNum)
    __errorCheck_rosterNum(rosterNum)
    if rosterNum == -1:
        oStatList = []
        for x in range(0, 9):
            oStatList.append(statJson["Character Game Stats"][f"Team {teamNum} Roster {x}"]["Offensive Stats"])
        return oStatList
    else:
        return statJson["Character Game Stats"][f"Team {teamNum} Roster {rosterNum}"]["Offensive Stats"]

# grabs defensive stats of a character as seen in the stat json
# if no roster provided, returns a list of all character's defensive stats
def defensiveStats(statJson: dict, teamNum: int, rosterNum: int = -1):
    __errorCheck_teamNum(teamNum)
    __errorCheck_rosterNum(rosterNum)
    if rosterNum == -1:
        dStatList = []
        for x in range(0, 9):
            dStatList.append(statJson["Character Game Stats"][f"Team {teamNum} Roster {x}"]["Defensive Stats"])
        return dStatList
    else:
        return statJson["Character Game Stats"][f"Team {teamNum} Roster {rosterNum}"]["Defensive Stats"]

# returns fielding handedness of character
def fieldingHand(statJson: dict, teamNum: int, rosterNum: int):
    __errorCheck_teamNum(teamNum)
    __errorCheck_rosterNum2(rosterNum)
    return statJson["Character Game Stats"][f"Team {teamNum} Roster {rosterNum}"]["Fielding Hand"]

# returns batting handedness of character
def battingHand(statJson: dict, teamNum: int, rosterNum: int):
    __errorCheck_teamNum(teamNum)
    __errorCheck_rosterNum2(rosterNum)
    return statJson["Character Game Stats"][f"Team {teamNum} Roster {rosterNum}"]["Batting Hand"]


# defensive stats

# tells how many batters were faced by character
# if no character given, returns batters faced by that team
def battersFaced(statJson: dict, teamNum: int, rosterNum: int = -1):
    if rosterNum == -1:
        total = 0
        for x in range(0, 9):
            total += defensiveStats(statJson, teamNum, x)["Batters Faced"]
        return total
    else:
        return defensiveStats(statJson, teamNum, rosterNum)["Batters Faced"]

# tells how many runs a character allowed when pitching
# if no character given, returns runs allowed by that team
def runsAllowed(statJson: dict, teamNum: int, rosterNum: int = -1):
    if rosterNum == -1:
        total = 0
        for x in range(0, 9):
            total += defensiveStats(statJson, teamNum, x)["Runs Allowed"]
        return total
    else:
        return defensiveStats(statJson, teamNum, rosterNum)["Runs Allowed"]

# tells how many walks a character allowed when pitching
# if no character given, returns walks by that team
def battersWalked(statJson: dict, teamNum: int, rosterNum: int = -1):
    return battersWalkedBallFour(statJson, teamNum, rosterNum) + battersHitByPitch(statJson, teamNum, rosterNum)

# returns how many times a character has walked a batter via 4 balls
# if no character given, returns how many times the team walked via 4 balls
def battersWalkedBallFour(statJson: dict, teamNum: int, rosterNum: int = -1):
    if rosterNum == -1:
        total = 0
        for x in range(0, 9):
            total += defensiveStats(statJson, teamNum, x)["Batters Walked"]
        return total
    else:
        return defensiveStats(statJson, teamNum, rosterNum)["Batters Walked"]

# returns how many times a character walked a batter by hitting them by a pitch
# if no character given, returns walked via HBP for the team
def battersHitByPitch(statJson: dict, teamNum: int, rosterNum: int = -1):
    if rosterNum == -1:
        total = 0
        for x in range(0, 9):
            total += defensiveStats(statJson, teamNum, x)["Batters Hit"]
        return total
    else:
        return defensiveStats(statJson, teamNum, rosterNum)["Batters Hit"]

# returns how many hits a character allowed as pitcher
# if no character given, returns how many hits a team allowed
def hitsAllowed(statJson: dict, teamNum: int, rosterNum: int = -1):
    if rosterNum == -1:
        total = 0
        for x in range(0, 9):
            total += defensiveStats(statJson, teamNum, x)["Hits Allowed"]
        return total
    else:
        return defensiveStats(statJson, teamNum, rosterNum)["Hits Allowed"]

# returns how many homeruns a character allowed as pitcher
# if no character given, returns how many homeruns a team allowed
def homerunsAllowed(statJson: dict, teamNum: int, rosterNum: int = -1):
    if rosterNum == -1:
        total = 0
        for x in range(0, 9):
            total += defensiveStats(statJson, teamNum, x)["HRs Allowed"]
        return total
    else:
        return defensiveStats(statJson, teamNum, rosterNum)["HRs Allowed"]

# returns how many pitches a character threw
# if no character given, returns how many pitches a team threw
def pitchesThrown(statJson: dict, teamNum: int, rosterNum: int = -1):
    if rosterNum == -1:
        total = 0
        for x in range(0, 9):
            total += defensiveStats(statJson, teamNum, x)["Pitches Thrown"]
        return total
    else:
        return defensiveStats(statJson, teamNum, rosterNum)["Pitches Thrown"]

# returns final pitching stamina of a pitcher
# if no character given, returns total stamina of a team
def stamina(statJson: dict, teamNum: int, rosterNum: int = -1):
    if rosterNum == -1:
        total = 0
        for x in range(0, 9):
            total += defensiveStats(statJson, teamNum, x)["Stamina"]
        return total
    else:
        return defensiveStats(statJson, teamNum, rosterNum)["Stamina"]

# returns if a character was a pitcher
def wasPitcher(statJson: dict, teamNum: int, rosterNum: int):
    __errorCheck_rosterNum2(rosterNum)
    if defensiveStats(statJson, teamNum, rosterNum)["Was Pitcher"] == 1:
        return True
    else:
        return False

# returns how many strikeouts a character pitched
# if no character given, returns how mnany strikeouts a team pitched
def strikeoutsPitched(statJson: dict, teamNum: int, rosterNum: int = -1):
    if rosterNum == -1:
        total = 0
        for x in range(0, 9):
            total += defensiveStats(statJson, teamNum, x)["Strikeouts"]
        return total
    else:
        return defensiveStats(statJson, teamNum, rosterNum)["Strikeouts"]

# returns how many star pitches a charcter threw
# if no character given, returns how many star pitches a team threw
def starPitchesThrown(statJson: dict, teamNum: int, rosterNum: int = -1):
    if rosterNum == -1:
        total = 0
        for x in range(0, 9):
            total += defensiveStats(statJson, teamNum, x)["Star Pitches Thrown"]
        return total
    else:
        return defensiveStats(statJson, teamNum, rosterNum)["Star Pitches Thrown"]

# returns how many big plays a character had
# if no character given, returns how many big plays a team had
def bigPlays(statJson: dict, teamNum: int, rosterNum: int = -1):
    if rosterNum == -1:
        total = 0
        for x in range(0, 9):
            total += defensiveStats(statJson, teamNum, x)["Big Plays"]
        return total
    else:
        return defensiveStats(statJson, teamNum, rosterNum)["Big Plays"]

# returns how many outs a charcter was pitching for
# if no character given, returns how many outs a team pitched for
def outsPitched(statJson: dict, teamNum: int, rosterNum: int = -1):
    if rosterNum == -1:
        total = 0
        for x in range(0, 9):
            total += defensiveStats(statJson, teamNum, x)["Outs Pitched"]
        return total
    else:
        return defensiveStats(statJson, teamNum, rosterNum)["Outs Pitched"]

# returns a dict which tracks how many pitches a charcter was at a position for
def pitchesPerPosition(statJson: dict, teamNum: int, rosterNum: int):
    __errorCheck_rosterNum2(rosterNum)
    return defensiveStats(statJson, teamNum, rosterNum)["Pitches Per Position"][0]

# returns a dict which tracks how many outs a charcter was at a position for
def outsPerPosition(statJson: dict, teamNum: int, rosterNum: int):
    __errorCheck_rosterNum2(rosterNum)
    return defensiveStats(statJson, teamNum, rosterNum)["Outs Per Position"][0]


# offensive stats

# returns how many at bats a character had
# if no character given, returns how many at bats a team had
def atBats(statJson: dict, teamNum: int, rosterNum: int = -1):
    if rosterNum == -1:
        total = 0
        for x in range(0, 9):
            total += offensiveStats(statJson, teamNum, x)["At Bats"]
        return total
    else:
        return offensiveStats(statJson, teamNum, rosterNum)["At Bats"]

# returns how many hits a character had
# if no character given, returns how many hits a team had
def hits(statJson: dict, teamNum: int, rosterNum: int = -1):
    if rosterNum == -1:
        total = 0
        for x in range(0, 9):
            total += offensiveStats(statJson, teamNum, x)["Hits"]
        return total
    else:
        return offensiveStats(statJson, teamNum, rosterNum)["Hits"]

# returns how many singles a character had
# if no character given, returns how many singles a team had
def singles(statJson: dict, teamNum: int, rosterNum: int = -1):
    if rosterNum == -1:
        total = 0
        for x in range(0, 9):
            total += offensiveStats(statJson, teamNum, x)["Singles"]
        return total
    else:
        return offensiveStats(statJson, teamNum, rosterNum)["Singles"]

# returns how many doubles a character had
# if no character given, returns how many doubles a team had
def doubles(statJson: dict, teamNum: int, rosterNum: int = -1):
    if rosterNum == -1:
        total = 0
        for x in range(0, 9):
            total += offensiveStats(statJson, teamNum, x)["Doubles"]
        return total
    else:
        return offensiveStats(statJson, teamNum, rosterNum)["Doubles"]

# returns how many triples a character had
# if no character given, returns how many triples a teams had
def triples(statJson: dict, teamNum: int, rosterNum: int = -1):
    if rosterNum == -1:
        total = 0
        for x in range(0, 9):
            total += offensiveStats(statJson, teamNum, x)["Triples"]
        return total
    else:
        return offensiveStats(statJson, teamNum, rosterNum)["Triples"]

# returns how many homeruns a character had
# if no character given, returns how many homeruns a team had
def homeruns(statJson: dict, teamNum: int, rosterNum: int = -1):
    if rosterNum == -1:
        total = 0
        for x in range(0, 9):
            total += offensiveStats(statJson, teamNum, x)["Homeruns"]
        return total
    else:
        return offensiveStats(statJson, teamNum, rosterNum)["Homeruns"]

# returns how many successful bunts a character had
# if no character given, returns how many successful bunts a team had
def buntsLanded(statJson: dict, teamNum: int, rosterNum: int = -1):
    if rosterNum == -1:
        total = 0
        for x in range(0, 9):
            total += offensiveStats(statJson, teamNum, x)["Successful Bunts"]
        return total
    else:
        return offensiveStats(statJson, teamNum, rosterNum)["Successful Bunts"]

# returns how many sac flys a character had
# if no character given, returns how many sac flys a team had
def sacFlys(statJson: dict, teamNum: int, rosterNum: int = -1):
    if rosterNum == -1:
        total = 0
        for x in range(0, 9):
            total += offensiveStats(statJson, teamNum, x)["Sac Flys"]
        return total
    else:
        return offensiveStats(statJson, teamNum, rosterNum)["Sac Flys"]

# returns how many times a character struck out when batting
# if no character given, returns how many times a team struck out when batting
def strikeouts(statJson: dict, teamNum: int, rosterNum: int = -1):
    if rosterNum == -1:
        total = 0
        for x in range(0, 9):
            total += offensiveStats(statJson, teamNum, x)["Strikeouts"]
        return total
    else:
        return offensiveStats(statJson, teamNum, rosterNum)["Strikeouts"]

# returns how many times a character was walked when batting
# if no character given, returns how many times a team was walked when batting
def walks(statJson: dict, teamNum: int, rosterNum: int):
    return walksBallFour(statJson, teamNum, rosterNum) + walksHitByPitch(statJson, teamNum, rosterNum)

# returns how many times a character was walked via 4 balls when batting
# if no character given, returns how many times a team was walked via 4 balls when batting
def walksBallFour(statJson: dict, teamNum: int, rosterNum: int = -1):
    if rosterNum == -1:
        total = 0
        for x in range(0, 9):
            total += offensiveStats(statJson, teamNum, x)["Walks (4 Balls)"]
        return total
    else:
        return offensiveStats(statJson, teamNum, rosterNum)["Walks (4 Balls)"]

# returns how many times a character was walked via hit by pitch when batting
# if no character given, returns how many times a team was walked via hit by pitch when batting
def walksHitByPitch(statJson: dict, teamNum: int, rosterNum:int = -1):
    if rosterNum == -1:
        total = 0
        for x in range(0, 9):
            total += offensiveStats(statJson, teamNum, x)["Walks (Hit)"]
        return total
    else:
        return offensiveStats(statJson, teamNum, rosterNum)["Walks (Hit)"]

# returns how many RBI's a character had
# if no character given, returns how many RBI's a team had
def rbi(statJson: dict, teamNum: int, rosterNum: int = -1):
    if rosterNum == -1:
        total = 0
        for x in range(0, 9):
            total += offensiveStats(statJson, teamNum, x)["RBI"]
        return total
    else:
        return offensiveStats(statJson, teamNum, rosterNum)["RBI"]

# returns how many times a character successfully stole a base
# if no character given, returns how many times a team successfully stole a base
def basesStolen(statJson: dict, teamNum: int, rosterNum: int = -1):
    if rosterNum == -1:
        total = 0
        for x in range(0, 9):
            total += offensiveStats(statJson, teamNum, x)["Bases Stolen"]
        return total
    else:
        return offensiveStats(statJson, teamNum, rosterNum)["Bases Stolen"]

# returns how many star hits a character used
# if no character given, returns how many star hits a team used
def starHitsUsed(statJson: dict, teamNum: int, rosterNum: int = -1):
    if rosterNum == -1:
        total = 0
        for x in range(0, 9):
            total += offensiveStats(statJson, teamNum, x)["Star Hits"]
        return total
    else:
        return offensiveStats(statJson, teamNum, rosterNum)["Star Hits"]




# complicated stats

# returns the batting average of a character
# if no character given, returns the batting average of a team
def battingAvg(statJson: dict, teamNum: int, rosterNum: int = -1):
    nAtBats = atBats(statJson, teamNum, rosterNum)
    nHits = hits(statJson, teamNum, rosterNum)
    nWalks = walks(statJson, teamNum, rosterNum)
    return float(nHits) / float(nAtBats - nWalks)

# returns the on base percentage of a character
# if no character given, returns the on base percentage of a team
def obp(statJson: dict, teamNum: int, rosterNum: int = -1):
    nAtBats = atBats(statJson, teamNum, rosterNum)
    nHits = hits(statJson, teamNum, rosterNum)
    nWalks = walks(statJson, teamNum, rosterNum)
    return float(nHits + nWalks) / float(nAtBats)

# returns the SLG of a character
# if no character given, returns the SLG of a team
def slg(statJson: dict, teamNum: int, rosterNum: int = -1):
    nAtBats = atBats(statJson, teamNum, rosterNum)
    nSingles = singles(statJson, teamNum, rosterNum)
    nDoubles = doubles(statJson, teamNum, rosterNum)
    nTriples = triples(statJson, teamNum, rosterNum)
    nHomeruns = homeruns(statJson, teamNum, rosterNum)
    nWalks = walks(statJson, teamNum, rosterNum)
    return float(nSingles + nDoubles*2 + nTriples*3 + nHomeruns*4) / float(nAtBats - nWalks)

# returns the OPS of a character
# if no character given, returns the OPS of a team
def ops(statJson: dict, teamNum: int, rosterNum: int = -1):
    return obp(statJson, teamNum, rosterNum) + slg(statJson, teamNum, rosterNum)


# event stats
# these all probably invlove looping through all the events


# manual exception handling stuff

# tells if the teamNum is invalid
def __errorCheck_teamNum(teamNum: int):
    if teamNum != 0 and teamNum != 1:
        raise Exception(f'Invalid team arg {teamNum}. Function only accepts team args of 0 (home team) or 1 (away team).')

# tells if rosterNum is invalid. allows -1 arg
def __errorCheck_rosterNum(rosterNum: int):
    if rosterNum < -1 or rosterNum > 8:
        raise Exception(f'Invalid roster arg {rosterNum}. Function only accepts roster args of from 0 to 8.')

# tells if rosterNum is invalid. does not allow -1 arg
def __errorCheck_rosterNum2(rosterNum: int):
    if rosterNum < 0 or rosterNum > 8:
        raise Exception(f'Invalid roster arg {rosterNum}. Function only accepts roster args of from 0 to 8.')


