from order_book import Order, SideType
from tests.common import check_order_book


def test_add_order_2_1():
    inputs = [
        Order(price=2, quantity=2, side=SideType.BUY),
        Order(price=2, quantity=2, side=SideType.SELL),
    ]
    outputs = {
        # Asks
        'asks': [
            # (price, volume)
        ],
        # Bids
        'bids': [
            # (price, volume)
        ],
        # Filled orders
        'trades': [],
    }
    check_order_book(inputs, outputs)


def test_add_order_2_2():
    inputs = [
        Order(price=2, quantity=2, side=SideType.BUY),
    ]
    outputs = {
        # Asks
        'asks': [
            # (price, volume)
        ],
        # Bids
        'bids': [(2, 2)],
        # Filled orders
        'trades': [],
    }
    check_order_book(inputs, outputs)


def test_add_order_2_3():
    inputs = [
        Order(price=2, quantity=2, side=SideType.SELL),
    ]
    outputs = {
        # Asks
        'asks': [(2, 2)],
        # Bids
        'bids': [
            # (price, volume)
        ],
        # Filled orders
        'trades': [],
    }
    check_order_book(inputs, outputs)


def test_add_order_2_4():
    inputs = [
        Order(price=2, quantity=2, side=SideType.BUY),
        Order(price=2, quantity=2, side=SideType.BUY),
        Order(price=2, quantity=3, side=SideType.BUY),
    ]
    outputs = {
        # Asks
        'asks': [
            # (price, volume)
        ],
        # Bids
        'bids': [(2, 7)],
        # Filled orders
        'trades': [],
    }
    check_order_book(inputs, outputs)


def test_add_order_2_5():
    inputs = [
        Order(price=2, quantity=2, side=SideType.SELL),
        Order(price=2, quantity=1, side=SideType.SELL),
        Order(price=2, quantity=2, side=SideType.SELL),
    ]
    outputs = {
        # Asks
        'asks': [(2, 5)],
        # Bids
        'bids': [
            # (price, volume)
        ],
        # Filled orders
        'trades': [],
    }
    check_order_book(inputs, outputs)


def test_add_order_2_6():
    inputs = [
        Order(price=2, quantity=2, side=SideType.BUY),
        Order(price=2, quantity=2, side=SideType.BUY),
        Order(price=2, quantity=3, side=SideType.BUY),
        Order(price=2, quantity=4, side=SideType.SELL),
    ]
    outputs = {
        # Asks
        'asks': [
            # (price, volume)
        ],
        # Bids
        'bids': [(2, 3)],
        # Filled orders
        'trades': [],
    }
    check_order_book(inputs, outputs)


def test_add_order_2_7():
    inputs = [
        Order(price=2, quantity=2, side=SideType.BUY),
        Order(price=2, quantity=8, side=SideType.SELL),
        Order(price=2, quantity=2, side=SideType.BUY),
        Order(price=2, quantity=3, side=SideType.BUY),
    ]
    outputs = {
        # Asks
        'asks': [(2, 1)],
        # Bids
        'bids': [
            # (price, volume)
        ],
        # Filled orders
        'trades': [],
    }
    check_order_book(inputs, outputs)


def test_add_order_2_8():
    inputs = [
        Order(price=3, quantity=4, side=SideType.BUY),
        Order(price=2, quantity=2, side=SideType.SELL),
        Order(price=2, quantity=1, side=SideType.SELL),
        Order(price=2, quantity=2, side=SideType.SELL),
        Order(price=1, quantity=4, side=SideType.BUY),
    ]
    outputs = {
        # Asks
        'asks': [(2, 1)],
        # Bids
        'bids': [(1, 4)],
        # Filled orders
        'trades': [],
    }
    check_order_book(inputs, outputs)
