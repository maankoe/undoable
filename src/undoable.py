
import copy

_undo_stack = {}
_redo_stack = {}

def _getcopy(self, attr):
    return copy.copy(getattr(self, attr))


# def undoable(*attr_names):
#     def _undoable(f):
#         def __undoable(self, *args, **kwargs):
#             if self not in _undo_stack:
#                 _undo_stack[self] = []
#             edit = {k: _getcopy(self, k) for k in attr_names}
#             _undo_stack[self].append(edit)
#             return f(self, *args, **kwargs)
#         return __undoable
#     return _undoable
#
#
# def undo(f):
#     def _undo(self, *args, **kwargs):
#         if self not in _undo_stack or len(_undo_stack[self]) == 0:
#             return
#         edit = _undo_stack[self].pop()
#         redo_edit = {k: _getcopy(self, k) for k in edit.keys()}
#         if self not in _redo_stack:
#             _redo_stack[self] = []
#         _redo_stack[self].append(redo_edit)
#         for k in edit:
#             setattr(self, k, edit[k])
#         return f(self, *args, **kwargs)
#     return _undo
#
# def redo(f):
#     def _redo(self, *args, **kwargs):
#         if self not in _redo_stack or len(_redo_stack[self]) == 0:
#             return
#         edit = _redo_stack[self].pop()
#         for k in edit:
#             setattr(self, k, edit[k])
#         return f(self, *args, **kwargs)
#     return _redo

def undoable(*attr_names):
    def _undoable(f):
        def __undoable(self, *args, **kwargs):
            edit = {k: _getcopy(self, k) for k in attr_names}
            self._undo_stack.append(edit)
            return f(self, *args, **kwargs)
        return __undoable
    return _undoable


class Undoable:
    def __init__(self):
        self._undo_stack = []
        self._redo_stack = []

    def _do_edit(self, pop_stack, push_stack):
        if len(pop_stack) == 0:
            return
        edit = pop_stack.pop()
        redo_edit = {k: _getcopy(self, k) for k in edit.keys()}
        push_stack.append(redo_edit)
        for k in edit:
            setattr(self, k, edit[k])

    def undo(self):
        self._do_edit(self._undo_stack, self._redo_stack)

    def redo(self):
        self._do_edit(self._redo_stack, self._undo_stack)


class State(Undoable):
    a = "Hello"
    b = "world"

    @undoable('a', 'b')
    def set_a(self, x):
        self.a = x
        self.b = x



state = State()

print(state.a, state.b)

state.set_a(1)

print(state.a, state.b)

state.undo()

print(state.a, state.b)

state.redo()

print(state.a, state.b)
