from cvxopt.modeling import variable, op
from node import Node

class Graph:
    def __init__(self, costs=[], producers=[], consumers=[]):
        self.costs = costs
        self.producers = producers
        self.consumers = consumers

    def min_cost(self, array, expected):
        self.costs = []
        self.producers = []
        self.consumers = []

        self.create_graph_from_array(array)
        x = variable(len(self.producers) * len(self.consumers), 'x')
        z = 0
        k = 0
        for i in range(len(self.costs)):
            for j in range(len(self.costs[i])):
                z += self.costs[i][j] * x[k]
                k += 1

        terms = [x >= 0]

        for i in range(len(self.producers)):
            term1 = 0
            temp = 0
            temp += i
            for j in range(len(self.consumers)):
                term1 += x[j + i * len(self.consumers)]
                temp += 1
            terms.append(term1 <= self.producers[i].chips)

        for i in range(len(self.consumers)):
            term2 = 0
            temp = 0
            temp += i
            for j in range(len(self.producers)):
                term2 += x[temp]
                temp += len(self.consumers)
            terms.append(term2 == self.consumers[i].chips)

        problem = op(z, terms)
        problem.solve(solver='glpk')

        print("Chips moves ", problem.objective.value()[0], ", expected " + str(expected))

    def create_graph_from_array(self, array):
        aver = self.average(array)
        for i in range(len(array)):
            if array[i] > aver:
                self.producers.append(Node(array[i] - aver, i))
            elif array[i] < aver:
                self.consumers.append(Node(aver - array[i], i))

        self.costs = [[0 for j in range(len(self.consumers))] for i in range(len(self.producers))]
        for i in range(len(self.producers)):
            for j in range(len(self.consumers)):
                left_diff = self.producers[i].index - self.consumers[j].index
                right_diff = len(array) - self.producers[i].index + self.consumers[j].index

                if left_diff > 0:
                    self.costs[i][j] = min([left_diff, right_diff])
                elif left_diff < 0:
                    left_diff = len(array) - self.consumers[j].index + self.producers[i].index
                    right_diff = self.consumers[j].index - self.producers[i].index
                    self.costs[i][j] = (min([left_diff, right_diff]))

    def average(self, array):
        return self.sum_of_elements(array) / len(array)

    @staticmethod
    def sum_of_elements(array):
        summa = 0
        for item in array:
            summa += item
        return summa