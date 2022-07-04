import unittest

from undoable import *


# class Stateful(Undoable):
#     def __init__(self, x):
#       super().__init__()
#       self.x = x

#     @undoable('x')
#     def set_value(self, x):
#         self.x = x

class StatefulMeta(metaclass=UndoableMeta):
    def __init__(self, x):
        self.x = x

    @undoable('x')
    def set_value(self, x):
        self.x = x


class Stateful(Undoable):
    def __init__(self, x):
        super().__init__()
        self.x = x

    @undoable('x')
    def set_value(self, x):
        self.x = x


class TestUndoable(unittest.TestCase):
    def test_undoable_meta(self):
        state = StatefulMeta("Hello")
        self.assertEqual("Hello", state.x)
        state.set_value("world")
        self.assertEqual("world", state.x)
        state.undo()
        self.assertEqual("Hello", state.x)
        state.redo()
        self.assertEqual("world", state.x)

    def test_undoable(self):
        state = Stateful("Hello")
        self.assertEqual("Hello", state.x)
        state.set_value("world")
        self.assertEqual("world", state.x)
        state.undo()
        self.assertEqual("Hello", state.x)
        state.redo()
        self.assertEqual("world", state.x)