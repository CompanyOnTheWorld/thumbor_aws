# coding: utf-8

from boto.s3.bucket import Bucket
from thumbor.utils import logger
from tornado.concurrent import return_future
import urllib2

import tc_aws.connection
import thumbor.loaders.http_loader as http_loader

import datetime

def _get_bucket(url):
    """
    Returns a tuple containing bucket name and bucket path.
    url: A string of the format /bucket.name/file/path/in/bucket
    """

    url_by_piece = url.lstrip("/").split("/")
    bucket_name = url_by_piece[0]
    bucket_path = "/".join(url_by_piece[1:])
    return bucket_name, bucket_path


def _normalize_url(url):
    """
    :param url:
    :return: exactly the same url since we only use http loader if url stars with http prefix.
    """
    return url


def _validate_bucket(context, bucket):
    allowed_buckets = context.config.get('S3_ALLOWED_BUCKETS', default=None)
    return not allowed_buckets or bucket in allowed_buckets


@return_future
def load(context, url, callback):
    enable_http_loader = context.config.get('AWS_ENABLE_HTTP_LOADER', default=False)

    if enable_http_loader and url.startswith('http'):
        return http_loader.load_sync(context, url, callback, normalize_url_func=_normalize_url)

    url = urllib2.unquote(url)

    bucket = context.config.get('S3_LOADER_BUCKET', default=None)

    if not bucket:
        bucket, url = _get_bucket(url)

    if _validate_bucket(context, bucket):
        bucket_loader = Bucket(
            connection=tc_aws.connection.get_connection(context),
            name=bucket
        )
        file_key = None
        try:
            file_key = bucket_loader.get_key(url)
        except Exception, e:
            logger.warn("ERROR retrieving image from S3 {0}: {1}".format(url, str(e)))

        if file_key:
            callback(file_key.read())
            return

    callback(None)
