'''
Intended to parse "decoded" files which would be present on a user's computer

How to use:
- import RioStatLib obviously
- open a Rio stat json file
- convert from json string to obj using json.loads(jsonStr)
- create StatObj with your stat json obj using the following:
	myStats = RioStatLib.StatObj(jsonObj)
- call any of the built in methods to get some stats

- ex:
	import RioStatLib
	import json
	with open("path/to/RioStatFile.json", "r") as jsonStr:
		jsonObj = json.loads(jsonStr)
		myStats = RioStatLib(jsonObj)
		homeTeamOPS = myStats.ops(0)
		awayTeamSLG = myStats.slg(1)
		booERA = myStats.era(0, 4) # Boo in this example is the 4th character on the home team
		
Roster args:
- arg == 0 means team0 which is the home team
- arg == 1 means team1 which is the away team
- arg == -1 means all characters (if function allows)
'''


# create stat obj
class StatObj:
    def __init__(this, statJson: dict):
        this.statJson = statJson


    # large info functions

    # returns it in int form
    def gameID(this):
        return int(this.statJson["GameID"].replace(',', ''), 16)

    # should look to convert to unix or some other standard date fmt
    def date(this):
        return this.statJson["Date"]

    # tells if a game was a ranked game or not
    def isRanked(this):
        rankedStatus = this.statJson["Ranked"]
        if rankedStatus == 0:
            return False
        else:
            return True

    # reutrns the stadium that was played on
    def stadium(this):
        return this.statJson["StadiumID"]

    # returns name of player. teamNum == 0 is home team, teamNum == 1 is away team
    def player(this, teamNum: int):
        if teamNum == 0:
            return this.statJson["Home Player"]
        elif teamNum == 1:
            return this.statJson["Away Player"]
        else:
            this.__errorCheck_teamNum(teamNum)

    # returns final score of said team
    def score(this, teamNum: int):
        if teamNum == 0:
            return this.statJson["Home Score"]
        elif teamNum == 1:
            return this.statJson["Away Score"]
        else:
            this.__errorCheck_teamNum(teamNum)

    # returns how many innings were selected for the game
    def inningsTotal(this):
        return this.statJson["Innings Selected"]

    # returns how many innings were played in the game
    def inningsPlayed(this):
        return this.statJson["Innings Played"]

    # returns if the game ended in a mercy or not
    def isMercy(this):
        if this.inningsTotal() - this.inningsPlayed() >= 1 and not this.wasQuit():
            return True
        else:
            return False

    # returns if the same was quit out early
    def wasQuit(this):
        if this.statJson["Quitter Team"] == "":
            return False
        else:
            return True

    # returns the name of the quitter if the game was quit. empty string if no quitter
    def quitter(this):
        return this.statJson["Quitter Team"]

    # returns average ping of the game
    def ping(this):
        return this.statJson["Average Ping"]

    # returns number of lag spikes in a game
    def lagspikes(this):
        return this.statJson["Lag Spikes"]

    # returns the full dict of character game stats as shown in the stat file
    def characterGameStats(this):
        return this.statJson["Character Game Stats"]

    # returns if the game has any superstar characters in it
    def isSuperstarGame(this):
        isStarred = False
        charStats = this.characterGameStats()
        for character in charStats:
            if charStats[character]["Superstar"] == 1:
                isStarred = True
        return isStarred

    # TODO: function that tells if no stars, stars, or mixed stars?

    # character stats
    # (this, teamNum: int, rosterNum: int):

    # returns name of specified character
    # if no roster spot is provided, returns a list of characters on a given team
    def characterName(this, teamNum: int, rosterNum: int = -1):
        this.__errorCheck_teamNum(teamNum)
        this.__errorCheck_rosterNum(rosterNum)
        if rosterNum == -1:
            charList = []
            for x in range(0, 9):
                charList.append(this.statJson["Character Game Stats"][f"Team {teamNum} Roster {x}"]["CharID"])
            return charList
        else:
            return this.statJson["Character Game Stats"][f"Team {teamNum} Roster {rosterNum}"]["CharID"]

    # returns if a character is starred
    # if no arg, returns if any character on the team is starred
    def isStarred(this, teamNum: int, rosterNum: int = -1):
        this.__errorCheck_teamNum(teamNum)
        this.__errorCheck_rosterNum(rosterNum)
        if rosterNum == -1:
            for x in range(0, 9):
                if this.statJson["Character Game Stats"][f"Team {teamNum} Roster {x}"]["Superstar"] == 1:
                    return True
        else:
            if this.statJson["Character Game Stats"][f"Team {teamNum} Roster {rosterNum}"]["Superstar"] == 1:
                return True
            else:
                return False

    # returns name of chatacter who is the captian
    def captain(this, teamNum: int):
        this.__errorCheck_teamNum(teamNum)
        captain = ""
        for character in this.characterGameStats():
            if character["Captain"] == 1 and int(character["Team"]) == teamNum:
                captain = character["CharID"]
        return captain

    # grabs offensive stats of a character as seen in the stat json
    # if no roster provided, returns a list of all character's offensive stats
    def offensiveStats(this, teamNum: int, rosterNum: int = -1):
        this.__errorCheck_teamNum(teamNum)
        this.__errorCheck_rosterNum(rosterNum)
        if rosterNum == -1:
            oStatList = []
            for x in range(0, 9):
                oStatList.append(this.statJson["Character Game Stats"][f"Team {teamNum} Roster {x}"]["Offensive Stats"])
            return oStatList
        else:
            return this.statJson["Character Game Stats"][f"Team {teamNum} Roster {rosterNum}"]["Offensive Stats"]

    # grabs defensive stats of a character as seen in the stat json
    # if no roster provided, returns a list of all character's defensive stats
    def defensiveStats(this, teamNum: int, rosterNum: int = -1):
        this.__errorCheck_teamNum(teamNum)
        this.__errorCheck_rosterNum(rosterNum)
        if rosterNum == -1:
            dStatList = []
            for x in range(0, 9):
                dStatList.append(this.statJson["Character Game Stats"][f"Team {teamNum} Roster {x}"]["Defensive Stats"])
            return dStatList
        else:
            return this.statJson["Character Game Stats"][f"Team {teamNum} Roster {rosterNum}"]["Defensive Stats"]

    # returns fielding handedness of character
    def fieldingHand(this, teamNum: int, rosterNum: int):
        this.__errorCheck_teamNum(teamNum)
        this.__errorCheck_rosterNum2(rosterNum)
        return this.statJson["Character Game Stats"][f"Team {teamNum} Roster {rosterNum}"]["Fielding Hand"]

    # returns batting handedness of character
    def battingHand(this, teamNum: int, rosterNum: int):
        this.__errorCheck_teamNum(teamNum)
        this.__errorCheck_rosterNum2(rosterNum)
        return this.statJson["Character Game Stats"][f"Team {teamNum} Roster {rosterNum}"]["Batting Hand"]


    # defensive stats

    # tells the era of a character
    # if no character given, returns era of that team
    def era(this, teamNum: int, rosterNum: int = -1):
        return 9 * float(this.runsAllowed(teamNum, rosterNum)) / this.inningPitched(teamNum, rosterNum)

    # tells how many batters were faced by character
    # if no character given, returns batters faced by that team
    def battersFaced(this, teamNum: int, rosterNum: int = -1):
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.defensiveStats(teamNum, x)["Batters Faced"]
            return total
        else:
            return this.defensiveStats(teamNum, rosterNum)["Batters Faced"]

    # tells how many runs a character allowed when pitching
    # if no character given, returns runs allowed by that team
    def runsAllowed(this, teamNum: int, rosterNum: int = -1):
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.defensiveStats(teamNum, x)["Runs Allowed"]
            return total
        else:
            return this.defensiveStats(teamNum, rosterNum)["Runs Allowed"]

    # tells how many walks a character allowed when pitching
    # if no character given, returns walks by that team
    def battersWalked(this, teamNum: int, rosterNum: int = -1):
        return this.battersWalkedBallFour(teamNum, rosterNum) + this.battersHitByPitch(teamNum, rosterNum)

    # returns how many times a character has walked a batter via 4 balls
    # if no character given, returns how many times the team walked via 4 balls
    def battersWalkedBallFour(this, teamNum: int, rosterNum: int = -1):
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.defensiveStats(teamNum, x)["Batters Walked"]
            return total
        else:
            return this.defensiveStats(teamNum, rosterNum)["Batters Walked"]

    # returns how many times a character walked a batter by hitting them by a pitch
    # if no character given, returns walked via HBP for the team
    def battersHitByPitch(this, teamNum: int, rosterNum: int = -1):
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.defensiveStats(teamNum, x)["Batters Hit"]
            return total
        else:
            return this.defensiveStats(teamNum, rosterNum)["Batters Hit"]

    # returns how many hits a character allowed as pitcher
    # if no character given, returns how many hits a team allowed
    def hitsAllowed(this, teamNum: int, rosterNum: int = -1):
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.defensiveStats(teamNum, x)["Hits Allowed"]
            return total
        else:
            return this.defensiveStats(teamNum, rosterNum)["Hits Allowed"]

    # returns how many homeruns a character allowed as pitcher
    # if no character given, returns how many homeruns a team allowed
    def homerunsAllowed(this, teamNum: int, rosterNum: int = -1):
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.defensiveStats(teamNum, x)["HRs Allowed"]
            return total
        else:
            return this.defensiveStats(teamNum, rosterNum)["HRs Allowed"]

    # returns how many pitches a character threw
    # if no character given, returns how many pitches a team threw
    def pitchesThrown(this, teamNum: int, rosterNum: int = -1):
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.defensiveStats(teamNum, x)["Pitches Thrown"]
            return total
        else:
            return this.defensiveStats(teamNum, rosterNum)["Pitches Thrown"]

    # returns final pitching stamina of a pitcher
    # if no character given, returns total stamina of a team
    def stamina(this, teamNum: int, rosterNum: int = -1):
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.defensiveStats(teamNum, x)["Stamina"]
            return total
        else:
            return this.defensiveStats(teamNum, rosterNum)["Stamina"]

    # returns if a character was a pitcher
    def wasPitcher(this, teamNum: int, rosterNum: int):
        this.__errorCheck_rosterNum2(rosterNum)
        if this.defensiveStats(teamNum, rosterNum)["Was Pitcher"] == 1:
            return True
        else:
            return False

    # returns how many strikeouts a character pitched
    # if no character given, returns how mnany strikeouts a team pitched
    def strikeoutsPitched(this, teamNum: int, rosterNum: int = -1):
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.defensiveStats(teamNum, x)["Strikeouts"]
            return total
        else:
            return this.defensiveStats(teamNum, rosterNum)["Strikeouts"]

    # returns how many star pitches a charcter threw
    # if no character given, returns how many star pitches a team threw
    def starPitchesThrown(this, teamNum: int, rosterNum: int = -1):
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.defensiveStats(teamNum, x)["Star Pitches Thrown"]
            return total
        else:
            return this.defensiveStats(teamNum, rosterNum)["Star Pitches Thrown"]

    # returns how many big plays a character had
    # if no character given, returns how many big plays a team had
    def bigPlays(this, teamNum: int, rosterNum: int = -1):
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.defensiveStats(teamNum, x)["Big Plays"]
            return total
        else:
            return this.defensiveStats(teamNum, rosterNum)["Big Plays"]

    # returns how many outs a charcter was pitching for
    # if no character given, returns how many outs a team pitched for
    def outsPitched(this, teamNum: int, rosterNum: int = -1):
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.defensiveStats(teamNum, x)["Outs Pitched"]
            return total
        else:
            return this.defensiveStats(teamNum, rosterNum)["Outs Pitched"]
	
    # returns how many innings a charcter was pitching for
    # if no character given, returns how many innings a team pitched for
    def inningsPitched(this, teamNum: int, rosterNum: int = -1):
        return float(this.outsPitched(teamNum, rosterNum)) / 3

    # returns a dict which tracks how many pitches a charcter was at a position for
    def pitchesPerPosition(this, teamNum: int, rosterNum: int):
        this.__errorCheck_rosterNum2(rosterNum)
        return this.defensiveStats(teamNum, rosterNum)["Pitches Per Position"][0]

    # returns a dict which tracks how many outs a charcter was at a position for
    def outsPerPosition(this, teamNum: int, rosterNum: int):
        this.__errorCheck_rosterNum2(rosterNum)
        return this.defensiveStats(teamNum, rosterNum)["Outs Per Position"][0]


    # offensive stats

    # returns how many at bats a character had
    # if no character given, returns how many at bats a team had
    def atBats(this, teamNum: int, rosterNum: int = -1):
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.offensiveStats(teamNum, x)["At Bats"]
            return total
        else:
            return this.offensiveStats(teamNum, rosterNum)["At Bats"]

    # returns how many hits a character had
    # if no character given, returns how many hits a team had
    def hits(this, teamNum: int, rosterNum: int = -1):
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.offensiveStats(teamNum, x)["Hits"]
            return total
        else:
            return this.offensiveStats(teamNum, rosterNum)["Hits"]

    # returns how many singles a character had
    # if no character given, returns how many singles a team had
    def singles(this, teamNum: int, rosterNum: int = -1):
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.offensiveStats(teamNum, x)["Singles"]
            return total
        else:
            return this.offensiveStats(teamNum, rosterNum)["Singles"]

    # returns how many doubles a character had
    # if no character given, returns how many doubles a team had
    def doubles(this, teamNum: int, rosterNum: int = -1):
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.offensiveStats(teamNum, x)["Doubles"]
            return total
        else:
            return this.offensiveStats(teamNum, rosterNum)["Doubles"]

    # returns how many triples a character had
    # if no character given, returns how many triples a teams had
    def triples(this, teamNum: int, rosterNum: int = -1):
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.offensiveStats(teamNum, x)["Triples"]
            return total
        else:
            return this.offensiveStats(teamNum, rosterNum)["Triples"]

    # returns how many homeruns a character had
    # if no character given, returns how many homeruns a team had
    def homeruns(this, teamNum: int, rosterNum: int = -1):
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.offensiveStats(teamNum, x)["Homeruns"]
            return total
        else:
            return this.offensiveStats(teamNum, rosterNum)["Homeruns"]

    # returns how many successful bunts a character had
    # if no character given, returns how many successful bunts a team had
    def buntsLanded(this, teamNum: int, rosterNum: int = -1):
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.offensiveStats(teamNum, x)["Successful Bunts"]
            return total
        else:
            return this.offensiveStats(teamNum, rosterNum)["Successful Bunts"]

    # returns how many sac flys a character had
    # if no character given, returns how many sac flys a team had
    def sacFlys(this, teamNum: int, rosterNum: int = -1):
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.offensiveStats(teamNum, x)["Sac Flys"]
            return total
        else:
            return this.offensiveStats(teamNum, rosterNum)["Sac Flys"]

    # returns how many times a character struck out when batting
    # if no character given, returns how many times a team struck out when batting
    def strikeouts(this, teamNum: int, rosterNum: int = -1):
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.offensiveStats(teamNum, x)["Strikeouts"]
            return total
        else:
            return this.offensiveStats(teamNum, rosterNum)["Strikeouts"]

    # returns how many times a character was walked when batting
    # if no character given, returns how many times a team was walked when batting
    def walks(this, teamNum: int, rosterNum: int):
        return this.walksBallFour(teamNum, rosterNum) + this.walksHitByPitch(teamNum, rosterNum)

    # returns how many times a character was walked via 4 balls when batting
    # if no character given, returns how many times a team was walked via 4 balls when batting
    def walksBallFour(this, teamNum: int, rosterNum: int = -1):
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.offensiveStats(teamNum, x)["Walks (4 Balls)"]
            return total
        else:
            return this.offensiveStats(teamNum, rosterNum)["Walks (4 Balls)"]

    # returns how many times a character was walked via hit by pitch when batting
    # if no character given, returns how many times a team was walked via hit by pitch when batting
    def walksHitByPitch(this, teamNum: int, rosterNum:int = -1):
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.offensiveStats(teamNum, x)["Walks (Hit)"]
            return total
        else:
            return this.offensiveStats(teamNum, rosterNum)["Walks (Hit)"]

    # returns how many RBI's a character had
    # if no character given, returns how many RBI's a team had
    def rbi(this, teamNum: int, rosterNum: int = -1):
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.offensiveStats(teamNum, x)["RBI"]
            return total
        else:
            return this.offensiveStats(teamNum, rosterNum)["RBI"]

    # returns how many times a character successfully stole a base
    # if no character given, returns how many times a team successfully stole a base
    def basesStolen(this, teamNum: int, rosterNum: int = -1):
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.offensiveStats(teamNum, x)["Bases Stolen"]
            return total
        else:
            return this.offensiveStats(teamNum, rosterNum)["Bases Stolen"]

    # returns how many star hits a character used
    # if no character given, returns how many star hits a team used
    def starHitsUsed(this, teamNum: int, rosterNum: int = -1):
        if rosterNum == -1:
            total = 0
            for x in range(0, 9):
                total += this.offensiveStats(teamNum, x)["Star Hits"]
            return total
        else:
            return this.offensiveStats(teamNum, rosterNum)["Star Hits"]




    # complicated stats

    # returns the batting average of a character
    # if no character given, returns the batting average of a team
    def battingAvg(this, teamNum: int, rosterNum: int = -1):
        nAtBats = this.atBats(teamNum, rosterNum)
        nHits = this.hits(teamNum, rosterNum)
        nWalks = this.walks(teamNum, rosterNum)
        return float(nHits) / float(nAtBats - nWalks)

    # returns the on base percentage of a character
    # if no character given, returns the on base percentage of a team
    def obp(this, teamNum: int, rosterNum: int = -1):
        nAtBats = this.atBats(teamNum, rosterNum)
        nHits = this.hits(teamNum, rosterNum)
        nWalks = this.walks(teamNum, rosterNum)
        return float(nHits + nWalks) / float(nAtBats)

    # returns the SLG of a character
    # if no character given, returns the SLG of a team
    def slg(this, teamNum: int, rosterNum: int = -1):
        nAtBats = this.atBats(teamNum, rosterNum)
        nSingles = this.singles(teamNum, rosterNum)
        nDoubles = this.doubles(teamNum, rosterNum)
        nTriples = this.triples(teamNum, rosterNum)
        nHomeruns = this.homeruns(teamNum, rosterNum)
        nWalks = this.walks(teamNum, rosterNum)
        return float(nSingles + nDoubles*2 + nTriples*3 + nHomeruns*4) / float(nAtBats - nWalks)

    # returns the OPS of a character
    # if no character given, returns the OPS of a team
    def ops(this, teamNum: int, rosterNum: int = -1):
        return this.obp(teamNum, rosterNum) + this.slg(teamNum, rosterNum)


    # event stats
    # these all probably invlove looping through all the events

    # returns the dict of events in a game
    def events(this):
        return this.statJson['Events'][0]

    # returns the number of the last event
    def eventFinal(this):
        eventDict = this.events()
        finalEvent = 0
        for event in eventDict:
            eventNum = event["Event Num"]
            if eventNum > finalEvent:
                finalEvent = eventNum
        return finalEvent

    # returns a single event specified by it's number
    # if event is less than 0 or greater than the highest event, returns the last event
    def eventByNum(this, eventNum: int):
        eventDict = this.events()
        finalEvent = this.eventFinal()
        if eventNum < 0 or eventNum > finalEvent:
            eventNum = finalEvent
        for event in eventDict:
            if event["Event Num"] == eventNum:
                return event
        return {} # empty dict if no matching event found, which should be impossible anyway


    # manual exception handling stuff

    # tells if the teamNum is invalid
    def __errorCheck_teamNum(this, teamNum: int):
        if teamNum != 0 and teamNum != 1:
            raise Exception(f'Invalid team arg {teamNum}. Function only accepts team args of 0 (home team) or 1 (away team).')

    # tells if rosterNum is invalid. allows -1 arg
    def __errorCheck_rosterNum(this, rosterNum: int):
        if rosterNum < -1 or rosterNum > 8:
            raise Exception(f'Invalid roster arg {rosterNum}. Function only accepts roster args of from 0 to 8.')

    # tells if rosterNum is invalid. does not allow -1 arg
    def __errorCheck_rosterNum2(this, rosterNum: int):
        if rosterNum < 0 or rosterNum > 8:
            raise Exception(f'Invalid roster arg {rosterNum}. Function only accepts roster args of from 0 to 8.')
