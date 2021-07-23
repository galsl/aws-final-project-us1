#!flask/bin/python
import json
from flask import Flask, Response, request
from helloworld.flaskrun import flaskrun

import requests
from flask_cors import CORS
import boto3
import uuid
import simplejson as json #for json.dump to wirk with decimal type 


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
    print(resp['Items'])

    return Response(json.dumps(resp['Items']), mimetype='application/json', status=200)
    #curl -i http://"localhost:8000/get_customers"
    
    
@application.route('/add_customer', methods=['POST'])
def add_customer():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('customers')
    data = request.data
    data_json = json.loads(data)
    print(data)

    print(request.get_json())
    print("sad")

    customer_uuid = (str(uuid.uuid4()))
    data_json['id'] = customer_uuid
    print(id)
    table.put_item(Item=data_json)
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)
#curl -i -X POST -H "Content-Type: application/json" -d '{"id": "4b53d831-838c-4a00-91ae-0fb7d671df15"}' http://localhost:8000/add_customer        


@application.route('/delete_customer', methods=['POST'])
def delete_customer():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('customers')
    data = request.data
    data_json = json.loads(data)
    customer_id = data_json['id']

    response = table.delete_item(
        Key={
            'id': customer_id,
        }
    )

    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)
    
    
@application.route('/edit_customer', methods=['POST'])
def edit_customer():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('customers')
    data = request.data
    data_json = json.loads(data)
    print(id)
    table.put_item(Item=data_json)
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)
 
    
if __name__ == '__main__':
    flaskrun(application)
