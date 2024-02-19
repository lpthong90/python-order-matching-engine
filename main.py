from order_book import (OrderData, OrderBook, Order, SideType)
from helper import (
    build_order_book,
    build_order,
)

order_book, orders = build_order_book([
    OrderData(id=None, price=1, volume=3, side=SideType.BUY),
    OrderData(id=None, price=2, volume=2, side=SideType.BUY),
    OrderData(id=None, price=3, volume=1, side=SideType.BUY),

    OrderData(id=None, price=4, volume=1, side=SideType.SELL),
    OrderData(id=None, price=5, volume=2, side=SideType.SELL),
    OrderData(id=None, price=6, volume=3, side=SideType.SELL),
])
order_book.print_book()

order_book.cancel_order(orders[1].id)
order_book.cancel_order(orders[4].id)
order_book.print_book()

order = build_order(OrderData(id=None, price=7, volume=5, side=SideType.BUY))
order_book.execute_order(order)
order_book.print_book()

order_book.print_filled_orders()
