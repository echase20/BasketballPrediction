listsoffar = []
a = 0
b = 0
c = 0
import random
class Node:
    def __init__(self, data):
        self.data = data
        self.children = []
    def add_children(self, node):
        self.children.append(node)

def make_tree2():
    top = Node("")
    for i in range(11):
        first_level = Node([i*10, 1])
        top.add_children(first_level)
        remainder = 100 - first_level.data[0]
        iterations = remainder / 10
        for j in range(int(iterations) + 1):
            second_level = Node([j*10, 2])
            first_level.add_children(second_level)
            remainder = 100 - second_level.data[0] - first_level.data[0]
            iterations = remainder / 10
            for k in range(int(iterations) + 1):
                third_level = Node([k*10, 3])
                second_level.add_children(third_level)
                remainder = 100 - third_level.data[0] - second_level.data[0] - first_level.data[0]
                iterations = remainder / 10
                for a in range(int(iterations) + 1):
                    fourth_level = Node([a*10, 4])
                    third_level.add_children(fourth_level)
                    remainder = 100 - fourth_level.data[0] - third_level.data[0] - second_level.data[0] - first_level.data[0]
                    first_level_values = get_possible_values(first_level.data[0])
                    second_level_values = get_possible_values(second_level.data[0])
                    third_level_values = get_possible_values(third_level.data[0])
                    fourth_level_values = get_possible_values(fourth_level.data[0])
                    fifth_level_values = get_possible_values(remainder - 10)
                    for b in range(5):
                        first_variable = random.choice(first_level_values)
                        second_variable = random.choice(second_level_values)
                        third_variable = random.choice(third_level_values)
                        fourth_variable = random.choice(fourth_level_values)
                        fifth_variable = random.choice(fifth_level_values)
                        total = first_variable + second_variable + third_variable + fourth_variable + fifth_variable
                        if (total != 100):
                            if 100 - total > 0:
                                variables = [1,2,3,4,5]
                                difference = 100 - total
                                choice = random.choice(variables)
                                if choice == 1:
                                    first_variable += difference
                                if choice == 2:
                                    second_variable += difference
                                if choice == 3:
                                    third_variable += difference
                                if choice == 4:
                                    fourth_variable += difference
                                if choice == 5:
                                    fifth_variable += difference
                                fifth_level = Node([[first_variable, second_variable, third_variable, fourth_variable, fifth_variable], 5])
                                fourth_level.add_children(fifth_level)
                            if 100 - total < 0:
                                variables = [first_variable, second_variable, third_variable, fourth_variable, fifth_variable]
                                difference = total - 100
                                highest_value = max(variables)
                                if highest_value == first_variable:
                                    first_variable -= difference
                                if highest_value == second_variable:
                                    second_variable -= difference
                                if highest_value == third_variable:
                                    third_variable -= difference
                                if highest_value == fourth_variable:
                                    fourth_variable -= difference
                                if highest_value == fifth_variable:
                                    fifth_variable -= difference
                                fifth_level = Node(
                                    [[first_variable, second_variable, third_variable, fourth_variable, fifth_variable],
                                     5])
                                fourth_level.add_children(fifth_level)
                        else:
                            fifth_level = Node(
                                [[first_variable, second_variable, third_variable, fourth_variable, fifth_variable],
                                 5])
                            fourth_level.add_children(fifth_level)
    return top
def print_node(node):
    t = 0
    print(node.data)
    if len(node.children) != 0:
        for i in range(len(node.children)):
            print_node(node.children[i])
def get_possible_values(number):
    if number == 100:
        return [100]
    else:
        list_of_values = []
        for i in range(10):
            list_of_values.append(number + i)
        return list_of_values
print_node(make_tree2())