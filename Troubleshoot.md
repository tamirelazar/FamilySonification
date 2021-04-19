# Work Journal for Braid

Documentation of things I can and can't do with braid.

## Ideas to attempt
* Creating full measures instead of trying to create quarters - can be set through triggers.
    * Also try to get global triggers working.
    * Also!!!!!! try to set the exact same pattern in the beginning of each cycle. This can be implemented in braid as a setting for a thread (refresh pattern every cycle)
* Adding support for partial measure triggers (thread.trigger(func, 0.5, True), etc)


## Conclusions so far
1. Function calls as notes: braid runs them once, stores their return value, then plays this. This means patterns cannot be context aware, no matter what.
    
    Solution: call from trigger, create the pattern yearly instead of quarterly.
2. Braid works with the custom class Thread, but the core.Driver class that controls general playback is a child class of the threading.Thread class (whatever that means).
3. Indeed, it seems every time thread.pattern gets an input, it parses it (all at once). Means i can make this work with precalculating each year, w/ the calculating function getting called from the trigger of global_beat and launches into creating and updating all other threads.
## Things that work
### Playing single note from pattern
for the following pattern
```python
global_beat.pattern = [build_quarter(year, 1), build_quarter(year, 2), build_quarter(year, 3), build_quarter(year, 4)]
```
This works:

```python
def build_quarter(year, q):
    ret = []
    for i in range(q):
        ret.append(q)
    return ret
```

However, this works only for the first time, then doesn't play:
```python
def build_quarter(year, q):
    global_beat.play(2)
```

Also not working:
```python
def build_quarter(year, q):
    sub_beat.play(2) # other thread
```

### Playing single note from trigger
for the following trigger
```python
global_beat.trigger(trig, 1, True)
```

This works:
```python
def trig():
    sub_beat.play(7) # other thread
```

This works very unreliably, probably race condition:
```python
def trig():
    global_beat.play(7) # other thread
```