"""Helper S3 (MinIO) untuk data lake. Endpoint dan kunci dari environment."""
import os

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError


def bucket() -> str:
    return os.environ["S3_BUCKET"]


def client():
    return boto3.client(
        "s3",
        endpoint_url=os.environ["S3_ENDPOINT"],
        aws_access_key_id=os.environ["S3_ACCESS_KEY"],
        aws_secret_access_key=os.environ["S3_SECRET_KEY"],
        region_name="us-east-1",
        config=Config(s3={"addressing_style": "path"}, retries={"max_attempts": 3}),
    )


def put_bytes(key: str, data: bytes) -> None:
    client().put_object(Bucket=bucket(), Key=key, Body=data)


def get_bytes(key: str) -> bytes:
    return client().get_object(Bucket=bucket(), Key=key)["Body"].read()


def delete(key: str) -> None:
    client().delete_object(Bucket=bucket(), Key=key)


def exists(key: str) -> bool:
    try:
        client().head_object(Bucket=bucket(), Key=key)
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] in ("404", "NoSuchKey", "NotFound"):
            return False
        raise


def list_keys(prefix: str) -> list[str]:
    keys = []
    for page in client().get_paginator("list_objects_v2").paginate(Bucket=bucket(), Prefix=prefix):
        keys += [o["Key"] for o in page.get("Contents", [])]
    return keys
