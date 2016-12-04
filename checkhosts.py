import paramiko
import sqlite3
import time
import sys
k = paramiko.RSAKey.from_private_key_file("/home/rein/.ssh/id_rsa")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    conn = sqlite3.connect("/home/rein/git/physicslab/status.db")
    c = conn.cursor()
    c.execute('''SELECT * FROM status WHERE 1 LIMIT 1''')
except:
    print("Creating new DB")
    conn = sqlite3.connect("/home/rein/git/physicslab/status.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE status (date text, host text, isup int, status int, users int, usage real)''')
for hostd in range(1,45):
    host = 'physics-lab%02d.utsc-labs.utoronto.ca'%hostd
    try:
        ssh.connect(host, timeout=3, username='research', pkey=k)
        isup = 1
        try:
            pass
        except:
            users = -1
        command = "/usr/bin/who | /usr/bin/wc -l | xargs"
        stdin , stdout, stderr = ssh.exec_command(command)
        users = int(stdout.read().decode('ascii').strip())
        command = "top | head -n 4 |tail -n 1|cut -d' ' -f3|cut -d'%' -f1"
        stdin , stdout, stderr = ssh.exec_command(command)
        usage = float(stdout.read().decode('ascii').strip())
        sys.stdout.write('.')
    except Exception as e:
        isup = 0
        users = -1
        usage = 0.
        sys.stdout.write('x')
    sys.stdout.flush()
    ssh.close()
    date = time.strftime("%Y-%m-%d %H:%M:%S")

    isin = c.execute("SELECT * FROM status WHERE host='%s' LIMIT 1"%host).fetchone()
    if not isin:
        c.execute("INSERT INTO status VALUES ('','%s',0,0,0,0)"%host)
    c.execute("UPDATE status SET date='%s', isup=%d, users=%d, usage=%f WHERE host='%s'" % (date,isup,users,usage,host))

    #c.execute("INSERT INTO status VALUES ('"+date+"', '"+host+"', 0, 0, 0)")
sys.stdout.write('\n')
conn.commit()
conn.close()
