
def _comparator(x, y):
    """Default comparator for the mergesort function"""
    return x <= y


def merge(arr, leftIndex, middle, rightIndex, comparator):
    """Merges two subarrays of arr[]"""
    sizeOne = middle - leftIndex + 1
    sizeTwo = rightIndex - middle

    # create temp arrays
    leftTemp = [0] * (sizeOne)
    rightTemp = [0] * (sizeTwo)

    # Copy data to temp arrays L[] and R[]
    for i in range(0, sizeOne):
        leftTemp[i] = arr[leftIndex + i]

    for j in range(0, sizeTwo):
        rightTemp[j] = arr[middle + 1 + j]

    # Merge the temp arrays back into arr..r]
    i = 0
    j = 0
    k = leftIndex

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


def mergesort(arr, leftIndex=None, rightIndex=None, comparator=None):
    """ Generic mergesort
    use leftIndex and rightIndex to sort between two indices
    left defualts to 0
    right defaults to last arr index
    pass a comparator function if you need to define how to compare the the two arrays
    ex:             x.distance <= y.distance
    defaults to:    x <= y
    """
    if leftIndex is None:
        leftIndex = 0
    if rightIndex is None:
        rightIndex = len(arr) - 1
    if comparator is None:
        comparator = _comparator

    if leftIndex < rightIndex:
        middle = (leftIndex + (rightIndex - 1)) / 2
        # same as (l+r)/2, but avoids overflow for large l and h

        # Sort first and second halves
        mergesort(arr, leftIndex, middle, comparator)
        mergesort(arr, middle + 1, rightIndex, comparator)
        merge(arr, leftIndex, middle, rightIndex, comparator)

