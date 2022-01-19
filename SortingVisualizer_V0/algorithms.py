from VisualArray import VisualArray, Bar, Union, _resolution
from types import FunctionType


"""Insertion Sort"""


def insertion_sort(arr: Union[VisualArray, list]) -> None:
    if isinstance(arr, list):
        arr: VisualArray = VisualArray(arr)
        arr.run()

    for i in range(1, len(arr)):
        val: int = arr[i].val

        j: int = i - 1
        while 0 <= j and val < arr[j]:
            arr.select(i)
            arr.select_2(j + 1)
            arr.select_2(j)

            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = val

    arr.end_sort()

    while True:
        if arr.check_input(insertion_sort) == 3:
            return


def default_insertion_sort() -> None:
    __default_array: VisualArray = VisualArray(sample_size=40, delay=0.009)
    __default_array.run()

    insertion_sort(__default_array)


"""Bubble Sort"""


def bubble_sort(arr: Union[VisualArray, list]) -> None:
    if isinstance(arr, list):
        arr: VisualArray = VisualArray(arr)
        arr.run()

    for i in range(len(arr) - 1):
        for j in range(len(arr) - i - 1):
            arr.select(len(arr) - i - 1)
            arr.select_2(j + 1)
            arr.select_2(j)

            if arr[j + 1] < arr[j]:
                arr[j + 1], arr[j] = arr[j], arr[j + 1]

    arr.end_sort()

    while True:
        if arr.check_input(bubble_sort) == 3:
            return


def default_bubble_sort() -> None:
    __default_array: VisualArray = VisualArray(sample_size=80, delay=0.0004)
    __default_array.run()

    bubble_sort(__default_array)


"""Quick Sort"""


def _partition(start: int, end: int, array: VisualArray) -> int:
    pivot_index: int = start
    pivot: Bar = array[pivot_index]

    while start < end:
        array.select(pivot_index)
        array.select_2(start)
        array.select_2(end)

        while start < len(array) and array[start] <= pivot:
            start += 1

        while array[end] > pivot:
            end -= 1

        if start < end:
            array[start], array[end] = array[end], array[start]

    array[end], array[pivot_index] = array[pivot_index], array[end]

    return end


def _real_quick_sort(array: VisualArray, start: int, end: int) -> None:
    if start < end:
        p: int = _partition(start, end, array)

        _real_quick_sort(array, start, p - 1)
        _real_quick_sort(array, p + 1, end)


def quick_sort(array: Union[VisualArray, list]) -> None:
    if isinstance(array, list):
        array = VisualArray(array)
        array.run()

    _real_quick_sort(array, 0, len(array) - 1)
    array.end_sort()

    while True:
        if array.check_input() == 3:
            array.running = False
            _real_quick_sort(array, 0, len(array) - 1)


def default_quick_sort() -> None:
    __default_array: VisualArray = VisualArray(sample_size=_resolution[0], delay=0.0005)
    __default_array.run()

    _real_quick_sort(__default_array, 0, len(__default_array) - 1)
    __default_array.end_sort()

    while True:
        if __default_array.check_input() == 3:
            __default_array.running = False
            _real_quick_sort(__default_array, 0, len(__default_array) - 1)


"""Merge Sort"""


def merge_sort(array: Union[VisualArray, list]) -> None:
    if isinstance(array, list):
        array: VisualArray = VisualArray(array)
        array.run()

    unit: int = 1
    while unit <= len(array):
        for h in range(0, len(array), unit * 2):
            l, r = h, min(len(array), h + 2 * unit)
            mid: int = h + unit

            # merge xs[h:h + 2 * unit]
            p, q = l, mid
            while p < mid and q < r:
                # use <= for stable merge merge
                array.select_2(mid)
                array.select_2(p)
                array.select_2(q)

                if array[p] <= array[q]:
                    p += 1
                else:
                    tmp: Bar = array[q]
                    array[p + 1: q + 1] = array[p:q]
                    array[p] = tmp
                    p, mid, q = p + 1, mid + 1, q + 1

        unit *= 2

    array.end_sort()


def default_merge_sort() -> None:
    __default_array: VisualArray = VisualArray(sample_size=360, delay=0.0005)
    __default_array.run()

    merge_sort(__default_array)

    while True:
        if __default_array.check_input() == 3:
            merge_sort(__default_array)


"""Testing functions"""


def is_sorted(iterable: any, invalidator_predicate: FunctionType = lambda x, y: x < y) -> bool:
    """Applies the invalidating predicate on every (i-1)th and (i)th element in the given iterable.
       returns false if any two elements validate the predicate.
       Default is iterable[i - 1] < iterable[i]"""

    for i in range(1, len(iterable)):
        if invalidator_predicate(iterable(i), iterable(i - 1)):
            return False

    return True


"""In Progress"""


if __name__ == "__main__":
    default_quick_sort()
