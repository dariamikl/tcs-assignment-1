# Created by dariamiklashevskaya at 16/09/2018
import re

warnings = {
    'W1': 'Accepting state is not defined',
    'W2': 'Some states are not reachable from initial state',
    'W3': 'FSA is nondeterministic', }

'''Warnings'''
WARNING1 = 'W1: Accepting state is not defined'
WARNING2 = 'W2: Some states are not reachable from initial state'
WARNING3 = 'W3: FSA is nondeterministic'

warnings_raised = []
report = ""
template = r'states={((\w+,)*\w+|'')}\nalpha={((\w+,)*\w+|'')}\ninit.st={((\w+,)*\w+|'')}\nfin.st={((\w+,)*\w+|'')}\ntrans={((\w+>\w+>\w+,)*\w+>\w+>\w+|'')}'

f = open("result.txt", 'w')


class Error(Exception):
    name = 'Error:'
    message = ''

    def __str__(self):
        return '{0}: {1}'.format(self.name, self.message)


class E1(Error):
    name = 'E1'

    def __init__(self, state):
        super().__init__()
        self.message = "A state '{0}' is not in set of states".format(state)


class E2(Error):
    name = 'E2'
    message = 'Some states are disjoint'


class E3(Error):
    name = 'E3'

    def __init__(self, trans):
        super().__init__()
        self.message = "A transition '{0}' is not represented in the alphabet".format(trans)


class E4(Error):
    name = 'E4'
    message = 'Initial state is not defined'


class E5(Error):
    name = 'E5'
    message = 'Input file is malformed'


def init():
    file = open("fsa.txt", "r")
    content = file.read()
    check_input(content)
    content_list = content.split("\n")
    # for i in range(content_list.__len__()):
    #     f.write(f'{i}. {content_list.__getitem__(i)}')
    states = parse_into_list(content_list.__getitem__(0))
    alpha = parse_into_list(content_list.__getitem__(1))
    init_state = parse_into_list(content_list.__getitem__(2))[0]
    fin_states = parse_into_list(content_list.__getitem__(3))
    trans_list = parse_into_list(content_list.__getitem__(4))

    # f.write(f'states: {states}\n')
    # f.write(f'alphabet: {alpha}\n')
    # f.write(f'initial state: {init_state}\n')
    # f.write(f'final states: {fin_states}\n')
    # f.write(f'transition list: {trans_list}\n')

    # checking
    check_init_state(init_state, states)
    check_accepting_states(fin_states, states)
    parsed_trans_list = parse_transitions(trans_list, states, alpha)
    # f.write(parsed_trans_list)
    check_components(states, init_state, parsed_trans_list)
    complete = check_completeness(states, parsed_trans_list, alpha)
    if complete:
        f.write("FSA is complete")
    else:
        f.write("FSA is incomplete")
    write_warnings(warnings_raised)


def add_state(state, states):
    states.append(state)


def add_alphabet_item():
    pass


def add_finite_state():
    pass


def add_initial_state(state):
    pass


def create_transition_matrix():
    pass


def add_transition():
    pass


def check_input(content):
    match = re.match(template, content)
    # f.write(content)
    if not match:
        raise E5()


def parse_into_list(str):
    str_list = str[str.find("{") + 1:str.find("}")].split(',')

    # f.write(str_list)
    return str_list


def parse_transitions(trans_list, states, alpha):
    adjacency_matrix = []
    parsed_list = []

    for trans in trans_list:
        parsed_items = trans.split('>')
        # f.write(parsed_items)
        check_states([parsed_items[0], parsed_items[2]], states)
        check_transition(parsed_items[1], alpha)
        parsed_list.append(parsed_items)

    return parsed_list


def check_init_state(state, states):
    check_states([state], states)
    if not state:
        raise E4()


def check_states(states_to_validate, states):
    for state in states_to_validate:
        if not states.__contains__(state) and state:
            raise E1(state)


def raise_warning(warning):
    warnings_raised.append(warning)


'''Warnings'''


def write_warnings(w_list):
    w_list = list(set(w_list))
    w_list.sort()

    if w_list:
        f.write("\nWarning:")

    for warning in w_list:
        f.write('\n{0}'.format(warning))


def check_accepting_states(fin_states, states):
    if fin_states.__len__() == 1 and fin_states[0].__eq__(''):
        raise_warning(WARNING1)

    check_states(fin_states, states)


def check_transition(transition, alpha):
    if not alpha.__contains__(transition):
        raise E3(transition)


def dfs(graph, first, visited={}):
    visited = set(list(visited) + [first])

    not_visited = set([t[2] for t in graph[first]]) - visited

    for next in not_visited:
        visited = set(list(visited) + list(dfs(graph, next, visited)))
    return visited


def check_components(states, init_state, parsed_trans_list):
    graph = {}

    for state in states:
        graph[state] = []

    for transition in parsed_trans_list:
        graph[transition[0]].append(transition)

    is_one = False

    for state in states:
        component = dfs(graph, state)
        if component.__len__() != states.__len__():
            raise_warning(WARNING2)
        is_one = is_one or component.__len__() == states.__len__()

    if not is_one:
        raise E2


def check_completeness(states, parsed_trans_list, alpha):
    res = True
    d = {}

    for state in states:
        d[state] = []

    for transition in parsed_trans_list:
        d[transition[0]] += [transition[1]]

    for k in d:
        res = len(set(d[k])) == len(alpha) and res

        if res and len(set(d[k])) != len(d[k]):
            raise_warning(WARNING3)

    return res


try:
    init()
except Error as e:
    f.write("Error:\n")
    f.write(str(e))
