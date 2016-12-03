import os
import html
import subprocess
from flask import Flask, request 
import math
import csv

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
        <h1>Status</h1>
        <table border=1>
            <tr>
                <th>Host</th>
                <th>Up</th>
                <th>Users</th>
            </tr>
        """
    with open("/home/rein/git/physicslab/status.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        for r in reader:
            html += "<tr>"
            for i,c in enumerate(r):
                if i==1:
                    if c=="1":
                        html += "<td style='background-color: green;'>"+c+"</td>"
                    else:
                        html += "<td style='background-color: red;'>"+c+"</td>"
                elif i==2:
                    if int(c)>0:
                        html += "<td style='background-color: orange;'>"+c+"</td>"
                    elif int(c)==0:
                        html += "<td style='background-color: green;'>"+c+"</td>"
                    else:
                        html += "<td>"+c+"</td>"

                else:
                    html += "<td>"+c+"</td>"
            html += "</tr>"
    html += """
        </table>
        """
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
