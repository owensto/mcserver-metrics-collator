import json
from mcstatus import MinecraftServer
import boto3
from datetime import datetime
import pytz

# import requests

#initialize dynamoDB + table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ServerStats1-MySimpleTable-PNGW3TAVC5MR')


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    # serverInput = event["queryStringParameters"]["serverIP"]
    # print(serverInput)
    # print("----------------------------------")
    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    #initialize variables
    server = MinecraftServer.lookup("play.gemcraftmc.net")
    status = server.status()
    playerCount = str(status.players.online)
    timeStamp = str(datetime.now(pytz.timezone('US/Eastern')))
    #deposit data in tables
    table.put_item(
        Item={
            'timeStamp' : timeStamp,
            'players' : playerCount,
        }
    )
    print(playerCount)
    return {
        "statusCode": 200,
        "body": json.dumps({
            'timeStamp' : timeStamp,
            'players' : playerCount,
 #           'serverIP' : server,
            # "location": ip.text.replace("\n", "")
        }),
    }
