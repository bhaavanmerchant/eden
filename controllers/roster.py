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

    alloted_roles = []
    rows = db().select(
                        db.hrm_roster_roles.roles
                        )

    for row in rows:
        alloted_roles.append(row["roles"])

    volunteers={} # {volunteer_id:volunteer_name}
    rows=db(db.pr_person).select()

    for row in rows:
        volunteers[str(row["id"])]=row["first_name"]+" "+row["last_name"]

    defaults = [
                request.vars.event,
                request.vars.project_selector,
                request.vars.timeframe,
                request.vars.timeslot
                ] # Return the default selection for the drop downs.
    table_id = db.hrm_roster_table.update_or_insert(event=defaults[0],week=defaults[2],slot=defaults[3])
    rows = db(
                db.hrm_roster_shift.table_id==table_id
            ).select()
    filled_slots = []
    for row in rows:
        #determine col
        col = (string_to_date(row["date"]) - project_date).days
        v_id = str(row["person_id"])
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
        
        slot = dict( row = row_tbi, col = col, vid = v_id)
        filled_slots.append(slot)
               
    slots = ["8:00 - 12:00","12:00 - 4:00","4:00 - 8:00"]
    job_roles = ["-- Select --"]
    jr = []
    rows = db().select(
                        db.hrm_job_role.name
                        )

    for row in rows:
        jr.append(row["name"])

    job_roles += jr
    
    event = ["Project","Organisation","Scenario","Site","Incident"]
    time_dets = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"];
    project_date = datetime.date.today() #Default starting day of roster is current date.
    projects=[]
    
    for i in range(len(defaults)):
        if not defaults[i]:
            defaults[i] = "0"

    if defaults[0] == "0":
        rows = db(
                    db.project_project
                ).select()
        i = 0
        for row in rows:
            projects.append(row["code"])
            if int(defaults[1]) == i:
                project_date = row["start_date"]
            i += 1

    elif defaults[0] == "1":
        rows = db().select(db.org_organisation.name)
        
        for row in rows:
            projects.append(row["name"])
        
    elif defaults[0] == "2":
        True
        #rows=db().select(db.org_organisation.name)
        #for row in rows:
        #    projects.append(row["name"])
    
    elif defaults[0] == "3":
        True
        #rows=db().select(db.org_organisation.name)
        #for row in rows:
        #    projects.append(row["name"])

    elif defaults[0] == "4":
        rows = db(db.irs_ireport).select()
        i=0
        for row in rows:
            projects.append(row["name"])
            if int(defaults[1]) == i:
                project_date = row["datetime"].date()
            i+=1            

    else:
        defaults[0] == "0"

    project_day = datetime.date.weekday(project_date) #To determine the previous Monday, determine the weekday of the starting date.
    project_date = project_date - datetime.timedelta( days = project_day )  #Subtract that day of the week, to get its previous Monday.

    if len(request.args)>0 and request.args[0]=="pdf":

        from gluon.contrib.pyfpdf import FPDF, HTMLMixin
    
        rows = [
                THEAD(TR(TH("Key",_width="70%"), TH("Value",_width="30%"))),
                TBODY(TR(TD("Hello"),TD("60")), 
                TR(TD("World"),TD("40")))
                ]
        table = TABLE(*rows, _border = "0", _align = "center", _width = "50%")

        # create a custom class with the required functionalities 
        class MyFPDF(FPDF, HTMLMixin):
            def header(self): 
                "hook to draw custom page header (logo and title)"
                logo = os.path.join( request.env.web2py_path, "applications", request.application, "static", "img", "sahanasmall_05.png" )
                self.image(logo, 10, 8, 33)
                self.set_font("Arial", "B", 15)
                self.cell(65) # padding
                self.cell(60, 10, "Roster", 1, 0, "C")
                self.ln(20)
                
            def footer(self):
                "hook to draw custom page footer (printing page numbers)"
                self.set_y(-15)
                self.set_font("Arial","I",8)
                txt = "Page %s of %s" % (self.page_no(), self.alias_nb_pages())
                self.cell(0,10,txt,0,0,"C")
        pdf=MyFPDF()
        # create a page and serialize/render HTML objects
        pdf.add_page()
        pdf.write_html(
                        str(XML(table, sanitize=False))
                        )
        # prepare PDF to download:
        response.headers["Content-Type"] = "application/pdf"
        return pdf.output(dest="S")


    return dict(message = T("Rostering Tool"), numb = 6, projects = projects, slots = slots, job_roles = job_roles, alloted_roles = alloted_roles, volunteers = volunteers, time_dets = time_dets, project_date = project_date, filled_slots = filled_slots, event = event, defaults = defaults)

def people():
    """
        List of people specific to a job role
    """
    rows = db(db.hrm_job_role).select()
    subrows = db(db.hrm_human_resource).select()
    #people=db(db.pr_person).select()
    volunteers={}    # {volunteer_id:volunteer_name}
    for row in rows:    #Seems inefficient, will try db chaining later to improvise
        specific_volunteers = {}
        for subrow in subrows:
            for job_role in subrow["job_role_id"]:
                if job_role == row["id"]:
                    person = db(
                                db.pr_person.id == subrow["person_id"]
                                ).select()
                    specific_volunteers[str(person[0]["id"])] = person[0]["first_name"] + " " + person[0]["last_name"]
        volunteers[ str( row["name"] ) ] = specific_volunteers
    
    alloted_roles = []
    rows=db().select(
                    db.hrm_roster_roles.roles
                    )

    for row in rows:
        alloted_roles.append(row["roles"])

    r = int(request.vars.row);
    return DIV(
                DIV(alloted_roles[r], _id="volunteer_role"), FORM(
                                                                    INPUT( _name="volunteer_quick_search", _id="volunteer_quick_search")
                                                                ),
                *[ DIV(volunteers[alloted_roles[r]][v_id], _class="volunteer_names", _id=v_id) for v_id in volunteers [ alloted_roles[r] ] ] 
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

    table_id=1 #Hard coded. Needs to change
    db(
        db.hrm_roster_shift.table_id==table_id
      ).delete()

    for i in range( len(items) / 3 ):
        a = db.hrm_roster.insert()
        roster_col = str( items["array[" + str(i) + "][col]"] )
        roster_row = str( items["array[" + str(i) + "][row]"] )
        person = str( items["array[" + str(i) + "][vid]"] )
        date_from_week = datetime.date(2012,4,4) + dateutil.relativedelta.relativedelta( days = int(roster_col) ) #Hard coded. Date needs to change
        db.hrm_roster_shift.insert(
                                    roster_id = a, table_id = table_id, date = date_from_week, role = alloted_roles[ int(roster_row) ], person_id = person
                                    )
    return "Successfully saved!"

def add_role():
    """
    Add volunteers role to the corresponding table
    """
    table_id = 1
    job_roles = ["Team Leader", "Team Member", "Trainee"]
    pt = db( db.hrm_roster_roles.table_id == table_id ).count()
    db.hrm_roster_roles.insert(
                                table_id = table_id, roles = job_roles[ int(request.vars.new_job_role)-1 ], position_in_table = pt
                                )
    redirect( URL("index") )
    return job_roles[ request.vars.new_job_role ]

def del_role():
    """
    Delete volunteers role from the corresponding table
    """
    table_id = 1
    result = db(
                db.hrm_roster_roles.table_id == table_id and db.hrm_roster_roles.position_in_table == request.args[0]
                ).delete()

    def remap_table(table_id):
        #pt=db(db.hrm_roster_roles.table_id==table_id).count()
        rows = db(
                    db.hrm_roster_roles.table_id == table_id
                ).select()

        for i in range( len(rows) ):
            db(
                db.hrm_roster_roles.table_id == table_id and db.hrm_roster_roles.position_in_table == rows[i].position_in_table
                ).update(
                        position_in_table = i
                        )

    remap_table(table_id)
    redirect( URL("index") )
    return result

def requests():
    """
    Managing Change requests
    """
    return dict(message = "Panel")

def hrm():
    output = s3_rest_controller("pr", "person")
    return output

def tables():
    return s3_rest_controller("hrm","roster_table")
