# coding: utf-8

import datetime
from tornado.concurrent import return_future
import tc_aws.loaders.s3_loader as s3_loader
from tc_aws.metrics.adapters import ThumborLibratoMetrics


METRICS = ThumborLibratoMetrics()


@return_future
def load(context, url, callback):
    start = datetime.datetime.now()
    def wrapper(*args, **kwargs):
        finish = datetime.datetime.now()
        took = (finish - start).total_seconds() * 1000
        METRICS.timing('loader.load', took)
        return callback(*args, **kwargs)

    s3_loader.load(context, url, wrapper)
