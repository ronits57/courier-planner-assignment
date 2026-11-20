"""Phase 2 - parcel prioritisation.

Merge sort is chosen as the main algorithm: O(n log n) in best/average/worst
case, and *stable*, so parcels with equal keys keep their input order.
Insertion sort and quick sort are included only for the runtime comparison.
"""


def merge_sort(items, key):
    """Return a new list sorted ascending by key(item). Stable, O(n log n)."""
    if len(items) <= 1:
        return list(items)
    mid = len(items) // 2
    left = merge_sort(items[:mid], key)
    right = merge_sort(items[mid:], key)
    merged, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):      # <= keeps the sort stable
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def insertion_sort(items, key):
    """O(n^2) baseline used for comparison."""
    a = list(items)
    for i in range(1, len(a)):
        cur, k = a[i], key(a[i])
        j = i - 1
        while j >= 0 and key(a[j]) > k:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = cur
    return a


def quick_sort(items, key):
    """Quick sort with median-of-three pivot (comparison only)."""
    a = list(items)

    def qs(lo, hi):
        while lo < hi:
            mid = (lo + hi) // 2
            trio = sorted([(key(a[lo]), lo), (key(a[mid]), mid), (key(a[hi]), hi)])
            p = trio[1][1]
            a[p], a[hi] = a[hi], a[p]
            pivot = key(a[hi])
            i = lo
            for j in range(lo, hi):
                if key(a[j]) < pivot:
                    a[i], a[j] = a[j], a[i]
                    i += 1
            a[i], a[hi] = a[hi], a[i]
            # recurse on smaller side, loop on larger -> O(log n) stack
            if i - lo < hi - i:
                qs(lo, i - 1); lo = i + 1
            else:
                qs(i + 1, hi); hi = i - 1

    qs(0, len(a) - 1)
    return a


def prioritise(parcels):
    """Earliest deadline first; ties broken by higher priority score."""
    return merge_sort(parcels, key=lambda p: (p.deadline, -p.priority))
