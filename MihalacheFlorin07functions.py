def get(triangle, l):
    if l == 0:
        return triangle[0:2]
    elif l == 1:
        return triangle[1:3]
    else:
        return triangle[0:1] + triangle[2:3]


def get_shortest(l1, l2, l3):
    return min(l1, l2, l3)


def get_longest(l1, l2, l3):
    return max(l1, l2, l3)


def get_middle(l1, l2, l3):
    lst = [l1, l2, l3]
    lst = sorted(lst)
    return lst[1]


def compute_triangle(l1, l2, l3):
    return get_shortest(l1, l2, l3) + get_middle(l1, l2, l3) - get_longest(l1, l2, l3)


def computer_pitagoras(ls, lm, ll):
    return ls * ls + lm * lm - ll * ll
