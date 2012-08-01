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
    import datetime;
    import dateutil;
    alloted_roles=[]
    rows=db().select(db.hrm_roster_roles.roles)
    for row in rows:
        alloted_roles.append(row['roles'])
    volunteers={} # {volunteer_id:volunteer_name}
    rows=db(db.pr_person).select()
    for row in rows:
        volunteers[str(row['id'])]=row['first_name']+' '+row['last_name']
    time_dets=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'];
    project_date=datetime.date(2012,4,4);
    rows=db(db.hrm_roster_shift).select()
    filled_slots=[]
    for row in rows:
        #determine col
        exploded_date=row['date'].split('-')
        
        col = (datetime.date(int(exploded_date[0]),int(exploded_date[1]),int(exploded_date[2]))-project_date).days
        v_id = str(row['person_id'])
        #v_id='4'
        #determine row
        row_tbi=len(alloted_roles)+2 #To prevent garbage value raising an exception
        for i in range(len(alloted_roles)):
            already_filled=False
            if alloted_roles[i] == row['role']:
                for filled_slot in filled_slots:
                    if (filled_slot['col']==col and filled_slot['row']==i):
                        already_filled=True
                #logic to check if this i th row is free
                #if free populate filled_slots
            if already_filled:
                continue
            if alloted_roles[i] == row['role']:
                row_tbi=i
                break
        slot=dict(row=row_tbi, col=col, vid=v_id)
        filled_slots.append(slot)
               
    slots=['8:00 - 12:00','12:00 - 4:00','4:00 - 8:00']
    job_roles=['-- Select --']
    jr=[]
    rows=db().select(db.hrm_job_role.name)
    for row in rows:
        jr.append(row['name'])
    job_roles+=jr
    occasion=['Project','Organisation','Scenario','Site','Incident']
    projects=['Project Alpha', 'Project Beta', 'Peoject Gamma', 'Project Delta', 'Project Epsilon', 'Project Zeta', 'Project Eta']
    if len(request.args)>0 and request.args[0]=="pdf":
        from gluon.contrib.pyfpdf import FPDF, HTMLMixin
        rows = [THEAD(TR(TH("Key",_width="70%"), TH("Value",_width="30%"))),
        TBODY(TR(TD("Hello"),TD("60")), 
                  TR(TD("World"),TD("40")))]
        table = TABLE(*rows, _border="0", _align="center", _width="50%")

        # create a custom class with the required functionalities 
        class MyFPDF(FPDF, HTMLMixin):
            def header(self): 
                "hook to draw custom page header (logo and title)"
                logo=os.path.join(request.env.web2py_path,"applications",request.application,"static","img","sahanasmall_05.png")
                self.image(logo,10,8,33)
                self.set_font('Arial','B',15)
                self.cell(65) # padding
                self.cell(60,10,"Roster",1,0,'C')
                self.ln(20)
                
            def footer(self):
                "hook to draw custom page footer (printing page numbers)"
                self.set_y(-15)
                self.set_font('Arial','I',8)
                txt = 'Page %s of %s' % (self.page_no(), self.alias_nb_pages())
                self.cell(0,10,txt,0,0,'C')
        pdf=MyFPDF()
        # create a page and serialize/render HTML objects
        pdf.add_page()
        pdf.write_html(str(XML(table, sanitize=False)))
        # prepare PDF to download:
        response.headers['Content-Type']='application/pdf'
        return pdf.output(dest='S')


    return dict(message=T("Rostering Tool"), numb=6, projects=projects,slots=slots,job_roles=job_roles, alloted_roles=alloted_roles,volunteers=volunteers,time_dets=time_dets,project_date=project_date,filled_slots=filled_slots,occasion=occasion)

def people():
    """
        List of people specific to a job role
    """
    rows=db(db.hrm_job_role).select()
    subrows=db(db.hrm_person_role).select()
    #people=db(db.pr_person).select()
    volunteers={}    # {volunteer_id:volunteer_name}
    for row in rows:    #Seems inefficient, will try db chaining later to improvise
        specific_volunteers={}
        for subrow in subrows:
            if subrow['job_role_id']==row['id']:
                person=db(db.pr_person.id == subrow['person_id']).select()
                specific_volunteers[str(person[0]['id'])] = person[0]['first_name'] + ' ' + person[0]['last_name']
        volunteers[str(row['name'])]=specific_volunteers
    alloted_roles=[]
    rows=db().select(db.hrm_roster_roles.roles)
    for row in rows:
        alloted_roles.append(row['roles'])
    r=int(request.vars.row);
    return DIV(DIV(alloted_roles[r], _id='volunteer_role'), FORM(INPUT(_name='volunteer_quick_search', _id='volunteer_quick_search')), *[DIV(volunteers[alloted_roles[r]][v_id], _class="volunteer_names", _id=v_id) for v_id in volunteers[alloted_roles[r]]]);


def roster_submit():
    from gluon.contrib import simplejson as json
    import datetime
    import dateutil
    j=0
    roster_info = str(request.vars)    
    roster_info = roster_info[9:-1]
    alloted_roles=[]
    roster_info=str(roster_info)
    roster_info=roster_info.replace("'",'"')
    items = json.loads(roster_info)
    rows=db().select(db.hrm_roster_roles.roles)
    for row in rows:
        alloted_roles.append(row['roles'])
    table_id=1;
    db(db.hrm_roster_shift.table_id==table_id).delete()
    for i in range(len(items)/3):
        a=db.hrm_roster.insert()
        roster_col=str(items["array["+str(i)+"][col]"])
        roster_row=str(items["array["+str(i)+"][row]"])
        person=str(items["array["+str(i)+"][vid]"])
        date_from_week=datetime.date(2012,4,4)+dateutil.relativedelta.relativedelta( days = int(roster_col));
        db.hrm_roster_shift.insert(roster_id=a, table_id=table_id, date=date_from_week, role=alloted_roles[int(roster_row)], person_id=person)
    return DIV("Successfully saved! " + str(len(items)))

def add_role():
    table_id=1
    job_roles=['Team Leader', 'Team Member', 'Trainee']
    pt=db(db.hrm_roster_roles.table_id==table_id).count()
    db.hrm_roster_roles.insert(table_id=table_id, roles=job_roles[int(request.vars.new_job_role)-1],position_in_table=pt)
    redirect(URL('index'))
    return job_roles[request.vars.new_job_role]

def del_role():
    table_id=1
    result = db(db.hrm_roster_roles.table_id==table_id and db.hrm_roster_roles.position_in_table==request.args[0]).delete()
    def remap_table(table_id):
        #pt=db(db.hrm_roster_roles.table_id==table_id).count()
        rows=db(db.hrm_roster_roles.table_id==table_id).select()
        for i in range(len(rows)):
            db(db.hrm_roster_roles.table_id==table_id and db.hrm_roster_roles.position_in_table==rows[i].position_in_table).update(position_in_table=i)
    remap_table(table_id)
    redirect(URL('index'))
    return result

def admin():
    occasion=['Project','Organisation','Scenario','Site','Incident']
    projects=['Project Alpha', 'Project Beta', 'Peoject Gamma', 'Project Delta', 'Project Epsilon', 'Project Zeta', 'Project Eta']
    jr=[]
    rows=db().select(db.hrm_job_role.name)
    for row in rows:
        jr.append(row['name'])
    return dict(message='Panel', occasion=occasion, projects=projects, job_roles=jr)
