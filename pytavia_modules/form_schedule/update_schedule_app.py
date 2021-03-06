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
from flask             import redirect

from pytavia_stdlib    import idgen
from pytavia_stdlib    import utils
from pytavia_core      import database
from pytavia_core      import config
from pytavia_core      import helper
from pytavia_core      import bulk_db_insert
from pytavia_core      import bulk_db_update
from pytavia_core      import bulk_db_multi

class edit_schedule_app:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def

    def process(self, params):
        response = helper.response_msg(
            "EDIT_NEW_MEMBERS",
            "EDIT NEW MEMBERS", {},
            "0000"
        )
        data = request.form

        data_edit     = self.mgdDB.db_schedule_mahasiswa.find_one(
            {
                "pkey": data['edit-data']
            }
        )
        
        schedule      = data_edit["schedule"]
        name_classz   = data_edit["name-class"]
        name_teacher  = data_edit["name-teacher"]
        name_room     = data_edit["name-room"]

        # ).sort("nama " , 1).skip( int(page) * int(num_per_page)).limit(
        #     int(int(page * num_per_page) + num_per_page)
        # )

        response = render_template(
            "form-schedule.html",
            NEW_SCHEDULE = schedule,
            NEW_NAME_CLASS    = name_classz,
            NEW_NAME_ROOM  = name_room,
            NEW_NAME_TEACHER    = name_teacher,
            TYPE    = 'EDIT',
        )
        return response

        # schedule      = data["schedule"]
        # name_classz   = data["name-class"]
        # name_teacher  = data["name-teacher"]
        # name_room     = data["name-room"]
        
        # self.mgdDB.db_members.update_one(
        #     { "pkey" : id },
        #     { "$set" : {
        #         "nama" : nama,
        #         "kota" : kota,
        #         "no_kamar" : no_kamar,
        #     }}
        # )
        # response.put( "data" , {
        #     "nama" : nama,
        #     "kota" : kota,
        #     "no_kamar" : no_kamar,
        #     "ne param" : id
        # })
        # except:
        #     self.webapp.logger.debug(traceback.format_exc())
        #     response.put( "status"      ,  "gagal" )
        #     response.put( "desc"        ,  "gagal boy" )
        #     response.put( "status_code" ,  "9999" )
        # end try
        return response
    # end def
# end class
