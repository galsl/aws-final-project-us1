#!flask/bin/python
import json
from flask import Flask, Response, request
from helloworld.flaskrun import flaskrun

import requests
from flask_cors import CORS
import boto3
import uuid



application = Flask(__name__)
# for CORS support (requirements update  + app import CORS required)
CORS(application, resources={r"/*": {"origins": "*"}}) 


@application.route('/', methods=['GET'])
def get():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)

@application.route('/', methods=['POST'])
def post():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)
    
    
    
@application.route('/get_customers', methods=['GET'])
def get_customers():
    data = request.get_json()
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('customers')
    # replace table scan
    resp = table.scan()
    print(str(resp))
    return Response(json.dumps(str(resp['Items'])), mimetype='application/json', status=200)
    #curl -i http://"localhost:8000/get_customers"
    
    
@application.route('/add_customer', methods=['POST'])
def add_customer():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('customers')
    data = request.data
    data_dict = json.loads(data)
    customer_uuid = (str(uuid.uuid4()))
    data_dict['id'] = customer_uuid
    print(id)
    table.put_item(Item=data_dict)
    
    
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)
        

if __name__ == '__main__':
    flaskrun(application)
