import types
import inspect

from undoable_utils import undo, redo, record_status


def undoable(*attr_names):
    def _undoable(decorated):
        if inspect.isclass(decorated):
            return _undoable_class_decorator(decorated, *attr_names)
        elif isinstance(decorated, types.FunctionType):
            return _undoable_method_decorator(decorated, *attr_names)
    return _undoable


class Undoable:
    def __init__(self):
        self._undo_stack = []
        self._redo_stack = []

    undo = undo
    redo = redo

    def __str__(self):
        return f"{self._undo_stack}:{self._redo_stack}"


def _init(original_init, *members):
    def __init(self, *args, **kwargs):
        for member_name in members:
            setattr(self, "_" + member_name, None)
        self._undo_stack = []
        self._redo_stack = []
        original_init(self, *args, **kwargs)
        # We have to clear the undo/redo stack after init as this performs edits
        self._redo_stack = []
        self._undo_stack = []
    return __init


def _create_property(member_name):
    backing_member_name = "_" + member_name
    @property
    def member(self):
        return getattr(self, backing_member_name)

    @member.setter
    @undoable(backing_member_name)
    def member(self, value):
        return setattr(self, backing_member_name, value)

    return member


def _undoable_method_decorator(f, *attr_names):
    def __undoable(self, *args, **kwargs):
        record_status(self, attr_names)
        return f(self, *args, **kwargs)

    return __undoable


def _undoable_class_decorator(cls, members):
    cls.__init__ = _init(cls.__init__, *members)
    cls.undo = undo
    cls.redo = redo
    for member_name in members:
        setattr(cls, member_name, _create_property(member_name))
    return cls
