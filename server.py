import os
import html
import subprocess
from flask import Flask, request 
import math
import csv
import sqlite3

class FlaskApp(Flask):
    def __init__(self, *args, **kwargs):
        super(FlaskApp, self).__init__(*args, **kwargs)

app = FlaskApp(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    html = """
        <!doctype html>
        <title>Status</title>
        <h1>Machines</h1>
        <table border=1>
            <tr>
                <th>Host</th>
                <th>Up</th>
                <th>Status</th>
                <th>Users</th>
            </tr>
        """
    conn = sqlite3.connect('/home/rein/git/physicslab/status.db')
    c = conn.cursor()
    for row in c.execute('SELECT host, isup, status, users FROM status ORDER BY date'):
        html += "<tr>"
        for i,c in enumerate(row):
            if i==0:
                html += "<td>"+c+"</td>"
            elif i==1:
                if c==1:
                    html += "<td style='background-color: green;'>%d</td>"%c
                else:
                    html += "<td style='background-color: red;'>%d</td>"%c
            elif i==2:
                if c>0:
                    html += "<td style='background-color: orange;'>%d</td>"%c
                elif c==0:
                    html += "<td style='background-color: green;'>%d</td>"%c
                else:
                    html += "<td>%d</td>"%c
            elif i==3:
                if c>0:
                    html += "<td style='background-color: orange;'>%d</td>"%c
                elif c==0:
                    html += "<td style='background-color: green;'>%d</td>"%c
                else:
                    html += "<td>%d</td>"%c

        html += "</tr>"
    conn.commit()
    conn.close()
    html += """
        </table>
        <h1>Jobs</h1>
        <table border=1>
            <tr>
                <th>ID</th>
                <th>date</th>
                <th>command</th>
                <th>host</th>
                <th>status</th>
            </tr>
        """
    conn = sqlite3.connect('/home/rein/git/physicslab/jobs.db')
    c = conn.cursor()
    for row in c.execute('SELECT id, date,command,host,status FROM jobs ORDER BY date'):
        html += "<tr>"
        for i,c in enumerate(row):
            if i==0:
                html += "<td>%d</td>"%c
            if i==1:
                html += "<td>"+c+"</td>"
            elif i==2:
                html += "<td>"+c+"</td>"
            elif i==3:
                if c is not None:
                    html += "<td>"+c+"</td>"
                else:
                    html += "<td>-</td>"
            elif i==4:
                if c==0:
                    html += "<td style='background-color: orange;'>Waitingto start (%d)</td>"%c
                elif c==1:
                    html += "<td style='background-color: orange;'>Running preparation (%d)</td>"%c
                elif c==2:
                    html += "<td style='background-color: orange;'>Running (%d)</td>"%c
                elif c==3:
                    html += "<td style='background-color: orange;'>Running post (%d)</td>"%c
                elif c==4:
                    html += "<td style='background-color: green;'>Done (%d)</td>"%c
                elif c==5:
                    html += "<td style='background-color: orange;'>Paused (%d)</td>"%c
                else:
                    html += "<td style='background-color: red;'>%d</td>"%c
        html += "</tr>"
    html += """
        </table>
        """
    conn.commit()
    conn.close()

    return html
    sid = request.form['sid']
    try:
        sidi = int(sid)
    except:
        return '''
        <!doctype html>
        <title>No success</title>
        <h1>Student id invalid. Should be 10 digits. Please try again.</h1>
        '''
if __name__ == '__main__':
    app.run(debug=True,threaded=True)
