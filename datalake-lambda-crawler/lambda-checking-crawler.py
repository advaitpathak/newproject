import boto3
import json
from botocore.config import Config

# standard mode handles retries on additional exceptions
config = Config(
    retries={
        'max_attempts': 10,
        'mode': 'standard'
    }
)

glue = boto3.client('glue', config=config)
sfn = boto3.client('stepfunctions', config=config)


def handler(event, context):
    crawler_name = event.get("CrawlerName")
    activity = event.get("ActivityArn")
    print("INFO: crawler_name : " + crawler_name)
    print("INFO: ActivityArn : " + activity)
    print("INFO: Starting Glue Crawler")

    try:
        start_crawler_response = glue.start_crawler(Name=crawler_name)
    except glue.exceptions.CrawlerRunningException as exception:
        print(f'ERROR: Crawler in progress - {exception}')
    # todo::check if this logic is needed
    except Exception as exception:
        # send activity failure token
        # task = sfn.get_activity_task(activityArn=activity, workerName='InvokeCrawlerWorker')
        # response = sfn.send_task_failure(taskToken=task['taskToken'], output=json.dumps(event))
        print(f'ERROR: Problem while invoking crawler - {exception}')

    return event


if __name__ == '__main__':
    event = {
        'Comment': 'Invoking crawler from SF to catch error',
        'CrawlerName': 'TDL-LAN-CMBS-Prop-RPT-dev',
        'ActivityArn': 'arn:aws:states:us-east-1:040890314520:activity:cmbs-user-perm-activity-dev'
    }
    context = None
    handler(event, context)


# import boto3
# import json
#
# client = boto3.client('glue')
# glue = boto3.client(service_name='glue', region_name='us-east-1',
#                     endpoint_url='https://glue.us-east-1.amazonaws.com')
# # step-fn-activity
# client_sf = boto3.client('stepfunctions')
#
#
# # crawler_name="TDL-LAN-CMBS-Bond"CrawlerName
# def lambda_handler(event, context):
#     print('event : ', [event])
#     # eventinfo = json.loads(event)
#     # print(eventinfo)
#     crawler_name = event.get("CrawlerName")
#     activity = event.get("ActivityArn")
#     print("crawler_name : " + crawler_name)
#     print("ActivityArn : " + activity)
#     print("Starting Glue Crawler")
#
#     class CrawlerException(Exception):
#         pass
#
#     try:
#         response = client.start_crawler(Name=crawler_name)
#     except CrawlerRunningException as c:
#         raise CrawlerException('Crawler In Progress!')
#         print('Crawler in progress')
#     except Exception as e:
#         # send activity failure token
#         task = client_sf.get_activity_task(activityArn=activity, workerName='InvokeCrawlerWorker')
#         print(task)
#         response = client_sf.send_task_failure(taskToken=task['taskToken'], output=json.dumps(event))
#         print('Problem while invoking crawler')
#
#     return event
