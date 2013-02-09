import json
import sys

default_config = {
    "SHOW_DETAILED_INFO": True,
    "SHOW_TODO":  True,
    "COMMAND_EXECUTION": False,
    "SERVICE_EXECUTION": True,
    "SERVICES_FAVORITES": [],
}

SERVICE_VALID_ACTIONS = ("reload", "start", "stop", "restart", "status")

CURRENT_TAB = ""

def load_config(conn):
    c = conn.cursor()
    query = "SELECT id, json from config order by id"
    c.execute(query)
    result = c.fetchone()
    try:
        configuration = json.loads(result[1])
    except (ValueError, TypeError) as e:
        configuration = {}

    for k, v in default_config.items():
        setattr(sys.modules[__name__], k, configuration.get(k, v))

def save_configuration(conn, conf):
    c = conn.cursor()
    query = "SELECT id, json from config order by id"
    c.execute(query)
    result = c.fetchone()
    if not result:
        query = "INSERT INTO config (json) VALUES (?)"
        c.execute(query, (json.dumps(conf),))
    else:
        try:
            configuration = json.loads(result[1])
        except ValueError as e:
            configuration = {}
        configuration.update(conf)
        query = "UPDATE config set json = ? where id = ?"
        c.execute(query, (json.dumps(configuration), result[0]))
        conn.commit()

    # After saving the new configuration, we must load it again
    load_config(conn)
