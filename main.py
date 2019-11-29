lines = []


def parse(line):
    global lines
    # checking if it is interrogation
    if '?' in line:
        print('interrogation')
    else:
        print('affirmation')
        tokens = line.split('(')
        name_token = tokens[0]
        print(name_token)
        if ':' not in line:
            terms_tokens = str(tokens[1]).strip(')\n').split(',')
            # print(list(map(lambda x: int(x), terms_tokens)))
        else:
            pass



def main():
    with open('test1.txt') as fp:
        for line in fp:
            if line.strip():
                parse(line)


if __name__ == '__main__':
    main()