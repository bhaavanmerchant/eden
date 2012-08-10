## -*- coding: utf-8 -*-
tablename = "hrm_roster_table"
table = db.define_table(tablename, 
                                Field('occasion'),
                                Field('week'), 
                                Field('slot'),
                                s3db.project_project_id()
                        )

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
                                 Field('change_req'),
                                 *s3_meta_fields()
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

#tablename = "hrm_roster_change"
#table = db.define_table(tablename,
#                                Field('initial_shift',db.hrm_roster_shift),
#                                Field('requested_date'),
#                                Field('requested_table',db.hrm_roster_shift))
