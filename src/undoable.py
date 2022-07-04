
import copy

_undo_stack = {}
_redo_stack = {}

def _getcopy(self, attr):
    return copy.copy(getattr(self, attr))


def undoable(*attr_names):
    def _undoable(f):
        def __undoable(self, *args, **kwargs):
            edit = {k: _getcopy(self, k) for k in attr_names}
            self._undo_stack.append(edit)
            return f(self, *args, **kwargs)
        return __undoable
    return _undoable


def undo(self):
    _do_edit(self, self._undo_stack, self._redo_stack)

def redo(self):
    _do_edit(self, self._redo_stack, self._undo_stack)

def _do_edit(self, pop_stack, push_stack):
        if len(pop_stack) == 0:
            return
        edit = pop_stack.pop()
        redo_edit = {k: _getcopy(self, k) for k in edit.keys()}
        push_stack.append(redo_edit)
        for k in edit:
            setattr(self, k, edit[k])



class Undoable:
    def __init__(self):
        self._undo_stack = []
        self._redo_stack = []

    def undo(self):
        _do_edit(self, self._undo_stack, self._redo_stack)

    def redo(self):
        _do_edit(self, self._redo_stack, self._undo_stack)
        
class UndoableMeta(type):
    def __new__(meta, name, bases, attrs):
        obj = type.__new__(meta, name, bases + (Undoable,), attrs)
        obj._undo_stack = []
        obj._redo_stack = []
        obj.undo = undo
        obj.redo = redo
        return obj


    

    


