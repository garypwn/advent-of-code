from bisect import bisect


class RangeSet:
    """
    A collated series of ranges of unique integers.
    Functionally acts as a sorted set, except that it can store internal ranges as
    start (inclusive) and stop (exclusive) points.
    """

    def __init__(self):
        self.intervals = list()
        self._length = 0

    def __iter__(self):
        """Enumerates over the intervals as if they were a normal list of integers"""
        for interval in self.intervals:
            for i in range(*interval):
                yield i

    def __len__(self):
        if not self._length:
            self._length = sum(i[1] - i[0] for i in self.intervals)

        return self._length

    def add(self, r):
        """
        Adds a range to the series. This can be a tuple of start (inclusive) and stop (exclusive) points,
        or it can be a range object. When r overlaps a range already in the series, it will 'blob' together

        Worst case is O(n) when the underlying list dimension needs to be changed. Best case is O(log(n)) when
        exactly one blob is made and insertion can be done in place.
        """
        if isinstance(r, range):
            r = r.start, r.stop

        # First we identify the previous and next intervals
        idx = bisect(self.intervals, r[0], key=lambda x: x[0])
        left = self.intervals[idx - 1] if idx > 0 else None
        right = self.intervals[idx] if idx < len(self.intervals) else None

        # Make blobs
        # Left blob is easy since there is guaranteed to be at most one range to blob into this one
        blob_l = (left[0], max(r[1], left[1])) if left and left[1] >= r[0] else None

        # Right blob is much harder since the stop point of r may be in a range many indices later
        # i.e. a large number of ranges could be getting blobbed together.
        lr_deleted_flag = False
        if not right:
            blob_r = None
        elif right[0] <= r[1] <= right[1]:
            # Single blob easy case
            blob_r = (r[0], right[1])
        elif r[1] > right[1]:
            # Hard many case
            r_idx = bisect(self.intervals, r[1], lo=idx, key=lambda x: x[0]) - 1
            blob_r = (r[0], max(r[1], self.intervals[r_idx][1]))

            # Now we need to delete the slice of ranges that are getting consumed by the blob.
            # Also, if there's a blob_l, we should do our deletions all at once to save an O(n) operation
            if blob_l:
                del self.intervals[idx:r_idx + 1]
                lr_deleted_flag = True
            else:
                del self.intervals[idx:r_idx]
        else:
            blob_r = None

        # Finally, if r joins the left and right together, it makes a big LR blob.
        blob_lr = (blob_l[0], blob_r[1]) if blob_l and blob_r else None

        # Do insertion
        if blob_lr:
            if not lr_deleted_flag:
                del self.intervals[idx]
            self.intervals[idx - 1] = blob_lr
        elif blob_l:
            self.intervals[idx - 1] = blob_l
        elif blob_r:
            self.intervals[idx] = blob_r
        else:
            self.intervals.insert(idx, r)

        self._length = None
