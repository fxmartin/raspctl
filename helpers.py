import config
import os
import re
import stat
import storage
import subprocess
import uuid

class Dummy(object):
    def __init__(self, data, text=""):
        self.data = data
        self.text = text

        for k, v in data.items():
            setattr(self, k, v)

    def __getitem__(self, k):
        return self.data[k]

    def __getattr__(self, k):
        return self.text

    def __str__(self):
        return str(self.data)

def check_program_is_installed(prg_name):
    return subprocess.call("which %s" % prg_name, shell=True) == 0


def current_tab(tab_name):
    setattr(config, "CURRENT_TAB", tab_name)

def is_tab_active(tabname):
    return 'active' if config.CURRENT_TAB == tabname else ''

class player():
    @staticmethod
    def is_installed():
        return check_program_is_installed('mpd') and check_program_is_installed('mpc')

    @staticmethod
    def play(song):
        _execute("mpc clear")
        _execute("mpc add %s" % song)
        _execute("mpc play 1")

    @staticmethod
    def stop():
        _execute("mpc clear")

    @staticmethod
    def volume(volume):
        _execute("mpc volume %s" % volume)

def execute_command(class_, action, extra_params):
    if config.COMMAND_EXECUTION == False:
        return "The command execution is NOT available."

    command = filter(lambda x: x['class_'] == class_ and
                               x['action'] == action,
                     storage.read('commands'))
    if not command:
        return "Command not found"

    command = command[0]

    for key, value in extra_params.items():
        command['command'] = command['command'].replace("$%s" % key, value)

    subprocess.call(command['command'], shell=True)
    return "Executing: %s" % command

def _execute(cmd):
    try:
        output = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()
        return output[0]
    except OSError:
        return ""

# Yep, I like extremely long and descriptive names for
# functions and variables (if you haven't noticed it yet) =)
def execute_system_information_script():
    # Ok, let's explain this a little bit. The script system_info.sh gets information
    # about the system and throw the results to the STDOUT with a key-value format.
    # From here we execute the mentioned script and load it in Python Dictionary
    # dinamically, so, the names you use in the script for identifying a information
    # will be the same in the Python code. Please take a look to the comments of the
    # mentioned file for further information.
    result = _execute(os.getcwd() + "/scripts/system_info.sh")
    info = {}
    for line in result.split('\n'):
        try:
            constant, value = line.split(':', 1)
            info[constant] = value
        except ValueError:
            pass
    return info

class session():
    @staticmethod
    def create():
        session_id = uuid.uuid4().hex

        filepath = config.PATH_SESSION + session_id

        fd = os.open(filepath, os.O_CREAT, int("0400", 8))
        # XXX If I have a file descriptor without execute fdopen
        # is there something I need to close? :/
        f = os.fdopen(fd)
        f.close()

        return session_id

    @staticmethod
    def _check_permissions(file_path):
        try:
            st = os.stat(file_path)
        except OSError:
            return False
        filemode = stat.S_IMODE(st.st_mode)
        just_user_readable_permissions = filemode == int("0400", 8)
        same_username_that_executing_the_app = st.st_uid == os.getuid()
        return same_username_that_executing_the_app and just_user_readable_permissions

    @staticmethod
    def is_logged(session_id):
        if not session_id: return False

        file_path = config.PATH_SESSION + session_id
        return session._check_permissions(file_path)

    @staticmethod
    def logout(session_id):
        # The session id must have 32 chars - uuid4.
        # The session don't should have 'funny characters' because
        # we are using os.remove and an unauthenticated person could
        # potentially remove a file in the FS
        if not re.match('^[0-9a-f]{32}$', session_id):
            return
        try:
            os.remove(config.PATH_SESSION + session_id)
        except:
            pass
