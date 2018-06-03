import unittest
from mergesort import mergesort
from tsp import (
    create_edge_list,
    distance_comparator,
    does_create_cycle,
    create_tour,
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

    def test_merges_larger_edge_set(self):
        larger_inputs = [
            [0, 1, 1], [1, 2, 4], [2, 3, 6], [3, 1, 5],
            [4, 3, 4], [5, 6, 2], [6, 7, 2], [7, 9, 1],
            [8, 2, 2], [9, 0, 5], [10, 7, 2], [11, 3, 4],
            [12, 4, 8], [13, 6, 2], [14, 1, 3], [15, 4, 9],
        ]

        vertices = [Vertex(id, x, y) for id, x, y in larger_inputs]
        edge_list = create_edge_list(vertices)
        mergesort(edge_list, comparator=distance_comparator)

        prev_distance = 0
        for edge in edge_list:
            dist = edge.distance - prev_distance
            if dist < 0:
                raise Exception('Merge did not sort by distance asc')


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

    def test_longer_edge_list(self):
        larger_inputs = [
            [0, 1, 1], [1, 2, 4], [2, 3, 6], [3, 1, 5],
            [4, 3, 4], [5, 6, 2], [6, 7, 2], [7, 9, 1],
            [8, 2, 2], [9, 0, 5], [10, 7, 2], [11, 3, 4],
            [12, 4, 8], [13, 6, 2], [14, 1, 3], [15, 4, 9],
        ]

        vertices = [Vertex(id, x, y) for id, x, y in larger_inputs]
        edge_list = create_edge_list(vertices)
        actual = [[edge.v1.id, edge.v2.id] for edge in edge_list]
        expected = [
            [0, 1,], [0, 2,], [0, 3,], [0, 4,], [0, 5,], [0, 6,], [0, 7,], [0, 8,], [0, 9,],
            [0, 10,], [0, 11,], [0, 12,], [0, 13,], [0, 14,], [0, 15,], [1, 2,], [1, 3,],
            [1, 4,], [1, 5,], [1, 6,], [1, 7,], [1, 8,], [1, 9,], [1, 10,], [1, 11,], [1, 12,],
            [1, 13,], [1, 14,], [1, 15,], [2, 3,], [2, 4,], [2, 5,], [2, 6,], [2, 7,], [2, 8,],
            [2, 9,], [2, 10,], [2, 11,], [2, 12,], [2, 13,], [2, 14,], [2, 15,], [3, 4,], [3, 5,],
            [3, 6,], [3, 7,], [3, 8,], [3, 9,], [3, 10,], [3, 11,], [3, 12,], [3, 13,], [3, 14,],
            [3, 15,], [4, 5,], [4, 6,], [4, 7,], [4, 8,], [4, 9,], [4, 10,], [4, 11,], [4, 12,],
            [4, 13,], [4, 14,], [4, 15,], [5, 6,], [5, 7,], [5, 8,], [5, 9,], [5, 10,], [5, 11,],
            [5, 12,], [5, 13,], [5, 14,], [5, 15,], [6, 7,], [6, 8,], [6, 9,], [6, 10,], [6, 11,],
            [6, 12,], [6, 13,], [6, 14,], [6, 15,], [7, 8,], [7, 9,], [7, 10,], [7, 11,], [7, 12,],
            [7, 13,], [7, 14,], [7, 15,], [8, 9,], [8, 10,], [8, 11,], [8, 12,], [8, 13,], [8, 14,],
            [8, 15,], [9, 10,], [9, 11,], [9, 12,], [9, 13,], [9, 14,], [9, 15,], [10, 11,],
            [10, 12,], [10, 13,], [10, 14,], [10, 15,], [11, 12,], [11, 13,], [11, 14,], [11, 15,],
            [12, 13,], [12, 14,], [12, 15,], [13, 14,], [13, 15,], [14, 15,],
        ]
        self.assertEqual(len(edge_list), 120)
        self.assertSequenceEqual(actual, expected)


class TestCreateTour(unittest.TestCase):

    def test_basic_edge_list(self):
        coords = [[1, 1], [2, 4], [3, 6], [1, 5], [3, 4], [6, 2]]
        cities = [Vertex(i, coord[0], coord[1]) for i, coord in enumerate(coords)]

        edge_list = create_edge_list(cities)
        mergesort(edge_list, comparator=distance_comparator)

        tour_list, distance = create_tour(edge_list, len(cities))

        self.assertEqual(len(tour_list), 6)
        self.assertEqual(distance, 18)
        edge_vertices = [[edge.v1.id, edge.v2.id] for edge in tour_list]
        self.assertSequenceEqual(
            edge_vertices,
            [[1, 3], [1, 4], [2, 3], [0, 4], [0, 5], [2, 5]],
        )


class TestDoesCreateCycle(unittest.TestCase):

    def test_does_create_cycle_v1_to_v2(self):
        vertices = [Vertex(i, i * 2, i * 2) for i in range(4)]

        tour_list = [
            Edge(vertices[0], vertices[1]),
            Edge(vertices[1], vertices[2]),
        ]
        has_cycle = does_create_cycle(tour_list, Edge(vertices[2], vertices[0]))
        self.assertEqual(has_cycle, True)


    def test_does_create_cycle_v2_to_v1(self):
        vertices = [Vertex(i, i * 2, i * 2) for i in range(4)]

        tour_list = [
            Edge(vertices[0], vertices[1]),
            Edge(vertices[1], vertices[2]),
        ]
        has_cycle = does_create_cycle(tour_list, Edge(vertices[0], vertices[2]))
        self.assertEqual(has_cycle, True)

    def test_does_not_create_cycle(self):
        vertices = [Vertex(i, i * 2, i * 2) for i in range(4)]

        tour_list = [
            Edge(vertices[0], vertices[1]),
            Edge(vertices[1], vertices[2]),
        ]
        has_cycle = does_create_cycle(tour_list, Edge(vertices[2], vertices[3]))
        self.assertEqual(has_cycle, False)

    def test_can_add_to_empty_list(self):
        vertices = [Vertex(i, i * 2, i * 2) for i in range(4)]

        tour_list = []
        has_cycle = does_create_cycle(tour_list, Edge(vertices[2], vertices[3]))
        self.assertEqual(has_cycle, False)

    def test_can_add_to_one_item_list(self):
        vertices = [Vertex(i, i * 2, i * 2) for i in range(4)]

        tour_list = [Edge(vertices[1], vertices[2])]
        has_cycle = does_create_cycle(tour_list, Edge(vertices[0], vertices[1]))
        self.assertEqual(has_cycle, False)

    def test_can_add_to_one_item_list_reverse_vertices(self):
        vertices = [Vertex(i, i * 2, i * 2) for i in range(4)]

        tour_list = [Edge(vertices[1], vertices[2])]
        has_cycle = does_create_cycle(tour_list, Edge(vertices[1], vertices[0]))
        self.assertEqual(has_cycle, False)

    def test_real_use_case(self):
        inputs = [
            [0, 1, 1,],
            [1, 2, 4,],
            [2, 3, 6,],
            [3, 1, 5,],
            [4, 3, 4,],
            [5, 6, 2,],
            [6, 7, 2,],
            [7, 1, 2,],
        ]
        vertices = [Vertex(id, x, y) for id, x, y in inputs]

        tour_list = [
            Edge(vertices[0],vertices[7]),
            Edge(vertices[1],vertices[3]),
            Edge(vertices[1],vertices[4]),
            Edge(vertices[5],vertices[6]),
            Edge(vertices[2],vertices[3]),
        ]

        has_cycle = does_create_cycle(tour_list, Edge(vertices[2], vertices[4]))
        self.assertEqual(has_cycle, True)




if __name__ == '__main__':
    unittest.main()
