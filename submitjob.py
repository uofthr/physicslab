import sqlite3
conn = sqlite3.connect('jobs.db',timeout=3)
c = conn.cursor()
#c.execute("DROP TABLE jobs")
#c.execute('''CREATE TABLE jobs (id integer primary key autoincrement, name text, date text, commandpre text, command text, filecopypost text, commandpost text, commandpause text, host text, status int)''')

name            = "run2"
filecopypost    = "/tmp/rebound/problems/ss_lab1/restart_0051_col.bin"
commandpre      = "bash <(curl -s 'https://raw.githubusercontent.com/uofthr/ss_lab1/7e82b4f/pre.bash') "
command         = "nohup sh -c 'cd /tmp/rebound/problems/ss_lab1 && ./rebound && touch /tmp/done.tag || touch /tmp/error.tag' &"
commandpost     = "nohup sh -c 'rm -rf /tmp/rebound && touch /tmp/done.tag || touch /tmp/error.tag' &"
commandpause    = "killall rebound"

c.execute('INSERT INTO jobs VALUES (NULL, "%s", "2016-12-03", "%s", "%s", "%s", "%s", "%s", NULL, 0)'%(name,commandpre,command,filecopypost,commandpost,commandpause))

for row in c.execute('SELECT * FROM jobs ORDER BY date'):
    print(row)
conn.commit()
conn.close()

