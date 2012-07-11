# -*- coding: utf-8 -*-
tablename = "hrm_roster"
table = db.define_table(tablename, *s3_meta_fields())
tablename = "hrm_roster_organisation"
table = db.define_table(tablename, Field('roster',db.hrm_roster), s3db.org_organisation_id())
tablename = "hrm_roster_project"
table = db.define_table(tablename, Field('roster',db.hrm_roster),  s3db.project_project_id())
tablename = "hrm_roster_site"
table = db.define_table(tablename, Field('roster',db.hrm_roster),  s3db.super_link("site_id", "org_site"),)
tablename = "hrm_roster_incident" 
table = db.define_table(tablename, Field('roster',db.hrm_roster), s3db.event_incident_id())
tablename = "hrm_roster_scenario"
table = db.define_table(tablename, Field('roster',db.hrm_roster), s3db.scenario_scenario_id())
tablename = "hrm_shift"
table = db.define_table(tablename, 
                            Field('roster',db.hrm_roster),
                            s3db.project_task_id(label=T("task")), 
                            s3db.pr_person_id(label=T("person")), 
                            Field("starttime", "datetime", label=T("start")), 
                            Field("endtime", "datetime", label=T("end"))
                        )

