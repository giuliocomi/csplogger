#!/usr/bin/env python
# coding: utf-8

import json
from flask import Flask, request, jsonify, Response, render_template
import sqlite3
from flask_limiter import Limiter, HEADERS
from flask_limiter.util import get_remote_address
from jsonschema import validate
from costants import VALID_SCHEMA, MAX_FIELD_SIZE, DEFAULT_LIMITS

conn = sqlite3.connect('databases/csp_violations.db', check_same_thread=False)

# create database file and table, if not present
conn.execute('CREATE TABLE IF NOT EXISTS violations (cspreportblockeduri TEXT,cspreportdocumenturi,cspreportoriginalpolicy TEXT,cspreportreferrer TEXT,cspreportviolateddirective TEXT, cspreportlinenumber TEXT, cspreportcolumnnumber TEXT, cspreportsourcefile TEXT, remoteaddr TEXT, useragent TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)')


# override to get rid of the information disclosure of 'Server' header, ensure that some Security Headers are present
class empoweredHeadersFlask(Flask):
    def process_response(self, response):
         response.headers['Server'] = "CSP report-uri endpoint"
         response.headers['Strict-Transport-Security'] = "max-age=31536000;" 
         response.headers['X-Frame-Options'] = "SAMEORIGIN"
         response.headers['Content-Security-Policy'] = "style-src 'self'; script-src 'self' 'unsafe-inline'"
         response.headers['X-Content-Type-Option'] = "nosniff"
         return(response)

app = empoweredHeadersFlask(__name__)

# prevent feature abuses
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=DEFAULT_LIMITS
)
limiter.header_mapping = {
    HEADERS.LIMIT : "X-My-Limit",
    HEADERS.RESET : "X-My-Reset",
    HEADERS.REMAINING: "X-My-Remaining"
}

def validate_json(input):
        # valid log format and content to accept; the length restriction on this field is applied during the insertion in the database
       try:
            validate(input, VALID_SCHEMA)
       except:
            raise

@app.route('/log', methods=['POST'])
def log():
        cur = conn.cursor()
      
        # check if the input adheres to the schema expected
        try:
	    req_data = json.loads(request.data)
            validate_json(req_data)
        except Exception as e:
	    print(str(e))
            return "" # the less information we leak, the better!

        # save CSP violation in the database (after applying a restriction on the length of the values)
        try:
            cur.execute('INSERT INTO violations (cspreportblockeduri,cspreportdocumenturi,cspreportoriginalpolicy,cspreportreferrer,cspreportviolateddirective, cspreportlinenumber, cspreportcolumnnumber, cspreportsourcefile, remoteaddr, useragent) VALUES (?,?,?,?,?,?,?,?,?,?)', 
			(str(req_data["csp-report"]["blocked-uri"])[0:MAX_FIELD_SIZE], 
			str(req_data["csp-report"]["document-uri"])[0:MAX_FIELD_SIZE],
			str(req_data["csp-report"]["original-policy"])[0:MAX_FIELD_SIZE], 
			str(req_data["csp-report"]["referrer"])[0:MAX_FIELD_SIZE],
			str(req_data["csp-report"]["violated-directive"])[0:MAX_FIELD_SIZE], 
			str(req_data.get('csp-report', {}).get('line-number', ''))[0:MAX_FIELD_SIZE], 
			str(req_data.get('csp-report', {}).get('column-number', ''))[0:MAX_FIELD_SIZE], 
			str(req_data.get('csp-report', {}).get('source-file', ''))[0:MAX_FIELD_SIZE],
			str(request.remote_addr)[0:MAX_FIELD_SIZE], 
			str(request.user_agent)[0:MAX_FIELD_SIZE]))
            conn.commit()
        except Exception as error:
            print(str(error)) 
	    pass   
        return ""	

@app.route('/records', methods=['GET'])
def records():
        conn.row_factory = sqlite3.Row 
        cur = conn.cursor()
        entries = cur.execute('SELECT * FROM violations').fetchall()
        conn.commit()
        return jsonify([dict(ix) for ix in entries]) # jsonify sets mime-type to application/json
        
@app.route('/dashboard', methods=['GET'])
def dashboard():    
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=8443, ssl_context='adhoc')
