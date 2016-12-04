import sqlite3
conn = sqlite3.connect('jobs.db')
c = conn.cursor()
c.execute("DROP TABLE jobs")
c.execute('''CREATE TABLE jobs (id integer primary key autoincrement, name text, date text, commandpre text, command text, filecopypost text, commandpost text, commandpause text, host text, status int)''')

name            = "run1"
filecopypost    = "/tmp/rebound/problems/ss_lab1/restart_0051_col.bin"
commandpre      = "bash <(curl -H 'Cache-Control: no-cache' -s https://raw.githubusercontent.com/uofthr/ss_lab1/master/pre.bash?a"
command         = "cd /tmp/rebound/problems/ss_lab1 && rebound && touch /tmp/done.tag || touch /tmp/error.tag"
commandpost     = "rm -f /tmp/rebound"
commandpause    = "killall rebound"

c.execute('INSERT INTO jobs VALUES (NULL, '2016-12-03', "%s", "%s", "%s", "%s", NULL, 0)'%(commandpre,command,commandpost,commandpause))

for row in c.execute('SELECT * FROM jobs ORDER BY date'):
    print(row)
conn.commit()
conn.close()

