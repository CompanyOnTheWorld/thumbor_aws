import os
import librato


class ThumborLibratoMetrics:

    def __init__(self):
        user = os.environ.get('LIBRATO_USER')
        token = os.environ.get('LIBRATO_TOKEN')
        self.api = librato.connect(user, token)

        count = int(os.environ.get('LIBRATO_QUEUE_AUTO_SUBMIT_COUNT', 100))
        self.queue = self.api.new_queue(auto_submit_count=count)

        prefix = os.environ.get('LIBRATO_METRIC_PREFIX', 'thumbor.runtime_metrics')
        self.metric_prefix = prefix

    # mimicing statsd interface for now
    def incr(self, metricname):
        self.queue.add(self._prefixed_name(metricname), 1, type='counter')

    def timing(self, metricname, value, unit='ms'):
        name = self._prefixed_name(metricname)
        print name
        print value
        self.queue.add(name, value, display_units_short=unit)

    def _prefixed_name(self, metricname):
        return self.metric_prefix + '.' + metricname
