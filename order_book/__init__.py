from enum import Enum
from typing import Union, Dict, NamedTuple, Optional, Tuple, List, Generator
from py_simple_trees import AVLTree, AVLNode, TraversalType  # type: ignore

from order_book.double_linked_list import LinkedList

ID_TYPE = Union[int, str]


class SideType(Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderData(NamedTuple):
    id: Optional[ID_TYPE]
    price: float
    quantity: float
    side: SideType


class IDGenerator:
    def __init__(self, prefix: Optional[str] = None):
        self.count = 0
        self.prefix = prefix

    @property
    def new_id(self) -> Union[int, str]:
        self.count += 1
        if self.prefix is None:
            return self.count
        return f"{self.prefix}-{self.count}"


class Order:
    ID_GENERATOR = IDGenerator(prefix="order")

    def __init__(self, price: float, quantity: float, side: SideType):
        self.id = self.__class__.ID_GENERATOR.new_id
        self.price: float = price
        self.remained_quantity: float = quantity
        self.quantity = quantity
        self.side: SideType = side  # 'BUY' 'SELL'

        self.price_level: Optional[PriceLevel] = None

    @property
    def matched_quantity(self):
        return self.quantity - self.remained_quantity

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

    def is_match(self, price: float):
        if self.side == SideType.BUY:
            return self.price >= price
        else:  # self.side == SideType.SELL
            return self.price <= price

    def print_out(self):  # pragma: no cover
        print(
            "Order ",
            self.id,
            " ",
            self.price,
            " ",
            self.remained_quantity,
            " ",
            self.quantity,
            " ",
            self.matched_quantity,
        )


class Trade:
    ID_GENERATOR = IDGenerator(prefix="trade")

    def __init__(
        self, order_id: ID_TYPE, side: SideType, price: float, quantity: float
    ):
        self.id = self.__class__.ID_GENERATOR.new_id
        self.order_id = order_id
        self.side = side
        self.price = price
        self.quantity = quantity


class PriceLevel:
    def __init__(self, price: float):
        self.price = price
        self.total_quantity: float = 0
        self.orders = LinkedList[Union[int, str], Order]()

    def add_order(self, order: Order):
        if self.orders.add(order.id, order):
            self.total_quantity += order.remained_quantity
            order.price_level = self

    def re_add_order(self, order: Order):
        if self.orders.add_head(order.id, order):
            self.total_quantity += order.remained_quantity
            order.price_level = self

    def cancel_order(self, order: Order):
        if self.orders.remove(order.id):
            self.total_quantity -= order.remained_quantity

    def pop_order(self) -> Optional[Order]:
        order_node = self.orders.pop()
        if order_node is None:
            return None
        order = order_node.value
        if order is not None:
            self.total_quantity -= order.remained_quantity
        return order

    def has_no_orders(self):
        return self.orders.size == 0


class PriceLevelAVLTree(AVLTree[float, PriceLevel, AVLNode]):
    def __init__(self):
        super().__init__()
        self.root = None

    def insert(self, price_level: PriceLevel):
        self.root = self._insert(
            self.root, AVLNode(key=price_level.price, value=price_level)
        )

    def remove(self, price_level: PriceLevel):
        self.root = self._remove(self.root, AVLNode(key=price_level.price))

    def update(self, price_level: PriceLevel):
        self.root = self._update(
            self.root, AVLNode(key=price_level.price, value=price_level)
        )


class OrderBook:
    def __init__(self):
        self.bids_tree = PriceLevelAVLTree()
        self.asks_tree = PriceLevelAVLTree()
        self.best_bid_price_level = None
        self.best_ask_price_level = None

        self.price_levels = {}

    def add_order(self, order: Order):
        if order.side == SideType.BUY:
            self.best_bid_price_level = self._add_order(
                self.bids_tree, self.best_bid_price_level, order
            )
        else:  # order.side == SideType.SELL:
            self.best_ask_price_level = self._add_order(
                self.asks_tree, self.best_ask_price_level, order
            )

    # def execute_order(self, order: Order) -> dict:
    #     if order.side == SideType.BUY:
    #         (
    #             self.asks_tree,
    #             self.best_ask_price_level,
    #             filled_orders,
    #         ) = self._execute_order(order, self.asks_tree)
    #     else:  # order.side == 'SELL':
    #         (
    #             self.bids_tree,
    #             self.best_bid_price_level,
    #             filled_orders,
    #         ) = self._execute_order(order, self.bids_tree)
    #     return filled_orders

    def cancel_order(self, order: Order):
        price_level = order.price_level
        if price_level is None:
            return
        price_level.cancel_order(order)
        if price_level.orders.size == 0:
            self._remove_price_level(order.side, price_level)

    def is_empty_bids(self) -> bool:
        return self.bids_tree.root is None

    def is_empty_asks(self) -> bool:
        return self.asks_tree.root is None

    def is_empty(self, side: SideType) -> bool:
        if side == SideType.BUY:
            return self.is_empty_bids()
        else:
            return self.is_empty_asks()

    def _add_new_price_level(
        self,
        prices_tree: PriceLevelAVLTree,
        best_price_level: Optional[PriceLevel],
        order: Order,
    ) -> PriceLevel:
        price_level = PriceLevel(order.price)
        price_level.add_order(order)
        prices_tree.insert(price_level)
        self.price_levels[order.price] = price_level

        if best_price_level is None:
            return price_level
        if order.side == SideType.BUY and best_price_level.price < price_level.price:
            return price_level
        if order.side == SideType.SELL and best_price_level.price > price_level.price:
            return price_level
        return best_price_level

    def _add_order(
        self,
        price_tree: PriceLevelAVLTree,
        best_price_level: Optional[PriceLevel],
        order: Order,
    ) -> Optional[PriceLevel]:
        if order.price not in self.price_levels:
            return self._add_new_price_level(price_tree, best_price_level, order)
        else:
            price_level = self.price_levels[order.price]
            price_level.add_order(order)
            return best_price_level

    def best_price_levels(self, side: SideType) -> Generator[PriceLevel, None, None]:
        if side == SideType.SELL:
            for price_level_node in self.asks_tree.traversal(
                traversal_type=TraversalType.IN_ORDER
            ):
                yield price_level_node.value
        else:  # order.side == SideType.SELL
            for price_level_node in self.bids_tree.traversal(
                traversal_type=TraversalType.IN_ORDER, reverse=True
            ):
                yield price_level_node.value

    def best_matched_orders(
        self, order: Order
    ) -> Generator[Order, Tuple[Order, Order], None]:
        clear_price_levels = []

        for price_level in self.best_price_levels(order.other_side):
            if not order.is_match(price_level.price):
                break

            if price_level.has_no_orders():
                clear_price_levels.append(price_level)
                continue

            best_match_order = price_level.pop_order()
            while best_match_order is not None:
                order, best_match_order = yield best_match_order

                if order.remained_quantity == 0:
                    break

                best_match_order = price_level.pop_order()

            if best_match_order is None:
                if price_level.has_no_orders():
                    clear_price_levels.append(price_level)
            else:
                if best_match_order.remained_quantity == 0:
                    if price_level.has_no_orders():
                        clear_price_levels.append(price_level)
                else:
                    price_level.re_add_order(best_match_order)

            if order.remained_quantity == 0:
                break

        for price_level in clear_price_levels:
            self._remove_price_level(order.other_side, price_level)

        if order.remained_quantity > 0:
            self.add_order(order)

    def _remove_price_level(self, side: SideType, price_level: PriceLevel):
        del self.price_levels[price_level.price]
        if side == SideType.BUY:
            self.bids_tree.remove(price_level)
        else:
            self.asks_tree.remove(price_level)


class MatchingEngine:
    def __init__(self, order_book: Optional[OrderBook] = None):
        self.order_book = order_book or OrderBook()

        self.orders: Dict[Union[int, str], Order] = {}
        self.filled_orders: Dict[int, Order] = {}

    def add_order(self, order: Order) -> Tuple[Order, list]:
        if self.order_book.is_empty(order.other_side) or self._is_unmatched_best_price(
            order
        ):
            self.order_book.add_order(order)
            self.orders[order.id] = order
            return order, []

        updated_order, trades = self._execute_order(order)

        return updated_order, trades

    def cancel_order(self, order: Order):
        if order.id not in self.orders:
            return

        order = self.orders[order.id]
        self.order_book.cancel_order(order)

    def _is_matched_best_price(self, order: Order) -> bool:
        if order.side == SideType.BUY:
            return order.price >= self.order_book.best_ask_price_level.price
        else:  # order.side == SideType.SELL
            return order.price <= self.order_book.best_bid_price_level.price

    def _is_unmatched_best_price(self, order: Order) -> bool:
        return not self._is_matched_best_price(order)

    def _execute_order(self, order: Order) -> Tuple[Order, List[Trade]]:
        trades = []
        try:
            orders_gen = self.order_book.best_matched_orders(order)
            match_order = next(orders_gen)
            while order.remained_quantity > 0 or match_order is not None:
                matched_quantity = min(
                    match_order.remained_quantity, order.remained_quantity
                )

                match_order.remained_quantity -= matched_quantity
                trades.append(
                    Trade(
                        order_id=match_order.id,
                        quantity=matched_quantity,
                        side=match_order.side,
                        price=match_order.price,
                    )
                )

                order.remained_quantity -= matched_quantity
                trades.append(
                    Trade(
                        order_id=order.id,
                        quantity=matched_quantity,
                        side=order.side,
                        price=match_order.price,
                    )
                )

                match_order = orders_gen.send((order, match_order))

        except StopIteration:
            return order, trades
