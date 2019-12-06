lines = []


def parse(line):
    global lines
    # checking if it is interrogation
    if line[0] == '?':
        print('interrogation')
    elif line[0] == ':':
        print('response to interrogation')
    else:
        print('affirmation')
        tokens = line.split('(')
        name_token = tokens[0]
        print(name_token)
        if ':' not in line:
            terms_tokens = str(tokens[1]).strip(')\n').split(',')
            # print(list(map(lambda x: int(x), terms_tokens)))
        else:
            line_tokens = str(tokens[1]).strip(')\n').split(':')
            print(line_tokens)



def main():
    with open('test1.txt') as fp:
        for line in fp:
            if line.strip():
                parse(line)


if __name__ == '__main__':
    main()