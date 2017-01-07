import flask, subprocess, time, os, sys
from flask import request, Response
from ansi2html import Ansi2HTMLConverter

app = flask.Flask(__name__)

@app.route('/')
def index():
    def runit():
        conv = Ansi2HTMLConverter()
        PlayBook = './myplaybook.yml'
        cmd = '/bin/ansible-playbook --check ' + PlayBook
        p = subprocess.Popen([cmd],
                             shell = True,
                             stdout = subprocess.PIPE,
                             universal_newlines = True)
        for line in iter(p.stdout.readline,''):
            yield conv.convert(line.rstrip())
        p.communicate()
        exit_code = p.wait()
        yield 'rc = ' + str(exit_code)
    return Response(runit(), mimetype='text/html')
app.run(debug=True, port=5000, host='0.0.0.0')


