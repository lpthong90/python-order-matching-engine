from order_book import OrderData, SideType
from tests.common import check_order_book


def test_add_order_2_1():
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
        [],
    ]
    check_order_book(inputs, outputs)


def test_add_order_2_2():
    inputs = [
        OrderData(id=None, price=2, volume=2, side=SideType.BUY),
    ]
    outputs = [
        # Asks
        [
            # (price, volume)
        ],
        # Bids
        [(2, 2)],
        # Filled orders
        [],
    ]
    check_order_book(inputs, outputs)


def test_add_order_2_3():
    inputs = [
        OrderData(id=None, price=2, volume=2, side=SideType.SELL),
    ]
    outputs = [
        # Asks
        [(2, 2)],
        # Bids
        [
            # (price, volume)
        ],
        # Filled orders
        [],
    ]
    check_order_book(inputs, outputs)


def test_add_order_2_4():
    inputs = [
        OrderData(id=None, price=2, volume=2, side=SideType.BUY),
        OrderData(id=None, price=2, volume=2, side=SideType.BUY),
        OrderData(id=None, price=2, volume=3, side=SideType.BUY),
    ]
    outputs = [
        # Asks
        [
            # (price, volume)
        ],
        # Bids
        [(2, 7)],
        # Filled orders
        [],
    ]
    check_order_book(inputs, outputs)


def test_add_order_2_5():
    inputs = [
        OrderData(id=None, price=2, volume=2, side=SideType.SELL),
        OrderData(id=None, price=2, volume=1, side=SideType.SELL),
        OrderData(id=None, price=2, volume=2, side=SideType.SELL),
    ]
    outputs = [
        # Asks
        [(2, 5)],
        # Bids
        [
            # (price, volume)
        ],
        # Filled orders
        [],
    ]
    check_order_book(inputs, outputs)


def test_add_order_2_6():
    inputs = [
        OrderData(id=None, price=2, volume=2, side=SideType.BUY),
        OrderData(id=None, price=2, volume=2, side=SideType.BUY),
        OrderData(id=None, price=2, volume=3, side=SideType.BUY),
        OrderData(id=None, price=2, volume=4, side=SideType.SELL),
    ]
    outputs = [
        # Asks
        [
            # (price, volume)
        ],
        # Bids
        [(2, 3)],
        # Filled orders
        [],
    ]
    check_order_book(inputs, outputs)


def test_add_order_2_7():
    inputs = [
        OrderData(id=None, price=2, volume=2, side=SideType.BUY),
        OrderData(id=None, price=2, volume=8, side=SideType.SELL),
        OrderData(id=None, price=2, volume=2, side=SideType.BUY),
        OrderData(id=None, price=2, volume=3, side=SideType.BUY),
    ]
    outputs = [
        # Asks
        [(2, 1)],
        # Bids
        [
            # (price, volume)
        ],
        # Filled orders
        [],
    ]
    check_order_book(inputs, outputs)


def test_add_order_2_8():
    inputs = [
        OrderData(id=None, price=3, volume=4, side=SideType.BUY),
        OrderData(id=None, price=2, volume=2, side=SideType.SELL),
        OrderData(id=None, price=2, volume=1, side=SideType.SELL),
        OrderData(id=None, price=2, volume=2, side=SideType.SELL),
        OrderData(id=None, price=1, volume=4, side=SideType.BUY),
    ]
    outputs = [
        # Asks
        [(2, 1)],
        # Bids
        [(1, 4)],
        # Filled orders
        [],
    ]
    check_order_book(inputs, outputs)
