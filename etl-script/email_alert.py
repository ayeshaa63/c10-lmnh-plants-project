"""send an email to users outlining any plants where theres been sensor failures"""

import boto3
from botocore.exceptions import ClientError
from datetime import datetime
from os import environ as ENV
from dotenv import load_dotenv


def create_message(sensor_failures: list[str]) -> str:
    """Creates the message for emails"""

    message = """<h1 style="font-weight: bold;text-decoration: underline;">Sensor Failures</h1>"""
    for failure in sensor_failures:
        message += f"""<h3>{failure}</h3> """

    message = message.replace("\n", "")

    return message


def get_to_emails():
    """gets the emails of the recipients and in this case us"""

    nathan_email = ENV['NATHAN_EMAIL']
    dana_email = ENV['DANA_EMAIL']
    howard_email = ENV['HOWARD_EMAIL']
    ayesha_email = ENV['AYESHA_EMAIL']

    return [nathan_email, dana_email, howard_email, ayesha_email]


def send_email(sensor_failures: list[str]):
    """sends an email report of plant sensor faults using AWS SES"""
    current_datetime = datetime.now()
    region = ENV['REGION']
    ses = boto3.client('ses', region_name=region)
    from_email = ENV['NATHAN_EMAIL']

    message = create_message(sensor_failures)
    to_emails = get_to_emails()
    subject = f"Sensor Failures @{current_datetime}"

    try:
        response = ses.send_email(
            Destination={
                'ToAddresses': to_emails,
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': 'UTF-8',
                        'Data': f'{message}',
                    },
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': f"{subject}",
                },
            },
            Source=from_email,
        )
    except ClientError as e:
        print("Error sending email:", e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:", response['MessageId'])


if __name__ == '__main__':
    load_dotenv()
    msg = ['ERROR :: PLANT 3 :: plant sensor fault ::',
           'ERROR :: PLANT 8 :: plant sensor fault ::']
    send_email(msg)
