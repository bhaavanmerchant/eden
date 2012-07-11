# -*- coding: utf-8 -*-
tablename = "hrm_roster"
table = db.define_table(tablename, *s3_meta_fields())
tablename = "hrm_roster_organisation"
table = db.define_table(tablename, Field('roster',db.hrm_roster), s3db.super_link("id", "org_organisation"))
tablename = "hrm_roster_project"
table = db.define_table(tablename, Field('roster',db.hrm_roster), s3db.super_link("id", "project_project"))
tablename = "hrm_roster_site"
table = db.define_table(tablename, Field('roster',db.hrm_roster),  s3db.super_link("site_id", "org_site"))
tablename = "hrm_roster_incident" 
table = db.define_table(tablename, Field('roster',db.hrm_roster), s3db.super_link("id", "event_incident"))
tablename = "hrm_roster_scenario"
table = db.define_table(tablename, Field('roster',db.hrm_roster), s3db.super_link("id", "scenario_scenario"))
tablename = "hrm_shift"
table = db.define_table(tablename, 
                            Field('roster',db.hrm_roster),
                            s3db.project_task_id(label=T("task")), 
                            s3db.pr_person_id(label=T("person")), 
                            Field("starttime", "datetime", label=T("start")), 
                            Field("endtime", "datetime", label=T("end"))
                        )

