import sqlite3
import sys
import paramiko 
k = paramiko.RSAKey.from_private_key_file("/home/rein/.ssh/id_rsa")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
conn = sqlite3.connect('status.db')
c = conn.cursor()
c.execute("UPDATE status SET status=0 WHERE 1")
conn.commit()
conn.close()

for hostd in range(1,45):
    host = 'physics-lab%02d.utsc-labs.utoronto.ca'%hostd
    try:
        ssh.connect(host, timeout=3, username='research', pkey=k)
        command = "rm -f /tmp/*.tag"
        stdin , stdout, stderr = ssh.exec_command(command)
        sys.stdout.write('.')
        ssh.close()
    except:
        sys.stdout.write('x')
    sys.stdout.flush()

