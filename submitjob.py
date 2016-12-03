import sqlite3
conn = sqlite3.connect('jobs.db')
c = conn.cursor()
c.execute("DROP TABLE jobs")
c.execute('''CREATE TABLE jobs (id integer primary key autoincrement, date text, commandpre text, command text, commandpost text, commandpause text, host text, status int)''')
c.execute('''INSERT INTO jobs VALUES (NULL, '2016-12-03', 'nohup sh -c "sleep 10 && touch /tmp/done.tag || touch /tmp/error.tag" > /dev/null &',  'nohup sh -c "sleep 10 && touch /tmp/done.tag || touch /tmp/error.tag" >/dev/null &', 'nohup sh -c "sleep 10 && touch /tmp/done.tag || touch /tmp/error.tag" >/dev/null &',  'killall rebound', NULL, 0)''')

for row in c.execute('SELECT * FROM jobs ORDER BY date'):
    print(row)
conn.commit()
conn.close()

