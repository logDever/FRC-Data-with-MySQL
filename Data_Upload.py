import mysql.connector
import csv

## User Variables
# For purposes of this project, all of the data is being taken at once
masterfilename = "artificialDataA.csv"
masterhostname = "localhost"
masterusername = "pythonUser"
masterpasswd = "1234"
masterdb = "sat4650 artificial data"
mastertable = "artificialdataa"
masterdebug=True
## Function to read the data and save it in a 2D array
def Save_CSV(fileName):
    fileData =[]
    with open(fileName, 'r')as csvFile:# CSV File open
        csvReader = csv.reader(csvFile) # CSV Reader object
        next(csvReader)
        for row in csvReader:
            fileData.append(row)
    return fileData


## Because the csv reads everything as strings, we need to condition our records to the appropriate data type,
## this function does so for the 2022 season
def Condition_Record(currentRecord):
    outputRecord = [None] * len(currentRecord)

    # Process each column based on its expected type
    outputRecord[0] = currentRecord[0] if currentRecord[0] else None # Event_Name (varchar(45))
    outputRecord[1] = currentRecord[1] if currentRecord[1] else None # Match_Type (varchar(45))
    outputRecord[2] = int(currentRecord[2]) if currentRecord[2].isdigit() else None # Match_Num (int)
    outputRecord[3] = currentRecord[3] if currentRecord[3] else None # Scouter_Initials (varchar(5))
    outputRecord[4] = int(currentRecord[4]) if currentRecord[4].isdigit() else None # Team_Num (int)
    outputRecord[5] = currentRecord[5] if currentRecord[5] else None # Team_Name (varchar(45))
    outputRecord[6] = int(currentRecord[6]) if currentRecord[6].isdigit() else 0 # Start_Position (int)
    outputRecord[7] = int(currentRecord[7]) if currentRecord[7].isdigit() else 0 # Auto_Cargo_Upper (int)
    outputRecord[8] = int(currentRecord[8]) if currentRecord[8].isdigit() else 0 # Auto_Cargo_Lower (int)
    outputRecord[9] = int(currentRecord[9]) if currentRecord[9].isdigit() else 0 # Auto_Tarmac (int)
    outputRecord[10] = int(currentRecord[10]) if currentRecord[10].isdigit() else 0 # Tele_Cargo_Upper (int)
    outputRecord[11] = int(currentRecord[11]) if currentRecord[11].isdigit() else 0 # Tele_Cargo_Lower (int)
    outputRecord[12] = int(currentRecord[12]) if currentRecord[12].isdigit() else 0 # Hangar_Level (int)
    outputRecord[13] = int(currentRecord[13]) if currentRecord[13].isdigit() else 0 # Hangar_Time (int)
    outputRecord[14] = int(currentRecord[14]) if currentRecord[14].isdigit() else 0 # Use_Launch_Pad (int)
    outputRecord[15] = int(currentRecord[15]) if currentRecord[15].isdigit() else 0 # Cargo_Loaded_Start (int)
    outputRecord[16] = int(currentRecord[16]) if currentRecord[16].isdigit() else 0 # Defense_Rating (int)
    outputRecord[17] = int(currentRecord[17]) if currentRecord[17].isdigit() else 0 # Speed_Rating (int)
    outputRecord[18] = int(currentRecord[18]) if currentRecord[18].isdigit() else 0 # Tippy (int)
    outputRecord[19] = int(currentRecord[19]) if currentRecord[19].isdigit() else 0 # Died_in_Match (int)
    outputRecord[20] = int(currentRecord[20]) if currentRecord[20].isdigit() else 0 # Penalties (int)

    return outputRecord

## This function will be callable by a system to inject packets of data into the database!
def Store_Record(fileName=masterfilename,
                 debug = masterdebug, hostname=masterhostname, username=masterusername, passwd=masterpasswd,
                 db=masterdb):

    ## Get data
    matchData = Save_CSV(fileName)

    ## Server config
    cnx = mysql.connector.connect(
        host=hostname,
        user=username,
        passwd=passwd,
        database=db
    )
    cursor = cnx.cursor()  # Create SQL cursor object

    if debug:
        cursor.execute(f"DELETE FROM {mastertable}")  # Delete data when debugging to keep things clean


    conditionedData = []
    for record in matchData:
        conditionedData.append(Condition_Record(record))

    # language=SQL
    # noinspection SqlNoDataSourceInspection
    sqlInjection = """
    INSERT INTO `artificialdataa` (
        `Event_Name`, `Match_Type`, `Match_Num`, `Scouter_Initials`, `Team_Num`,
        `Team_Name`, `Start_Position`, `Auto_Cargo_Upper`, `Auto_Cargo_Lower`, `Auto_Tarmac`, `Tele_Cargo_Upper`,
        `Tele_Cargo_Lower`, `Hangar_Level`, `Hangar_Time`, `Use_Launch_Pad`, `Cargo_Loaded_Start`, `Defense_Rating`,
        `Speed_Rating`, `Tippy`, `Died_in_Match`, `Penalties`
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
    """
    cursor.executemany(sqlInjection, conditionedData)
    cnx.commit()
    cursor.close()
    cnx.close()

Store_Record()
