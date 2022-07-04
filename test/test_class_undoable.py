from test_utils import StatefulViaDecorator
import test_undoable


test_undoable.Stateful = StatefulViaDecorator

class TestClassUndoable(test_undoable.TestUndoable):
    pass