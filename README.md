# Undoable
Adds an undo and redo stack to state changes in a class via a decorator

The `Undoable` interface has two public functions:
```
class Undoable:
    def undo(self):
        """Undoes last change recorded and puts it on redo stack"""
    
    def redo(self):
        """Redoes last edit on redo stack and puts it on undo stack"""
```

The `@undoable(*member_names)` decorator defines the list of member variables to be recorded
* as they are edited in a decorated method, or
* as their values are changed in a decorated class.

This decorator takes as input the names of variables to record.
Changes to variables not listed cannot be undone.

## Example usage 

### via extension and decorated method

```
class Stateful(Undoable):       # Extends Undoable
    def __init__(self, x):
        super().__init__()
        self.x = x

    @undoable('x')              # Record changes to 'x' in this decorated method
    def set_value(self, x):
        self.x = x
```

```
stateful = Stateful(1)
stateful.set_value(2)
# stateful.x == 2
stateful.undo()
# stateful.x == 1
stateful.redo()
# stateful.x == 2
```


### via decorated class

```
@undoable('x')                  # Record all changes to 'x' in this decorated class
class Stateful:
    def __init__(self, x):
        self.x = x
```

```
stateful = Stateful(1)
stateful.x = 2
# stateful.x == 2
stateful.undo()
# stateful.x == 1
stateful.redo()
# stateful.x == 2
```
