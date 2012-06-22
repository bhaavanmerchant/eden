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
    alloted_roles=['Team Leader', 'Team Member', 'Team Member', 'Team Member', 'Trainee', 'Trainee', 'Trainee' ]
    volunteers={'a1':'Mari Hargis', 'a2':'Ismael Nolin','a3':'Sherry Febres','a4':'Barabara Gamino','a5':'Augustina Northam','a6':'Artie Timms','a7':'Kimberely Lamey','a8':'Ignacio Crumble','a9':'Vinnie Launius','a10':'Roxane Cremin'}; # {volunteer_id:volunteer_name}
    time_dets=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'];
    project_date=datetime.date(2012,4,4);
    return dict(message=T("Rostering Tool"), numb=6, projects=['Project Alpha', 'Project Beta', 'Peoject Gamma', 'Project Delta', 'Project Epsilon', 'Project Zeta', 'Project Eta'],slots=['8:00 - 12:00','12:00 - 4:00','4:00 - 8:00'],job_roles=['-- Select --','Team Leader', 'Team Member', 'Trainee'], alloted_roles=alloted_roles,volunteers=volunteers,time_dets=time_dets,project_date=project_date)

def people():
    """
        List of people specific to a job role
    """
    volunteers={'a1':'Mari Hargis', 'a2':'Ismael Nolin','a3':'Sherry Febres','a4':'Barabara Gamino','a5':'Augustina Northam','a6':'Artie Timms'}; # {volunteer_id:volunteer_name}
    alloted_roles=['Team Leader', 'Team Member', 'Team Member', 'Team Member', 'Trainee', 'Trainee', 'Trainee' ];
    r=int(request.vars.row);
    return DIV(DIV(alloted_roles[r], _id='volunteer_role'), *[DIV(volunteers[v_id], _class="volunteer_names", _id=v_id) for v_id in volunteers]);
    
