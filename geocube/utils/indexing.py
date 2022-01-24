
def key_to_range(key, r):
    if isinstance(key, slice):
        s = (
            0 if key.start is None else key.start,
            r if key.stop is None else key.stop,
            1 if key.step is None else key.step
        )
        return s[0], s[1], s[2], slice(None, None, None if s[2] == 1 else s[2])
    return key, key + 1, 1, 0


def empty(size):
    return tuple([slice(None)]*size)
