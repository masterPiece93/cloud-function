import logging
from typing import List
from google.cloud import storage

logger = logging.getLogger(__name__)

def bucket_metadata(bucket_name) -> List[str]:
    """Prints out a bucket's metadata."""
    # bucket_name = 'your-bucket-name'
    message: list = []
    storage_client = storage.Client()
    try:
        bucket = storage_client.get_bucket(bucket_name)
    except Exception as e:
        logger.exception(e)
        message.append('unsuccessful')
    else:
        message.append("Connected to Bucket.")
        message.append(f"|---- ID : {bucket.id}")
        message.append(f"|---- Name: {bucket.name}")
        message.append(f"|---- Storage Class: {bucket.storage_class}")
        message.append(f"|---- Location: {bucket.location}")
        message.append(f"|---- Location Type: {bucket.location_type}")
        message.append(f"|---- Cors: {bucket.cors}")
        message.append(f"|---- Default Event Based Hold: {bucket.default_event_based_hold}")
        message.append(f"|---- Default KMS Key Name: {bucket.default_kms_key_name}")
        message.append(f"|---- Metageneration: {bucket.metageneration}")
        message.append(
            f"|---- Public Access Prevention: {bucket.iam_configuration.public_access_prevention}"
        )
        message.append(f"|---- Retention Effective Time: {bucket.retention_policy_effective_time}")
        message.append(f"|---- Retention Period: {bucket.retention_period}")
        message.append(f"|---- Retention Policy Locked: {bucket.retention_policy_locked}")
        message.append(f"|---- Object Retention Mode: {bucket.object_retention_mode}")
        message.append(f"|---- Requester Pays: {bucket.requester_pays}")
        message.append(f"|---- Self Link: {bucket.self_link}")
        message.append(f"|---- Time Created: {bucket.time_created}")
        message.append(f"|---- Versioning Enabled: {bucket.versioning_enabled}")
        message.append(f"|---- Labels: {bucket.labels}")
    return message
