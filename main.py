from order_book import (Order, SideType, MatchingEngine)


matching_engine = MatchingEngine()

order_buy_1, trades_1 = matching_engine.add_order(Order(price=1, quantity=3, side=SideType.BUY))
print("trades_1", trades_1)
order_buy_2, trades_2 = matching_engine.add_order(Order(price=2, quantity=2, side=SideType.BUY))
print("trades_2", trades_2)
order_buy_3, trades_3 = matching_engine.add_order(Order(price=3, quantity=1, side=SideType.BUY))
print("trades_3", trades_3)

order_sell_1, trades_4 = matching_engine.add_order(Order(price=4, quantity=1, side=SideType.SELL))
print("trades_4", trades_4)
order_sell_2, trades_5 = matching_engine.add_order(Order(price=5, quantity=2, side=SideType.SELL))
print("trades_5", trades_5)
order_sell_3, trades_6 = matching_engine.add_order(Order(price=6, quantity=3, side=SideType.SELL))
print("trades_6", trades_6)

order_sell_4, trades_7 = matching_engine.add_order(Order(price=2, quantity=4, side=SideType.SELL))
print("order_buy_4", order_sell_4)
print("trades_7", trades_7)

matching_engine.order_book.bids_tree.print()
matching_engine.order_book.asks_tree.print()



