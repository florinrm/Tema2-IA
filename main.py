from elements import make_constant, make_atom, make_var, make_affirmation, make_interrogation, is_simple_affirmation, \
    is_complex_affirmation, is_interrogation, are_all_variables_constant

lines = []


def not_empty(word):
    return len(list(filter(lambda x: x != '', word))) > 0


def parse(line):
    global lines
    # checking if it is interrogation
    if line[0] == '?':  # interrogation
        token = line[1:].rstrip().lstrip()
        tokens_atom = token.split('(')
        name_atom = tokens_atom[0]
        terms_atom = tokens_atom[1].strip(')').split(',')
        terms = []
        if not_empty(terms_atom):
            for term in terms_atom:
                tok = term.lstrip().rstrip()
                if '?' not in tok:
                    terms.append(make_constant(tok))
                else:
                    terms.append(make_var(tok))
        atom = make_atom(name_atom, terms)
        interrogation = make_interrogation(atom, [])
        # print(interrogation)
        lines.append(interrogation)
    elif line[0] == ':':  # interrogation answers
        # print('response to interrogation')
        response = line[1:].rstrip().lstrip()
        if response == 'True' or response == 'False':
            lines[-1][2].append(response)
        else:
            sol_tokens = list(map(lambda x: x.rstrip().lstrip(), response.split(';')))
            solutions = []
            for token in sol_tokens:
                sol_token = list(map(lambda x: x.rstrip().lstrip(), token.split(':')))
                sol_var = make_var(sol_token[0])
                sol_constant = make_constant(sol_token[1])
                solutions.append((sol_var, sol_constant))
            lines[-1][2].append(solutions)
        # print(lines[-1][2])
    else:  # affirmation
        tokens = line.split('(')
        name_token = tokens[0]
        # print(name_token)
        if ':' not in line:  # if we don't have any conditions
            terms_tokens = str(tokens[1]).rstrip().strip('\t\n\r').strip(')').split(',')
            atom_terms = []
            if not_empty(terms_tokens):  # if we have any terms
                for token in terms_tokens:
                    tok = token.rstrip().lstrip()
                    if '?' not in tok:
                        atom_terms.append(make_constant(tok))  # constant
                    else:
                        atom_terms.append(make_var(tok[1:]))  # variable
            atom = make_atom(name_token, atom_terms)
            affirmation = make_affirmation(atom, [], line.rstrip().lstrip())
            # print(affirmation)
            lines.append(affirmation)
        else:  # else if we have any conditions
            rest = line[len(name_token):].rstrip().strip('\t\n\r')
            condition_tokens = rest.split(':')

            # terms of affirmation
            atom_terms = []
            terms = condition_tokens[0].rstrip().strip('(').strip(')').split(',')
            if not_empty(terms):  # if we have any terms
                for token in terms:
                    tok = token.rstrip().lstrip()
                    if '?' not in tok:
                        atom_terms.append(make_constant(tok))  # constant
                    else:
                        atom_terms.append(make_var(tok[1:]))  # variable
            atom = make_atom(name_token, atom_terms)

            # conditions
            conditions_tokens = list(map(lambda x: x.rstrip().lstrip() + ')',
                                         condition_tokens[1].rstrip().split('),')))
            conditions = []
            for condition in conditions_tokens:
                cond_tokens = condition.split('(')
                name_condition = cond_tokens[0]
                atoms_condition = []
                terms_condition = cond_tokens[1].strip(')').split(',')

                if not_empty(terms_condition):  # if we have any terms
                    for token in terms_condition:
                        tok = token.rstrip().lstrip()
                        if '?' not in tok:
                            atoms_condition.append(make_constant(tok))  # constant
                        else:
                            atoms_condition.append(make_var(tok[1:]))  # variable
                condition_atom = make_atom(name_condition, atoms_condition)
                conditions.append(condition_atom)
            affirmation = make_affirmation(atom, conditions, line.rstrip().lstrip())
            # print(affirmation)
            lines.append(affirmation)


def find_all_solutions(name):
    solutions = []
    for statement in lines:
        if is_simple_affirmation(statement) and name == statement[1][1]:
            solutions.append(list(map(lambda x: x[1][0], statement[1][2])))
    return solutions


def find_solutions(statement):
    solutions = []
    if is_interrogation(statement):
        all_solutions = find_all_solutions(statement[1][1])
        # print(all_solutions)
        # de verificat cand avem doar constante (true / false)
        variables = list(map(lambda x: x[1], statement[1][2]))
        print(variables)
        if are_all_variables_constant(statement):
            return len(list(filter(lambda x: x == variables, all_solutions))) != 0
        for i in range(len(variables)):
            if '?' not in variables[i]:
                all_solutions = list(filter(lambda x: x[i] == variables[i], all_solutions))
        fuck = []
        for sol in all_solutions:
            muie = [(variables[i], sol[i]) for i in range(len(variables))]
            muie = list(filter(lambda x: '?' in x[0], muie))
            solutions.append(muie)

    return solutions


def solve(statement, indent_level=0):
    if is_simple_affirmation(statement):
        print(('\t' * indent_level) + 'Scopuri de demonstrat: ' + str(statement[3]))
        indent_level += 1
        print(('\t' * indent_level) + str(statement[3]) + ' e un fapt dat')
        indent_level -= 1

    elif is_complex_affirmation(statement):
        print(('\t' * indent_level) + 'Scopuri de demonstrat: ' + str(statement[3]).split(':')[0])
        indent_level += 1
        print(('\t' * indent_level) + 'Încercăm: ' + str(statement[3]))
        print(('\t' * indent_level) + 'Scopuri de demonstrat: ' + str(statement[3]).split(':')[1])


def main():
    with open('test.txt') as fp:
        for line in fp:
            if line.strip():
                parse(line)

        for line in lines:
            print(line)

    for statement in lines:
        solve(statement)
    print('Gata.')

    print(lines[4])
    print(find_solutions(lines[4]))
    print(find_solutions(lines[5]))

    print(find_solutions(lines[10]))
    print(find_solutions(lines[11]))
    print(find_solutions(lines[12]))


if __name__ == '__main__':
    main()

'''
idea: P(?X), Q(?Y), R(?Z)
P(1), P(2), Q(3), Q(5)


another idea, with variables: dict of var - values {X: [1, 2, 3], Y: [1, 5, 2]}, checking for validation
'''
