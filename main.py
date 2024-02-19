from order_book import (OrderData, OrderBook, Order, SideType, MatchingEngine)
from helper import (
    update_matching_engine,
)

orders_data = [
    OrderData(id=None, price=1, volume=3, side=SideType.BUY),
    OrderData(id=None, price=2, volume=2, side=SideType.BUY),
    OrderData(id=None, price=3, volume=1, side=SideType.BUY),

    OrderData(id=None, price=4, volume=1, side=SideType.SELL),
    OrderData(id=None, price=5, volume=2, side=SideType.SELL),
    OrderData(id=None, price=6, volume=3, side=SideType.SELL),
]
order_book = OrderBook()
matching_engine = MatchingEngine(order_book)
matching_engine, orders = update_matching_engine(matching_engine, orders_data)

matching_engine.cancel_order(orders[1])
matching_engine.cancel_order(orders[4])
