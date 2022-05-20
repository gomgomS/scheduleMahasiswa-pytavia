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

from pymongo           import MongoClient, GEO2D
from bson.son          import SON

from pytavia_stdlib    import idgen
from pytavia_stdlib    import utils
from pytavia_core      import database
from pytavia_core      import config
from pytavia_core      import helper
from pytavia_core      import bulk_db_insert
from pytavia_core      import bulk_db_update
from pytavia_core      import bulk_db_multi

class filter_schedule_app:

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

        data = request.form

        name_fields_search    = data["name_fields_search"]        
        # near
        if name_fields_search == 'range_location':
            lon = float(data['lon'])
            lat = float(data['lat'])
            range_loc = float(data['search'])

            # return str([lat,lon,range_loc])   

            user_view = self.mgdDB.db_schedule_mahasiswa.find(
                {
                    "status": {"$not":{"$regex":"DEACTIVE"}},
                    "hq_geo_pos":{"$nearSphere" : {"$geometry":{'type':"point","coordinates":[lon,lat]},"$maxDistance":range_loc}}
                    # "hq_geo_pos": SON([("$near", [lon,lat]),("$maxDistance",range_loc)])
                }
            ).sort([("day" , 1),("schedule",1)])  
        # text
        elif name_fields_search == 'elastic':
            search                = data["search"]

            if search == 'senin':
                search = search + ' 2'
            elif search == 'minggu':
                search = search + ' 1' 
            elif search == 'selasa':
                search = search + ' 3'
            elif search == 'rabu':
                search = search + ' 4'
            elif search == 'kamis':
                search = search + ' 5'
            elif search == 'jumat':
                search = search + ' 6' 
            elif search == 'sabtu':
                search = search + ' 7'            
            else:
                search = search
         
            self.mgdDB.db_schedule_mahasiswa.create_index([
                    ("day","text"),("schedule","text"),("name-room","text"),
                    ("name-class","text"),("name-teacher","text")
                ]
            )

            user_view = self.mgdDB.db_schedule_mahasiswa.find(
                {
                    "status": {"$not":{"$regex":"DEACTIVE"}},
                    "$text": {"$search": search}
                }
            ).sort([("day" , 1),("schedule",1)])            
        # index
        else:
            if data.get("search_day"):
                search                = data["search_day"]
            else:
                search                = data["search"]            

            self.mgdDB.db_schedule_mahasiswa.create_index([
                    (name_fields_search,1)
                ]
            )
        
            user_view = self.mgdDB.db_schedule_mahasiswa.find(
                {
                    "status": {"$not":{"$regex":"DEACTIVE"}},
                    name_fields_search:search
                    # "is_root": "FALSE",
                    # "pkey": {
                    #     "$nin": data_array_added
                    # }
                }
            ).sort([("day" , 1),("schedule",1)])
       
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
