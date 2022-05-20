import json
import time
import pymongo
import sys
import urllib.parse
import base64
import traceback
import random
import urllib.request
import io
import requests
import json
import hashlib

sys.path.append("pytavia_core")
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib")
sys.path.append("pytavia_storage")
sys.path.append("pytavia_modules")
sys.path.append("pytavia_modules")


from flask             import render_template_string
from flask             import render_template
from flask             import request

from pytavia_stdlib    import idgen
from pytavia_stdlib    import utils
from pytavia_core      import database
from pytavia_core      import config
from pytavia_core      import helper
from pytavia_core      import bulk_db_insert
from pytavia_core      import bulk_db_update
from pytavia_core      import bulk_db_multi

class schedule_app:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def

    def process(self, params):
        response = helper.response_msg(
            "CREATE_COMPANY_SUCCESS",
            "CREATE COMPANY SUCCESS", {},
            "0000"
        )
        if request.method == 'POST':
            data = request.form

            schedule      = data["schedule"]
            day           = data["day"]
            name_classz   = data["name-class"]
            name_teacher  = data["name-teacher"]
            name_room     = data["name-room"]
            hq_geo_lat    = float(data["lat"])
            hq_geo_lon    = float(data["lon"])
            hq_geo_pos    =  { "type" : "Point",
                              "coordinates":[hq_geo_lon,hq_geo_lat]
                            }
            

            mdl_add_new_schedule = database.new(
                self.mgdDB , "db_schedule_mahasiswa"
            )
            mdl_add_new_schedule.put( "schedule" , schedule)
            mdl_add_new_schedule.put( "day" , day)
            mdl_add_new_schedule.put( "name-class" , name_classz )
            mdl_add_new_schedule.put( "name-teacher" , name_teacher )
            mdl_add_new_schedule.put( "name-room" , name_room )
            mdl_add_new_schedule.put( "hq_geo_pos" , hq_geo_pos)

            db_handle  = database.get_database( config.mainDB )
            bulk_multi = bulk_db_multi.bulk_db_multi({
                "db_handle" : db_handle,
                "app"       : self.webapp
            })
            bulk_multi.add_action(
                bulk_db_multi.ACTION_INSERT ,
                mdl_add_new_schedule
            )

            bulk_multi.execute({})

            user_view     = self.mgdDB.db_schedule_mahasiswa.find(
                {
                    "status": {"$not":{"$regex":"DEACTIVE"}}
                }
            ).sort([("day" , 1),("schedule",1)])
            # sort([("day" , pymongo.ASCENDING),("" , pymongo.ASCENDING)])
            # ).sort("nama " , 1).skip( int(page) * int(num_per_page)).limit(
            #     int(int(page * num_per_page) + num_per_page)
            # )
            ALL_DATA     = list( user_view )

            response = render_template(
                "form-schedule.html",
                NEW_SCHEDULE    = schedule,
                NEW_DAY         = day,
                NEW_NAME_CLASS  = name_classz,
                NEW_NAME_ROOM   = name_room,
                NEW_NAME_TEACHER= name_teacher,
                ALL_DATA        = ALL_DATA
            )
        else:
            user_view     = self.mgdDB.db_schedule_mahasiswa.find(
                {
                    "status": {"$not":{"$regex":"DEACTIVE"}},
                    # "is_root": "FALSE",
                    # "pkey": {
                    #     "$nin": data_array_added
                    # }
                }
            ).sort([("day" , 1),("schedule",1)])
            # ).sort("nama " , 1).skip( int(page) * int(num_per_page)).limit(
            #     int(int(page * num_per_page) + num_per_page)
            # )
            ALL_DATA     = list( user_view )
            
            response = render_template(
                "form-schedule.html",
                ALL_DATA = ALL_DATA
            )
        
        # response = {
        #     "timestamp"         : 'now_time',
        #     "company_user_list" : 'company_user_list'
        # }
          
        return response
    # end def
# end class
