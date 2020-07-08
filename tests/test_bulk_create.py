import pytest
import os

from cf_zalando_ids.bulk_create import bulk_create, read_blocked_ids, make_short_code, bulk_save


def test_make_short_code():
    blocked = read_blocked_ids()
    res1 = make_short_code(blocked)
    res2 = make_short_code(blocked)
    assert res1 != res2
    assert 'l' not in res1
    assert 'l' not in res2
    assert res1 in blocked


def test_bulk_create():
    blocked = read_blocked_ids()
    res = bulk_create(blocked, [("MEN's SKU 1", 1000)])
    assert len(blocked) == (9894 + 2000)
    assert len(res["MEN's SKU 1"]) == 1000


def test_read_blocked_ids():
    res = read_blocked_ids()
    assert len(res) == 9894
    assert '8c33vLEN' in res


def test_bulk_save(tmpdir):
    rinn = {
        'total': [[1, 1, 'TESTSKU1', 'circularity.id/1234abcd', 'https://circularity.id/abcd1234']],
        'sku1': [[1, 1, 'TESTSKU1', 'circularity.id/1234abcd', 'https://circularity.id/abcd1234']],
    }
    bulk_save(rinn, tmpdir)
    assert os.path.exists(os.path.join(tmpdir, 'total.csv'))
    assert os.path.exists(os.path.join(tmpdir, 'sku1.csv'))