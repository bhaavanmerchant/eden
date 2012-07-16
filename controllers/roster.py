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
    alloted_roles=['Team Leader', 'Team Member', 'Team Member', 'Team Member', 'Trainee', 'Trainee', 'Trainee' ] #db().select(db.hrm_roster_roles)
    volunteers={'a1':'Mari Hargis', 'a2':'Ismael Nolin','a3':'Sherry Febres','a4':'Barabara Gamino','a5':'Augustina Northam','a6':'Artie Timms','a7':'Kimberely Lamey','a8':'Ignacio Crumble','a9':'Vinnie Launius','a10':'Roxane Cremin'}; # {volunteer_id:volunteer_name}
    time_dets=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'];
    project_date=datetime.date(2012,4,4);
    slots=['8:00 - 12:00','12:00 - 4:00','4:00 - 8:00']
    job_roles=['-- Select --']
    job_roles+=['Team Leader', 'Team Member', 'Trainee']
    filled_slots=[{'row':3, 'col':2, 'vid':'a5'}]
    projects=['Project Alpha', 'Project Beta', 'Peoject Gamma', 'Project Delta', 'Project Epsilon', 'Project Zeta', 'Project Eta']
    return dict(message=T("Rostering Tool"), numb=6, projects=projects,slots=slots,job_roles=job_roles, alloted_roles=alloted_roles,volunteers=volunteers,time_dets=time_dets,project_date=project_date,filled_slots=filled_slots)

def people():
    """
        List of people specific to a job role
    """
    volunteers={'a1':'Mari Hargis', 'a2':'Ismael Nolin','a3':'Sherry Febres','a4':'Barabara Gamino','a5':'Augustina Northam','a6':'Artie Timms'}; # {volunteer_id:volunteer_name}
    alloted_roles=['Team Leader', 'Team Member', 'Team Member', 'Team Member', 'Trainee', 'Trainee', 'Trainee' ]; #db().select(db.hrm_roster_roles)
    r=int(request.vars.row);
    return DIV(DIV(alloted_roles[r], _id='volunteer_role'), *[DIV(volunteers[v_id], _class="volunteer_names", _id=v_id) for v_id in volunteers]);


def roster_submit():
    import simplejson as json
    import datetime
    import dateutil
    j=0
    #roster_info = json.JSONDecoder().decode(request.vars)
    roster_info = str(request.vars)
    roster_info = roster_info[9:-1]
    alloted_roles=['Team Leader', 'Team Member', 'Team Member', 'Team Member', 'Trainee', 'Trainee', 'Trainee' ]; #db().select(db.hrm_roster_roles)
    table_id=1;
    a=db.hrm_roster.insert()
    roster_col=2
    roster_row=4
    date_from_week=datetime.date(2012,4,4)+dateutil.relativedelta.relativedelta( days = roster_col);
    db.hrm_roster_shift.insert(roster_id=a, table_id=table_id, date=date_from_week, role=alloted_roles[roster_row])
    return DIV("Successfully saved!" + roster_info + str(a))
