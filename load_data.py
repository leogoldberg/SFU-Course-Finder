import csv
import MySQLdb
from config import config

mydb = MySQLdb.connect(host=config.host,
                       user=config.user,
                       passwd=config.password,
                       db=config.db)

cursor = mydb.cursor()
# remove table schedules if it already exists
cursor.execute("DROP TABLE schedules")

# create new table Schedules
cursor.execute(
    """CREATE TABLE schedules(
        room char(25),
        day char(20),
        start_time char(20),
        end_time char(20),
        course char(25),
        link char(120),
        PRIMARY KEY(room, course, start_time, end_time, day))""")

csv_data = csv.reader(open('room_info.csv'))

for row in csv_data:
    print(row)
    print(row[0])
    cursor.execute('INSERT INTO schedules(room, day, start_time, end_time, course, link )'
                   'VALUES("%s", "%s", "%s", "%s", "%s", "%s")',
                   row)

# remove all single quotes from data entries
cursor.execute("""UPDATE schedules SET room = TRIM(BOTH "'" FROM room),
                    day = TRIM(BOTH "'" FROM day),
                    start_time = TRIM(BOTH "'" FROM start_time),
                    end_time = TRIM(BOTH "'" FROM end_time),
                    course = TRIM(BOTH "'" FROM course),
                    link = TRIM(BOTH "'" FROM link)""")

# # close the connection to the database.
mydb.commit()
cursor.close()
print("Done")
