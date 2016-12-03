import paramiko
import sqlite3
import time
import sys
k = paramiko.RSAKey.from_private_key_file("/home/rein/.ssh/id_rsa")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

connj = sqlite3.connect("/home/rein/git/physicslab/jobs.db")
conns = sqlite3.connect("/home/rein/git/physicslab/status.db")
cj = connj.cursor()
cs = conns.cursor()
while 1:
    todo = cj.execute("SELECT id,commandpre FROM jobs WHERE status==0").fetchone()
    if todo:
        freehost = cs.execute("SELECT host FROM status WHERE isup=1 AND status=0 LIMIT 1").fetchone()
        if freehost:
            host = freehost[0]
            cs.execute("UPDATE status SET status=1 WHERE host='%s'"%(host))
            conns.commit()
            cj.execute("UPDATE jobs SET host='%s', status=1 WHERE id=%d"%(host,todo[0]))
            connj.commit()
            ssh.connect(host, timeout=3, username='research', pkey=k)
            command = "/usr/bin/who | /usr/bin/wc -l | xargs"
            stdin , stdout, stderr = ssh.exec_command(todo[1])
            print(stdout.read())
            print(stderr.read())
    time.sleep(1)

    #sys.stdout.write('.')
    #sys.stdout.flush()
    #try:
    #    users = int(stdout.read().decode('ascii').strip())
    #except Exception as e:
    #    isup = 0
    #    users = -1
    #ssh.close()
    #date = time.strftime("%Y-%m-%d %H:%M:%S")
    #c.execute("UPDATE status SET date='%s', isup=%d, users=%d WHERE host='%s'" % (date,isup,users,host))

    #c.execute("INSERT INTO status VALUES ('"+date+"', '"+host+"', 0, 0, 0)")
sys.stdout.write('\n')
