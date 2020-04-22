import requests


class EC2Meta:
    @staticmethod
    def instance_type():
        return requests.get('http://169.254.169.254/latest/meta-data/instance-type').text
