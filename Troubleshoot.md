# Work Journal for Braid

Documentation of things I can and can't do with braid.

## Conclusions so far
1. Function calls as notes: braid runs them once, stores their return value, then plays this. This means patterns cannot be context aware, no matter what.
    
    Solution: call from trigger, create the pattern yearly instead of quarterly.

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