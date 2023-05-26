import copy


def _get_copy(self, attr):
    return copy.copy(getattr(self, attr))


def _do_edit(self, pop_stack, push_stack):
    pop_edit = pop_stack.pop()
    push_edit = _current_values(self, pop_edit.keys())
    push_stack.append(push_edit)
    for k in pop_edit:
        setattr(self, k, pop_edit[k])


def _current_values(self, attr_names):
    return {k: _get_copy(self, k) for k in attr_names}


def record_status(self, attr_names):
    edit = _current_values(self, attr_names)
    self._undo_stack.append(edit)
    self._redo_stack = []


def undo(self):
    if len(self._undo_stack) == 0:
        raise IndexError("Empty undo stack")
    _do_edit(self, self._undo_stack, self._redo_stack)


def redo(self):
    if len(self._redo_stack) == 0:
        raise IndexError("Empty redo stack")
    _do_edit(self, self._redo_stack, self._undo_stack)
