from elements import make_constant, make_atom, make_var, make_affirmation, make_interrogation, is_simple_affirmation, \
    is_complex_affirmation, is_interrogation, are_all_variables_constant, is_affirmation, get_conditions

lines = []


def not_empty(word):
    return len(list(filter(lambda x: x != '', word))) > 0


def parse(line, add=True):
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
        interrogation = make_interrogation(atom, [], line.rstrip().lstrip())
        # print(interrogation)
        if add:
            lines.append(interrogation)
        return interrogation
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
            if add:
                lines.append(affirmation)
            return affirmation
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
            if add:
                lines.append(affirmation)
            return affirmation


def find_affirmations_by_interrogation(interrogation):
    if is_interrogation(interrogation):
        return list(filter(lambda x: x[1][1] == interrogation[1][1] and is_affirmation(x), lines))
    return []


def check_if_simple_affirmation(name):
    for statement in lines:
        if name == statement[1][1] and is_simple_affirmation(statement):
            return True, statement
    return False, None


def check_if_complex_affirmation(name):
    for statement in lines:
        if name == statement[1][1] and is_complex_affirmation(statement):
            return True, statement
    return False, None


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
        # print(variables)
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
        if len(solutions) == 0:
            return False
    elif is_complex_affirmation(statement):
        # cauta solutiile de la fiecare statement
        conditions = get_conditions(statement)
        all_vars = []
        solutions = []
        for cond in conditions:
            # take the variables
            variables = list(map(lambda x: x[1], cond[2]))
            all_vars += variables
            all_vars = list(set(all_vars))

            # print(variables)
            # print(cond)

            # name of cond - gotta find the statement
            # print(cond[1])

            check1 = check_if_simple_affirmation(cond[1])
            check2 = check_if_complex_affirmation(cond[1])

            if check1[0]:
                # print("yiss")

                interogate = check1[1]
                # print(interogate)
                aux = list(interogate)
                # print(list(map(lambda x: (x[0], '?' + x[1]) if x[0] == 'VAR' else (x[0], x[1]), cond[2])))
                cond_variables = list(map(lambda x: (x[0], '?' + x[1]) if x[0] == 'VAR' else (x[0], x[1]), cond[2]))
                # print(cond_variables)
                copy_cond = list(cond)
                copy_cond[2] = cond_variables
                cond = tuple(copy_cond)
                # print(cond)

                aux[1] = cond
                interogate = tuple(aux)
                # print(interogate)
                query = make_interrogation(aux[1], [], aux[-1])
                # print(query)
                partial_sols = find_solutions(query)
                print(partial_sols)
                if not partial_sols:
                    return False
                solutions.append(partial_sols)
            elif check2[0]:
                # print('sex anal')
                interogate = check2[1]
                # print(interogate)
        print(all_vars)
        for var in all_vars:
            for sol_cond in solutions:
                # print(sol_cond)
                for sol in sol_cond:
                    print(sol)
    if len(list(filter(lambda x: x is True, solutions))) == len(solutions):
        return True
    return solutions


'''
idee: ia variabilele din conditii, baga intr-un set
iei toate solutiile, faci insersectie pe variabile
'''


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

        solutions = []

        conditions = get_conditions(statement)
        if conditions is not None:
            for condition in conditions:
                print(condition)

    elif is_interrogation(statement):
        print(('\t' * indent_level) + 'Scopuri de demonstrat: ' + str(statement[3]).split(':')[0])
        indent_level += 1
        print(('\t' * indent_level) + 'Încercăm sa cautam solutii pentru interogatia: ' + str(statement[3]))
        solutions = find_solutions(statement)
        if not solutions:
            indent_level += 1
            print(('\t' * indent_level) + 'Nu s-au putut gasi solutii')
            indent_level -= 2
            return
        indent_level += 1
        print(('\t' * indent_level) + 'Solutiile sunt:')
        indent_level += 1
        for solution in solutions:
            plm = str(list(map(lambda x: str(x[0][1:]) + ' : ' + str(x[1]), solution))).replace(',', ';') \
                .strip('[').strip(']').replace('\'', '')
            print(('\t' * indent_level) + str(plm))


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

    '''
    print(lines[4])
    print(find_solutions(lines[4]))
    print(find_solutions(lines[5]))

    print(find_solutions(lines[10]))
    print(find_solutions(lines[11]))
    print(find_solutions(lines[12]))
    '''
    print(find_solutions(lines[-1]))


if __name__ == '__main__':
    main()

'''
idea: P(?X), Q(?Y), R(?Z)
P(1), P(2), Q(3), Q(5)


another idea, with variables: dict of var - values {X: [1, 2, 3], Y: [1, 5, 2]}, checking for validation
'''

'''
afirmatie complexa - mai multe conditii

iau fiecare conditie si generez solutiile acesteia - caut in lista de definitii si vad daca e simpla sau nu
- daca e simpla, o fac ca interogatie si generez solutiile
- daca nu e simpla, caut definitia ei si apelezi iar cautare de solutii pe rahatul ala
'''
