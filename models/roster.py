# -*- coding: utf-8 -*-
#tablename = "hrm_roster_slots"
#table = db.define_table(tablename, Field('event'), Field('event_id'), Field('slot'))
tablename = "hrm_roster_table"
table = db.define_table(tablename, Field('week'), Field('slot'))
tablename = "hrm_roster"
table = db.define_table(tablename, Field('roster_table',db.hrm_roster_table), *s3_meta_fields())
tablename = "hrm_roster_organisation"
table = db.define_table(tablename, Field('roster',db.hrm_roster), s3db.super_link("org_id", "org_organisation"))
tablename = "hrm_roster_project"
table = db.define_table(tablename, Field('roster',db.hrm_roster), s3db.super_link("project_id", "project_project"))
tablename = "hrm_roster_site"
table = db.define_table(tablename, Field('roster',db.hrm_roster),  s3db.super_link("site_id", "org_site"))
tablename = "hrm_roster_incident" 
table = db.define_table(tablename, Field('roster',db.hrm_roster), s3db.super_link("event_id", "event_incident"))
tablename = "hrm_roster_scenario"
table = db.define_table(tablename, Field('roster',db.hrm_roster), s3db.super_link("scenario_id", "scenario_scenario"))
tablename = "hrm_shift"
table = db.define_table(tablename, 
                            Field('roster',db.hrm_roster),
                            s3db.project_task_id(label=T("task")), 
                            s3db.pr_person_id(label=T("person")), 
                            Field("starttime", "datetime", label=T("start")), 
                            Field("endtime", "datetime", label=T("end"))
                        )

tablename = "hrm_roster_roles" #roles: volunteer, team leader etc. defined for a table.
table = db.define_table(tablename, s3db.superlink("table_id", "hrm_roster_table"), Field('roles'))
tablename = "hrm_roster_type" #type: event, scenario, project etc.
table = db.define_table(tablename, s3db.superlink("table_id", "hrm_roster_table"), Field('type'))

