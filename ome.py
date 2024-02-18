from enum import Enum
from typing import Union, Dict, NamedTuple, Optional

from data_structures.double_linked_list import LinkedList
from data_structures.avl_tree import AVLTree


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

    def print_out(self):
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


class Book:
    def __init__(self):
        self.bids_tree: AVLTree[float, PriceLevel] = AVLTree[float, PriceLevel]()
        self.asks_tree: AVLTree[float, PriceLevel] = AVLTree[float, PriceLevel]()
        self.best_bid_price_level: Optional[PriceLevel] = None
        self.best_ask_price_level: Optional[PriceLevel] = None

        self.orders: Dict[int, Order] = {}
        self.filled_orders: Dict[int, Order] = {}

    def execute_order(self, order: Order):
        if order.side == SideType.BUY:
            self._execute_bid_order(order)
        else:  # order.side == 'SELL':
            self._execute_ask_order(order)

    def _delete_price_level(self, side: SideType, price_level: PriceLevel):
        if side == SideType.BUY:
            self.bids_tree.delete_node(price_level.price)
        else:
            self.asks_tree.delete_node(price_level.price)

    def cancel_order(self, order_id: ID_TYPE):
        if order_id not in self.orders:
            return

        order = self.orders[order_id]
        price_level = order.price_level
        if price_level is None:
            return
        price_level.cancel_order(order)
        if price_level.orders.size == 0:
            self._delete_price_level(order.side, price_level)

    def _add_new_price_level(self, prices_tree: AVLTree[float, PriceLevel], best_price_level: PriceLevel, order: Order) -> PriceLevel:
        price_level = PriceLevel(order.price)
        price_level.add_order(order)
        prices_tree.insert_node(price_level.price, price_level)

        if best_price_level is None:
            best_price_level = price_level
            return best_price_level

        if order.side == SideType.BUY and best_price_level.price <  price_level.price:
            best_price_level = price_level
        elif order.side == SideType.SELL and best_price_level.price >  price_level.price:
            best_price_level = price_level

        return best_price_level

    def _add_order(self, price_tree: AVLTree[float, PriceLevel], best_price_level: PriceLevel, order: Order) -> PriceLevel:
        self.orders[order.id] = order
        price_level = price_tree.find_value(order.price)
        if price_level is None:
            return self._add_new_price_level(price_tree, best_price_level, order)
        else:
            price_level.total_volume += order.volume
            price_tree.update(price_level.price, price_level)
            return best_price_level

    def _refresh_best_ask_price_level(self):
        if self.best_ask_price_level.orders.size == 0:
            self.asks_tree.delete_node(self.best_ask_price_level.price)
            self.best_ask_price_level = self.asks_tree.min_node_value

    def _refresh_best_bid_price_level(self):
        if self.best_bid_price_level.orders.size == 0:
            self.bids_tree.delete_node(self.best_bid_price_level.price)
            self.best_bid_price_level = self.bids_tree.min_node_value

    def _execute_bid_order(self, order: Order):
        while self._is_matched(order):
            if self.best_ask_price_level.orders.size == 0:
                self._refresh_best_ask_price_level()

            if self.best_ask_price_level is None:
                break

            maker_order = self.best_ask_price_level.pop_order()

            if maker_order.price > order.price:
                self.best_ask_price_level.re_add_order(maker_order)
                break

            if maker_order.volume > order.volume:
                maker_order.volume -= order.volume
                self.filled_orders[maker_order.id] = maker_order
                order.volume = 0
                self.filled_orders[order.id] = order
                self.best_ask_price_level.re_add_order(maker_order)
                break

            if maker_order.volume == order.volume:
                maker_order.volume = 0
                self.filled_orders[maker_order.id] = maker_order
                order.volume = 0
                self.filled_orders[order.id] = order
                break

            if maker_order.volume < order.volume:
                order.volume -= maker_order.volume
                self.filled_orders[order.id] = order
                maker_order.volume = 0
                self.filled_orders[maker_order.id] = maker_order

        if self.best_ask_price_level is not None and self.best_ask_price_level.orders.size == 0:
            self._refresh_best_ask_price_level()

        if order.volume > 0:
            self.best_bid_price_level = self._add_order(self.bids_tree, self.best_bid_price_level, order)

    def _is_empty_bids(self):
        return self.best_bid_price_level is None and self.bids_tree.is_empty()

    def _is_empty_asks(self):
        return self.best_ask_price_level is None and self.asks_tree.is_empty()

    def _is_matched(self, order: Order) -> bool:
        if order.side == SideType.BUY:
            if self.best_ask_price_level is None:
                return False
            if self.asks_tree.is_empty():
                return False
            return order.price >= self.best_ask_price_level.price
        else:  # order.side == SideType.SELL
            if self.best_bid_price_level is None:
                return False
            if self.bids_tree.is_empty():
                return False
            return order.price <= self.best_bid_price_level.price

    def _execute_ask_order(self, order: Order):
        while self._is_matched(order):
            if self.best_bid_price_level.orders.size == 0:
                self._refresh_best_bid_price_level()

            if self.best_bid_price_level is None:
                break

            maker_order = self.best_bid_price_level.pop_order()

            if maker_order.price > order.price:
                self.best_bid_price_level.re_add_order(maker_order)
                break

            if maker_order.volume > order.volume:
                maker_order.volume -= order.volume
                self.filled_orders[maker_order.id] = maker_order
                order.volume = 0
                self.filled_orders[order.id] = order
                self.best_bid_price_level.re_add_order(maker_order)
                break

            if maker_order.volume == order.volume:
                maker_order.volume = 0
                self.filled_orders[maker_order.id] = maker_order
                order.volume = 0
                self.filled_orders[order.id] = order
                break

            if maker_order.volume < order.volume:
                order.volume -= maker_order.volume
                self.filled_orders[order.id] = order
                maker_order.volume = 0
                self.filled_orders[maker_order.id] = maker_order

        if self.best_bid_price_level is not None and self.best_bid_price_level.orders.size == 0:
            self._refresh_best_bid_price_level()

        if order.volume > 0:
            self.best_ask_price_level = self._add_order(self.asks_tree, self.best_ask_price_level, order)

    def get_ask_price_levels(self):
        price_levels = self.asks_tree.get_all_nodes()
        price_levels.reverse()
        price_levels = map(lambda pl: (pl[1].price, pl[1].total_volume), price_levels)
        return price_levels

    def get_bid_price_levels(self):
        price_levels = self.bids_tree.get_all_nodes()
        price_levels.reverse()
        price_levels = map(lambda pl: (pl[1].price, pl[1].total_volume), price_levels)
        return price_levels

    def print_bids(self):
        price_levels = self.get_bid_price_levels()
        for pl in price_levels:
            print("Bid ", pl[0], pl[1])

    def print_asks(self):
        price_levels = self.get_ask_price_levels()
        for pl in price_levels:
            print("Ask ", pl[0], pl[1])

    def print_book(self):
        print("=====================")
        print("Side | Price | Volume")
        self.print_asks()
        print("-----")
        self.print_bids()

    def print_filled_orders(self):
        print("======Filled Orders=======")
        print("OrderId | Price | Remained | Volume | Filled")
        for order_id, order in self.filled_orders.items():
            order.print_out()
