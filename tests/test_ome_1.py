from tests.common import check_order_book


def test_add_order_1():
    inputs = [
        # List of order data
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
