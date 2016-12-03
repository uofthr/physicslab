import paramiko
import csv
import sys
k = paramiko.RSAKey.from_private_key_file("/home/rein/.ssh/id_rsa")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

with open("status.csv", "w") as csvfile:
    writer = csv.writer(csvfile)
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
            users = stdout.read().decode('ascii').strip()
        except Exception as e:
            isup = 0
            users = -1
        ssh.close()
        writer.writerow([host,isup,users]) 
    sys.stdout.write('\n')
