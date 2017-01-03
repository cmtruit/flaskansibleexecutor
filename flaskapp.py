import flask
import subprocess
import time
import os
import sys
#from tempfile import NamedTemporaryFile
from ansible.inventory import Inventory
from ansible.vars import VariableManager
from ansible.parsing.dataloader import DataLoader
from ansible.utils.display import Display
from collections import namedtuple
from ansible.executor.playbook_executor import PlaybookExecutor
from cStringIO import StringIO
from ansi2html import Ansi2HTMLConverter

app = flask.Flask(__name__)

@app.route('/')
def index():
  def runit():
     variable_manager = VariableManager()
     loader = DataLoader()
     inventory = Inventory(loader=loader, 
                           variable_manager=variable_manager,  
                           host_list='/home/myhostlist'
                          )

     playbook_path = './myplaybook.yml'

     if not os.path.exists(playbook_path):
         print '[INFO] The playbook does not exist'
         sys.exit()

     Options = namedtuple('Options', ['listtags', 
                                      'listtasks', 
                                      'listhosts', 
                                      'syntax', 
                                      'connection', 
                                      'module_path', 
                                      'forks', 
                                      'remote_user', 
                                      'private_key_file', 
                                      'ssh_common_args', 
                                      'ssh_extra_args', 
                                      'sftp_extra_args', 
                                      'scp_extra_args', 
                                      'become', 
                                      'become_method', 
                                      'become_user', 
                                      'verbosity', 
                                      'check'])

     options = Options(listtags=False, 
                       listtasks=False, 
                       listhosts=False, 
                       syntax=False, 
                       connection='ssh',
                       module_path=None, 
                       forks=100, 
                       remote_user='slotlocker', 
                       private_key_file=None, 
                       ssh_common_args=None, 
                       ssh_extra_args=None, 
                       sftp_extra_args=None, 
                       scp_extra_args=None, 
                       become=True, 
                       become_method=None, 
                       become_user='root', 
                       verbosity=1, 
                       check=False)

     passwords = {}
     conv = Ansi2HTMLConverter() 
     old_stdout = sys.stdout
     sys.stdout = mystdout = StringIO()
     mystdout.reset()
     PlaybookExecutor(playbooks=[playbook_path], 
                      inventory=inventory, 
                      variable_manager=variable_manager,  
                      loader=loader, 
                      options=options,  
                      passwords=passwords).run()
     sys.stdout = old_stdout 
     mystdout.seek(0)
     if  mystdout.readline():
       for line in mystdout: 
         yield conv.convert(line.rstrip())
     mystdout.close()
  return flask.Response(runit(), mimetype='text/html')  

app.run(debug=True, port=5000, host='0.0.0.0')
