#!flask/bin/python
import json
from flask import Flask, Response, request
from helloworld.flaskrun import flaskrun

import requests
from flask_cors import CORS
import boto3
import uuid
import simplejson as json #for json.dump to wםrk with decimal type 
import io 


application = Flask(__name__)
CORS(application, resources={r"/*": {"origins": "*"}}) 


@application.route('/', methods=['GET'])
def get():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)

@application.route('/', methods=['POST'])
def post():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)
    
    
    
@application.route('/get_customers', methods=['GET'])
def get_customers():
    data = request.data
    data_json = json.loads(data)
    uid = data_json['uid']    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    
    table = dynamodb.Table('customers')

    respponse = table.get_item(Key={
            'uid': uid,
    })
    
    return Response(json.dumps(respponse['Items']), mimetype='application/json', status=200)
    #curl -i http://"localhost:8000/get_customers"
    
    
@application.route('/add_customer', methods=['POST'])
def add_customer():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('customers')
    data = request.data
    data_json = json.loads(data)
    print(data)

    print(request.get_json())

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
 

@application.route('/sns', methods=['GET'])
def sns():
    sns = boto3.client("sns", region_name="us-east-1")
    topic_arn ="arn:aws:sns:us-east-1:332983652655:topic_name"
    print(topic_arn)

    
    sns.publish(TopicArn=topic_arn, 
            Message="message text", 
            Subject="subject used in emails only")

    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)
    
    
    
    
    
@application.route('/uploadImage', methods=['POST'])
def uploadImage():
    bucket = 'aws-project-webapp-files'
    image = request.files['image']
    s3 = boto3.resource('s3', region_name='us-east-1')
    path  = "images/%s.jpg" %  (str(uuid.uuid4()))
    
    s3.Bucket(bucket).upload_fileobj(image, path, ExtraArgs={'ACL': 'public-read', 'ContentType': 'image/jpeg'}) 
    img = 'https://aws-project-webapp-files.s3.amazonaws.com/'+ path
    return {"img": img}
 
@application.route('/uploadImageDB', methods=['POST'])
def uploadImageDB():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('users')
    data = request.data
    data_json = json.loads(data)
    user_id = data_json['uid']
    img = data_json['img']

    table.put_item(Item = {
        'uid': user_id,
        'img': img
        
    })
    return Response(json.dumps( {"success": "true"}), mimetype='application/json', status=200)


@application.route('/getUserImage', methods=['POST'])
def getUserImage():
    data = request.data
    data_json = json.loads(data)
    uid = data_json['uid']

    print(uid)

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('users')
    respponse = table.get_item(Key={
            'uid': uid,
    })
    
    img = respponse['Item']['img']
    print(img)


    return Response(json.dumps({"img": img}), mimetype='application/json', status=200)
    #curl -i http://"localhost:8000/get_customers"
    
     
if __name__ == '__main__':
    flaskrun(application)
