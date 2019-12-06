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


def make_affirmation(atom, condition):
    return AFFIRMATION, atom, condition


def make_interrogation(atom, solutions):
    return INTERROGATION, atom, solutions
