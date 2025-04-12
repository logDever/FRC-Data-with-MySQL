import mysql.connector

masterfilename = "artificialDataA.csv"
masterhostname = "localhost"
masterusername = "pythonUser"
masterpasswd = "1234"
masterdb = "sat4650 artificial data"
# noinspection SpellCheckingInspection
mastertable = "artificialdataa"

def Overview_Print(targetAverage, targetTeleAverage, targetAutoAverage, targetAverageDroppedCoral,
                   targetGoodParnterAverage,
                   targetBadPartnerAverage, targetAverageClimbPoints, targetAverageSpeedRating, targetNumber):
    print(
        "***********************************\n"
        f"Averages for {targetNumber:}: \n\n"
        f"Total Average: {targetAverage:.3f}\n"
        f"Tele Average: {targetTeleAverage:.3f}\n"
        f"Auto-Average: {targetAutoAverage:.3f}\n"
        f"Average Dropped Coral: {targetAverageDroppedCoral:.3f}\n"
        f"Good Partner: {targetGoodParnterAverage:.3f}\n"
        f"Bad Partner: {targetBadPartnerAverage:.3f}\n"
        f"Average Climb Points: {targetAverageClimbPoints:.3f}\n"
        f"Average Speed: {targetAverageSpeedRating:.3f}\n"
    )

def Calculate_Data(targetData):
    calcData = []

    # Climb Score
    def Match_Climb(climbVal):
        match(climbVal):
            case 0:
                return 0
            case 1:
                return 4
            case 2:
                return 6
            case 3:
                return 10
            case 4:
                return 16
            case _:
                return None
    climb_score = Match_Climb(targetData[12])
    calcData.append(climb_score)

    # Tele Cargo Score
    tele_cargo_score = (
            targetData[10]*2 + targetData[11]
    )
    calcData.append(tele_cargo_score)

    # Auto Cargo Score
    auto_cargo_score = targetData[8] * 2 + targetData[7] * 4
    calcData.append(auto_cargo_score)

    # Auto Tarmac
    auto_tarmac = targetData[9]*2

    # Total Auto Score
    total_auto_score = (
            auto_tarmac + auto_cargo_score
    )
    calcData.append(total_auto_score)

    # Did Climb?
    did_climb = 1 if climb_score > 0 else 0
    calcData.append(did_climb)

    # Total Tele Score
    total_tele_score = (
            climb_score + tele_cargo_score
    )
    calcData.append(total_tele_score)

    # Individual Score
    individual_score = (
        total_tele_score + auto_cargo_score
    )
    calcData.append(individual_score)


    ## Index Mapping
    # 0 -> Event_Name (varchar(45))
    # 1 -> Match_Type (varchar(45))
    # 2 -> Match_Num (int)
    # 3 -> Scouter_Initials (varchar(5))
    # 4 -> Team_Num (int)
    # 5 -> Team_Name (varchar(45))
    # 6 -> Start_Position (int)
    # 7 -> Auto_Cargo_Upper (int)
    # 8 -> Auto_Cargo_Lower (int)
    # 9 -> Auto_Tarmac (int)
    # 10 -> Tele_Cargo_Upper (int)
    # 11 -> Tele_Cargo_Lower (int)
    # 12 -> Hangar_Level (int)
    # 13 -> Hangar_Time (int)
    # 14 -> Use_Launch_Pad (int)
    # 15 -> Cargo_Loaded_Start (int)
    # 16 -> Defense_Rating (int)
    # 17 -> Speed_Rating (int)
    # 18 -> Tippy (int)
    # 19 -> Died_in_Match (int)
    # 20 -> Penalties (int)

    # 21 -> climb_score
    # 22 -> tele_cargo_score
    # 23 -> auto_cargo_score
    # 24 -> total_auto_score
    # 25 -> did_climb
    # 26 -> total_tele_score
    # 27 -> individual_score

    return calcData



def Call_Data_Team(teamnumber, doPrint = True, hostname=masterhostname, username=masterusername, passwd=masterpasswd,
                 db=masterdb, table=mastertable):
    outputData = []
    ## Server config
    cnx = mysql.connector.connect(
        host=hostname,
        user=username,
        passwd=passwd,
        database=db
    )
    cursor = cnx.cursor()  # Create SQL cursor object

    # SQL code to earch by team number
    # noinspection SqlNoDataSourceInspection
    teamNumQuery = f"SELECT * FROM `{table}` WHERE `Team_Num` = %s"

    # Execute
    cursor.execute(teamNumQuery, (teamnumber,))
    outputData = [list(row) for row in cursor.fetchall()]

    # Cleanup
    cursor.close()
    cnx.close()

    # Run calculations and append data
    for i, record in enumerate(outputData):
        outputData[i].extend(Calculate_Data(record))
        if doPrint:
            print(
                f"Event_Name: {outputData[i][0]}\n"
                f"Match_Type: {outputData[i][1]}\n"
                f"Match_Num: {outputData[i][2]}\n"
                f"Scouter_Initials: {outputData[i][3]}\n"
                f"Team_Num: {outputData[i][4]}\n"
                f"Team_Name: {outputData[i][5]}\n"
                f"Start_Position: {outputData[i][6]}\n"
                f"Auto_Cargo_Upper: {outputData[i][7]}\n"
                f"Auto_Cargo_Lower: {outputData[i][8]}\n"
                f"Auto_Tarmac: {outputData[i][9]}\n"
                f"Tele_Cargo_Upper: {outputData[i][10]}\n"
                f"Tele_Cargo_Lower: {outputData[i][11]}\n"
                f"Hangar_Level: {outputData[i][12]}\n"
                f"Hangar_Time: {outputData[i][13]}\n"
                f"Use_Launch_Pad: {outputData[i][14]}\n"
                f"Cargo_Loaded_Start: {outputData[i][15]}\n"
                f"Defense_Rating: {outputData[i][16]}\n"
                f"Speed_Rating: {outputData[i][17]}\n"
                f"Tippy: {outputData[i][18]}\n"
                f"Died_in_Match: {outputData[i][19]}\n"
                f"Penalties: {outputData[i][20]}\n"
                f"climb_score: {outputData[i][21]}\n"
                f"tele_cargo_score: {outputData[i][22]}\n"
                f"auto_cargo_score: {outputData[i][23]}\n"
                f"total_auto_score: {outputData[i][24]}\n"
                f"did_climb: {outputData[i][25]}\n"
                f"total_tele_score: {outputData[i][26]}\n"
                f"individual_score: {outputData[i][27]}\n"
                "***********************************"
            )
    return outputData

def Call_Team_Overview(teamnumber, doPrint = True, hostname=masterhostname, username=masterusername, passwd=masterpasswd,
                 db=masterdb, table=mastertable):
    teamData = Call_Data_Team(teamnumber, False, hostname, username, passwd, db, table)
    # Totals
    teamTeleTotal = 0
    teamAutoTotal = 0
    teamTotal = 0
    teamTotalClimbPoints = 0
    teamTotalSpeedRating = 0
    teamtotalDefenseRating = 0
    teamUpperTotal = 0
    teamLowerTotal = 0
    teamTotalClimbTime = 0
    teamTotalClimbCount = 0

    for record in teamData:
        teamTeleTotal += record[26]
        teamAutoTotal += record[24]
        teamTotal += record[27]
        teamTotalClimbPoints += record[21]
        teamTotalSpeedRating += record[17]
        teamtotalDefenseRating += record[16]
        teamUpperTotal += record[10] + record[7]
        teamLowerTotal += record[11] + record[8]
        teamTotalClimbTime += record[13]
        teamTotalClimbCount += record[25]


    # Averages
    teamTeleAverage = teamTeleTotal / len(teamData)
    teamAutoAverage = teamAutoTotal / len(teamData)
    teamAverage = teamTotal / len(teamData)
    teamAverageClimbPoints = teamTotalClimbPoints / len(teamData)
    teamAverageSpeedRating = teamTotalSpeedRating / len(teamData)
    teamAverageDefenseRating = teamtotalDefenseRating / len(teamData)
    teamUpperAverage = teamUpperTotal / len(teamData)
    teamLowerAverage = teamLowerTotal / len(teamData)
    teamAverageClimbTime = teamTotalClimbTime / len(teamData)
    teamClimbRate = teamTotalClimbCount / len(teamData)

    teamAverages = [teamTeleAverage, teamAutoAverage, teamAverage, teamAverageClimbPoints, teamAverageSpeedRating,
                    teamAverageDefenseRating, teamUpperAverage, teamLowerAverage, teamAverageClimbTime,
                    teamClimbRate, teamnumber]
    def Overview_Print(targetTeleAverage, targetAutoAverage, targetAverage, targetAverageClimbPoints,
                       targetAverageSpeedRating, targetAverageDefenseRating, targetUpperAverage, targetLowerAverage,
                       targetAverageClimbTime, targetClimbRate, targetNumber):
        print(
            "***********************************\n"
            f"Averages for {targetNumber:}: \n\n"
            f"Total Average: {targetAverage:.3f}\n"
            f"Tele Average: {targetTeleAverage:.3f}\n"
            f"Auto-Average: {targetAutoAverage:.3f}\n"
            f"Average Climb Points: {targetAverageClimbPoints:.3f}\n"
            f"Average Climb Time: {targetAverageClimbTime:.3f}\n"
            f"Average Climb Rate: {targetClimbRate:.3f}\n"
            f"Average Defense: {targetAverageDefenseRating:.3f}\n"
            f"Average Speed: {targetAverageSpeedRating:.3f}\n"
            f"Average Cargo in Upper: {targetUpperAverage:.3f}\n"
            f"Average Cargo in Lower: {targetLowerAverage:.3f}\n"
        )
    if doPrint:
        Overview_Print(teamTeleAverage, teamAutoAverage, teamAverage, teamAverageClimbPoints, teamAverageSpeedRating,
                    teamAverageDefenseRating, teamUpperAverage, teamLowerAverage, teamAverageClimbTime,
                    teamClimbRate, teamnumber)
    return teamAverages
def Find_Teams(doPrint = True, hostname=masterhostname, username=masterusername, passwd=masterpasswd,
                 db=masterdb, table=mastertable):
    allTeamNums = []
    ## Server config
    cnx = mysql.connector.connect(
        host=hostname,
        user=username,
        passwd=passwd,
        database=db
    )
    cursor = cnx.cursor()  # Create SQL cursor object

    # SQL code to earch by team number
    # noinspection SqlNoDataSourceInspection
    allTeamNumQuery = f"SELECT `Team_Num` FROM `{table}`"

    # Execute
    cursor.execute(allTeamNumQuery)
    allTeamNums = [row[0] for row in cursor.fetchall()]
    allTeamNums = list(set(allTeamNums))
    cnx.close()
    if doPrint:
        print("All team numbers:", allTeamNums)
    return allTeamNums

def Match_Search_Metric_Overview(searchMetric):
        match searchMetric:
            case "Teleop Performance":
                return 0
            case "Autonomous Performance":
                return 1
            case "Total Performance":
                return 2
            case "Climb Points":
                return 3
            case "Speed Rating":
                return 4
            case "Defense Rating":
                return 5
            case "Upper Cargo Average":
                return 6
            case "Lower Cargo Average":
                return 7
            case  "Climb Time":
                return 8
            case "Climb Rate":
                return 9
            case _:
                print("Case Error")
                exit()

def Find_Best_Teams(teamCount = 3, searchMetric = "Total Performance", dataoroverview = 0, doPrint = True, hostname=masterhostname, username=masterusername, passwd=masterpasswd,
                 db=masterdb):

    topTeamOverview = [] * teamCount
    allTeamNums = Find_Teams(False)
    allTeamOverview = []
    allTeamDict = {}
    searchMetricValue = Match_Search_Metric_Overview(searchMetric)
    for teamNum in allTeamNums:
        allTeamOverview.append(Call_Team_Overview(teamNum, False))
    for team in allTeamOverview:
        teamNumber = team[10]
        allTeamDict[teamNumber] = team[searchMetricValue]

    sortedTeams = sorted(allTeamDict.items(), key=lambda searchValue: searchValue[1], reverse=True)
    topTeams = sortedTeams[:teamCount]
    for teamNum in topTeams:
        topTeamOverview.append(Call_Team_Overview(teamNum[0], False))
    if doPrint:
        print("***********************************")
        print(f"Showing the top {teamCount} teams for \"{searchMetric}\"")
        for team in topTeamOverview:
            Call_Team_Overview(team[10])

    match dataoroverview:
        case 0:
            return topTeams
        case 1:
            return topTeamOverview
        case _:
            return topTeams, topTeamOverview

def Match_Search_Metric(searchMetric):
    match searchMetric:
        case "Event_Name":
            return 0
        case "Match_Type":
            return 1
        case "Match_Num":
            return 2
        case "Scouter_Initials":
            return 3
        case "Team_Num":
            return 4
        case "Team_Name":
            return 5
        case "Start_Position":
            return 6
        case "Auto_Cargo_Upper":
            return 7
        case "Auto_Cargo_Lower":
            return 8
        case "Auto_Tarmac":
            return 9
        case "Tele_Cargo_Upper":
            return 10
        case "Tele_Cargo_Lower":
            return 11
        case "Hangar_Level":
            return 12
        case "Hangar_Time":
            return 13
        case "Use_Launch_Pad":
            return 14
        case "Cargo_Loaded_Start":
            return 15
        case "Defense_Rating":
            return 16
        case "Speed_Rating":
            return 17
        case "Tippy":
            return 18
        case "Died_in_Match":
            return 19
        case "Penalties":
            return 20
        case "climb_score":
            return 21
        case "tele_cargo_score":
            return 22
        case "auto_cargo_score":
            return 23
        case "total_auto_score":
            return 24
        case "did_climb":
            return 25
        case "total_tele_score":
            return 26
        case "individual_score":
            return 27
        case _:
            print("Invalid Metric")
            return None

def Print_Specific_Team_Data(searchmetric, teamnum, teamdata):
    print("***********************************")
    print(f"Showing all data about \"{searchmetric}\" for Team {teamnum}")
    for index in range(len(teamdata)):
        printstring = f"Match {index+1}: {teamdata[index]}"
        print(printstring)
    return

def Call_Specific_Team_Data(teamnumber, searchmetric, doPrint = True, hostname=masterhostname, username=masterusername, passwd=masterpasswd,
                 db=masterdb, table=mastertable):
    teamData = Call_Data_Team(teamnumber, False, hostname, username, passwd, db, table)
    matchedMetric = Match_Search_Metric(searchmetric)
    returnData = []
    for record in teamData:
        returnData.append(record[matchedMetric])
    if doPrint:
        Print_Specific_Team_Data(searchmetric, teamnumber, returnData)
    return returnData
Call_Specific_Team_Data(1502, "Tippy")
Find_Teams()
Find_Best_Teams(5,"Total Performance",1,True)
Call_Data_Team(1502)
Call_Team_Overview(1502)