from elements import make_constant, make_atom, make_var, make_affirmation, make_interrogation

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
        #print(lines[-1][2])
    else:  # affirmation
        tokens = line.split('(')
        name_token = tokens[0]
        #print(name_token)
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
            affirmation = make_affirmation(atom, [])
            #print(affirmation)
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
            conditions_tokens = list(map(lambda x: x.rstrip().lstrip(), condition_tokens[1].rstrip().split(',')))
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
            affirmation = make_affirmation(atom, conditions)
            #print(affirmation)
            lines.append(affirmation)


def main():
    with open('test.txt') as fp:
        for line in fp:
            if line.strip():
                parse(line)
        for line in lines:
            print(line)


if __name__ == '__main__':
    main()
