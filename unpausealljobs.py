import paramiko
import sqlite3
import time
import sys
k = paramiko.RSAKey.from_private_key_file("/home/rein/.ssh/id_rsa")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

connj = sqlite3.connect("/home/rein/git/physicslab/jobs.db")
cj = connj.cursor()
conns = sqlite3.connect("/home/rein/git/physicslab/status.db")
cs = conns.cursor()
todo = cj.execute("SELECT id,host,command FROM jobs WHERE status==5").fetchall()
for pref in todo:
    sys.stdout.write('.')
    jobid, host,command = pref
    ssh.connect(host, timeout=3, username='research', pkey=k)
    stdin, stdout, stderr = ssh.exec_command(command)
    cs.execute("UPDATE status SET status=2 WHERE host='%s'"%(host))
    conns.commit()
    cj.execute("UPDATE jobs SET status=2 WHERE id=%d"%(jobid))
    connj.commit()

sys.stdout.write('\n')
