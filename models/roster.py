## -*- coding: utf-8 -*-
event_types = Storage(
                project_project = T("Project"),
                irs_ireport = T("Incident"),
                scenario_scenario = T("Scenario"),
                org_organisation = T("Organisation"),
                #org_site = T("Site")
                )

tablename = "hrm_roster_event"
table = s3db.super_entity(tablename, "roster_event_id",
                            event_types,
                              Field("name")
                        )
tablename = "hrm_roster_slots"
table = db.define_table(tablename,
                            Field('slot1'),
                            Field('slot2'),
                            Field('slot3'),
                            Field('slot4'),
                            Field('slot5')
                        )
tablename = "hrm_roster_table"
table = db.define_table(tablename,
                                Field('type'), 
                                Field('start_date',"datetime"), 
                                Field('slots_id',db.hrm_roster_slots),
                                s3db.super_link("roster_event_id", "hrm_roster_event"),
                        )
s3db.configure(table, super_entity = db.hrm_roster_event)
s3db.add_component(table, hrm_roster_event=s3db.super_key(db.hrm_roster_event))
tablename = "hrm_roster_instance"
table = db.define_table(tablename,
                            Field("table_id",db.hrm_roster_table),
                            Field('week'),
                            Field('slot')
                        )
tablename = "hrm_roster"
table = db.define_table(tablename, 
                                 Field('change_req'),
                                 *s3_meta_fields()
                        )
tablename = "hrm_roster_shift"
table = db.define_table(tablename,
                            Field("roster_id",db.hrm_roster),
                            Field("instance_id",db.hrm_roster_instance),
                            Field("date"),
                            Field("role"),
                            Field("slot_level"),
                            s3db.pr_person_id()
                        )
tablename = "hrm_roster_roles" #roles: volunteer, team leader etc. defined for a table.
table = db.define_table(tablename, Field("instance_id", db.hrm_roster_instance), Field('roles'), Field('position_in_table','integer'))

tablename = "hrm_roster_change"
table = db.define_table(tablename,
                                Field('initial_shift',db.hrm_roster_shift),
                                Field('requested_date'),
                                Field('requested_table',db.hrm_roster_shift)
                        )
