from order_book import OrderData, SideType
from tests.common import check_order_book


def test_add_order_5():
    inputs = [
        OrderData(id=None, price=1, quantity=3, side=SideType.BUY),
        OrderData(id=None, price=2, quantity=2, side=SideType.BUY),
        OrderData(id=None, price=3, quantity=1, side=SideType.BUY),
        OrderData(id=None, price=4, quantity=1, side=SideType.SELL),
        OrderData(id=None, price=5, quantity=2, side=SideType.SELL),
        OrderData(id=None, price=6, quantity=3, side=SideType.SELL),
        OrderData(id=None, price=7, quantity=6, side=SideType.BUY),
    ]
    outputs = [
        # Asks
        [],
        [  # Bids
            (3, 1),
            (2, 2),
            (1, 3),
        ],
        [],
    ]
    check_order_book(inputs, outputs)
