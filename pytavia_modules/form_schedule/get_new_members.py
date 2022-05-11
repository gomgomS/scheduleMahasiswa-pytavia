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
import random

sys.path.append("pytavia_core")
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib")
sys.path.append("pytavia_storage")
sys.path.append("pytavia_modules")

from datetime           import datetime
from pytavia_stdlib     import idgen
from pytavia_stdlib     import utils
from pytavia_core       import database
from pytavia_core       import config
from pytavia_core       import helper
from pytavia_core       import bulk_db_insert
from pytavia_core       import bulk_db_update
from pytavia_core       import bulk_db_multi

class get_new_members:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def

    def process(self, params):
        response = helper.response_msg(
            "GET_NEW_MEMBERS_SUCCESS",
            "GET NEW MEMBERS SUCCESS", {},
            "0000"
        )
        try:
            page          = float(1)
            num_per_page  = float(1)
            now_time      = int(time.time() * 1000)

            user_view     = self.mgdDB.db_members.find(
            ).sort("nama " , 1).skip( int(page) * int(num_per_page)).limit(
                int(int(page * num_per_page) + num_per_page)
            )
            company_user_list     = list( user_view )
            response.put( "data" , {
                "timestamp"         : now_time,
                "company_user_list" : company_user_list
            })
        except:
            self.webapp.logger.debug(traceback.format_exc())
            response.put( "status"      ,  "GET_USER_LIST_FAILED" )
            response.put( "desc"        ,  "GENERAL ERROR" )
            response.put( "status_code" ,  "9999" )
        # end try
        return response
    # end def
# end class
