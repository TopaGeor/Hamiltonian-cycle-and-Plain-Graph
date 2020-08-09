import unittest

from hamilton_cycle_and_plain_graph import neighbors
from hamilton_cycle_and_plain_graph import vertices
from hamilton_cycle_and_plain_graph import create_set
from hamilton_cycle_and_plain_graph import should_go


class TestFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = open("testing_graph.txt", "r")
        cls.result_neighbors = [
            ['B', 'C', 'D', 'E', 'H', 'I'],
            ['A', 'C', 'D', 'G', 'I'],
            ['A', 'B', 'D'],
            ['A', 'B', 'C', 'E', 'F'],
            ['A', 'D', 'F', 'H'],
            ['D', 'E', 'G', 'H'],
            ['B', 'F', 'H', 'I'],
            ['A', 'E', 'F', 'G', 'I'],
            ['A', 'B', 'G', 'H']]

        cls.result_vertices = [
            ['AB', 'AC', 'AD', 'AE', 'AH', 'AI'],
            ['BA', 'BC', 'BD', 'BG', 'BI'],
            ['CA', 'CB', 'CD'],
            ['DA', 'DB', 'DC', 'DE', 'DF'],
            ['EA', 'ED', 'EF', 'EH'],
            ['FD', 'FE', 'FG', 'FH'],
            ['GB', 'GF', 'GH', 'GI'],
            ['HA', 'HE', 'HF', 'HG', 'HI'],
            ['IA', 'IB', 'IG', 'IH']]

        cls.hamiltonian_cycle = "IABCDEFGHI"
        cls.updated_neighbors_table = [
            ['C', 'D', 'E', 'H'],
            ['D', 'G', 'I'],
            ['A'],
            ['A', 'B', 'F'],
            ['A', 'H'],
            ['D', 'H'],
            ['B', 'I'],
            ['A', 'E', 'F'],
            ['B', 'G']]

        cls.A = ['IB', 'IG']
        cls.result_create_set = [False, cls.A, 0]

        cls.j_to_i = "C"
        cls.i = 1
        cls.j = "str"
        cls.result_should_go = True

    def test_neighbors(self):
        neighbor_table = neighbors(self.graph)
        self.assertEqual(neighbor_table, self.result_neighbors)

    def test_vertices(self):
        vertices_table = vertices(self.result_neighbors)
        self.assertEqual(vertices_table, self.result_vertices)

    def test_create_set(self):
        set_result = create_set(self.hamiltonian_cycle,
                                self.updated_neighbors_table)
        self.assertEqual(set_result[0], self.result_create_set[0])
        self.assertEqual(set_result[1], self.result_create_set[1])
        self.assertEqual(set_result[2], self.result_create_set[2])

    def test_should_go(self):
        result_should_go = should_go(self.j_to_i, self.A, self.i, self.j)
        self.assertEqual(result_should_go, self.result_should_go)


if __name__ == '__main__':
    unittest.main()
