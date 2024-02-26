from __future__ import print_function
import json, os, logging, boto3
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
print('Loading function')

def lambda_handler(event, context):
    logger.info("Request from Bedrock: {}".format(json.dumps(event, indent=4, sort_keys=True)))
    parameters = {item['name']:item for item in event["parameters"]}
    logger.info("parameters: {}".format(json.dumps(parameters, indent=4, sort_keys=True)))
    email_draft = {
        "ToAddress": parameters['RecipientEmailAddress']["value"],
        "FromAddress": os.environ['SenderIdentity'],
        "Body": parameters['Body']["value"],
        "Subject": parameters['Subject']["value"]
        }
    
    #send-email. SES identity is configured beforehand
    client = boto3.client('ses', region_name='us-east-1')
    
    logger.info("Sending email to "+ email_draft["ToAddress"])
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [email_draft["ToAddress"]]
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': 'UTF-8',
                        'Data': email_draft["Body"],
                    }
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': email_draft["Subject"],
                },
            },
            Source=os.environ['SenderIdentity']
        )
    except ClientError as e:
        logger.info("AWS SNS Send Email Response {}".format(json.dumps(response, indent=4, sort_keys=True))) 
        lambda_response = {
        "messageVersion": "1.0", 
        "response":{
            "actionGroup": event['actionGroup'], 
            "apiPath": event['apiPath'],
            "httpMethod": event['httpMethod'],
            "httpStatusCode": 503,
            "responseBody": {
                "application/json": {
                    "body":{
                      "snsStatusCode":e.response['ResponseMetadata']['HTTPStatusCode'],
                      "snsError": e.response['Error']['Code']
                  }
                }
            }
        }
    }
        return lambda_response
        
        
    logger.info("AWS SNS Send Email Response {}".format(json.dumps(response, indent=4, sort_keys=True))) 

    
    lambda_response = {
        "messageVersion": "1.0", 
        "response":{
            "actionGroup": event['actionGroup'], 
            "apiPath": event['apiPath'],
            "httpMethod": event['httpMethod'],
            "httpStatusCode": 200,
            "responseBody": {
                "application/json": {
                    "body":{
                      "Response": "Email Sent Successfully. MessageId is: {} ".format(response['MessageId']),
                      "Sender": os.environ['SenderIdentity'],
                      "Recipient": email_draft["ToAddress"],
                      "Subject": email_draft["Subject"],
                      "Body": email_draft["Body"]
                  }
                }
            }
        }
    }

    logger.info("Email sent successfully. here is what was sent: {}".format(json.dumps(lambda_response, indent=4, sort_keys=True)))
    
    return lambda_response
    