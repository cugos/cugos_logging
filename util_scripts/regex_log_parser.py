import string,glob,os,re
import psycopg2

# REFERENCE MATERIAL
'''
 Column  |          Type          |                         Modifiers                          
---------+------------------------+------------------------------------------------------------
 mid     | integer                | not null default nextval('log_messages_mid_seq'::regclass)
 channel | character varying(50)  | not null
 date    | date                   | not null
 time    | time without time zone | not null
 teller  | character varying(50)  | not null
 message | text                   | not null

query = "insert into log_messages(mid, channel, date, time, teller, message) values (nextval('log_messages_mid_seq'),'%s','%s','%s','%s',%s)    "%(channel,datenow,timenow,teller,escaped_msg)
'''

conn = psycopg2.connect("dbname=mr_cugos user=gcorradini host=localhost port=5432")
crs = conn.cursor()

def regexParse(strLine):
	dateRe = re.compile(r'^(?P<hour>[0-9]{2}):(?P<min>[0-9]{2}):(?P<sec>[0-9]{2})')
	tellRe = re.compile(r'(?P<teller>[<][0-9a-zA-Z]*[>])')
	messRe = re.compile(r'(?P<message>[>].*$)')
	returnList = []
	try: 
		returnList.append(string.join(dateRe.findall(strLine)[0],":"))
		returnList.append(string.replace(string.replace(string.strip(tellRe.findall(strLine)[0]),"<",""),">",""))
		returnList.append(string.replace(string.strip(string.replace(messRe.findall(strLine)[0],">","")),"\x01",""))
	except:
		returnList.append('')
	return returnList


def regexDate(strDate):
	dateRe = re.compile(r'(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2})')
	return string.join(dateRe.findall(strDate)[0], "-")

def insertRecords(listTuples):
	for record in listTuples:
		print record
		query = "insert into log_messages(mid, channel, date, time, teller, message) values (nextval('log_messages_mid_seq'),'%s','%s','%s','%s',%s)    "%record
		crs.execute(query)


if __name__ == '__main__':
	logs = glob.glob("/var/www/irc_logs/parsing/*.log")
	dbrecords  = []
	for log in logs:
		reader = open(log,"r")
		nsplits = [i for i in string.split(reader.read(),"\n")]
		# pop the last NULL record
		nsplits.pop()
		# get the date from the first record and then remove it
		date = nsplits[0]
		nsplits.remove(nsplits[0])
		date = regexDate(date)
		for line in nsplits:
			newline = regexParse(line)
			if '' in newline: continue
			# construct record
			newline.insert(0,date)
			newline.insert(0,'cugos')
			# escape the message values
			newline[len(newline)-1] = psycopg2.extensions.adapt(newline[len(newline)-1].strip())
			dbrecords.append(tuple(newline))	

	
	insertRecords(dbrecords)	
	conn.commit()
	del crs
	del conn
