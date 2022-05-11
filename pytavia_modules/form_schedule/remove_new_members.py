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

from pytavia_stdlib    import idgen
from pytavia_stdlib    import utils
from pytavia_core      import database
from pytavia_core      import config
from pytavia_core      import helper
from pytavia_core      import bulk_db_insert
from pytavia_core      import bulk_db_update
from pytavia_core      import bulk_db_multi

class remove_new_members:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def

    def process(self, params):
        response = helper.response_msg(
            "REMOVE_USER_SUCCESS",
            "REMOVE USER SUCCESS", {},
            "0000"
        )
        # myclient = pymongo.MongoClient("localhost",27017)
        # mydb = myclient["haiii"]
        # mycol = mydb["customers"]

        # mydict = { "name": "John", "address": "Highway 37" }

        # x = mycol.insert_one(mydict)        
        try:
            fk_user_id    = params["pkey"]
            self.mgdDB.db_members.update_one(
                { "pkey"          : fk_user_id },
                { "$set"          : { "status"   : "yuk DEACTIVE" }} 
            )
            user_rec = self.mgdDB.db_members.find_one({
                "pkey"   : fk_user_id 
            })
            del user_rec["_id"]
            response.put( "data" , {
                "fk_user_id" : fk_user_id ,
                "user"       : user_rec   ,
                "status"     : "TELAH DEACTIVE"
            })
        except:
            self.webapp.logger.debug(traceback.format_exc())
            response.put( "status"      ,  "gagal" )
            response.put( "desc"        ,  "gagal boy" )
            response.put( "status_code" ,  "9999" )
        # end try
        return response
    # end def
# end class
