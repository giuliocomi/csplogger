#!/usr/bin/env python
# coding: utf-8

import json
from flask import Flask, request, jsonify, Response, render_template
import sqlite3
from flask_limiter import Limiter, HEADERS
from flask_limiter.util import get_remote_address
import jsonschema
from jsonschema import validate

conn = sqlite3.connect('databases/csp_violations.db', check_same_thread=False)

# create database file and table, if not present
conn.execute('CREATE TABLE IF NOT EXISTS violations (cspreportblockeduri TEXT,cspreportdocumenturi,cspreportoriginalpolicy TEXT,cspreportreferrer TEXT,cspreportviolateddirective TEXT, cspreportlinenumber TEXT, cspreportcolumnumber TEXT, cspreportsourcefile TEXT, remoteaddr TEXT, useragent TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)')

valid_schema = {
                    "type": "object",
                    "properties": {
                        "csp-report": {
                            "type": "object",
                            "properties": {
                                "blocked-uri": {
                                    "type": "string"
                                },
                                "document-uri": {
                                    "type": "string"
                                },
                                "original-policy": {
                                    "type": "string"
                                },
                                "referrer": {
                                    "type": "string"
                                },
                                "violated-directive": {
                                    "type": "string"
                                },
                                "line-number": {
                                    "type": "integer",
                                    "optional": True
                                },
                                "source-file": {
                                    "type": "string",
                                    "optional": True
                                },
                                "column-number": {
                                    "type": "integer",
                                    "optional": True
                                }
                            }
                        }
                    }
                }

max_field_size = 300


# override to get rid of the information disclosure of 'Server' header, ensure that some Security Headers are present
class empoweredHeadersFlask(Flask):
    def process_response(self, response):
         response.headers['Server'] = "CSP report-uri endpoint"
         response.headers['Strict-Transport-Security'] = "max-age=31536000;" 
         response.headers['X-Frame-Options'] = "SAMEORIGIN"
         response.headers['Content-Security-Policy'] = "style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'"
         response.headers['X-Content-Type-Option'] = "nosniff"
         return(response)

app = empoweredHeadersFlask(__name__)

# prevent feature abuses
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
limiter.header_mapping = {
    HEADERS.LIMIT : "X-My-Limit",
    HEADERS.RESET : "X-My-Reset",
    HEADERS.REMAINING: "X-My-Remaining"
}

def validate_json(input):
        # valid log format and content to accept; the length restriction on this field is applied during the insertion in the database
       try:
            validate(input, valid_schema)
       except:
            raise

@app.route('/log', methods=['POST'])
@limiter.limit("100/day")
def log():
        cur = conn.cursor()
        req_data = json.loads(request.data)

        # check if the input adheres to the schema expected
        try:
            validate_json(req_data)
        except jsonschema.exceptions.ValidationError as ve:
            return ""  # the less information we leak, the better!

        # save CSP violation in the database (after applying a restriction on the length of the values)
        try:
            cur.execute('INSERT INTO violations (cspreportblockeduri,cspreportdocumenturi,cspreportoriginalpolicy,cspreportreferrer,cspreportviolateddirective, cspreportlinenumber, cspreportcolumnnumber, cspreportsourcefile, remoteaddr, useragent) VALUES (?,?,?,?,?,?,?,?,?,?)', (str(req_data["csp-report"]["blocked-uri"])[0:max_field_size], str(req_data["csp-report"]["document-uri"])[0:max_field_size], str(req_data["csp-report"]["original-policy"])[0:max_field_size], str(req_data["csp-report"]["referrer"])[0:max_field_size], str(req_data["csp-report"]["violated-directive"])[0:max_field_size], str(req_data.get('csp-report', {}).get('line-number', ''))[0:max_field_size], str(req_data.get('csp-report', {}).get('column-number', ''))[0:max_field_size], str(req_data.get('csp-report', {}).get('source-file', ''))[0:max_field_size], str(request.remote_addr)[0:max_field_size], str(request.user_agent)[0:max_field_size]))
            conn.commit()
        except:
            pass    # the less information we leak, the better!
        return ""

@app.route('/records', methods=['GET'])
@limiter.limit("100/day")
def records():
        conn.row_factory = sqlite3.Row 
        cur = conn.cursor()
        entries = cur.execute('SELECT * FROM violations').fetchall()
        conn.commit()
        return jsonify([dict(ix) for ix in entries]) # jsonify sets mime-type to application/json
        
@app.route('/dashboard', methods=['GET'])
@limiter.limit("100/day")
def dashboard():    
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=8443, ssl_context='adhoc')
