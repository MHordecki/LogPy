"""
LogPy
Unorthodox logging library

by Michal Hordecki

http://github.com/MHordecki/LogPy
"""

from threading import Lock
import datetime
from collections import Sequence

class Message(object):
    def __init__(self, tags, args, kwargs):
        self.tags = set(str(t) for t in tags)
        self.args = args
        self.kwargs = kwargs
        self.date = datetime.datetime.now()

class LogPy(object):
    """
    Logging object.
    """

    def __init__(self, message_type = Message):
        self.outputs = set()
        self.message_type = message_type

        self.lock = Lock()

    def add_output(self, *args, **kwargs):
        self.outputs.add(Output(*args, **kwargs))

    def add_raw_output(self, output):
        self.outputs.add(output)

    def __call__(self, *tags, **kwargs):
        """
        Log a new message with the given tags.

        Returns another callable that accepts message content, instead.
        Example usage: log('tag1', 'tag2')('log content')
        """

        assert not kwargs or (kwargs and tuple(kwargs.keys()) == ('curry',)), 'Only \'curry\' keyword argument allowed.'
        if kwargs.get('curry', False):
            return self._spawn_curried(tags)
        
        def second_step(*args, **kwargs):
            msg = self.message_type(tags, args, kwargs)

            for output in self.outputs:
                output(msg)

        return second_step

    def _spawn_curried(self, tags):
        def wrapped(*_tags, **kwargs):
            return self(*(_tags + tags), **kwargs)

        return wrapped

    def log(self, *tags):
        self(*tags)

class Output(object):
    """
    Output manages where and in what form
    your logs are saved.
    """

    @staticmethod
    def default_formatter(format_string):
        def wrapped(message):
            return format_string.format(date = message.date,
                    tags = ' '.join(message.tags),
                    args = message.args,
                    kwargs = message.kwargs,
                    message = message)

        return wrapped

    def __init__(self, output, formatter = None, filter = lambda x: True):
        """
        Creates a new Output object.
        """

        self.output = output
        self.filters = filter if isinstance(filter, Sequence) else [filter]

        self._formatter = None
        self.formatter = formatter

    @property
    def formatter(self):
        return self._formatter

    @formatter.setter
    def formatter(self, value):
        if value is None:
            self._formatter = self.default_formatter('{date} : {tags} : {args} {kwargs}\n')
        elif isinstance(value, str):
            self._formatter = self.default_formatter(value)
        else:
            self._formatter = value

    def add_filter(self, filter):
        """
        Adds a new filter. filter parameter is a callable that 
        returns a boolean value. Only messages for which all filters
        evaluate to True will be processed by this output.
        """

        self.filters.append(filter)

    def __call__(self, message):
        """
        Launches the process for the given message.
        """

        if all(filter(message) for filter in self.filters):
            self.output(self.formatter(message))

