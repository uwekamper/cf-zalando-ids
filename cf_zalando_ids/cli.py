import logging
import click
import math

log = logging.getLogger()

from bulk_create import bulk_create, bulk_save, read_blocked_ids

def five_percent(num):
    res = num + (math.ceil(num / 100.0) * 5)
    print("Five percent of %d => %d" % (num, res))
    return res


@click.command()
def hello():
    skus = [
        ("women-top-sku1", five_percent(2500)),
        ("women-top-sku2", five_percent(1300)),
        ("women-top-sku3", five_percent(2000)),
        ("men-t-shirt-sku4", five_percent(1600)),
        ("men-t-shirt-sku5", five_percent(1600)),
        ("reserved", five_percent(1000)),
    ]
    blocked = read_blocked_ids()
    result = bulk_create(blocked, skus)
    bulk_save(result, './output')
    
if __name__ == '__main__':
    hello()

