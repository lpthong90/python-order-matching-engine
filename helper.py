import time

from ome import (OrderData, Order, Book)


def build_order(order_data: OrderData) -> Order:
    random_id = int(time.time() * 1e6)
    order = Order(
        random_id,
        order_data.price,
        order_data.volume,
        order_data.side
    )
    return order


def build_order_book(orders_data: list[OrderData]) -> [Book, list[Order]]:
    book = Book()
    orders = []
    for order_data in orders_data:
        order = build_order(order_data)
        book.execute_order(order)
        orders.append(order)
    return book, orders
