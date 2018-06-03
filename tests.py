import unittest
from mergesort import mergesort
from tsp import (
    create_edge_list,
    Vertex,
    Edge,
)

class TestMergeSort(unittest.TestCase):

    def test_merges_already_sorted_array(self):
        arr = [-3, -2, -1, 0, 1, 2, 3]
        mergesort(arr)

        self.assertSequenceEqual(
            arr,
            [-3, -2, -1, 0, 1, 2, 3],
        )

    def test_merges_reversed_array(self):
        arr = [3, 2, 1, 0, -1, -2, -3]
        mergesort(arr)

        self.assertSequenceEqual(
            arr,
            [-3, -2, -1, 0, 1, 2, 3],
        )

    def test_merges_multiple_same_entries(self):
        arr = [1, 1, 3, -2, -2, -5, 5, 3, -2]
        mergesort(arr)

        self.assertSequenceEqual(
            arr,
            [-5, -2, -2, -2, 1, 1, 3, 3, 5],
        )

    def test_merges_with_comparator_function(self):
        arr = [
            {'val': 4},
            {'val': 1},
            {'val': 3},
            {'val': 2},
            {'val': 0},
        ];

        def _comparator(x, y):
            return x['val'] <= y['val']

        mergesort(arr, comparator=_comparator)

        self.assertSequenceEqual(
            arr,
            [
                {'val': 0},
                {'val': 1},
                {'val': 2},
                {'val': 3},
                {'val': 4},
            ],
        )

    def test_merges_only_between_given_indices(self):
        """
        Not actually sure we need this, saw that we had functionality
        for it so I'd rather test for it and remove later if we don't need it
        rather than break it and find out we do need it.
        """
        arr = [3, 2, 6, 1, 4, 4, 7, 2, 3, 4]
        mergesort(arr, 1, 4)
        self.assertSequenceEqual(
            arr,
            [3, 1, 2, 4, 6, 4, 7, 2, 3, 4],
        )

    def test_merges_empty_array(self):
        arr = []
        mergesort(arr)
        self.assertSequenceEqual(
            arr,
            [],
        )


class TestCreateEdgeList(unittest.TestCase):

    def test_edge_list(self):
        vertices = [Vertex(i, i * 2, i * 2) for i in range(4)]
        edge_list = create_edge_list(vertices)

        self.assertEqual(len(edge_list), 6)
        expected = [
            {'v1': 0, 'v2': 1, 'distance': 3},
            {'v1': 0, 'v2': 2, 'distance': 6},
            {'v1': 0, 'v2': 3, 'distance': 8},
            {'v1': 1, 'v2': 2, 'distance': 3},
            {'v1': 1, 'v2': 3, 'distance': 6},
            {'v1': 2, 'v2': 3, 'distance': 3},
        ]
        actual = [{'v1': edge.v1.id, 'v2': edge.v2.id, 'distance': edge.distance} for edge in edge_list]
        self.assertSequenceEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
