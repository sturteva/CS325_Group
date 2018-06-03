from numbers import Number

def _comparator(x, y):
    """Default comparator for the mergesort function"""
    return x <= y


def merge(arr, left_index, middle, right_index, comparator):
    """Merges two subarrays of arr[]"""
    sizeOne = middle - left_index + 1
    sizeTwo = right_index - middle

    # create temp arrays
    leftTemp = [0] * (sizeOne)
    rightTemp = [0] * (sizeTwo)

    # Copy data to temp arrays L[] and R[]
    for i in range(0, sizeOne):
        leftTemp[i] = arr[left_index + i]

    for j in range(0, sizeTwo):
        rightTemp[j] = arr[middle + 1 + j]

    # Merge the temp arrays back into arr..r]
    i = 0
    j = 0
    k = left_index

    while i < sizeOne and j < sizeTwo:
        if comparator(leftTemp[i], rightTemp[j]):
            arr[k] = leftTemp[i]
            i += 1
        else:
            arr[k] = rightTemp[j]
            j += 1

        k += 1

    # Copy the remaining elements of L[], if there are any
    while i < sizeOne:
        arr[k] = leftTemp[i]
        i += 1
        k += 1

    # Copy the remaining elements of R[], if there are any
    while j < sizeTwo:
        arr[k] = rightTemp[j]
        j += 1
        k += 1


def mergesort(arr, left_index=None, right_index=None, comparator=None):
    """ Generic mergesort
    use left_index and right_index to sort between two indices
    left defualts to 0
    right defaults to last arr index
    pass a comparator function if you need to define how to compare the the two arrays
    ex:             x.distance <= y.distance
    defaults to:    x <= y
    """

    if left_index is None:
        left_index = 0
    if right_index is None:
        right_index = len(arr) - 1
    if comparator is None:
        comparator = _comparator

    if not isinstance(left_index, Number) or not isinstance(right_index, Number):
        raise Exception('left_index and right_index must be numbers')


    if left_index < right_index:
        middle = (left_index + (right_index - 1)) / 2
        # same as (l+r)/2, but avoids overflow for large l and h

        # Sort first and second halves
        mergesort(arr, left_index, middle, comparator)
        mergesort(arr, middle + 1, right_index, comparator)
        merge(arr, left_index, middle, right_index, comparator)

