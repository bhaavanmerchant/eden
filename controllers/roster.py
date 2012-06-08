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
        - custom View
    """

    return dict(message=T("Rostering Tool"), numb=6, projects=['Project Alpha', 'Project Beta', 'Peoject Gamma', 'Project Delta', 'Project Epsilon', 'Project Zeta', 'Project Eta'],slots=['8:00 - 12:00','12:00 - 4:00','4:00 - 8:00'],job_roles=['-- Select --','Team Leader', 'Team Member', 'Trainee'])
