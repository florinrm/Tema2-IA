import itertools
import sys
from copy import deepcopy

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


def are_all_variables_simple(statement):
    variables = statement[1][2]
    res = list(filter(lambda x: x[0] == 'VAR', variables))
    return len(variables) == len(res)


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
    sols = []
    for statement in lines:
        if name == statement[1][1] and is_complex_affirmation(statement):
            sols.append(statement)
    if len(sols) > 0:
        return True, sols
    return False, None


def find_all_solutions(name):
    solutions = []
    for statement in lines:
        if is_simple_affirmation(statement) and name == statement[1][1]:
            if are_all_variables_simple(statement):
                return True
            solutions.append(list(map(lambda x: x[1], statement[1][2])))
    return solutions


def sublist(lst1, lst2):
    return set(lst1) <= set(lst2)


def remove_ask_symbol(string):
    if string[0] == '?':
        string = string[1:]
    if string[0] == '?':
        string = string[1:]
    return string


def find_solutions(statement):
    solutions = []
    final_solutions = []
    if is_interrogation(statement):
        if check_if_simple_affirmation(statement[1][1])[0]:
            all_solutions = find_all_solutions(statement[1][1])
            if all_solutions == True:
                return True
            # de verificat cand avem doar constante (true / false)
            variables = list(map(lambda x: x[1], statement[1][2]))
            if are_all_variables_constant(statement):
                return len(list(filter(lambda x: x == variables, all_solutions))) != 0

            for i in range(len(variables)):
                if '?' not in variables[i]:
                    all_solutions = list(filter(lambda x: x[i] == variables[i], all_solutions))

            for sol in all_solutions:
                sol_temp = [(variables[i], sol[i]) for i in range(len(variables))]
                sol_temp = list(filter(lambda x: '?' in x[0], sol_temp))
                solutions.append(sol_temp)

            if len(solutions) == 0:
                return False
        elif check_if_complex_affirmation(statement[1][1])[0]:
            affirmations = deepcopy(check_if_complex_affirmation(statement[1][1])[1])
            variables = statement[1][2]
            sols = []
            if len(variables) == 0:  # just transform in interrogations
                for aff in affirmations:
                    partial_sol = find_solutions(aff)
                    if partial_sol == False:
                        continue
                    if partial_sol == True:
                        sols.append(True)
                        continue
                    sols += partial_sol
            else:  # replace the variables
                for x in range(len(affirmations)):
                    conditions = get_conditions(affirmations[x])
                    atom_vars = deepcopy(affirmations[x][1][2])
                    for i in range(len(variables)):
                        for j in range(len(conditions)):
                            copy_cond = list(conditions[j])
                            for k in range(len(conditions[j][2])):
                                if conditions[j][2][k][1] == atom_vars[i][1]:
                                    copy_cond[2][k] = (variables[i][0], variables[i][1])
                            conditions[j] = deepcopy(copy_cond)
                    temp = list(affirmations[x])
                    temp[2] = conditions
                    atom_temp = list(temp[1])
                    atom_temp[2] = variables
                    temp[1] = tuple(atom_temp)
                    affirmations[x] = tuple(temp)
                    partial_sol = find_solutions(affirmations[x])
                    if partial_sol == False:
                        continue
                    if partial_sol == True:
                        sols.append(True)
                        continue
                    sols += partial_sol
                return sols
    elif is_complex_affirmation(statement):
        # cauta solutiile de la fiecare statement
        conditions = get_conditions(statement)
        all_vars = []  # variables from conditions
        solutions = []  # problem solutions

        for cond in conditions:
            # take the variables
            variables = list(map(lambda x: x[1], cond[2]))
            all_vars += variables
            all_vars = list(set(all_vars))

            check1 = check_if_simple_affirmation(cond[1])
            check2 = check_if_complex_affirmation(cond[1])

            if check1[0] == True:
                if len(cond[2]) != len(check1[1][1][2]):
                    return False
            if check1[0]:
                interogate = check1[1]
                aux = list(interogate)
                cond_variables = list(
                    map(lambda e: (e[0], '?' + remove_ask_symbol(e[1])) if e[0] == 'VAR' else (e[0], e[1]), cond[2]))
                copy_cond = list(cond)
                copy_cond[2] = cond_variables
                cond = tuple(copy_cond)
                aux[1] = cond
                query = make_interrogation(aux[1], [], aux[-1])
                partial_sols = find_solutions(query)
                if not partial_sols:
                    return False
                solutions.append(partial_sols)
            elif check2[0]:
                interogations = check2[1]
                interogate_sols = []
                for interogate in interogations:
                    aux = list(interogate)
                    cond_variables = list(
                        map(lambda e: (e[0], '?' + e[1].lstrip('?')) if e[0] == 'VAR' else (e[0], e[1]), cond[2]))
                    copy_cond = list(cond)
                    copy_cond[2] = cond_variables
                    cond = tuple(copy_cond)
                    aux[1] = cond
                    query = make_interrogation(aux[1], [], aux[-1])
                    partial_sols = find_solutions(interogate)
                    if not partial_sols:
                        return False
                    if partial_sols == True:
                        continue
                    interogate_sols += partial_sols
                solutions.append(interogate_sols)
        var_viable_solutions = dict()
        for var in all_vars:
            var_solutions = []
            if len(solutions) == len(list(filter(lambda x: x == True, solutions))):
                return True
            for sol_cond in solutions:
                var_solution = []
                if sol_cond == False:
                    return False
                if sol_cond == True:
                    continue

                for sol in sol_cond:
                    single_sol = list(filter(lambda x: x[0][1:] == var, sol))
                    if len(single_sol) > 0:
                        var_solution.append(single_sol[0][1])
                if len(var_solution) > 0:
                    var_solutions.append(var_solution)
            if len(var_solutions) == 0:
                continue
            var_final_solutions = set(var_solutions[0])
            for s in var_solutions[1:]:
                var_final_solutions.intersection_update(s)

            var_final_solutions = list(var_final_solutions)
            if len(var_final_solutions) == 0:
                return False
            var_viable_solutions[var] = var_final_solutions

        list_of_lists = []
        for elem in var_viable_solutions.keys():
            lst = var_viable_solutions[elem]
            temp = []
            for val in lst:
                temp.append(('?' + elem.lstrip('?'), val))
            list_of_lists.append(temp)

        cartesian = []  # list of possible solutions
        for element in itertools.product(*list_of_lists):
            # print(element)
            cartesian.append(list(element))

        if cartesian == [[]]:
            return final_solutions

        for sol_cartesian in cartesian:
            ok = True
            for cond in conditions:
                cond_vars = deepcopy(cond[2])
                for s in sol_cartesian:
                    for i in range(len(cond_vars)):
                        if cond_vars[i][0] == 'VAR' and cond_vars[i][1] == s[0][1:]:
                            cond_vars[i] = ('CONST', s[1])
                cond_atom = make_atom(cond[1], cond_vars)
                cond_interrogation = make_interrogation(cond_atom, [], "")
                cond_solution = find_solutions(cond_interrogation)
                if type(cond_solution) == bool:
                    ok = ok & cond_solution
            if ok:
                final_solutions.append(sol_cartesian)
    if len(list(filter(lambda p: p is True, solutions))) == len(solutions):
        return True
    if is_complex_affirmation(statement):
        return final_solutions
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

        solutions = find_solutions(statement)
        if solutions == False:
            indent_level += 1
            print(('\t' * indent_level) + 'Nu se pot gasi solutii')
            indent_level -= 1
        elif solutions == True:
            indent_level += 1
            print(('\t' * indent_level) + str(statement[3]) + ' e un fapt dat')
            indent_level -= 1
        else:
            indent_level += 1
            print(('\t' * indent_level) + 'Solutiile sunt: ')
            indent_level += 1
            for sol in solutions:
                plm = str(list(map(lambda x: str(x[0][1:]) + ' : ' + str(x[1]), sol))).replace(',', ';') \
                    .strip('[').strip(']').replace('\'', '')
                print(('\t' * indent_level) + str(plm))
            indent_level -= 2

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

        if solutions == True:
            indent_level += 1
            print(('\t' * indent_level) + str(statement[3][2:]) + ' este un fapt adevarat')
            indent_level += 1
            return

        if len(list(filter(lambda x: x == True, solutions))) == len(solutions):
            indent_level += 1
            print(('\t' * indent_level) + 'Interogatia este un fapt adevarat')
            indent_level -= 1
            return

        indent_level += 1
        print(('\t' * indent_level) + 'Solutiile sunt:')
        indent_level += 1
        copy_solutions = []
        for sol in solutions:
            if sol not in copy_solutions:
                copy_solutions.append(sol)
        for solution in copy_solutions:
            sol_print = str(list(map(lambda x: str(x[0][1:]) + ' : ' + str(x[1]), solution))).replace(',', ';') \
                .strip('[').strip(']').replace('\'', '')
            print(('\t' * indent_level) + str(sol_print))


def main():
    with open(sys.argv[1]) as fp:
        for line in fp:
            if line.strip():
                parse(line)

        for line in lines:
            print(line)

    for statement in lines:
        solve(statement)
    print('Gata.')


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
