from email import message_from_string

from py.path import local
from pytest import fixture

from ailtdou.main.models import extract_text


@fixture
def messages():
    data = local(__file__).dirpath('data/payloads.txt').read()
    return [message_from_string(eval('"""%s"""' % body))
            for body in data.strip('\n').split('\n')]


def test_extract_text(messages):
    t0, t1, t2 = [extract_text(m) for m in messages]
    assert t0 == u'ffwewe2g2 fw  https://example.com #fe'
    assert t1 == u'PEP 302 http://bit.ly/T89p9W'
    assert t2 == (
        u'\u535a\u4e3b\u9700\u8981\u52a0\u5927\u7535\u91cf\uff0c\u575a\u6301'
        u'\u6cbb\u7597\uff1a\u300a\u6000\u65e7\u515a\u300b '
        u'http://wolege.ca/blog/2014/05/15/reminiscence/')
