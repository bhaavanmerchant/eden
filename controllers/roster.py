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
    filled_slots=[{'row':3, 'col':2, 'vid':'14'}]
    for row in rows:
        #determine col
        exploded_date=row['date'].split('-')
        col = (project_date - datetime.date(int(exploded_date[0]),int(exploded_date[1]),int(exploded_date[2]))).days
        #v_id = row['vid']
        v_id='a4'
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
            else:
                row_tbi=i
                break
        slot=dict(row=row_tbi, col=col, vid=v_id)
        #filled_slots.append(slot)
               
    slots=['8:00 - 12:00','12:00 - 4:00','4:00 - 8:00']
    job_roles=['-- Select --']
    jr=[]
    rows=db().select(db.hrm_job_role.name)
    for row in rows:
        jr.append(row['name'])
    job_roles+=jr
    occasion=['Project','Organisation','Scenario','Site','Incident']
    projects=['Project Alpha', 'Project Beta', 'Peoject Gamma', 'Project Delta', 'Project Epsilon', 'Project Zeta', 'Project Eta']
    return dict(message=T("Rostering Tool"), numb=6, projects=projects,slots=slots,job_roles=job_roles, alloted_roles=alloted_roles,volunteers=volunteers,time_dets=time_dets,project_date=project_date,filled_slots=filled_slots,occasion=occasion)

def people():
    """
        List of people specific to a job role
    """
    rows=db(db.hrm_job_role).select()
    subrows=db(db.hrm_person_role).select()
    #people=db(db.pr_person).select()
    volunteers={}    
    for row in rows:    #Seems inefficient, will try db chaining later to improvise
        specific_volunteers={}
        for subrow in subrows:
            if subrow['job_role_id']==row['id']:
                person=db(db.pr_person.id == subrow['person_id']).select()
                specific_volunteers[str(person[0]['id'])] = person[0]['first_name'] + ' ' + person[0]['last_name']
        volunteers[str(row['name'])]=specific_volunteers
    #volunteers={'Team Leader':{'a1':'Mari Hargis', 'a2':'Ismael Nolin','a3':'Sherry Febres','a4':'Barabara Gamino','a5':'Augustina Northam','a6':'Artie Timms'}, 'Team Member':{'a3':'Sherry Febres','a4':'Barabara Gamino','a5':'Augustina Northam','a6':'Artie Timms','a7':'Kimberely Lamey','a8':'Ignacio Crumble'},  'Trainee':{'a5':'Augustina Northam','a6':'Artie Timms','a7':'Kimberely Lamey','a8':'Ignacio Crumble','a9':'Vinnie Launius','a10':'Roxane Cremin'}}; # {volunteer_id:volunteer_name}
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
    #roster_info = json.JSONDecoder().decode(request.vars)
    #roster_info = json.loads('{"array[7][row]": "6", "array[4][col]": "2", "array[0][row]": "0", "array[2][vid]": "a7", "array[0][col]": "1", "array[2][row]": "2", "array[4][vid]": "a5", "array[3][vid]": "a7", "array[5][col]": "0", "array[1][col]": "1", "array[3][col]": "1", "array[0][vid]": "a2", "array[6][vid]": "a9", "array[5][vid]": "a8", "array[1][row]": "1", "array[4][row]": "3", "array[6][row]": "5", "array[7][col]": "0", "array[7][vid]": "a5", "array[6][col]": "0", "array[2][col]": "0", "array[5][row]": "4", "array[3][row]": "3", "array[1][vid]": "a5"}')
    roster_info = str(request.vars)    
    roster_info = roster_info[9:-1]
    #roster_info = {'array[1][vid]': 'a5', 'array[1][col]': '2', 'array[0][row]': '1', 'array[0][vid]': 'a5', 'array[1][row]': '3', 'array[0][col]': '0'}
    #alloted_roles=[]
    #items = json.loads(roster_info)
    #rows=db().select(db.hrm_roster_roles.roles)
    #for row in rows:
    #    alloted_roles.append(row['roles'])
    table_id=1;
    #a=db.hrm_roster.insert()
    #roster_col=2
    #roster_row=4
    #date_from_week=datetime.date(2012,4,4)+dateutil.relativedelta.relativedelta( days = roster_col);
    #db.hrm_roster_shift.insert(roster_id=a, table_id=table_id, date=date_from_week, role=alloted_roles[roster_row])
    return DIV("Successfully saved! " +  str(roster_info))

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
