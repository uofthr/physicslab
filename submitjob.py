import sqlite3
conn = sqlite3.connect('jobs.db')
c = conn.cursor()
c.execute("DROP TABLE jobs")
c.execute('''CREATE TABLE jobs (id integer primary key autoincrement, date text, commandpre text, command text, comandpost text, commandpause text, host text, status int)''')
c.execute('''INSERT INTO jobs VALUES (NULL, '2016-12-03', 'who && touch /tmp/done.tag || touch /tmp/error.tag', 'uptime', 'last', 'killall rebound', NULL, 0)''')

for row in c.execute('SELECT * FROM jobs ORDER BY date'):
    print(row)
conn.commit()
conn.close()

