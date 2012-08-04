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
                                 Field('change_req'),
                                 *s3_meta_fields()
                        )
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
                                s3db.irs_ireport_id()
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
db.org_organisation.update_or_insert(name='OrgAlpha',organisation_type_id='2',country='IN')
db.org_organisation.update_or_insert(name='OrgBeta',organisation_type_id='2',country='IN')
db.org_organisation.update_or_insert(name='OrgGamma',organisation_type_id='2',country='IN')
db.org_organisation.update_or_insert(name='OrgDelta',organisation_type_id='2',country='IN')
db.project_project.update_or_insert(organisation_id='1',name='Project Alpha',code='Project Alpha',description='sad',status='2',start_date='2012-08-04',end_date='2012-08-23',currency='USD')
db.project_project.update_or_insert(organisation_id='2',name='Project Beta',code='Project Beta',description='',status='2',start_date='2012-07-14',end_date='2012-08-23',currency='USD')
db.project_project.update_or_insert(organisation_id='2',name='Project Gamma',code='Project Gamma',description='',status='2',start_date='2012-08-01',end_date='2012-09-23',currency='USD')
db.project_project.update_or_insert(organisation_id='2',name='Project Delta',code='Project Delta',description='',status='2',start_date='2011-08-04',end_date='2011-08-23',currency='USD')
db.project_project.update_or_insert(organisation_id='3',name='Project Epsilon',code='Project Epsilon',description='',status='2',start_date='2012-02-21',end_date='2012-08-23',currency='USD')
db.irs_ireport.update_or_insert(sit_id='1',doc_id='2',name='iAlpha',location_id='250',datetime='2012-08-04 14:55:51',affected='1228',closed=False,comments='LOL',L3='Bangalore',L1='Karnataka',L0='India')
db.irs_ireport.update_or_insert(sit_id='1',doc_id='2',name='iBeta',location_id='250',datetime='2012-04-01 14:55:51',affected='1228',closed=False,comments='LOL',L3='Bangalore',L1='Karnataka',L0='India')
db.irs_ireport.update_or_insert(sit_id='1',doc_id='2',name='iGamma',location_id='250',datetime='2012-11-24 14:55:51',affected='1228',closed=False,comments='LOL',L3='Bangalore',L1='Karnataka',L0='India')
db.irs_ireport.update_or_insert(sit_id='1',doc_id='2',name='iDelta',location_id='250',datetime='2012-10-10 14:55:51',affected='1228',closed=False,comments='LOL',L3='Bangalore',L1='Karnataka',L0='India')
tablename = "hrm_roster_type" #type: event, scenario, project etc.
table = db.define_table(tablename, Field("table_id", db.hrm_roster_table), Field('type'))

tablename = "hrm_roster_change"
table = db.define_table(tablename,
                                Field('initial_shift',db.hrm_roster_shift),
                                Field('requested_date'),
                                Field('requested_table',db.hrm_roster_shift))
