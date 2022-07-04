from undoable import Undoable, undoable


class StatefulExtendsUndoable(Undoable):
    def __init__(self, x):
        super().__init__()
        self.x = x

    @undoable('x')
    def set_value(self, x):
        self.x = x


@undoable('x')
class StatefulViaDecorator:
    def __init__(self, x):
        self.x = x

    def set_value(self, x):
        self.x = x
