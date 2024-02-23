from order_book import OrderData, SideType
from tests.common import check_order_book


def test_add_order_3():
    inputs = [
        OrderData(id=None, price=1, quantity=3, side=SideType.BUY),
        OrderData(id=None, price=2, quantity=2, side=SideType.BUY),
        OrderData(id=None, price=3, quantity=1, side=SideType.BUY),
        OrderData(id=None, price=4, quantity=1, side=SideType.SELL),
        OrderData(id=None, price=5, quantity=2, side=SideType.SELL),
        OrderData(id=None, price=6, quantity=3, side=SideType.SELL),
        OrderData(id=None, price=4, quantity=3, side=SideType.BUY),
    ]
    outputs = {
        'asks': [
            (6, 3),
            (5, 2),
        ],
        'bids': [
            (4, 2),
            (3, 1),
            (2, 2),
            (1, 3),
        ],
        'trades': [],
    }
    check_order_book(inputs, outputs)
