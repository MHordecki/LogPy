LogPy
=====
Unorthodox logging for Python
-----------------------------

:Author: Michal Hordecki
:URL: http://github.com/MHordecki/LogPy

Introduction
============

LogPy is an alternative for standard Python logging facilities, loosely
based on Lisp's log5. LogPy is based on KISS principles - therefore I wanted
it to be as most transparent as possible. 

The main difference when compared to stdlib's logging is tag-based architecture.
In logging, each log has assigned a certain level (be it debug, error, etc.).
That's all. LogPy, on the other hand, sports tags - you can attach short strings
to each message. Tag can represent variety of things: severity level, module
name, or some custom log categorization.

LogPy requires Python 2.6 or higher. It works seamlessly on Python 3 too
(in fact, it's developed with py3k in mind and then backported to Python 2.6).

Getting started 
===============

Using LogPy is dead simple::

    from logpy import LogPy
    import sys

    log = LogPy()
    log.add_output(sys.stderr.write)

    log('debug')('Hello World!')

Voila! LogPy instances are callable. To output a log, call log "twice" - in
first call pass all tags of the log, and everything passed to the second one
will be considered a part of the message. The example will output logs to the
standard error output. Easy, isn't it?

Under the hood
--------------

LogPy has a few layers of abstraction:

    1. LogPy - it accepts data from the user, combines them into a Message
       instance and passes them down to all outputs.
    2. Output - it filters messages based on some predefined conditions, and
       if the message passes them all, it's formatted by the Formatter and
       then passed to the actual output.
    3. Formatter - takes message and formats it ;) (in standard implementation
       it uses string.format for the job).
    4. Actual output - a callable that, for example, outputs the Formatter's
       output to the screen.

All those layers/objects are callables.

Common tasks
============

Output filtering
----------------

With multiple outputs, you probably want to filter out some logs in each of them. There is support for that::

    log = LogPy()

    log.add_output(my_output, filter = lambda m: 'error' in m.tags)
    
    # Equivalent to:

    log.add_output(my_output, filter = [lambda m: 'error' in m.tags])

As you can see, filters are callables, taking ``Message`` object as an argument
and returning ``bool``. Multiple filters can be provided by a list.

Custom formatting
-----------------

You can customize formatting by either replacing the format string or by replacing the Formatting object altogether. Your choice.

Custom format string
~~~~~~~~~~~~~~~~~~~~

This one will meet 90% of your needs. You can change your format string with keyword argument to the add_output method of LogPy (also possible when directly instantiating Output objects)::

    log.add_output(..., formatter = 'my custom format string!')

When processing a message, method ``format`` of the string will be called with
following, predefined arguments:

    + date    - datetime object
    + tags    - space-delimited list of tags (string)
    + args    - list of arguments in the message
    + kwargs  - dict of keyword arguments in the message
    + message - the actual message object. All arguments above are actually
      just a syntactic sugar, as they are all attributes of this object.

Default format string looks like this: ``{date} : {tags} : {args} {kwargs}\n``

Don't forget to put a newline at the ending, or your logs will look crippled.

Working with multiple modules
-----------------------------

You can help yourself while using LogPy with multiple modules by predefining
some of the tags::

    # Main module

    log = LogPy()

    # Child module
    
    import mainmodule
    
    log = mainmodule.log('module:childmodule', curry = True)
    
    # Now:

    log('debug')('Hello World!')

    # is equivalent to

    log('module:childmodule', 'debug')('Hello World')

Custom format object
~~~~~~~~~~~~~~~~~~~~

In case you want the full power - you can get rid of the default formatter::

    log.add_output(..., formatter = my_formatter_object)

Formatter objects must comply to the simple protocol::

    class Formatter:
        def __call__(message: Message) -> Someting reasonable:
            pass

    class Message:
        tags = set(str)
        args = [] # passed by the user
        kwargs = {} # passed by the user
        date = datetime.datetime

(I have no idea whatsoever if there's standard formal notation for describing
protocols in Python besides things like zope.interface. I hope my ramblings
are clear.)

Where something reasonable means: everything that will be accepted by
the output of the Output (sounds kinda silly) - it usually means
``str``, but not always.

Custom Output object 
--------------------

If you're willing to scrap 50% of the LOC of LogPy, feel free to do so::

    log.add_raw_output(my_customized_output_object)

Worth mentioning is the fact that ``LogPy.add_output`` is just a wrapper for::

    log.add_output(...)
    # Equivalent to
    log.add_raw_output(Output(...))

Output protocol looks as follows::

    class Output:
        def __call__(message: Message):
            pass

In other words: you will be called with every log issued by the user.

Note: Please, treat messages as immutable objects - they are being reused
for all Outputs.

Thread safety
-------------

LogPy employs some basic thread safety; a threading.Lock is used in __call__ method of LogPy. It can be easily replaced::

    from threading import RLock

    log = LogPy()
    log.lock = RLock()


