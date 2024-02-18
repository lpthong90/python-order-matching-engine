from helper import build_order_book


def check(inputs, outputs):
    order_book, orders = build_order_book(inputs)
    assert list(order_book.get_ask_price_levels()) == outputs[0]
    assert list(order_book.get_bid_price_levels()) == outputs[1]
