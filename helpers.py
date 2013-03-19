import config
import os
import subprocess


# SOME HELPER OBJECTS
class Dummy(object):
    def __init__(self, cursor, data=None, text=""):
        self.return_text = text

        self.headers = map(lambda x: x[0], cursor.description)

        if "class" in self.headers:
            self.headers[self.headers.index("class")] = "class_"

        self.data = cursor.fetchone() if not data else data
        result = dict(zip(self.headers, self.data)) if self.data else {}

        for k, v in result.items():
            setattr(self, k, v)

    def __getattr__(self,k):
        return self.return_text


def multi_dummy(cursor):
    result = []
    for row in cursor:
        result.append(Dummy(cursor, row))
    return result


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


# Yep, I like extremely long and descriptive names for
# functions and variables (if you didn't noticed yed) =)
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
