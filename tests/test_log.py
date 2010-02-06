
from logpy import *

class FakeFile:
    def __call__(self, msg):
        self.msg = msg

class Fake: pass

def test_Output_custom_formatter_object():
    fake_msg = object()

    class Fmter:
        def __call__(self, msg):
            assert msg is fake_msg
            return 'foo!'

    file = FakeFile()
    o = Output(file)
    o.formatter = Fmter()

    o(fake_msg)

    assert file.msg == 'foo!'

def test_Output_string_formatter():
    fake_msg = Fake()
    fake_msg.tags = ['tag1', 'tag2', 'cat1:tag3']
    fake_msg.args = ['hello world!']
    fake_msg.kwargs = {'key': 1337}
    fake_msg.date = None

    file = FakeFile()
    o = Output(file, formatter = 'just testing, key = {kwargs[key]}')
    o(fake_msg)
    
    assert file.msg == 'just testing, key = 1337'

def test_Output_filter():
    class Fmter:
        def __init__(self): self.called = False
        def __call__(self, msg): self.called = True; return ''

    f = Fmter()
    o = Output(FakeFile(), formatter = f)
    o.add_filter(lambda m: hasattr(m, 'testattr'))
    
    o(Fake())
    assert not f.called

    fake = Fake()
    fake.testattr = True
    o(fake)
    assert f.called

def test_Output_filter_list_in_ctor():
    class Fmter:
        def __init__(self): self.called = False
        def __call__(self, msg): self.called = True; return ''

    f = Fmter()
    o = Output(FakeFile(), formatter = f, filter = [lambda m: hasattr(m, 'attr1'), lambda m: hasattr(m, 'attr2')])
    
    o(Fake())
    assert not f.called

    fake = Fake()
    fake.attr2 = True
    o(fake)
    assert not f.called

    fake = Fake()
    fake.attr2 = True
    fake.attr1 = True
    o(fake)
    assert f.called

def test_LogPy_currying():

    class FakeOutput:
        def __call__(self, msg):
            self.tags = set(msg.tags)
        
    l = LogPy()
    
    o = FakeOutput()
    l.add_raw_output(o)

    l('hello', curry = True)('world')('') 

    #assert o.tags == {'hello', 'world'} - waiting for 2.7
    assert o.tags == set(('hello', 'world'))
