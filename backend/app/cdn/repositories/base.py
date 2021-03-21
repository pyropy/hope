import boto3

class BaseCDNRepository:
    def __init__(self, client: boto3.client) -> None:
        self.client = client