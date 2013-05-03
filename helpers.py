import config
import os
import storage
import subprocess


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

def compose_command(command, value, extra):
    try:
        extra = json.loads(extra)
    except:
        extra = {"extra_parameters":{}}

    params = extra.get('extra_parameters', [])

    for param, default_value in params.items():
        v_param = "$" + param.upper()
        if default_value == None:
            default_value = ""

        command = command.replace(v_param, request.params.get(param.lower(), default_value))

    return command

def execute_command(class_, action):
    if config.COMMAND_EXECUTION == False:
        return "The command execution is NOT available."

    # XXX TODO FIXME: Add support for passing parameters to the commands
    #command = helpers.compose_command(result[COMMAND], value, result[EXTRA])

    command = filter(lambda x: x['class_'] == class_ and
                               x['action'] == action,
                     storage.read('commands'))
    if not command:
        return "Command not found"

    command = command[0]

    subprocess.call(command['command'], shell=True)
    return "Executing: %s" % command


def check_program_is_installed(prg_name):
    return subprocess.call("which %s" % prg_name, shell=True) == 0


def current_tab(tab_name):
    setattr(config, "CURRENT_TAB", tab_name)


def _execute(cmd):
    try:
        output = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()
        return output[0]
    except OSError:
        return ""

class Player():
    def is_installed(self):
        return check_program_is_installed('mpd') and check_program_is_installed('mpc')

    def play(self, song):
        _execute("mpc clear")
        _execute("mpc add " + song)
        _execute("mpc play 1")

    def stop(self):
        _execute("mpc clear")

    def volume(self, volume):
        _execute("mpc volume " + volume)

player = Player()


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

def is_tab_active(tabname):
    return 'active' if config.CURRENT_TAB == tabname else ''
