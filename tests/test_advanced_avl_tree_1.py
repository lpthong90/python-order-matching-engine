# from order_book.advanced_avl_tree import AdvancedAVLTree
# from tests.common import TestAdvancedAVLTree
from tests.common import check_advanced_avl_tree


def test_1():
    inputs = [
        ('insert', 1, 1),
        ('insert', 2, 2),
        ('insert', 3, 3),
        ('insert', 4, 4),
        ('insert', 5, 5),
        ('insert', 6, 6),
    ]
    outputs = {
        "parents": [(1, 2), (2, 4), (3, 2), (4, None), (5, 4), (6, 5)]
    }
    check_advanced_avl_tree(inputs, outputs)


def test_2():
    inputs = [
        ('insert', 1, 1),
        ('insert', 2, 2),
        ('insert', 3, 3),
        ('insert', 4, 4),
        ('insert', 5, 5),
        ('insert', 6, 6),
        ('delete', 4, None),
    ]
    outputs = {
        "parents": [(1, 2), (2, 5), (3, 2), (5, None), (6, 5)]
    }
    check_advanced_avl_tree(inputs, outputs)


def test_3():
    inputs = [
        ('insert', 1, 1),
        ('insert', 2, 2),
        ('insert', 3, 3),
        ('insert', 4, 4),
        ('insert', 5, 5),
        ('insert', 6, 6),
        ('delete', 4, None),
        ('delete', 5, None),
    ]
    outputs = {
        "parents": [(1, 2), (2, None), (3, 6), (6, 2)]
    }
    check_advanced_avl_tree(inputs, outputs)