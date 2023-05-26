import unittest

from test.test_utils import StatefulMulti


_empty_undo_error_regex = "[Ee]mpty.*[Uu]ndo"
_empty_redo_error_regex = "[Ee]mpty.*[Rr]edo"


class TestUndoableMulti(unittest.TestCase):
    def test_mock(self):
        state = StatefulMulti(1, 11)
        self.assertEqual(1, state.x)
        self.assertEqual(11, state.y)

    def test_empty_undo(self):
        state = StatefulMulti(1, 11)
        with self.assertRaisesRegex(IndexError, _empty_undo_error_regex):
            state.undo()

    def test_empty_redo(self):
        state = StatefulMulti(1, 11)
        with self.assertRaisesRegex(IndexError, _empty_redo_error_regex):
            state.redo()

    def test_set_undo(self):
        state = StatefulMulti(1, 11)
        state.x, state.y = 2, 12
        state.undo()
        self.assertEqual(2, state.x)
        self.assertEqual(11, state.y)

    def test_set_undo_undo(self):
        state = StatefulMulti(1, 11)
        state.x, state.y = 2, 12
        state.undo()
        self.assertEqual(11, state.y)
        state.undo()
        self.assertEqual(1, state.x)

    def test_set_undo_undo_redo(self):
        state = StatefulMulti(1, 11)
        state.x, state.y = 2, 12
        state.undo()
        state.undo()
        state.redo()
        self.assertEqual(11, state.y)
        self.assertEqual(2, state.x)
