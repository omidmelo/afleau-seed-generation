import boto3
import os

class SecretHandler:
    _client = None
    _cache = {}

    @classmethod
    def _get_client(cls):
        if cls._client is None:
            region_name = os.getenv("AWS_REGION_NAME", "us-east-1")
            cls._client = boto3.client("ssm", region_name=region_name)
        return cls._client

    @classmethod
    def get_secret_value(cls, secret_key):
        if secret_key in cls._cache:
            return cls._cache[secret_key]

        client = cls._get_client()        
        response = client.get_parameter(Name=secret_key, WithDecryption=True)
        secret_value = response["Parameter"]["Value"]
        cls._cache[secret_key] = secret_value

        return secret_value
