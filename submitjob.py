import sqlite3
conn = sqlite3.connect('jobs.db',timeout=3)
c = conn.cursor()
#c.execute("DROP TABLE jobs")
#c.execute('''CREATE TABLE jobs (id integer primary key autoincrement, name text, date text, commandpre text, command text, filecopypost text, commandpost text, commandpause text, host text, status int)''')

commit          = "6b75261"
name            = commit
filecopypost    = "/tmp/rebound/problems/ss_lab1/run1_*.bin"
commandpre      = "bash <(curl -s 'https://raw.githubusercontent.com/uofthr/ss_lab1/%s/pre.bash') "%commit
command         = "nohup sh -c '/tmp/rebound/problems/ss_lab1/run.bash' </dev/null >/dev/null 2>/dev/null &"
commandpost     = "rm -rf /tmp/rebound"
#commandpost     = "uptime"
commandpause    = "killall rebound"

for i in range(44):
    c.execute('INSERT INTO jobs VALUES (NULL, "%s", "2016-12-03", "%s", "%s", "%s", "%s", "%s", NULL, 0)'%(name,commandpre,command,filecopypost,commandpost,commandpause))

for row in c.execute('SELECT * FROM jobs ORDER BY date'):
    print(row)
conn.commit()
conn.close()

