from order_book import (OrderData, Book, Order, SideType)
from helper import (
    build_order_book,
    build_order,
)

book, orders = build_order_book([
    OrderData(id=None, price=1, volume=3, side=SideType.BUY),
    OrderData(id=None, price=2, volume=2, side=SideType.BUY),
    OrderData(id=None, price=3, volume=1, side=SideType.BUY),

    OrderData(id=None, price=4, volume=1, side=SideType.SELL),
    OrderData(id=None, price=5, volume=2, side=SideType.SELL),
    OrderData(id=None, price=6, volume=3, side=SideType.SELL),
])
book.print_book()

book.cancel_order(orders[1].id)
book.cancel_order(orders[4].id)
book.print_book()

order = build_order(OrderData(id=None, price=7, volume=5, side=SideType.BUY))
book.execute_order(order)
book.print_book()

book.print_filled_orders()
