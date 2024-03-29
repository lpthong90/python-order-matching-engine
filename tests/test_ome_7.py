from tests.common import check_order_book
from order_book import Order, SideType


def test_add_order_1():
    inputs = [
        Order(price=1, quantity=3, side=SideType.BUY),
        Order(price=2, quantity=2, side=SideType.BUY),
        Order(price=3, quantity=1, side=SideType.BUY),
        Order(price=4, quantity=1, side=SideType.SELL),
        Order(price=5, quantity=2, side=SideType.SELL),
        Order(price=6, quantity=3, side=SideType.SELL),
        Order(price=1, quantity=2, side=SideType.SELL),
    ]
    outputs = {
        'asks': [
            (6, 3),
            (5, 2),
            (4, 1),
        ],
        'bids': [(2, 1), (1, 3)],
        'trades': [],
    }
    check_order_book(inputs, outputs)
