from boto3 import client

SAMPLE_INSTANCE_DATA = {
    'Instances': [
        {'Cloud': 'aws', 'Region': 'us-east-1', 'Id': 'i-53d13a927070628de', 'Type': 'a1.2xlarge',
         'ImageId': 'ami-03cf127a',
         'LaunchTime': '2020-10-13T19:27:52.000Z', 'State': 'running',
         'StateReason': None, 'SubnetId': 'subnet-3c940491', 'VpcId': 'vpc-9256ce43',
         'MacAddress': '1b:2b:3c:4d:5e:6f', 'NetworkInterfaceId': 'eni-bf3adbb2',
         'PrivateDnsName': 'ip-172-31-16-58.ec2.internal', 'PrivateIpAddress': '172.31.16.58',
         'PublicDnsName': 'ec2-54-214-201-8.compute-1.amazonaws.com', 'PublicIpAddress': '54.214.201.8',
         'RootDeviceName': '/dev/sda1', 'RootDeviceType': 'ebs',
         'SecurityGroups': [{'GroupName': 'default', 'GroupId': 'sg-9bb1127286248719d'}],
         'Tags': [{'Key': 'Name', 'Value': 'Jenkins Master'}]
         },
        {'Cloud': 'aws', 'Region': 'us-east-1', 'Id': 'i-23a13a927070342ee', 'Type': 't2.medium',
         'ImageId': 'ami-03cf127a',
         'LaunchTime': '2020-10-18T21:27:49.000Z', 'State': 'Stopped',
         'StateReason': 'Client.UserInitiatedShutdown: User initiated shutdown', 'SubnetId': 'subnet-3c940491', 'VpcId': 'vpc-9256ce43',
         'MacAddress': '1b:2b:3c:4d:5e:6f', 'NetworkInterfaceId': 'eni-bf3adbb2',
         'PrivateDnsName': 'ip-172-31-16-58.ec2.internal', 'PrivateIpAddress': '172.31.16.58',
         'PublicDnsName': 'ec2-54-214-201-8.compute-1.amazonaws.com', 'PublicIpAddress': '54.214.201.8',
         'RootDeviceName': '/dev/sda1', 'RootDeviceType': 'ebs',
         'SecurityGroups': [{'GroupName': 'default', 'GroupId': 'sg-9bb1127286248719d'}],
         'Tags': [{'Key': 'Name', 'Value': 'Consul Node'}]
         },
        {'Cloud': 'aws', 'Region': 'us-east-1', 'Id': 'i-77z13a9270708asd', 'Type': 't2.xlarge',
         'ImageId': 'ami-03cf127a',
         'LaunchTime': '2020-10-18T21:27:49.000Z', 'State': 'Running',
         'StateReason': None, 'SubnetId': 'subnet-3c940491', 'VpcId': 'vpc-9256ce43',
         'MacAddress': '1b:2b:3c:4d:5e:6f', 'NetworkInterfaceId': 'eni-bf3adbb2',
         'PrivateDnsName': 'ip-172-31-16-58.ec2.internal', 'PrivateIpAddress': '172.31.16.58',
         'PublicDnsName': 'ec2-54-214-201-8.compute-1.amazonaws.com', 'PublicIpAddress': '54.214.201.8',
         'RootDeviceName': '/dev/sda1', 'RootDeviceType': 'ebs',
         'SecurityGroups': [{'GroupName': 'default', 'GroupId': 'sg-9bb1127286248719d'}],
         'Tags': [{'Key': 'Name', 'Value': 'Grafana'}]
         }
    ]
}


def get_state_reason(instance):
    instance_state = instance['State']['Name']
    if instance_state != 'running':
        return instance['StateReason']['Message']


class InstanceData:
    def __init__(self, ec2_client: client):
        self.ec2_client = ec2_client

    def get_instances(self):
       
        response = self.ec2_client.describe_instances()
        # response = ec2.describe_instances()
        response_list = response['Reservations']
        all_instances_list = []
        for each_response in response_list:
            instance_dict = {}
            instance = each_response['Instances'][0]

            instance_dict['Cloud'] = 'aws'
            #instance_dict['Region'] = instance['Placement']['AvailabilityZone']
            instance_dict['Region'] =  self.ec2_client.meta.region_name
            instance_dict['Id'] = instance['InstanceId']
            instance_dict['Type'] = instance['InstanceType']
            instance_dict['ImageId'] = instance['ImageId']
            instance_dict['LaunchTime'] = instance['LaunchTime']
            instance_dict['State'] = instance['State']['Name']
            if instance['State']['Name'] == 'running':
                instance_dict['StateReason'] = ''
            else:
                instance_dict['StateReason'] = instance['StateReason']
            instance_dict['SubnetId'] = instance['SubnetId']
            instance_dict['VpcId'] = instance['VpcId']
            instance_dict['MacAddress'] = instance['NetworkInterfaces'][0]['MacAddress']
            instance_dict['NetworkInterfaceId'] = instance['NetworkInterfaces'][0]['NetworkInterfaceId']
            instance_dict['PrivateDnsName'] = instance['PrivateDnsName']
            instance_dict['PrivateIpAddress'] = instance['PrivateIpAddress']
            instance_dict['PublicDnsName'] = instance['PublicDnsName']
            try:
                instance_dict['PublicIpAddress'] = instance['PublicIpAddress']
            except:
                instance_dict['PublicIpAddress'] = ''
            instance_dict['RootDeviceName'] = instance['RootDeviceName']
            instance_dict['RootDeviceType'] = instance['RootDeviceType']
            instance_dict['SecurityGroups'] = instance['SecurityGroups']
            try:
                instance_dict['Tags'] = instance['Tags']
            except:
                instance_dict['Tags'] = ''

            all_instances_list.append(instance_dict)
        my_instances = {}
        my_instances['Instances'] = all_instances_list

        return my_instances
        # return SAMPLE_INSTANCE_DATA


