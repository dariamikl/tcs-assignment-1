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


class Error(Exception):
    name = 'Error:'
    message = ''

    def __str__(self):
        return '{0}: {1}'.format(self.name, self.message)


class E1(Error):
    name = 'E1'

    def __init__(self, state):
        super().__init__()
        self.message = 'A state {0} is not in set of states'.format(state)


class E2(Error):
    name = 'E2'
    message = 'Some states are disjoint'


class E3(Error):
    name = 'E3'

    def __init__(self, trans):
        super().__init__()
        self.message = 'A transition {0} is not represented in the alphabet'.format(trans)


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
    for i in range(content_list.__len__()):
        print(f'{i}. {content_list.__getitem__(i)}')
    states = parse_into_list(content_list.__getitem__(0))
    alpha = parse_into_list(content_list.__getitem__(1))
    init_state = parse_into_list(content_list.__getitem__(2))[0]
    fin_states = parse_into_list(content_list.__getitem__(3))
    trans_list = parse_into_list(content_list.__getitem__(4))
    print(f'states: {states}\n')
    print(f'alphabet: {alpha}\n')
    print(f'initial state: {init_state}\n')
    print(f'final states: {fin_states}\n')
    print(f'transition list: {trans_list}\n')
    check_init_state(init_state)
    # check_state(init_state, states)
    check_accepting_st(fin_states)
    print_warnings(warnings_raised)
    parse_transitions(trans_list, states, alpha)


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
    print(content)
    if not match:
        raise E5()


def parse_into_list(str):
    str_list = str[str.find("{") + 1:str.find("}")].split(',')

    print(str_list)
    return str_list


def parse_transitions(list, states, alpha):
    adjacency_matrix = []
    # for
    for trans in list:
        parsed_items = trans.split('>')
        print(parsed_items)
        check_states({parsed_items[0], parsed_items[2]}, states)
        check_transition(parsed_items[1], alpha)


def check_init_state(state):
    if not state:
        raise E4()


def check_states(states_to_validate, states):
    for state in states_to_validate:
        if not states.__contains__(state) and state:
            raise E1(state)


def raise_warning(warning):
    warnings_raised.append(warning)


'''Warnings'''


def print_warnings(list):
    for warning in list:
        print('{0}\n'.format(warning))


def check_accepting_st(fin_states):
    if fin_states.__len__() == 1 and fin_states[0].__eq__(''):
        raise_warning(WARNING1)


def check_transition(transition, alpha):
    if not alpha.__contains__(transition):
        raise E3(transition)


def dfs(matrix):
    pass


try:
    init()
except Error as e:
    print(e)
