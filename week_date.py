import os, datetime,sys
sys.path.insert(0, '/core/TD/shotgunAPI/python-api-master')
import shotgun_api3


def registerCallbacks(reg):
    """
    Register our callbacks.
    :param reg: A Registrar instance provided by the event loop handler.
    """

    # Grab authentication env vars for this plugin. Install these into the env
    # if they don't already exist.
    server = os.environ["SG_SERVER"]
    script_name = os.environ["SGDAEMON_ASSIGNTOPROJECT_NAME"]
    script_key = os.environ["SGDAEMON_ASSIGNTOPROJECT_KEY"]

    # User-defined plugin args, change at will.
    args = {
        "task_week_field": "sg_week",
        "target_duedate_field": "due_date"
        
    }

    # Grab an sg connection for the validator.
    sg = shotgun_api3.Shotgun(server, script_name=script_name, api_key=script_key)

    # Bail if our validator fails.
    if not is_valid(sg, reg.logger, args):
        reg.logger.warning("Plugin is not valid, will not register callback.")
        return

    # Register our callback with the Shotgun_%s_Change event and tell the logger
    # about it.
    reg.registerCallback(
        script_name,
        script_key,
        update_level_manday,
        {"Shotgun_Task_Change": 'sg_week'},
        args,
    )
    reg.logger.debug("Registered callback.")


def is_valid(sg, logger, args):
    """
    Validate our args.
    :param sg: Shotgun API handle.
    :param logger: Logger instance.
    :param args: Any additional misc arguments passed through this plugin.
    :returns: True if plugin is valid, None if not.
    """

    # Make sure we have a valid sg connection.
    try:
        sg.find_one("Project", [])
    except Exception, e:
        logger.warning(e)
        return

    return True


def update_level_manday(sg, logger, event, args):
    """
    Updates an entity's status if the conditions are met.
    :param sg: Shotgun API handle.
    :param logger: Logger instance.
    :param event: A Shotgun EventLogEntry entity dictionary.
    :param args: Any additional misc arguments passed through this plugin.
    """
#     if (not event.get("meta", {}).get("entity_id") and
#         not event.get("meta", {}).get("old_value") and
#         not event.get("meta", {}).get("new_value")):
#             return
    if not event.get("meta", {}).get("entity_id"):
        return
    # Make some vars for convenience.
    task_id = event["entity"]["id"]
    
    filters = [["id", "is", task_id]]
    fields = ["sg_level", "id", "sg_week"]
    task = sg.find_one("Task", filters, fields)

    # If the Task status has been set to task_fin_status or task_na_status...
#     if new_value != old_value:
    if(task['sg_week']=='' or task['sg_week']==None):
        return
    
    
    data = task['sg_week']
    tmp = data.split('.')
        
    dt = datetime.datetime.now()
    year = dt.strftime("%Y")
    
    year = (year)
    month = (tmp[0])
    week = long(tmp[1])-1
    
    tmp_day = datetime.datetime.strptime(year+'-'+month+'-01', '%Y-%m-%d')
    
    t = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    n = tmp_day.weekday()
    
    if(t[n]=='sun'):
        #print week
        tmp_day = datetime.datetime.strptime(year+'-'+month+'-2', '%Y-%m-%d')
    
    last_monday = tmp_day - datetime.timedelta(days = tmp_day.weekday())
    
    month_week = last_monday.isocalendar()
    
    
    cal_week = month_week[1]+week
    
    end_date = datetime.datetime.strptime(str(month_week[0])+str(cal_week)+'-1', '%Y%W-%w')
    
    tmp = str(end_date).split('-')
    
    due_date = end_date + datetime.timedelta(days=4)
    due_date = str(due_date).split(' ')[0]
    
#     sg.update(
#         'Task',
#         task_id,
#         {'due_date': due_date}
#     )


