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

class view_full_schedule_app:

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
        user_view     = self.mgdDB.db_schedule_mahasiswa.find(
            {
                "status": {"$not":{"$regex":"DEACTIVE"}},
                # "is_root": "FALSE",
                # "pkey": {
                #     "$nin": data_array_added
                # }
            }
        ).sort("schedule" , 1)
        # ).sort("nama " , 1).skip( int(page) * int(num_per_page)).limit(
        #     int(int(page * num_per_page) + num_per_page)
        # )
        ALL_DATA     = list( user_view )
        eight = ['08:00','','','','','','','']
        nine = ['09:00','','','','','','','']
        ten = ['10:00','','','','','','','']
        one_one = ['11:00','','','','','','','']
        one_two = ['12:00','','','','','','','']
        one_three = ['13:00','','','','','','','']
        one_four = ['14:00','','','','','','','']
        one_five = ['15:00','','','','','','','']
        one_six = ['16:00','','','','','','','']
        one_seven = ['17:00','','','','','','','']
        one_eight = ['18:00','','','','','','','']
        NEW_ALL_DATA = []
        
        for data in ALL_DATA:
            if data['schedule'][:-3] == '08':       
                eight[int(data['day'])] = (data['day'],data['schedule'],data['name-room'],data['name-class'],data['name-teacher'])
            elif data['schedule'][:-3] == '09':       
                nine[int(data['day'])] = (data['day'],data['schedule'],data['name-room'],data['name-class'],data['name-teacher'])
            elif data['schedule'][:-3] == '10':       
                ten[int(data['day'])] = (data['day'],data['schedule'],data['name-room'],data['name-class'],data['name-teacher'])
            elif data['schedule'][:-3] == '11':       
                one_one[int(data['day'])] = (data['day'],data['schedule'],data['name-room'],data['name-class'],data['name-teacher'])
            elif data['schedule'][:-3] == '12':       
                one_two[int(data['day'])] = (data['day'],data['schedule'],data['name-room'],data['name-class'],data['name-teacher'])
            elif data['schedule'][:-3] == '13':       
                one_three[int(data['day'])] = (data['day'],data['schedule'],data['name-room'],data['name-class'],data['name-teacher'])
            elif data['schedule'][:-3] == '14':       
                one_four[int(data['day'])] = (data['day'],data['schedule'],data['name-room'],data['name-class'],data['name-teacher'])
            elif data['schedule'][:-3] == '15':       
                one_five[int(data['day'])] = (data['day'],data['schedule'],data['name-room'],data['name-class'],data['name-teacher'])
            elif data['schedule'][:-3] == '16':       
                one_six[int(data['day'])] = (data['day'],data['schedule'],data['name-room'],data['name-class'],data['name-teacher'])
            elif data['schedule'][:-3] == '17':       
                one_seven[int(data['day'])] = (data['day'],data['schedule'],data['name-room'],data['name-class'],data['name-teacher'])
            elif data['schedule'][:-3] == '18':       
                one_eight[int(data['day'])] = (data['day'],data['schedule'],data['name-room'],data['name-class'],data['name-teacher'])
        

        NEW_ALL_DATA.append(eight)
        NEW_ALL_DATA.append(nine)
        NEW_ALL_DATA.append(ten)
        NEW_ALL_DATA.append(one_one)
        NEW_ALL_DATA.append(one_two)
        NEW_ALL_DATA.append(one_three)
        NEW_ALL_DATA.append(one_four)
        NEW_ALL_DATA.append(one_five)
        NEW_ALL_DATA.append(one_six)
        NEW_ALL_DATA.append(one_seven)
        NEW_ALL_DATA.append(one_eight)
       
        response = render_template(
            "full-schedule.html",
            ALL_DATA = NEW_ALL_DATA
        )
        
        # response = {)
        #     "timestamp"         : 'now_time',
        #     "company_user_list" : 'company_user_list'
        # }
          
        return response
    # end def
# end class
