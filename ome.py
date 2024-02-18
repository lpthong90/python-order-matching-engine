from typing import Union

from data_structures.double_linked_list import (
    LinkedList,
    LinkedNode
)

from data_structures.avl_tree import (
    TreeNode,
    AVLTree
)


class Order(LinkedNode):
    def __init__(self, order_id: int, price: int, volume: int, side: str):
        super().__init__(order_id)

        self.order_id: int = order_id
        self.price: int = price
        self.volume: int = volume
        self.origin_volume = volume
        self.side: str = side  # 'BUY' 'SELL'

        self.price_level: Union[PriceLevel, None] = None

    def print_out(self):
        print("=====================")
        print("Order ", self.order_id, " ", self.price, " ", self.volume, " ", self.origin_volume)


class PriceLevel(LinkedNode, TreeNode):
    def __init__(self, price: int):
        LinkedNode.__init__(self, key=price)
        TreeNode.__init__(self, key=price)

        self.price: int = price
        self.total_volume: int = 0
        self.orders: LinkedList = LinkedList()

    def add_order(self, order):
        if self.orders.add(order):
            self.total_volume += order.volume
            order.price_level = self

    def re_add_order(self, order):
        if self.orders.add_head(order):
            self.total_volume += order.volume
            order.price_level = self

    def cancel_order(self, order: Order):
        if self.orders.remove(order):
            self.total_volume -= order.volume

    def pop_order(self) -> Order:
        order = self.orders.pop()
        self.total_volume -= order.volume
        return order


class Book:
    def __init__(self):
        self.bids_tree: AVLTree = AVLTree()
        self.asks_tree: AVLTree = AVLTree()
        self.best_bid_price_level: Union[PriceLevel, None] = None
        self.best_ask_price_level: Union[PriceLevel, None] = None

    def execute_order(self, order: Order):
        if order.side == 'BUY':
            self._execute_bid_order(order)
        else:  # order.side == 'SELL':
            self._execute_ask_order(order)

    def _execute_bid_order(self, order: Order):
        if not self.best_ask_price_level or order.price < self.best_ask_price_level.price:
            price_level_node = PriceLevel(order.price)
            price_level_node.add_order(order)
            self.bids_tree.insert_node(price_level_node)
            if self.best_bid_price_level is None or self.best_bid_price_level.price < price_level_node.price:
                self.best_bid_price_level = price_level_node
            return

        while self._is_bid_matched(order):
            if self.best_ask_price_level.orders.size == 0:
                self.asks_tree.delete_node(self.best_ask_price_level)
                self.best_ask_price_level = self.asks_tree.min_node
                if self.best_ask_price_level is None:
                    price_level_node = PriceLevel(order.price)
                    price_level_node.add_order(order)
                    self.bids_tree.insert_node(price_level_node)
                    if self.best_bid_price_level is None or self.best_bid_price_level.price < price_level_node.price:
                        self.best_bid_price_level = price_level_node
                    return

            maker_order = self.best_ask_price_level.pop_order()

            if maker_order.price > order.price:
                self.best_ask_price_level.re_add_order(maker_order)
                price_level_node = PriceLevel(order.price)
                price_level_node.add_order(order)
                self.bids_tree.insert_node(price_level_node)
                if self.best_bid_price_level is None or self.best_bid_price_level.price < price_level_node.price:
                    self.best_bid_price_level = price_level_node
                return

            if maker_order.volume > order.volume:
                maker_order.volume -= order.volume
                order.volume = 0
                self.best_ask_price_level.re_add_order(maker_order)
                break

            if maker_order.volume == order.volume:
                maker_order.volume = 0
                order.volume = 0
                break

            if maker_order.volume < order.volume:
                order.volume -= maker_order.volume
                maker_order.volume = 0

        if self.best_ask_price_level.orders.size == 0:
            self.asks_tree.delete_node(self.best_ask_price_level)
            self.best_ask_price_level = self.asks_tree.min_node

        if order.volume > 0:
            price_level = self.bids_tree.find(PriceLevel(order.price))
            if not price_level:
                price_level = PriceLevel(order.price)
                price_level.add_order(order)
            if self.best_bid_price_level.price < price_level.price:
                self.best_bid_price_level = price_level

    def _is_bid_matched(self, order: Order):
        if not self.best_ask_price_level:
            return False
        return self.best_ask_price_level.price <= order.price

    def _is_ask_matched(self, order: Order):
        if not self.best_bid_price_level:
            return False
        return self.best_bid_price_level.price >= order.price

    def _execute_ask_order(self, order: Order):
        if not self.best_bid_price_level or self.best_bid_price_level.price < order.price:
            price_level_node = PriceLevel(order.price)
            price_level_node.add_order(order)
            self.asks_tree.insert_node(price_level_node)
            if self.best_ask_price_level is None or self.best_ask_price_level.price > price_level_node.price:
                self.best_ask_price_level = price_level_node
            return

        while self._is_ask_matched(order):
            if self.best_bid_price_level.orders.size == 0:
                self.bids_tree.delete_node(self.best_bid_price_level)
                self.best_bid_price_level = self.bids_tree.max_node
                if self.best_bid_price_level is None:
                    price_level_node = PriceLevel(order.price)
                    price_level_node.add_order(order)
                    self.asks_tree.insert_node(price_level_node)
                    if self.best_ask_price_level is None or self.best_ask_price_level.price > price_level_node.price:
                        self.best_ask_price_level = price_level_node
                    return

            maker_order = self.best_bid_price_level.pop_order()

            if maker_order.price < order.price:
                self.best_bid_price_level.re_add_order(maker_order)
                price_level_node = PriceLevel(order.price)
                price_level_node.add_order(order)
                self.asks_tree.insert_node(price_level_node)
                if self.best_ask_price_level is None or self.best_ask_price_level.price > price_level_node.price:
                    self.best_ask_price_level = price_level_node
                return

            if maker_order.volume > order.volume:
                maker_order.volume -= order.volume
                order.volume = 0
                self.best_bid_price_level.re_add_order(maker_order)
                break

            if maker_order.volume == order.volume:
                maker_order.volume = 0
                order.volume = 0
                break

            if maker_order.volume < order.volume:
                order.volume -= maker_order.volume
                maker_order.volume = 0

        if self.best_bid_price_level.orders.size == 0:
            self.bids_tree.delete_node(self.best_bid_price_level)
            self.best_bid_price_level = self.bids_tree.max_node

        if order.volume > 0:
            price_level = self.asks_tree.find(PriceLevel(order.price))
            if not price_level:
                price_level = PriceLevel(order.price)
                price_level.add_order(order)
            if self.best_ask_price_level.price > price_level.price:
                self.best_ask_price_level = price_level

    def print_bids(self):
        price_levels = self.bids_tree.get_all_nodes()
        price_levels.reverse()
        for pl in price_levels:
            print("Bid ", pl.price, pl.total_volume)

    def print_asks(self):
        price_levels = self.asks_tree.get_all_nodes()
        price_levels.reverse()
        for pl in price_levels:
            print("Ask ", pl.price, pl.total_volume)

    def print_book(self):
        print("=====================")
        print("Side | Price | Volume")
        self.print_asks()
        print("-----")
        self.print_bids()


book = Book()

bid_order_1 = Order(1, 1, 3, 'BUY')
bid_order_2 = Order(2, 2, 2, 'BUY')
bid_order_3 = Order(3, 3, 1, 'BUY')

ask_order_1 = Order(4, 4, 3, 'SELL')
ask_order_2 = Order(5, 5, 2, 'SELL')
ask_order_3 = Order(6, 6, 1, 'SELL')

book.execute_order(bid_order_1)
book.execute_order(bid_order_2)
book.execute_order(bid_order_3)

book.execute_order(ask_order_1)
book.execute_order(ask_order_2)
book.execute_order(ask_order_3)
book.print_book()

bid_order_4 = Order(7, 1, 7, 'SELL')
book.execute_order(bid_order_4)
bid_order_4.print_out()

book.print_book()
