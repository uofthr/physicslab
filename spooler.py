import subprocess
import os
import sqlite3
import time
import sys

connj = sqlite3.connect("/home/rein/git/physicslab/jobs.db", timeout=10)
conns = sqlite3.connect("/home/rein/git/physicslab/status.db", timeout=10)
cj = connj.cursor()
cs = conns.cursor()
while 1:
    # command in queue
    todo = cj.execute("SELECT id,commandpre,command FROM jobs WHERE status==0").fetchone()
    if todo:
        freehost = cs.execute("SELECT host FROM status WHERE isup=1 AND status=0 LIMIT 1").fetchone()
        if freehost:
            jobid, commandpre, command = todo
            print("exex pre: "+commandpre)
            host = freehost[0]
            
            ret = os.popen("ssh research@%s 'rm /tmp/done.tag'"%host).read()

            cs.execute("UPDATE status SET status=1 WHERE host='%s'"%(host))
            conns.commit()
            cj.execute("UPDATE jobs SET host='%s', status=1 WHERE id=%d"%(host,jobid))
            connj.commit()
            
            ret = os.popen("ssh research@%s \"%s\""%(host,commandpre)).read()

            cs.execute("UPDATE status SET status=2 WHERE host='%s'"%(host))
            conns.commit()
            cj.execute("UPDATE jobs SET status=2 WHERE id=%d"%(jobid))
            connj.commit()
            
            ret = os.popen("ssh research@%s \"%s\""%(host,command))

    
    # command waiting for main command to finish
    todo = cj.execute("SELECT name,id,host,filecopypost, commandpost FROM jobs WHERE status==2").fetchall()
    for pref in todo:
        name, jobid, host,filecopypost,commandpost = pref
        ret = subprocess.call("ssh research@%s 'ls /tmp/done.tag &>/dev/null'"%host, shell=True)
        if ret==0:
            ret = os.popen("ssh research@%s 'rm -f /tmp/*.tag'"%host).read()
            
            print("copy post")
            
            cs.execute("UPDATE status SET status=3 WHERE host='%s'"%(host))
            conns.commit()
            cj.execute("UPDATE jobs SET status=3 WHERE id=%d"%(jobid))
            connj.commit()

            localfile="/data0/rein/physicslab/"+name+"%09d"%jobid
            ret = os.popen("mkdir "+localfile).read()
            ret = os.popen("scp research@%s:'%s' %s/"%(host,filecopypost,localfile)).read()

            cs.execute("UPDATE status SET status=4 WHERE host='%s'"%(host))
            conns.commit()
            cj.execute("UPDATE jobs SET status=4 WHERE id=%d"%(jobid))
            connj.commit()
            
            print("exec post")
            ret = os.popen("ssh research@%s \"%s\""%(host,commandpost)).read()
            
    
            print("all done")

            cs.execute("UPDATE status SET status=0 WHERE host='%s'"%(host))
            conns.commit()
            cj.execute("UPDATE jobs SET status=5 WHERE id=%d"%(jobid))
            connj.commit()
    time.sleep(1.)
sys.stdout.write('\n')
