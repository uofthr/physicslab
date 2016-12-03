import paramiko
import sqlite3
import time
import sys
k = paramiko.RSAKey.from_private_key_file("/home/rein/.ssh/id_rsa")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

conn = sqlite3.connect("/home/rein/git/physicslab/status.db")
c = conn.cursor()
#c.execute('''CREATE TABLE status (date text, host text, isup int, status int, users int)''')
for hostd in range(1,45):
    sys.stdout.write('.')
    sys.stdout.flush()
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
    except Exception as e:
        isup = 0
        users = -1
    ssh.close()
    date = time.strftime("%Y-%m-%d %H:%M:%S")
    c.execute("UPDATE status SET date='%s', isup=%d, users=%d WHERE host='%s'" % (date,isup,users,host))

    #c.execute("INSERT INTO status VALUES ('"+date+"', '"+host+"', 0, 0, 0)")
sys.stdout.write('\n')
conn.commit()
conn.close()
