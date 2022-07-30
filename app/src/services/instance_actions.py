from boto3 import client
import logging

class InstanceActions:
    def __init__(self, ec2_client: client):
        self.ec2_client = ec2_client

    def start_instance(self, instance_id):
        try:
            self.ec2_client.start_instances(
                InstanceIds=[str(instance_id)])
        except Exception as e:
            logging.exception(e)

    def stop_instance(self, instance_id):
        try:
            self.ec2_client.stop_instances(
                InstanceIds=[str(instance_id)])
        except Exception as e:
            logging.exception(e)
        

    def terminate_instance(self, instance_id):
        try:
            self.ec2_client.terminate_instances(
                InstanceIds=[str(instance_id)])
        except Exception as e:
            logging.exception(e)
     
    def action_selector(self, instance_action):
        return {
            'start': self.start_instance,
            'stop': self.stop_instance,
            'terminate': self.terminate_instance
        }.get(instance_action, lambda x: self.action_not_found(instance_action))

    @staticmethod
    def action_not_found(instance_action):
        raise RuntimeError("Unknown instance action selected: {}".format(instance_action))
