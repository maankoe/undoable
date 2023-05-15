import unittest

from test.test_utils import StatefulExtendsUndoable


_empty_undo_error_regex = "[Ee]mpty.*[Uu]ndo"
_empty_redo_error_regex = "[Ee]mpty.*[Rr]edo"


Stateful = StatefulExtendsUndoable


class TestUndoable(unittest.TestCase):
    def test_mock(self):
        state = Stateful(1)
        self.assertEqual(1, state.x)

    def test_mock_set_value(self):
        state = Stateful(1)
        state.set_value(2)
        self.assertEqual(2, state.x)

    def test_empty_undo(self):
        state = Stateful(1)
        with self.assertRaisesRegex(IndexError, _empty_undo_error_regex):
            state.undo()

    def test_empty_redo(self):
        state = Stateful(1)
        with self.assertRaisesRegex(IndexError, _empty_redo_error_regex):
            state.redo()

    def test_set_undo(self):
        state = Stateful(1)
        state.set_value(2)
        state.undo()
        self.assertEqual(1, state.x)

    def test_set_undo_undo(self):
        state = Stateful(1)
        state.set_value(2)
        state.undo()
        with self.assertRaisesRegex(IndexError, _empty_undo_error_regex):
            state.undo()

    def test_set_undo_redo(self):
        state = Stateful(1)
        state.set_value(2)
        state.undo()
        state.redo()
        self.assertEqual(2, state.x)

    def test_set_undo_redo_undo(self):
        state = Stateful(1)
        state.set_value(2)
        state.undo()
        state.redo()
        state.undo()
        self.assertEqual(1, state.x)

    def test_set_set_undo(self):
        state = Stateful(1)
        state.set_value(2)
        state.set_value(3)
        state.undo()
        self.assertEqual(2, state.x)

    def test_set_set_undo_redo(self):
        state = Stateful(1)
        state.set_value(2)
        state.set_value(3)
        state.undo()
        state.redo()
        self.assertEqual(3, state.x)

    def test_set_set_undo_undo(self):
        state = Stateful(1)
        state.set_value(2)
        state.set_value(3)
        state.undo()
        state.undo()
        self.assertEqual(1, state.x)

    def test_set_undo_set_undo(self):
        state = Stateful(1)
        state.set_value(2)
        state.undo()
        state.set_value(3)
        state.undo()
        self.assertEqual(1, state.x)

    def test_set_undo_set_redo(self):
        state = Stateful(1)
        state.set_value(2)
        state.undo()
        state.set_value(3)
        with self.assertRaisesRegex(IndexError, _empty_redo_error_regex):
            state.redo()

    def test_set_undo_set_undo_redo(self):
        state = Stateful(1)
        state.set_value(2)
        state.undo()
        state.set_value(3)
        state.undo()
        state.redo()
        self.assertEqual(state.x, 3)
