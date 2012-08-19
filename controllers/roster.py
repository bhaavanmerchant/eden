# -*- coding: utf-8 -*-

"""
    Roster Management

    A module to assign job on a time roster
"""

module = request.controller
resourcename = request.function

#if not deployment_settings.has_module(module):
#    raise HTTP(404, body="Module disabled: %s" % module)

# -----------------------------------------------------------------------------

def index():
    return dict(message = T("Rostering Tool"))



def roster():
    """
        Application Home page
    """
    import datetime
    import dateutil

    def string_to_date(string_date):
        """
            Convert a string date into datetime by exploding by '-'
        """
        exploded_date = string_date.split("-")
        return datetime.date(int(exploded_date[0]),
                                int(exploded_date[1]),
                                int(exploded_date[2])
                                        )

    defaults = [
                request.vars.timeframe,
                request.vars.timeslot
                ] # Return the default selection for the drop downs.

    for i in range(len(defaults)):
        if not defaults[i]:
            defaults[i] = "0"       #Assign defaults to prevent garbage

    table=s3db.hrm_roster_instance    #Create an instance of the table if it doesnot already exist.
    if len(request.args)>0:
        table_id=int(request.args[0]) #An instance of table implies a table_id, identified also with week and shift info.
        instance_id = table.update_or_insert(
                                                table_id = table_id, week = defaults[0], slot = defaults[1]
                                            ) 
    else:
        redirect( URL( c = "roster", f = "tables" ) )

    rows=db(table.table_id == table_id).select()

    for row in rows:
        if row["week"] == defaults[0] and row["slot"] == defaults[1]:
            instance_id = row["id"]    #Get the instance id of the roster table to perform operations on.

    alloted_roles = []          #View the alloted roles (all the rows) for this instance of roster.
    rows = db(
                s3db.hrm_roster_roles.instance_id == instance_id
                ).select()

    for row in rows:
        alloted_roles.append(row["roles"])

    volunteers={} # Return volunteer information in format: {volunteer_id:volunteer_name}
    rows=db(db.pr_person).select()

    for row in rows:
        volunteers[str(row["id"])] = row["first_name"] + " " + row["last_name"]


    table=s3db.hrm_roster_table  # View the event id information
    rows = db(table.id == table_id).select()

    for row in rows:
        event_id = row["roster_event_id"]

    
    slots = []  #Keep a track of already assigned shifts to this roster table type.
    table=s3db.hrm_roster_slots
    rows = db(table.table_id == table_id).select()

    for row in rows:
        subrows= db(s3db.hrm_slots.id == row["slots_id"]).select()
        for slot in subrows:
            slots.append(slot["name"])

    job_titles = ["-- Select --"]
    table=s3db.hrm_job_title
    jr = []   #Populate the job titles.
    rows = db(table).select()

    for row in rows:
        jr.append(row["name"])

    job_titles += jr

    time_dets = [T("Monday"),T("Tuesday"),T("Wednesday"),T("Thursday"),T("Friday"),T("Saturday"),T("Sunday")];
    
    rows = db(s3db.hrm_roster_table.roster_event_id == event_id).select()

    for row in rows:  #Get information of start day of roster.
        project_date = row["start_date"]
        event_type = row["type"] 

    project_day = datetime.date.weekday(project_date) #To determine the previous Monday, determine the weekday of the starting date.
    project_date = project_date - datetime.timedelta( days = project_day )  #Subtract that day of the week, to get its previous Monday.

    rows = db(
                db.hrm_roster_shift.instance_id == instance_id
            ).select()
    filled_slots = []       #To get prepopulated information. This is previous roster information. 
    for row in rows:
        #determine col
        col = (string_to_date(row["date"]) - project_date).days
        v_id = str(row["person_id"])
        slot_level = str(row["slot_level"])
        #determine row
        row_tbi = len(alloted_roles) + 2 #To prevent garbage value raising an exception
        for i in range(len(alloted_roles)):
            already_filled = False
            if alloted_roles[i] == row["role"]:
                for filled_slot in filled_slots:
                    if (filled_slot["col"] == col and filled_slot["row"] == i):
                        already_filled=True
                #logic to check if this i th row is free
                #if free populate filled_slots
            if already_filled:
                continue
            if alloted_roles[i] == row["role"]:
                row_tbi = i
                break
        
        slot = dict( row = row_tbi, col = col, vid = v_id, slot_level = slot_level )
        filled_slots.append(slot)
           


    return dict(message = T("Rostering Tool"), numb = 6, slots = slots, job_titles = job_titles, 
                                alloted_roles = alloted_roles, volunteers = volunteers, time_dets = time_dets, 
                                project_date = project_date, filled_slots = filled_slots, defaults = defaults,
                                instance_id=instance_id, table_id = table_id
                )

def people():
    """
        List of people specific to a job role. This is called by AJAX to populate the left panel.
    """
    rows = db(s3db.hrm_job_title).select()
    subrows = db(s3db.hrm_human_resource).select()
    volunteers = {}    # {volunteer_id:volunteer_name}

    for row in rows:
        specific_volunteers = {}

        for subrow in subrows:

            if subrow["job_title_id"] == row["id"]:   #Job title based volunteer differentiation.
                person = db(
                            db.pr_person.id == subrow["person_id"]
                            ).select()
                specific_volunteers[str(person[0]["id"])] = person[0]["first_name"] + " " + person[0]["last_name"]
        volunteers[ str( row["name"] ) ] = specific_volunteers
    

    table_id = int(request.args[0])
    instance_id = int(request.args[1])

    alloted_roles = []      #Iterate through the job titles in that instance of table to determine the desired list of volunteers for a particular row.
    rows=db(s3db.hrm_roster_roles.instance_id == instance_id).select()

    for row in rows:
        alloted_roles.append(row["roles"])

    r = int(request.vars.row);
    return DIV(
                DIV(alloted_roles[r], _id = "volunteer_role"), FORM(
                                                                    INPUT( _name = "volunteer_quick_search", _id = "volunteer_quick_search")
                                                                ), DIV(DIV(_class = "tooltip", _title = "Volunteers|List of volunteers matching the Job Title criteria. The panel can be use for quick searching.")),
                *[ DIV(volunteers[alloted_roles[r]][v_id], _class = "volunteer_names", _id = v_id) for v_id in volunteers [ alloted_roles[r] ] ] 
              )



def roster_submit():
    """
        This takes the JSON of table data and stores in database
    """
    from gluon.contrib import simplejson as json
    import datetime
    import dateutil

    j = 0

    roster_info = str(request.vars)     #Get the JSON
    roster_info = roster_info[9:-1]     #Trim the object information

    alloted_roles = []

    roster_info = str( roster_info )
    roster_info = roster_info.replace("'",'"') #The string received from Javascript has JSON elements inside single quotes. This requires replacement by double quotes for json.loads to process.

    items = json.loads(roster_info)

    rows=db().select(
                    db.hrm_roster_roles.roles
                    )

    for row in rows:
        alloted_roles.append(row["roles"])
    table_id=request.args[0]
    instance_id = request.args[1]
    db(
        db.hrm_roster_shift.instance_id==instance_id
      ).delete()            #Delete previous roster information for this instance. This will then be replaced.

    table=s3db.hrm_roster_table
    rows = db(table.id == table_id).select()
    for row in rows:
        event_id = row["roster_event_id"]

    rows = db(s3db.hrm_roster_table.roster_event_id == event_id).select()
    for row in rows:
        project_date = row["start_date"]  

    project_day = datetime.date.weekday(project_date) #To determine the previous Monday, determine the weekday of the starting date.
    project_date = project_date - datetime.timedelta( days = project_day )  #Subtract that day of the week, to get its previous Monday.

    for i in range( len(items) / 4 ):
        a = db.hrm_roster.insert()
        roster_col = str( items["array[" + str(i) + "][col]"] )
        roster_row = str( items["array[" + str(i) + "][row]"] )
        person = str( items["array[" + str(i) + "][vid]"] )
        slot_level = str( items["array[" + str(i) + "][slot_level]"] )
        date_from_week = project_date + dateutil.relativedelta.relativedelta( days = int(roster_col) )
        db.hrm_roster_shift.insert(
                                    roster_id = a, instance_id = instance_id, date = date_from_week, 
                                    role = alloted_roles[ int(roster_row) ], person_id = person, slot_level = slot_level
                                    )
    return T("Successfully saved!")

def reset():
    """
    To reset the given instance of table
    """
    table_id = request.args[0]
    instance_id = request.args[1]
    db(
        db.hrm_roster_shift.instance_id == instance_id
      ).delete()
    redirect( URL(c = "roster", f = "roster", args = [ table_id, instance_id ]) )
    return "Table reset!"

def add_role():
    """
    Add volunteers role to the corresponding table
    """
    table_id = request.args[0]
    instance_id = request.args[1]
    job_titles = []
    table=s3db.hrm_job_title
    jr = []
    rows = db(table).select()

    for row in rows:
        jr.append(row["name"])

    job_titles += jr
    pt = db(
            db.hrm_roster_roles.instance_id == instance_id
            ).count()
    db.hrm_roster_roles.insert(
                                instance_id = instance_id, roles = job_titles[ int(request.vars.new_job_title)-1 ], position_in_table = pt
                                )
    redirect( URL(c = "roster", f = "roster", args = [ table_id, instance_id, 1 ] ) )
    return job_titles[ request.vars.new_job_title ]

def del_role():
    """
    Delete volunteers role from the corresponding table
    """
    table_id=request.args[0]
    instance_id = request.args[1]
    result = db(
                db.hrm_roster_roles.instance_id == instance_id and db.hrm_roster_roles.position_in_table == request.args[2]
                ).delete()

    def remap_table(instance_id):
        rows = db(
                    db.hrm_roster_roles.instance_id == instance_id
                ).select()

        for i in range( len(rows) ):
            db(
                db.hrm_roster_roles.instance_id == instance_id and db.hrm_roster_roles.position_in_table == rows[i].position_in_table
                ).update(
                        position_in_table = i
                        )

    remap_table( instance_id )
    redirect( URL(c = "roster", f = "roster", args = [ table_id, instance_id, 1 ] ) )
    return result

def requests():
    """
    Managing Change requests
    """
    return dict( message = "Panel" )

def hrm():
    """
    A fallback for managing HRM.
    """
    output = s3_rest_controller( "pr", "person" )
    return output

def slots():
    """
    Add slots (shifts and slots are interchangeable at this stage). These slots can then be assigned to table by the 
    shifts  function.
    """
    return s3_rest_controller( "hrm", "slots" )

def shifts():
    """
    Assign shifts to each roster table.
    """
    if len(request.args) == 0:
        redirect( URL( c = "roster", f = "tables" ) )
 
    table_id = request.args[0]
    table = s3db.hrm_slots
    rows = db(table).select()
    slots = []

    for row in rows:
        slots.append([row["id"],row["name"]])

    if request.vars.slots and len(request.vars.slots)>0:
        table = s3db.hrm_roster_slots
        db(
            table.table_id == table_id
            ).delete()

        for slot in request.vars.slots:
            table.insert(
                            table_id = table_id, slots_id = slot
                        )

        redirect( URL(c="roster", f="roster", args=[table_id]) ) 

    return dict(message=T("Rostering tool"), specific=T("Manage shifts"), slots = slots)

def tables():
    """
    Manage and add tables which can then be used for rostering. This is a custom controller to mimic CRUD functionalities.
    """
    def string_to_date(string_date):
        """
            Convert a string date into datetime by exploding by '-'
        """
        exploded_date = string_date.split("-")
        return datetime.date(int(exploded_date[0]),
                                int(exploded_date[1]),
                                int(exploded_date[2])
                                        )
    selection = [
                request.vars.event,
                request.vars.project_selector,
                request.vars.start_date
                ] # Return the default selection for the drop downs.

    event = ["Project","Organisation","Incident"]

    projects=[]
    
    for i in range(len(selection)):
        if not selection[i]:
            selection[i] = "0"

    defaults = [
                selection[0],
                selection[1],
                datetime.date.today()
                ]

    if len(request.args)>0:
        if request.args[0] == "delete":
            table = s3db.hrm_roster_table
            db(
                table.id == int( request.args[1] )
                ).delete()
            redirect( URL(c = "roster", f = "tables", args = [ selection[0] ] ) )     

        else:
            defaults[0] = request.args[0]
            if request.args[0] == "0":
                table = s3db.project_project
                rows = db(table).select()

                for row in rows:
                    projects.append([row["id"], row["code"]])

                    if int(selection[1]) == row["id"]:
                        event_id = row["roster_event_id"]

            elif request.args[0] == "1":
                table = s3db.org_organisation
                rows = db( table ).select()

                for row in rows:
                    projects.append( [ row["id"], row["name"] ] )

                    if int(selection[1]) == row["id"]:
                        event_id=row["roster_event_id"]
                
            elif request.args[0] == "2":
                rows = db( s3db.irs_ireport ).select()

                for row in rows:
                    projects.append([row["id"], row["name"]])

                    if int(selection[1]) == row["id"]:
                        event_id=row["roster_event_id"]

        
    
    else:
        table = s3db.project_project
        rows = db(table).select()

        for row in rows:
            projects.append( [ row["id"], row["code"] ] )

            if int(selection[1]) == row["id"]:
                event_id=row["roster_event_id"]
    

    table = s3db.hrm_roster_slots
    rows = db( table ).select()
    slots=[]

    for row in rows:
        slots.append(row["id"])
    
    if selection[1] != "0":
        table = s3db.hrm_roster_table
        rows = table.update_or_insert( 
                                        roster_event_id = event_id, type = event[ int( selection[0] ) ],
                                        start_date = string_to_date( selection[2] )
                                        )

    table = s3db.hrm_roster_event
    roster_table = db(
                        table.id == s3db.hrm_roster_table.roster_event_id
                        ).select()
    
    return dict(
                message = T("Rostering Tool"), projects = projects, event = event,
                slots = slots, roster_table = roster_table, error="", defaults = defaults
                )
