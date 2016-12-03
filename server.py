import os
import html
import subprocess
from flask import Flask, request 
import math

class FlaskApp(Flask):
    def __init__(self, *args, **kwargs):
        super(FlaskApp, self).__init__(*args, **kwargs)

app = FlaskApp(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    return '''
    <!doctype html>
    <title>No success</title>
    <h1>Student id invalid. Should be 10 digits. Please try again.</h1>
    '''
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
