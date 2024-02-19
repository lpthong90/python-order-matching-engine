from tests.common import check_order_book


def test_add_order_1():
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
    check_order_book(inputs, outputs)

