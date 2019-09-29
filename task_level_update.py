import os,sys
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
        "task_level_field": "sg_level",
        "target_manday_field": "est_in_mins"
        
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
        {"Shotgun_Task_Change": args["target_manday_field"]},
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
    
    if  str(event) == 'None':
        return
    if  str(event["entity"]) == 'None':
        return
    if str(event["entity"]["id"]) == 'None':
        return
    # Make some vars for convenience.
    
    task_id = event["entity"]["id"]
    
    filters = [["id", "is", task_id]]
    fields = ["sg_level", "id", "duration", 'sg_week', 'step', 'est_in_mins']
    task = sg.find_one("Task", filters, fields)
    
        
    fields2 = ["code"]
    step_id = task['step']['id']
    filters2 = [["id", "is", step_id]]
    step = sg.find_one("Step", filters2, fields2)

    if(task['est_in_mins']=='' or str(task['est_in_mins'])=='None'):
        return
   
#     if (task['sg_level'].find('.')==-1) : 
#         return
    # If the Task status has been set to task_fin_status or task_na_status...
#     if new_value != old_value:
    def manday_def (x, dept):
        x = x / 480
        lev = ''
        
        if(dept=='Lookdev'):
            
            if(x <= 0.3) :
                lev = 'E'
                 
            elif ( x > 0.3 and x <= 1 ):
                lev='D'
            elif ( x > 1 and x <= 3 ):
                lev='C'
            elif ( x > 3 and x <= 5 ):
                lev='B'
            elif ( x > 5 and x <= 10 ):
                lev='A'
            elif ( x > 10 and x <= 20 ):
                lev='S'
            elif ( x > 20 ):
                lev='SS'
                
        if(dept=='Fur'):
            
            if(x <= 0.3) :
                lev = 'E'
                 
            elif ( x > 0.3 and x <= 1 ):
                lev='D'
            elif ( x > 1 and x <= 3 ):
                lev='C'
            elif ( x > 3 and x <= 5 ):
                lev='B'
            elif ( x > 5 and x <= 10 ):
                lev='A'
            elif ( x > 10 and x <= 20 ):
                lev='S'
            elif ( x > 20 ):
                lev='SS'
        #########################
        
        if(dept=='LitRig'):
            if(x <= 0.5) :
                lev = 'E'
                 
            elif ( x > 0.5 and x <= 5 ):
                lev='D'
            elif ( x > 5 and x <= 7 ):
                lev='C'
            elif ( x > 7 and x <= 10 ):
                lev='B'
            elif ( x > 10 and x <= 15 ):
                lev='A'
            elif ( x > 15 and x <= 20 ):
                lev='S'
            elif ( x > 20 ):
                lev='SS'
            
        if(dept=='Lighting'):
            if(x <= 0.5) :
                lev = 'E'
                 
            elif ( x > 0.5 and x <= 5 ):
                lev='D'
            elif ( x > 5 and x <= 7 ):
                lev='C'
            elif ( x > 7 and x <= 10 ):
                lev='B'
            elif ( x > 10 and x <= 15 ):
                lev='A'
            elif ( x > 15 and x <= 20 ):
                lev='S'
            elif ( x > 20 ):
                lev='SS'
            
            
        if(dept=='Compositing'):
            if(x <= 1) :
                lev = 'E'
                 
            elif ( x > 1 and x <= 3 ):
                lev='D'
            elif ( x > 3 and x <= 5 ):
                lev='C'
            elif ( x > 5 and x <= 7 ):
                lev='B'
            elif ( x > 7 and x <= 10 ):
                lev='A'
            elif ( x > 10 and x <= 15 ):
                lev='S'
            elif ( x > 15 ):
                lev='SS'
            
        if(dept=='Rigging'):
            if(x <= 1) :
                lev = 'E'
                 
            elif ( x > 1 and x <= 3 ):
                lev='D'
            elif ( x > 3 and x <= 5 ):
                lev='C'
            elif ( x > 5 and x <= 7 ):
                lev='B'
            elif ( x > 7 and x <= 10 ):
                lev='A'
            elif ( x > 10 and x <= 15 ):
                lev='S'
            elif ( x > 15 ):
                lev='SS'
            
        if(dept=='Matchmove'):
            if(x <= 0.5) :
                lev = 'E'
                 
            elif ( x > 0.5 and x <= 1 ):
                lev='D'
            elif ( x > 1 and x <= 3 ):
                lev='C'
            elif ( x > 3 and x <= 5 ):
                lev='B'
            elif ( x > 5 and x <= 10 ):
                lev='A'
            elif ( x > 10 and x <= 15 ):
                lev='S'
            elif ( x > 15 ):
                lev='SS'
        
        if(dept=='Matte'):
            if(x <= 0.5) :
                lev = 'E'
                 
            elif ( x > 0.5 and x <= 2 ):
                lev='D'
            elif ( x > 2 and x <= 5 ):
                lev='C'
            elif ( x > 5 and x <= 7 ):
                lev='B'
            elif ( x > 7 and x <= 12 ):
                lev='A'
            elif ( x > 12 and x <= 17 ):
                lev='S'
            elif ( x > 17 ):
                lev='SS'
            
        if(dept=='Modeling'):
            if(x <= 1) :
                lev = 'E'
                 
            elif ( x > 1 and x <= 3 ):
                lev='D'
            elif ( x > 3 and x <= 7 ):
                lev='C'
            elif ( x > 7 and x <= 10 ):
                lev='B'
            elif ( x > 10 and x <= 15 ):
                lev='A'
            elif ( x > 15 and x <= 20 ):
                lev='S'
            elif ( x > 20 ):
                lev='SS'
            
        if(dept=='Motion'):
            if(x <= 0.2) :
                lev = 'E'
                 
            elif ( x > 0.2 and x <= 0.5 ):
                lev='D'
            elif ( x > 0.5 and x <= 3 ):
                lev='C'
            elif ( x > 3 and x <= 5 ):
                lev='B'
            elif ( x > 5 and x <= 15 ):
                lev='A'
            elif ( x > 15 and x <= 25 ):
                lev='S'
            elif ( x > 25 ):
                lev='SS'
            
        if(dept=='Simulation'):
            if(x <= 0.5) :
                lev = 'E'
                 
            elif ( x > 0.5 and x <= 2 ):
                lev='D'
            elif ( x > 2 and x <= 5 ):
                lev='C'
            elif ( x > 5 and x <= 10 ):
                lev='B'
            elif ( x > 10 and x <= 15 ):
                lev='A'
            elif ( x > 15 and x <= 20 ):
                lev='S'
            elif ( x > 20 ):
                lev='SS'
            
        if(dept=='Animation'):
            if(x <= 0.5) :
                lev = 'E'
                 
            elif ( x > 0.5 and x <= 2 ):
                lev='D'
            elif ( x > 2 and x <= 4 ):
                lev='C'
            elif ( x > 4 and x <= 7 ):
                lev='B'
            elif ( x > 7 and x <= 12 ):
                lev='A'
            elif ( x > 12 and x <= 15 ):
                lev='S'
            elif ( x > 15 ):
                lev='SS'
            
        if(dept=='Concept'):
            if(x <= 0.5) :
                lev = 'E'
                 
            elif ( x > 0.5 and x <= 2 ):
                lev='D'
            elif ( x > 2 and x <= 3 ):
                lev='C'
            elif ( x > 3 and x <= 5 ):
                lev='B'
            elif ( x > 5 and x <= 10 ):
                lev='A'
            elif ( x > 10 and x <= 15 ):
                lev='S'
            elif ( x > 15 ):
                lev='SS'
                
        if(dept=='FX'):
            if(x <= 1) :
                lev = 'E'
                 
            elif ( x > 1 and x <= 3 ):
                lev='D'
            elif ( x > 3 and x <= 6 ):
                lev='C'
            elif ( x > 6 and x <= 8 ):
                lev='B'
            elif ( x > 8 and x <= 10 ):
                lev='A'
            elif ( x > 10 and x <= 20 ):
                lev='S'
            elif ( x > 20 ):
                lev='SS'
                                
        if(dept=='Layout'):
            if(x <= 0.5) :
                lev = 'E'
                 
            elif ( x > 0.5 and x <= 2 ):
                lev='D'
            elif ( x > 2 and x <= 4 ):
                lev='C'
            elif ( x > 4 and x <= 7 ):
                lev='B'
            elif ( x > 7 and x <= 12 ):
                lev='A'
            elif ( x > 12 and x <= 15 ):
                lev='S'
            elif ( x > 15 ):
                lev='SS'
                
        if(dept=='Digi_Environment'):
            if(x <= 1) :
                lev = 'E'
                 
            elif ( x > 1 and x <= 3 ):
                lev='D'
            elif ( x > 3 and x <= 7 ):
                lev='C'
            elif ( x > 7 and x <= 10 ):
                lev='B'
            elif ( x > 10 and x <= 15 ):
                lev='A'
            elif ( x > 15 and x <= 20 ):
                lev='S'
            elif ( x > 20 ):
                lev='SS'
                
        if(dept=='2.5D'):
            if(x <= 1) :
                lev = 'E'
                 
            elif ( x > 1 and x <= 3 ):
                lev='D'
            elif ( x > 3 and x <= 7 ):
                lev='C'
            elif ( x > 7 and x <= 10 ):
                lev='B'
            elif ( x > 10 and x <= 15 ):
                lev='A'
            elif ( x > 15 and x <= 20 ):
                lev='S'
            elif ( x > 20 ):
                lev='SS'
                
        if(dept=='Previsual'):
            if(x <= 3) :
                lev = 'E'
                 
            elif ( x > 3 and x <= 7 ):
                lev='D'
            elif ( x > 7 and x <= 10 ):
                lev='C'
            elif ( x > 10 and x <= 15 ):
                lev='B'
            elif ( x > 15 and x <= 20 ):
                lev='A'
            elif ( x > 20 and x <= 25 ):
                lev='S'
            elif ( x > 25 ):
                lev='SS'
                
                
        if(dept=='Postviz'):
            if(x <= 1) :
                lev = 'E'
                 
            elif ( x > 1 and x <= 3 ):
                lev='D'
            elif ( x > 3 and x <= 7 ):
                lev='C'
            elif ( x > 7 and x <= 10 ):
                lev='B'
            elif ( x > 10 and x <= 15 ):
                lev='A'
            elif ( x > 15 and x <= 20 ):
                lev='S'
            elif ( x > 20 ):
                lev='SS'
                
        if(dept=='Roto'):
            if(x <= 0.3) :
                lev = 'E'
                 
            elif ( x > 0.3 and x <= 0.5 ):
                lev='D'
            elif ( x > 0.5 and x <= 1 ):
                lev='C'
            elif ( x > 1 and x <= 3 ):
                lev='B'
            elif ( x > 3 and x <= 5 ):
                lev='A'
            elif ( x > 5 and x <= 7 ):
                lev='S'
            elif ( x > 7 ):
                lev='SS'
                
        if(dept=='Remove'):
            if(x <= 0.3) :
                lev = 'E'
                 
            elif ( x > 0.3 and x <= 0.5 ):
                lev='D'
            elif ( x > 0.5 and x <= 1 ):
                lev='C'
            elif ( x > 1 and x <= 3 ):
                lev='B'
            elif ( x > 3 and x <= 5 ):
                lev='A'
            elif ( x > 5 and x <= 7 ):
                lev='S'
            elif ( x > 7 ):
                lev='SS'
        return lev
            
    level = manday_def(task['est_in_mins'], step['code'])
    
    if(level==None or level==''):
        return
    
    sg.update(
        'Task',
        task_id,
        {'sg_level': level}
    )
    
    logger.info(
        "Going to Task with id %s to Project with id %s." % (task_id, level)
    )

