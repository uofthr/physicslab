import paramiko
import sqlite3
import time
import sys
k = paramiko.RSAKey.from_private_key_file("/home/rein/.ssh/id_rsa")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

connj = sqlite3.connect("/home/rein/git/physicslab/jobs.db", timeout=10)
conns = sqlite3.connect("/home/rein/git/physicslab/status.db", timeout=10)
cj = connj.cursor()
cs = conns.cursor()
while 1:
    # command in queue
    todo = cj.execute("SELECT id,commandpre FROM jobs WHERE status==0").fetchone()
    if todo:
        freehost = cs.execute("SELECT host FROM status WHERE isup=1 AND status=0 LIMIT 1").fetchone()
        if freehost:
            jobid, commandpre = todo
            print("exex pre: "+commandpre)
            host = freehost[0]
            cs.execute("UPDATE status SET status=1 WHERE host='%s'"%(host))
            conns.commit()
            cj.execute("UPDATE jobs SET host='%s', status=1 WHERE id=%d"%(host,jobid))
            connj.commit()
            ssh.connect(host, timeout=3, username='research', pkey=k)
            stdin , stdout, stderr = ssh.exec_command(commandpre)
            out = stdout.read()
            #print(out)
            #out = stderr.read()
            #print(out)
            ssh.close()
    time.sleep(1)
    # command waiting for pre to finish
    todo = cj.execute("SELECT id,host,command FROM jobs WHERE status==1").fetchall()
    for pref in todo:
        jobid, host,command = pref
        ssh.connect(host, timeout=3, username='research', pkey=k)
        stdin, stdout, stderr = ssh.exec_command("ls /tmp/done.tag >/dev/null")
        if len(stderr.read())>0:
            done = 0
        else:
            print("exex: "+command)
            done = 1
            stdin, stdout, stderr = ssh.exec_command("rm /tmp/done.tag")
            out = stdout.read()
            cs.execute("UPDATE status SET status=2 WHERE host='%s'"%(host))
            conns.commit()
            cj.execute("UPDATE jobs SET status=2 WHERE id=%d"%(jobid))
            connj.commit()
            stdin, stdout, stderr = ssh.exec_command(command)
            out = stdout.read()
        ssh.close()
    
    # command waiting for main command to finish
    todo = cj.execute("SELECT name,id,host,filecopypost, commandpost FROM jobs WHERE status==2").fetchall()
    for pref in todo:
        name, jobid, host,filecopypost,commandpost = pref
        ssh.connect(host, timeout=3, username='research', pkey=k)
        stdin, stdout, stderr = ssh.exec_command("ls /tmp/done.tag >/dev/null")
        if len(stderr.read())>0:
            done = 0
        else:
            done = 1
            stdin, stdout, stderr = ssh.exec_command("rm /tmp/done.tag")
            out = stdout.read()
            
            print("copy post")
            sftp = ssh.open_sftp()
            localfile="/data0/rein/physicslab/"+name+"_%09d.bin"%jobid
            sftp.get(filecopypost, localfile)
            sftp.close()


            print("exec post")
            cs.execute("UPDATE status SET status=3 WHERE host='%s'"%(host))
            conns.commit()
            cj.execute("UPDATE jobs SET status=3 WHERE id=%d"%(jobid))
            connj.commit()
            stdin, stdout, stderr = ssh.exec_command(commandpost)
            out = stdout.read()
        ssh.close()
    
    # command waiting for post command to finish
    todo = cj.execute("SELECT id,host FROM jobs WHERE status==3").fetchall()
    for pref in todo:
        jobid, host = pref
        ssh.connect(host, timeout=3, username='research', pkey=k)
        stdin, stdout, stderr = ssh.exec_command("ls /tmp/done.tag >/dev/null")
        if len(stderr.read())>0:
            done = 0
        else:
            done = 1
            print("all done")
            stdin, stdout, stderr = ssh.exec_command("rm /tmp/done.tag")
            out = stdout.read()
            cs.execute("UPDATE status SET status=0 WHERE host='%s'"%(host))
            conns.commit()
            cj.execute("UPDATE jobs SET status=4 WHERE id=%d"%(jobid))
            connj.commit()
        ssh.close()

sys.stdout.write('\n')
