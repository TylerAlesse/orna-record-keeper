import sqlite3

def query(connection: sqlite3.Connection, sql: str, params=[]):
    cursor = connection.cursor()
    try:
        cursor.execute(sql, params)
    except Exception as err:
        print("query failed:", err)
        return None
    finally:
        cursor.close()

#********************#
#* Reference Tables *#
#********************#

createCodexStatusTypeReference = '''
    CREATE TABLE "_CodexEntryStatus" (
        "Name"	TEXT,
        PRIMARY KEY("Name")
    )
'''
insertCodexStatusTypeReference = '''
    INSERT INTO "_CodexEntryStatus" ("Name") VALUES (?)'''
paramsCodexStatusTypeReference = [
    ("Missing",),
    ("Seen",),
    ("Complete",),
    ("Impossible",)
]

createCodexEntryTypeReference = '''
    CREATE TABLE "_CodexEntryType" (
        "Name"	TEXT,
        PRIMARY KEY("Name")
    )
'''
insertCodexEntryTypeReference = '''
    INSERT INTO "_CodexEntryType" ("Name") VALUES (?)'''
paramsCodexEntryTypeReference = [
    ("Monster",),
    ("Boss",),
    ("Raid",)
]

createEventsReference = '''
    CREATE TABLE "_Events" (
        "Name"	TEXT,
        PRIMARY KEY("Name")
    )
'''
insertEventsReference = '''
    INSERT INTO "_Events" ("Name") VALUES (?)'''
paramsEventsReference = [
    (None,),
    ("REMOVED",),
    ("Balor Invades",),
    ("Beastfelled",),
    ("Canada D'eh",),
    ("Fallen Heroes of Avalon",),
    ("Fool of April",),
    ("Legend of Lyonesse",),
    ("Menders of Hearts",),
    ("Merlin",),
    ("Nothren Legends: Ragnarok",),
    ("Of Giants and Titans",),
    ("Ornaversary",),
    ("Riftfall",),
    ("Paths of Fomoria: House of Autumna",),
    ("Paths of Fomoria: House of Nocturna",),
    ("Paths of Fomoria: House of Wintara",),
    ("Paths of Fomoria: House of Sumner",),
    ("Phoenixrise",),
    ("Stop Scruug!",),
    ("Summer Solstice",),
    ("Sumner Games",),
    ("Terra's Day",),
    ("Terra's Legacy",),
    ("The Cursed Queens",),
    ("The Crimson Festival",),
    ("The Hallowed",),
    ("The Mimics Are Loose",),
    ("The Mischievous Clurichauns",),
    ("The Plight of Apollyon",),
    ("The Winter Wild Hunts",),
    ("Thronemakers",),
    ("Winter Solstice",),
    ("Wyrmhunt",),
    ("Terra's Legacy: Natureblight",),
    ("Paths of Fomoria",)
]

createGuildsReference = '''
    CREATE TABLE "_Guilds" (
        "Name"	TEXT,
        PRIMARY KEY("Name")
    )
'''
insertGuildsReference = '''
    INSERT INTO "_Guilds" ("Name") VALUES (?)'''
paramsGuildsReference = [
    ("Traveler's Guild",),
    ("Angler's Guild",),
    ("Blades of Finesse",),
    ("Spelunking Guild",),
    ("Seer's Guild",),
    ("Conqueror's Guild",),
    ("Monumental Guild",),
    ("Circle of Anguish",),
    ("Titanfelled",)
]

createItemTypesReference = '''
    CREATE TABLE "_ItemTypes" (
        "Name"	TEXT,
        "Order"	INTEGER NOT NULL,
        PRIMARY KEY("Name")
    )
'''
insertItemTypesReference = '''
    INSERT INTO "_ItemTypes" ("Name", "Order") VALUES (?, ?) '''
paramsItemTypesReference = [
    ("Curatives",	 0),
    ("Items",	     1),
    ("Weapons",	     2),
    ("Head",	     3),
    ("Armor",	     4),
    ("Off-hand",	 5),
    ("Legs",	     6),
    ("Accessories",	 7),
    ("Amities",	     8),
    ("Materials",	 9),
    ("Adornments",	10),
    ("Currencies",	11),
    ("Fish",	    12),
    ("Other",	    13)
]

createQualitiesReference = '''
    CREATE TABLE "_Qualities" (
        "Name"	TEXT,
        "Order"	INTEGER NOT NULL,
        "PercentLow"	INTEGER,
        "PercentHigh"	INTEGER,
        PRIMARY KEY("Name")
    )
'''
insertQualitiesReference = '''
    INSERT INTO "_Qualities" ("Name", "Order", "PercentLow", "PercentHigh")
    VALUES (?, ?, ?, ?)'''
paramsQualitiesReference = [
    ("Broken",	     0,	  70,    90),
    ("Poor",	     1,	  90,    99),
    ("Standard",	 2,	 100,   100),
    ("Superior",	 3,	 110,   120),
    ("Famed",	     4,	 120,   130),
    ("Legendary",	 5,	 140,   170),
    ("Ornate",	     6,	 170,   200),
    ("Masterforged", 7,	None,  None),
    ("Demonforged",	 8,	None,  None)
]

createRaritiesReference = '''
    CREATE TABLE "_Rarities" (
        "Name"	TEXT,
        "Order"	INTEGER NOT NULL,
        PRIMARY KEY("Name")
    )
'''
insertRaritiesReference = '''
    INSERT INTO "_Rarities" ("Name", "Order") VALUES (?, ?)'''
paramsRaritiesReference = [
    ("Common",	    0),
    ("Superior",	1),
    ("Famed",	    2),
    ("Legendary",	3),
    ("Celestial",	4)
]

#******************#
#* Storage Tables *#
#******************#

createPlayerRecordData = '''
    CREATE TABLE "PlayerRecordData" (
        "Level"	INTEGER,
        "DateObtained"	TEXT NOT NULL,
        "TotalEXP"	INTEGER NOT NULL,
        "Playtime"	REAL,
        "GlobalRank"	INTEGER,
        "RegionalRank"	INTEGER,
        "CompetitiveRank"	INTEGER,
        "MonsterKills"	INTEGER,
        "BossKills"	INTEGER,
        "PlayerKills"	INTEGER,
        "QuestsCompleted"	INTEGER,
        "AreasExplored"	INTEGER,
        "AreasTaken"	INTEGER DEFAULT 286,
        "DungeonsCompleted"	INTEGER,
        "MonumentsCompleted"	INTEGER,
        "TowersCompleted"	INTEGER,
        "ColiseumsCompleted"	INTEGER,
        "ItemsUpgraded"	INTEGER,
        "FishCaught"	INTEGER,
        "DistanceTravelled"	INTEGER,
        "Reputation"	INTEGER,
        "Codex"	INTEGER,
        "Notes"	TEXT,
        PRIMARY KEY("Level")
    )
'''

createItemData = '''
    CREATE TABLE "ItemData" (
        "ID"	INTEGER,
        "Name"	TEXT NOT NULL,
        "Tier"	INTEGER NOT NULL,
        "Type"	TEXT NOT NULL,
        "Rarity"	TEXT NOT NULL,
        "IsEvent"	INTEGER,
        "IsRaidDrop"	INTEGER,
        "IsBossScaling"	INTEGER,
        "BSP"	REAL,
        "PSC"	INTEGER,
        "Filepath"	TEXT,
        "Base64"	TEXT,
        "Ignored"	INTEGER,
        "Removed"	INTEGER,
        PRIMARY KEY("ID"),
        FOREIGN KEY("Rarity") REFERENCES "_Rarities"("Name"),
        FOREIGN KEY("Type") REFERENCES "_ItemTypes"("Name")
    )
'''

createItemCollection = '''
    CREATE TABLE "ItemCollection" (
        "ID"	INTEGER,
        "Quantity"	INTEGER NOT NULL DEFAULT 0,
        PRIMARY KEY("ID"),
        FOREIGN KEY("ID") REFERENCES "ItemData"("ID")
    )
'''

createGuildData = '''
    CREATE TABLE "GuildData" (
        "PlayerLevel"	INTEGER,
        "Name"	TEXT,
        "Level"	INTEGER,
        "EXP"	INTEGER,
        PRIMARY KEY("PlayerLevel", "Name"),
        FOREIGN KEY("Name") REFERENCES "_Guilds" ("Name")
    )
'''

createEquipmentCollection = '''
    CREATE TABLE "EquipmentCollection" (
        "ID"	INTEGER,
        "QualityPercent"	INTEGER,
        "QualityName"	TEXT,
        "IsPerfect"	INTEGER,
        PRIMARY KEY("ID"),
        FOREIGN KEY("ID") REFERENCES "ItemData" ("ID")
        FOREIGN KEY("QualityName") REFERENCES "_Qualities" ("Name")
    )
'''

createCodexData = '''
    CREATE TABLE "CodexData" (
        "ID"	INTEGER,
        "Type"	TEXT NOT NULL,
        "Tier"	INTEGER NOT NULL,
        "Name"	TEXT NOT NULL,
        "Event"	TEXT,
        "Status"	TEXT NOT NULL,
        "Manifested"	INTEGER NOT NULL DEFAULT 0,
        "Kills"	INTEGER NOT NULL DEFAULT 0,
        "Filepath"	TEXT,
        PRIMARY KEY("ID"),
        FOREIGN KEY("Event") REFERENCES "_Events"("Name"),
        FOREIGN KEY("Status") REFERENCES "_CodexEntryStatus"("Name"),
        FOREIGN KEY("Type") REFERENCES "_CodexEntryType"("Name")
    )
'''


def main():
    database_name = "./DBManager/record_keeper.db"
    conn = sqlite3.connect(database_name)

    # Making of the Reference Tables
    query(conn, createCodexStatusTypeReference)
    query(conn, createCodexEntryTypeReference)
    query(conn, createEventsReference)
    query(conn, createGuildsReference)
    query(conn, createItemTypesReference)
    query(conn, createQualitiesReference)
    query(conn, createRaritiesReference)

    # Making of the Storage Tables
    query(conn, createItemData)             #? Arguably a Ref table, but not really
    query(conn, createItemCollection)       #? Relies on ItemData
    query(conn, createEquipmentCollection)  #? Relies on ItemData
    query(conn, createCodexData)
    query(conn, createPlayerRecordData)
    query(conn, createGuildData)
    
    # Filling of the Reference Tables
    for param in paramsCodexStatusTypeReference:
        query(conn, insertCodexStatusTypeReference, param)
    
    for param in paramsCodexEntryTypeReference:
        query(conn, insertCodexEntryTypeReference, param)
    
    for param in paramsEventsReference:
        query(conn, insertEventsReference, param)
    
    for param in paramsGuildsReference:
        query(conn, insertGuildsReference, param)
    
    for param in paramsItemTypesReference:
        query(conn, insertItemTypesReference, param)
    
    for param in paramsQualitiesReference:
        query(conn, insertQualitiesReference, param)
    
    for param in paramsRaritiesReference:
        query(conn, insertRaritiesReference, param)

if __name__ == '__main__':
    main()