from ome import (Book, OrderData, Order, SideType, ID_TYPE)
from helper import (
    build_order_book,
    build_order,
)


def check(inputs, outputs):
    order_book, orders = build_order_book(inputs)
    assert list(order_book.get_ask_price_levels()) == outputs[0]
    assert list(order_book.get_bid_price_levels()) == outputs[1]


def test_add_order_0():
    inputs = [
        # List of order data
    ]
    outputs = [
        # Asks
        [
            # (price, volume)
        ],
        # Bids
        [
            # (price, volume)
        ],
        # Filled orders
        [
        ]
    ]
    check(inputs, outputs)


def test_add_order_1():
    inputs = [
        OrderData(id=None, price=2, volume=2, side=SideType.BUY),
        OrderData(id=None, price=2, volume=2, side=SideType.SELL),
    ]
    outputs = [
        # Asks
        [
            # (price, volume)
        ],
        # Bids
        [
            # (price, volume)
        ],
        # Filled orders
        [
            2, 2
        ]
    ]
    check(inputs, outputs)


def test_add_order():
    inputs = [
        OrderData(id=None, price=1, volume=3, side=SideType.BUY),
        OrderData(id=None, price=2, volume=2, side=SideType.BUY),
        OrderData(id=None, price=3, volume=1, side=SideType.BUY),

        OrderData(id=None, price=4, volume=1, side=SideType.SELL),
        OrderData(id=None, price=5, volume=2, side=SideType.SELL),
        OrderData(id=None, price=6, volume=3, side=SideType.SELL),
    ]
    outputs = [
        [
            (6, 3),
            (5, 2),
            (4, 1),
        ], [
            (3, 1),
            (2, 2),
            (1, 3),
        ], [
        ]
    ]
    check(inputs, outputs)

