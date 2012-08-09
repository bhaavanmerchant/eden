## -*- coding: utf-8 -*-
##tablename = "hrm_roster_slots"
##table = db.define_table(tablename, Field('event'), Field('event_id'), Field('slot'))
tablename = "hrm_roster_table"
table = db.define_table(tablename, 
                                Field('occasion'),
                                Field('week'), 
                                Field('slot'),
                                s3db.project_project_id()
                        )
##tablename = "hrm_roster_event"
##table = db.define_table(tablename,
##                                Field('occasion'),
##                
##                        )
##tablename = "hrm_roster_date"
##table = db.define_table(tablename,
##                            Field('type'),
##                            #Field('foreign_key'),
##                            Field('start_date','datetime'),
##                            s3db.project_project_id()
##                        )
##db.hrm_roster_table.insert(week='21', slot='1')
tablename = "hrm_roster"
table = db.define_table(tablename, 
#                                Field('roster_table',
#                                    db.hrm_roster_table),
                                 Field('change_req'),
                                 *s3_meta_fields()
                        )
##tablename = "hrm_roster_organisation"
##table = db.define_table(tablename, 
##                                Field('roster',db.hrm_roster), 
##                                #s3db.super_link("id", "org_organisation")
##                                s3db.org_organisation_id()
##                        )
##tablename = "hrm_roster_project"
##table = db.define_table(tablename, 
##                                Field('roster',db.hrm_roster), 
##                                #s3db.super_link("id", "project_project")
##                                s3db.project_project_id()
##                        )
##tablename = "hrm_roster_site"
##table = db.define_table(tablename, 
##                                Field('roster',db.hrm_roster), 
##                                s3db.super_link("site_id", "org_site")
##                        )
##tablename = "hrm_roster_incident" 
##table = db.define_table(tablename, 
##                                Field('roster',db.hrm_roster), 
##                                #s3db.super_link("id", "event_incident")
##                                s3db.irs_ireport_id()
##                        )
##tablename = "hrm_roster_scenario"
##table = db.define_table(tablename, 
##                                Field('roster',db.hrm_roster), 
##                                #s3db.super_link("id", "scenario_scenario")
##                                s3db.scenario_scenario_id()
##                        )
tablename = "hrm_roster_shift"
table = db.define_table(tablename,
                            Field("roster_id",db.hrm_roster),
                            Field("table_id",db.hrm_roster_table),
                            Field("date"),
                            Field("role"),
                            s3db.pr_person_id()
                        )

tablename = "hrm_roster_roles" #roles: volunteer, team leader etc. defined for a table.
table = db.define_table(tablename, Field("table_id", db.hrm_roster_table), Field('roles'), Field('position_in_table','integer'))

tablename = "hrm_person_role" #Clarification needed if the naming of this is apt or should be changed ?
table = db.define_table(tablename, s3db.hrm_job_role_id(), s3db.pr_person_id())



#tablename = "hrm_roster_change"
#table = db.define_table(tablename,
#                                Field('initial_shift',db.hrm_roster_shift),
#                                Field('requested_date'),
#                                Field('requested_table',db.hrm_roster_shift))
