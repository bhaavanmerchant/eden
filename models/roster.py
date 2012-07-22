# -*- coding: utf-8 -*-
#tablename = "hrm_roster_slots"
#table = db.define_table(tablename, Field('event'), Field('event_id'), Field('slot'))
tablename = "hrm_roster_table"
table = db.define_table(tablename, 
                                Field('week'), 
                                Field('slot')
                        )
#db.hrm_roster_table.insert(week='21', slot='1')
tablename = "hrm_roster"
table = db.define_table(tablename, 
#                                Field('roster_table',
#                                    db.hrm_roster_table),
                                 *s3_meta_fields())
tablename = "hrm_roster_organisation"
table = db.define_table(tablename, 
                                Field('roster',db.hrm_roster), 
                                #s3db.super_link("id", "org_organisation")
                                s3db.org_organisation_id()
                        )
tablename = "hrm_roster_project"
table = db.define_table(tablename, 
                                Field('roster',db.hrm_roster), 
                                #s3db.super_link("id", "project_project")
                                s3db.project_project_id()
                        )
tablename = "hrm_roster_site"
table = db.define_table(tablename, 
                                Field('roster',db.hrm_roster), 
                                s3db.super_link("site_id", "org_site")
                        )
tablename = "hrm_roster_incident" 
table = db.define_table(tablename, 
                                Field('roster',db.hrm_roster), 
                                #s3db.super_link("id", "event_incident")
                                s3db.event_incident_id()
                        )
tablename = "hrm_roster_scenario"
table = db.define_table(tablename, 
                                Field('roster',db.hrm_roster), 
                                #s3db.super_link("id", "scenario_scenario")
                                s3db.scenario_scenario_id()
                        )
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
db.hrm_roster_table.update_or_insert(week="1", slot="1")
db.pr_person.update_or_insert(first_name='Mari', last_name='Hargis', gender=3, age_group=1, volunteer=True)
db.pr_person.update_or_insert(first_name='Ismael', last_name='Nolin', gender=3, age_group=1, volunteer=True)
db.pr_person.update_or_insert(first_name='Sherry', last_name='Febres', gender=3, age_group=1, volunteer=True)
db.pr_person.update_or_insert(first_name='Barabara', last_name='Gamino', gender=3, age_group=1, volunteer=True)
db.pr_person.update_or_insert(first_name='Augustina', last_name='Northam', gender=3, age_group=1, volunteer=True)
db.pr_person.update_or_insert(first_name='Artie', last_name='Timms', gender=3, age_group=1, volunteer=True)
db.pr_person.update_or_insert(first_name='Kimberely', last_name='Lamey', gender=3, age_group=1, volunteer=True)
db.pr_person.update_or_insert(first_name='Ignacio', last_name='Crumble', gender=3, age_group=1, volunteer=True)
db.pr_person.update_or_insert(first_name='Vinnie', last_name='Launius', gender=3, age_group=1, volunteer=True)
db.pr_person.update_or_insert(first_name='Roxane', last_name='Cremin', gender=3, age_group=1, volunteer=True)
db.hrm_job_role.update_or_insert(name='Team Leader')
db.hrm_job_role.update_or_insert(name='Team Member')
db.hrm_job_role.update_or_insert(name='Trainee')
db.hrm_person_role.update_or_insert(job_role_id='1', person_id='12')
db.hrm_person_role.update_or_insert(job_role_id='1', person_id='13')
db.hrm_person_role.update_or_insert(job_role_id='1', person_id='14')
db.hrm_person_role.update_or_insert(job_role_id='1', person_id='15')
db.hrm_person_role.update_or_insert(job_role_id='1', person_id='16')
db.hrm_person_role.update_or_insert(job_role_id='2', person_id='14')
db.hrm_person_role.update_or_insert(job_role_id='2', person_id='15')
db.hrm_person_role.update_or_insert(job_role_id='2', person_id='16')
db.hrm_person_role.update_or_insert(job_role_id='2', person_id='17')
db.hrm_person_role.update_or_insert(job_role_id='2', person_id='18')
db.hrm_person_role.update_or_insert(job_role_id='3', person_id='21')
db.hrm_person_role.update_or_insert(job_role_id='3', person_id='16')
db.hrm_person_role.update_or_insert(job_role_id='3', person_id='17')
db.hrm_person_role.update_or_insert(job_role_id='3', person_id='18')
db.hrm_person_role.update_or_insert(job_role_id='3', person_id='19')
db.hrm_person_role.update_or_insert(job_role_id='3', person_id='20')

tablename = "hrm_roster_type" #type: event, scenario, project etc.
table = db.define_table(tablename, Field("table_id", db.hrm_roster_table), Field('type'))

