#!/usr/bin/env python

from alarm import alarms
from bottle import route, run, template, request, static_file, redirect, post, get
import config
import datetime
import helpers
import storage
import subprocess
import time

config.load_config()

# STATIC ROUTES
@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=config.ROOT+"/static")  # Maybe os.path.join()?

@route('/favicon.ico')
def get_favicon():
    return static_file('favicon.ico', root=config.ROOT+"/static/img")

## HTTP HANDLERS
@route('/execute')
def execute():
    params = dict(request.params)
    try:
        _class = params.pop('class')
        action = params.pop('action')
    except KeyError:
        return "Invalid request. 'class' and 'action' parameters must be present."

    extra_params = params
    return helpers.execute_command(_class, action, extra_params)

@route('/commands')
def commands():
    helpers.current_tab("commands")
    rows = map(helpers.Dummy, storage.read('commands'))
    return template('commands', rows=rows)

@route('/command/edit/:id_')
def command_edit(id_=None):
    id_ = "" if id_ == "new" else int(id_)

    data = helpers.Dummy(storage.get_by_id('commands', id_))

    return template('edit', data=data)

@post('/command/save')
def command_save():
    id_ = request.POST.get('id')
    class_ = request.POST.get('class')
    action = request.POST.get('action')
    command = request.POST.get('command', '')

    if not class_ or not action:
        return "Invalid data. CLASS and ACTION are required fields."

    if id_:
        new_command = {"id_": int(id_), "class_": class_, "action": action, "command": command}
        commands = storage.replace('commands', new_command)
        storage.save_table('commands', commands)
    else:
        data = storage.read()
        ids = map(lambda x: x['id_'], data['commands'])
        id_ = max(ids)+1 if ids else 1

        new_command = {"id_": int(id_), "class_": class_, "action": action, "command": command}
        data['commands'].append(new_command)
        storage.save(data)

    redirect("/command/edit/%s" % id_)

@route('/command/delete/:id_')
def command_delete(id_=None):
    storage.delete('commands', int(id_))
    return "ok"

@route('/config')
def config_edit(config_saved=False):
    helpers.current_tab("config")
    return template('config', config=config, config_saved=config_saved)

@post('/save_configuration')
def config_save():
    def bool_eval(name):
        return request.POST.get(name) == "True"
    def int_default(name, default):
        try:
            n = int(request.POST.get(name))
            return n if n > 1024 else default
        except:
            return default

    conf = {
        'SHOW_DETAILED_INFO': bool_eval('SHOW_DETAILED_INFO'),
        'SHOW_TODO': bool_eval('SHOW_TODO'),
        'COMMAND_EXECUTION': bool_eval('COMMAND_EXECUTION'),
        'SERVICE_EXECUTION': bool_eval('SERVICE_EXECUTION'),
        'PORT': int_default('PORT', 8086),
    }

    config.save_configuration(conf)
    return config_edit(config_saved=True)

@route('/webcam')
def webcam():
    helpers.current_tab("webcam")
    fswebcam_is_installed = helpers.check_program_is_installed("fswebcam")
    return template('webcam', fswebcam_is_installed=fswebcam_is_installed)

@get('/take_picture')
def take_picture():
    if not helpers.check_program_is_installed("fswebcam"):
        return "Is seems you don't have fswebcam installed in your system. Install it using apt-get or aptitude and add your user to VIDEO group."

    command = "fswebcam -r 640x480 -S 3 %s/static/img/webcam_last.jpg" % config.ROOT
    subprocess.call(command, shell=True)
    return "done"

@get('/services')
def services():
    filter_favorites = request.params.get('filter_favorites') == "true"
    helpers.current_tab("services")
    if config.SERVICE_EXECUTION:
        services = helpers._execute("ls /etc/init.d/")
        services = filter(bool, services.split('\n'))
        favorite_services = config.SERVICES_FAVORITES
        if filter_favorites:
            services = favorite_services
    else:
        services, favorite_services = [], []
    return template('services', services=services, favorite_services=favorite_services,
                                filter_favorites=filter_favorites)

def _service_favorite(name):
    # Just mark a service (daemon) as favorite
    if name in config.SERVICES_FAVORITES:
        config.SERVICES_FAVORITES.remove(name)
    else:
        config.SERVICES_FAVORITES.append(name)
    new_config = {"SERVICES_FAVORITES": config.SERVICES_FAVORITES}

    config.save_configuration(new_config)
    return "Toggled favorite"

@get('/service/:name/:action')
def service_action(name=None, action=None):

    if action == "favorite":
        return _service_favorite(name)

    if action not in config.SERVICE_VALID_ACTIONS:
        return "Error! Invalid action!"

    if name not in helpers._execute("ls /etc/init.d/"):
        return "Error! Service not found!"

    result = helpers._execute("sudo %s/scripts/exec.sh service %s %s" % (config.ROOT, name, action))
    return result if result else "No information returned"

@get('/about')
def about():
    helpers.current_tab("about")
    return template('about')

@get('/system_info')
def system_info():
    def celsius_to_fahrenheit(cel):
        if not cel: return ""
        return cel * 9 / 5 + 32

    system_info = helpers.execute_system_information_script()

    temp = {}
    if system_info['TEMPERATURE']:
        temp['c'] = float(system_info['TEMPERATURE'])
        temp['f'] = celsius_to_fahrenheit(temp['c'])

    return template("system_info", info=system_info, temp=temp)

@get('/radio')
def radio(successfully_saved=False):
    if not helpers.player.is_installed():
        return template("radio-instructions")

    radios = sorted(storage.read('radio').items())
    helpers.current_tab("radio")
    return template("radio", radios=radios, successfully_saved=successfully_saved)

@get('/radio/install')
def radio_install():
    return template("radio-instructions")

@get('/radio/play')
def radio_play():
    helpers.player.play(request.GET.get('stream'))

@get('/radio/stop')
def radio_stop():
    helpers.player.stop()

@get('/radio/volume/:volume')
def radio_volume(volume=100):
    helpers.player.volume(volume)

@post('/radio/save')
def radio_save():
    radios = {}
    post = dict(request.POST)
    for key in post:
        name, value = key.split('_')
        if name != "name": continue
        radio_name = post.get('name_' + value)
        radio_stream = post.get('stream_' + value)
        if radio_name == "" or radio_stream == "": continue
        radios[radio_name] = radio_stream
    storage.save_table('radio', radios)
    return radio(successfully_saved=True)

@get('/alarm')
def alarm():
    helpers.current_tab('alarm')
    return template("alarms")

@get('/alarm/command')
def alarm_command():
    return template('alarms-command')

@get('/alarm/radio')
def alarm_radio():
    alarms = map(helpers.Dummy, storage.read('alarms'))
    return template('alarms-radio', alarms=alarms)

@get('/alarm/edit/:id')
def alarm_edit(id=None):
    id = "" if id == "new" else int(id)
    alarm = helpers.Dummy(storage.get_by_id('alarms', id))
    radios = sorted(storage.read('radio').items())
    return template('alarms-radio-edit', radios=radios, alarm=alarm)

@post('/alarm/save')
def alarm_save():
    fields = ['id_', 'name', 'volume', 'stream', 'action']
    data = dict([ (k, request.POST.get(k)) for k in fields  ])
    data['volume'] = int(data['volume'])

    try:
        date = request.POST.get('date')
        hour = request.POST.get('hour')
        data['at'] = time.mktime(time.strptime("%s %s" % (date, hour),
                                               "%Y-%m-%d %H:%M:%S"))
        dt = datetime.datetime.fromtimestamp(data['at'])
        data['date'] = dt.strftime('%Y-%m-%d')
        data['hour'] = dt.strftime('%H:%M:%S')
    except:
        return "Problem with the date... Chek it, please"

    if data['id_']:
        data['id_'] = int(data['id_'])
        alarms_data = storage.replace('alarms', data)
        storage.save_table('alarms', alarms_data)
    else:
        # TODO: All this logic of getting a new ID for the given table should
        # be handled by the storage lib
        stored = storage.read()
        ids = map(lambda x: x['id_'], stored['alarms'])
        data['id_'] = max(ids)+1 if ids else 1

        stored['alarms'].append(data)
        storage.save(stored)

    alarms.set_alarms(storage.read('alarms'))

    redirect('/alarm/edit/%s' % data['id_'])

@get('/alarm/delete/:id_')
def alarm_delete(id_):
    storage.delete('alarms', int(id_))
    alarms.set_alarms(storage.read('alarms'))
    return "ok"

@get('/')
def index():
    helpers.current_tab("index")
    return template("index")

if __name__ == '__main__':
    import sys
    reloader = '--debug' in sys.argv
    run(host='0.0.0.0', port=config.PORT, reloader=reloader)
