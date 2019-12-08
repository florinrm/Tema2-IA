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


def make_interrogation(atom, solutions):
    return INTERROGATION, atom, solutions


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
