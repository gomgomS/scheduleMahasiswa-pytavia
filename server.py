import json
import time
import pymongo
import sys
import urllib.parse
import base64

sys.path.append("pytavia_core"    ) 
sys.path.append("pytavia_settings") 
sys.path.append("pytavia_stdlib"  ) 
sys.path.append("pytavia_storage" ) 
sys.path.append("pytavia_modules" ) 
sys.path.append("pytavia_modules/rest_api_controller")
sys.path.append("pytavia_modules/form_schedule") 
sys.path.append("pytavia_modules/full_schedule") 

# adding comments
from pytavia_stdlib  import utils
from pytavia_core    import database 
from pytavia_core    import config 
from pytavia_core    import model
from pytavia_stdlib  import idgen 

from rest_api_controller import module1 

from form_schedule import schedule_app
from form_schedule import delete_schedule_app
from form_schedule import edit_schedule_app
from form_schedule import filter_schedule_app

from full_schedule import view_full_schedule_app

##########################################################

from flask import request
from flask import render_template
from flask import Flask
from flask import session
from flask import make_response
from flask import redirect
from flask import url_for
from flask import flash


from flask_wtf.csrf import CSRFProtect
from flask_wtf.csrf import CSRFError
#
# Main app configurations
#
app             = Flask( __name__, config.G_STATIC_URL_PATH )
# csrf            = CSRFProtect(app)
app.secret_key  = config.G_FLASK_SECRET
app.db_update_context, app.db_table_fks = model.get_db_table_paths(model.db)

########################## CALLBACK API ###################################

@app.route("/hi", methods=["GET"])
def api_hi():
    return 'check conn!!'
# end def

@app.route("/formschedule", methods=["POST","GET"])
def form():
    params = request.args.to_dict()
    response = schedule_app.schedule_app(app).process( params )
    return response
# end def

@app.route("/fullschedule", methods=["GET"])
def viewfull():
    params = request.args.to_dict()
    response = view_full_schedule_app.view_full_schedule_app(app).process( params )
    return response
# end def

@app.route("/filter", methods=["POST"])
def viewfilter():
    params = request.args.to_dict()
    response = filter_schedule_app.filter_schedule_app(app).process( params )
    return response
# end def

@app.route("/deleteschedule", methods=["POST"])
def deleteform():
    params = request.args.to_dict()
    response = delete_schedule_app.delete_schedule_app(app).process( params )
    return response
# end def

@app.route("/editschedule", methods=["POST"])
def editform():
    params = request.args.to_dict()
    response = edit_schedule_app.edit_schedule_app(app).process( params )
    return response
# end def

# @app.route("/updateschedule", methods=["POST"])
# def updateform():
#     params = request.args.to_dict()
#     response = update_schedule_app.update_schedule_app(app).process( params )
#     return response
# # end def

@app.route("/v1/api/api-v1", methods=["GET"])
def api_v1():
    params = request.args.to_dict()
    response = module1.module1(app).process( params )
    return response.stringify_v1()
# end def

@app.route("/v1/api/api-post-v1", methods=["POST"])
def api_post_v1():
    params = request.form.to_dict()
    response = module1.module1(app).process( params )
    return response.stringify_v1()
# end def

### Sample generic endpoints
"""
# TODO: update example using new db actions
### sample generic archive -- archive book
@app.route("/process/book/archive", methods=["POST"])
def book_proc_archive():
    params = request.form.to_dict()
    response = generic_proc.generic_proc(app).archive({
        "collection"    : "db_book",
        "pkey"          : params["pkey"]
    })

    if response.get('status_code') == config.G_STATUS['SUCCESS']['CODE']:
        return response.http_stringify()
    else:
        return response.http_stringify()

### sample generic restore -- restore book
@app.route("/process/book/restore", methods=["POST"])
def book_proc_restore():
    params = request.form.to_dict()
    response = generic_proc.generic_proc(app).restore({
        "collection"    : "db_book",
        "pkey"          : params["pkey"]
    })

    if response.get('status_code') == config.G_STATUS['SUCCESS']['CODE']:
        return response.http_stringify()
    else:
        return response.http_stringify()

### sample two way reference -- reference book to author and author to book
@app.route("/process/book/add_author", methods=["POST"])
def book_proc_add_author():
    params = request.form.to_dict()
    response = generic_proc.generic_proc(app).add_two_way_reference({
        "main"  : {
            "collection"    : "db_book",
            "pkey"          : params["book_pkey"]
        },  
        "sub"  : {
            "collection"    : "db_author",
            "pkey"          : params["author_pkey"]
        }
    })

    if response.get('status_code') == config.G_STATUS['SUCCESS']['CODE']:
        return response.http_stringify()
    else:
        return response.http_stringify()

### sample remove two way reference -- dereference book to author and vise versa
@app.route("/process/book/remove_group", methods=["POST"])
def book_proc_remove_group():
    params = request.form.to_dict()
    response = generic_proc.generic_proc(app).remove_two_way_reference({
        "main"  : {
            "collection"    : "db_book",
            "pkey"          : params["book_pkey"]
        },  
        "sub"  : {
            "collection"    : "db_author",
            "pkey"          : params["author_pkey"]
        }
    })

    if response.get('status_code') == config.G_STATUS['SUCCESS']['CODE']:
        return response.http_stringify()
    else:
        return response.http_stringify()
"""