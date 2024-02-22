from tests.common import check_order_book
from order_book import OrderData, SideType


def test_add_order_1():
    inputs = [
        OrderData(id=None, price=1, volume=3, side=SideType.BUY),
        OrderData(id=None, price=2, volume=2, side=SideType.BUY),
        OrderData(id=None, price=3, volume=1, side=SideType.BUY),
        OrderData(id=None, price=4, volume=1, side=SideType.SELL),
        OrderData(id=None, price=5, volume=2, side=SideType.SELL),
        OrderData(id=None, price=6, volume=3, side=SideType.SELL),
        OrderData(id=None, price=1, volume=3, side=SideType.SELL),
    ]
    outputs = [
        [
            (6, 3),
            (5, 2),
            (4, 1),
        ],
        [(1, 3)],
        [],
    ]
    check_order_book(inputs, outputs)
