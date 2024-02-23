from order_book import Order, SideType
from tests.common import check_order_book


def test_add_order_5():
    inputs = [
        Order(price=1, quantity=3, side=SideType.BUY),
        Order(price=2, quantity=2, side=SideType.BUY),
        Order(price=3, quantity=1, side=SideType.BUY),
        Order(price=4, quantity=1, side=SideType.SELL),
        Order(price=5, quantity=2, side=SideType.SELL),
        Order(price=6, quantity=3, side=SideType.SELL),
        Order(price=7, quantity=6, side=SideType.BUY),
    ]
    outputs = {
        # Asks
        'asks': [],
        'bids': [  # Bids
            (3, 1),
            (2, 2),
            (1, 3),
        ],
        'trades': [],
    }
    check_order_book(inputs, outputs)
