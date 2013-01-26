import subprocess
import config


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
