CONST = "CONST"
VAR = 'VAR'
ATOM = 'ATOM'
AFFIRMATION = 'AFFIRMATION'
INTERROGATION = 'INTERROGATION'
FUNCTION = 'FUNCTION'
TERM = 'TERM'
TERMS = 'TERMS'
COMMENT = 'COMMENT'


def make_constant(value):
    return CONST, value


def make_var(name):
    return VAR, name


def make_atom(name, terms):
    return ATOM, name, terms


def make_function(name, terms):
    return FUNCTION, name, terms


def make_affirmation(atom, condition, representation):
    return AFFIRMATION, atom, condition, representation


def make_interrogation(atom, solutions, representation):
    return INTERROGATION, atom, solutions, representation


def is_affirmation(statement):
    return statement[0] == AFFIRMATION


def is_simple_affirmation(statement):
    return is_affirmation(statement) and statement[2] == []


def is_complex_affirmation(statement):
    return is_affirmation(statement) and len(statement[2]) > 0


def is_interrogation(statement):
    return statement[0] == INTERROGATION


def is_atom(statement):
    return statement[0] == ATOM


def is_const(statement):
    return statement[0] == CONST


def is_variable(statement):
    return statement[0] == VAR


def get_variables(statement):
    variables = []


def are_all_variables_constant(statement):
    if is_affirmation(statement) or is_interrogation(statement):
        variables = list(filter(lambda x: '?' in x[1], statement[1][2]))
        return len(variables) == 0
    return False


def get_conditions(statement):
    if is_complex_affirmation(statement):
        return statement[2]
    return None
