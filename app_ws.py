# -*- coding: utf-8 -*-
import os
from create_app import create_app
from project_ws import ProjectConfig
from flask import abort, make_response, send_file, request

from site_exts import db
from datetime import datetime

app = create_app(ProjectConfig)

@app.before_request
def log_request():
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)

    block_ip_collection = db.database.ip_black_table
    system_ip_collection = db.database.system_white_table
    temp = block_ip_collection.find_one({"ip": ip_address})
    if temp:
        return "Block IP"
    if "site_admin" in request.path:
        item = system_ip_collection.find_one({"ip": ip_address})
        if item:
            pass
        else:
            return "Not Authorized"

@app.route('/manifest_ws.json')
def manifest():
    project_static_file = os.path.join(app.static_folder, 'manifest_ws.json')
    if os.path.isdir(project_static_file.encode()):
        return abort(403)
    if os.path.exists(project_static_file.encode()):
        return make_response(send_file(project_static_file))
    return abort(404)

if __name__ == '__main__':
    app.run('0.0.0.0', port=80, debug=True)
