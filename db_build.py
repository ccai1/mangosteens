# creates tables for database stored in DB_FILE: smapify.db
# field names created; no records
import sqlite3   #enable control of an sqlite database

DB_FILE="smapify.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor()

def createTable(tableName, fieldNames):
	'''creates new table with list of parameters to be taken in'''
              #facilitate db ops
	commandArgs = "("
	colTypes = []
	for name in fieldNames:
		commandArgs += name + " " + fieldNames[name] + ","
		colTypes.append(fieldNames[name])
	commandArgs = commandArgs[:-1]
	commandArgs += ")"
	c.execute("CREATE TABLE " + tableName + " "+ commandArgs)

def closeDB():
	db.commit() #save changes
	db.close()  #close database

usersParam = {"UserID":"INTEGER PRIMARY KEY","Username":"TEXT UNIQUE","Password":"TEXT","Playlists":"TEXT"}
createTable("users", usersParam)

songsParam = {"SongID":"INTEGER PRIMARY KEY","SongTitle":"TEXT","Artist":"TEXT","Genre":"TEXT","Mood":"TEXT","Minutes":"INTEGER","Seconds":"INTEGER"}
createTable("songs", songsParam)

playlistParam = {"PlaylistID":"INTEGER PRIMARY KEY", "Songs":"TEXT"}
createTable("playlists", playlistParam)

closeDB()
