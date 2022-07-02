import boto3
from botocore.config import Config


my_config = Config(
    region_name = 'us-west-2',
    signature_version = 'v4',
)


def get_machine_time():
    return 1602824750094  # No need to implement at the moment


def check_aws_connection():
    # TODO: implement real call to aws describe instances. If successful, return true. otherwise return False
    ec2 = boto3.client('ec2', config=my_config)
    try:
        response = ec2.describe_instances()
        return True
    except:
        return False



def check_db_connection():
    # TODO: implement real select query to db. If successful, return true. otherwise return False
    return True


def is_app_healthy(healthchecks):
    return all([check["Value"] for check in healthchecks])


def get_app_health():
    health_checks = [
        {"Name": "machine-time", "Value": get_machine_time()},
        {"Name": "aws-connection", "Value": check_aws_connection()},
        {"Name": "db-connection", "Value": check_db_connection()},
    ]
    return health_checks, is_app_healthy(health_checks)


check_aws_connection()
