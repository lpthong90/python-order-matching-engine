from enum import Enum
from typing import Union, Dict, NamedTuple, Optional

from order_book.double_linked_list import LinkedList
from order_book.advanced_avl_tree import AdvancedAVLTree


ID_TYPE = Union[int, str]


class SideType(Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderData(NamedTuple):
    id: Optional[ID_TYPE]
    price: float
    volume: float
    side: SideType


class Order:
    def __init__(self, id: ID_TYPE, price: float, volume: float, side: SideType):
        self.id: ID_TYPE = id
        self.price: float = price
        self.volume: float = volume
        self.origin_volume = volume
        self.side: SideType = side  # 'BUY' 'SELL'

        self.price_level: Optional[PriceLevel] = None

    def match_order(self, order) -> bool:
        if self.side == order.side:
            return False
        return self.match_price(order.price)

    def match_price(self, price: float) -> bool:
        if self.side == SideType.BUY:
            return self.price >= price
        else:
            return self.price <= price

    @property
    def other_side(self):
        if self.side == SideType.BUY:
            return SideType.SELL
        return SideType.BUY

    def print_out(self): # pragma: no cover
        print("Order ", self.id, " ", self.price, " ", self.volume, " ", self.origin_volume,
              " ", self.origin_volume - self.volume)


class PriceLevel:
    def __init__(self, price: float):
        self.price: float = price
        self.total_volume: float = 0
        self.orders: LinkedList[int, Order] = LinkedList[int, Order]()

    def add_order(self, order: Order):
        if self.orders.add(order.id, order):
            self.total_volume += order.volume
            order.price_level = self

    def re_add_order(self, order: Order):
        if self.orders.add_head(order.id, order):
            self.total_volume += order.volume
            order.price_level = self

    def cancel_order(self, order: Order):
        if self.orders.remove(order.id):
            self.total_volume -= order.volume

    def pop_order(self) -> Order:
        order = self.orders.pop().value
        self.total_volume -= order.volume
        return order

    def has_no_orders(self):
        return self.orders.size == 0


class OrderBook:
    def __init__(self):
        self.bids_tree: AdvancedAVLTree[float, PriceLevel] = AdvancedAVLTree[float, PriceLevel]()
        self.asks_tree: AdvancedAVLTree[float, PriceLevel] = AdvancedAVLTree[float, PriceLevel]()
        self.best_bid_price_level: Optional[PriceLevel] = None
        self.best_ask_price_level: Optional[PriceLevel] = None

        self.price_levels: Dict[float, PriceLevel] = {}

    def add_order(self, order: Order):
        if order.side == SideType.BUY:
            self.best_bid_price_level = self._add_order(self.bids_tree, self.best_bid_price_level, order)
        else:  # order.side == SideType.SELL:
            self.best_ask_price_level = self._add_order(self.asks_tree, self.best_ask_price_level, order)

    def execute_order(self, order: Order) -> dict:
        if order.side == SideType.BUY:
            self.best_ask_price_level, filled_orders = self._execute_order(order, self.best_ask_price_level)
        else:  # order.side == 'SELL':
            self.best_bid_price_level, filled_orders = self._execute_order(order, self.best_bid_price_level)
        return filled_orders

    def _delete_price_level(self, side: SideType, price_level: PriceLevel):
        del self.price_levels[price_level.price]
        if side == SideType.BUY:
            self.bids_tree.delete_node(price_level.price)
        else:
            self.asks_tree.delete_node(price_level.price)

    def cancel_order(self, order: Order):
        price_level = order.price_level
        if price_level is None:
            return
        price_level.cancel_order(order)
        if price_level.orders.size == 0:
            self._delete_price_level(order.side, price_level)

    def is_empty_bids(self) -> bool:
        self.bids_tree.is_empty()

    def is_empty_asks(self) -> bool:
        self.asks_tree.is_empty()

    def _add_new_price_level(self, prices_tree: AdvancedAVLTree[float, PriceLevel], best_price_level: PriceLevel, order: Order) -> PriceLevel:
        price_level = PriceLevel(order.price)
        price_level.add_order(order)
        prices_tree.insert_node(price_level.price, price_level)
        self.price_levels[order.price] = price_level

        if best_price_level is None:
            return price_level
        if order.side == SideType.BUY and best_price_level.price < price_level.price:
            return price_level
        if order.side == SideType.SELL and best_price_level.price > price_level.price:
            return price_level
        return best_price_level

    def _add_order(self, price_tree: AdvancedAVLTree[float, PriceLevel],
                   best_price_level: PriceLevel, order: Order) -> PriceLevel:
        if order.price not in self.price_levels:
            return self._add_new_price_level(price_tree, best_price_level, order)
        else:
            price_level = self.price_levels[order.price]
            price_level.add_order(order)
            price_tree.update(price_level.price, price_level)
            return best_price_level

    def _next_best_price_level(self, side: SideType) -> Optional[PriceLevel]:
        if side == SideType.BUY:
            if self.best_bid_price_level is None:
                return
            if self.best_bid_price_level.has_no_orders():
                del self.price_levels[self.best_bid_price_level.price]
                self.bids_tree.delete_node(self.best_bid_price_level.price)
                self.best_bid_price_level = self.bids_tree.max_node_value
                return self.best_bid_price_level
        else:  # side == SideType.SELL
            if self.best_ask_price_level is None:
                return
            if self.best_ask_price_level.has_no_orders():
                del self.price_levels[self.best_ask_price_level.price]
                self.asks_tree.delete_node(self.best_ask_price_level.price)
                self.best_ask_price_level = self.asks_tree.min_node_value
                return self.best_ask_price_level

    def _execute_order(self, order: Order, best_price_level: Optional[PriceLevel]) -> (Optional[PriceLevel], dict):
        filled_orders = {}

        while order.volume > 0 and self._is_matched_best_price(order, best_price_level):
            if best_price_level.has_no_orders():
                best_price_level = self._next_best_price_level(order.other_side)

            if best_price_level is None:
                break

            maker_order = best_price_level.pop_order()
            if not maker_order.match_order(order):
                best_price_level.re_add_order(maker_order)
                break

            matched_volume = min(maker_order.volume, order.volume)
            maker_order.volume -= matched_volume
            order.volume -= matched_volume

            filled_orders[maker_order.id] = maker_order
            filled_orders[order.id] = order

            if maker_order.volume > 0:
                best_price_level.re_add_order(maker_order)

        if best_price_level is not None and best_price_level.orders.size == 0:
            best_price_level = self._next_best_price_level(order.other_side)

        if order.volume > 0:
            self.add_order(order)

        return best_price_level, filled_orders

    def _is_matched_best_price(self, order: Order, best_price_level: PriceLevel) -> bool:
        if best_price_level is None:
            return False
        return order.match_price(best_price_level.price)


class MatchingEngine:
    def __init__(self, order_book: Optional[OrderBook]):
        self.order_book = order_book or OrderBook()

        self.orders: Dict[int, Order] = {}
        self.filled_orders: Dict[int, Order] = {}

    def execute_order(self, order: Order):
        if order.id in self.orders:
            return

        if order.side == SideType.BUY:
            filled_orders = self._execute_buy_order(order)
        else:  # order.side == SideType.SELL
            filled_orders = self._execute_sell_order(order)

        self.filled_orders = {**self.filled_orders, **filled_orders}

    def cancel_order(self, order: Order):
        if order.id not in self.orders:
            return

        order = self.orders[order.id]
        self.order_book.cancel_order(order)

    def _execute_buy_order(self, order: Order) -> dict:
        if self.order_book.is_empty_asks():
            self.order_book.add_order(order)
            self.orders[order.id] = order
            return {}
        return self.order_book.execute_order(order)

    def _execute_sell_order(self, order: Order) -> dict:
        if self.order_book.is_empty_bids():
            self.order_book.add_order(order)
            self.orders[order.id] = order
            return {}
        return self.order_book.execute_order(order)
