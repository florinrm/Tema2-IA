# Backward Reasoner

A mini interpreter for Prolog-like logical statements (affirmations, functions, interrogations)

How to run:
`python3 main.py file_input`
or
`py main.py file_input`

Example - input:
```prolog
P(1)  
P(2)
Q(3)
r(?a) : P(?a), Q(?b, hello)
t(?x)
s() : P(3), t(1)
s() : P(2), t(1)
pq(?x, ?y) : P(?x), Q(?y)
? P(1)
: True
? P(3)
: False
? Q(1)
: False
? P(X)
: False
? t(1)
: True
? Q(?y)
: y : 3
? P(?X)
: X : 1
: X : 2
? pq(1, 3)
: True
? pq(2, 3)
: True
? pq(?a, 3)
: a : 1
: a : 2
? pq(?x, 3)
: x : 1
: x : 2
? pq(?y, 3)
: y : 1
: y : 2
? pq(?a, ?b)
: a : 1 ; b : 3
: a : 2 ; b : 3
? s()
: True
```

Example - output:
```
Scopuri de demonstrat: P(1)
        P(1) e un fapt dat
Scopuri de demonstrat: P(2)
        P(2) e un fapt dat
Scopuri de demonstrat: Q(3)
        Q(3) e un fapt dat
Scopuri de demonstrat: r(?a)
        Încercăm: r(?a) : P(?a), Q(?b, hello)
        Scopuri de demonstrat:  P(?a), Q(?b, hello)
                Nu se pot gasi solutii
Scopuri de demonstrat: t(?x)
        t(?x) e un fapt dat
Scopuri de demonstrat: s()
        Încercăm: s() : P(3), t(1)
        Scopuri de demonstrat:  P(3), t(1)
                Nu se pot gasi solutii
Scopuri de demonstrat: s()
        Încercăm: s() : P(2), t(1)
        Scopuri de demonstrat:  P(2), t(1)
                s() : P(2), t(1) e un fapt dat
Scopuri de demonstrat: pq(?x, ?y)
        Încercăm: pq(?x, ?y) : P(?x), Q(?y)
        Scopuri de demonstrat:  P(?x), Q(?y)
                Solutiile sunt:
                        y : 3; x : 2
                        y : 3; x : 1
Scopuri de demonstrat: ? P(1)
        Încercăm sa cautam solutii pentru interogatia: ? P(1)
                P(1) este un fapt adevarat
Scopuri de demonstrat: ? P(3)
        Încercăm sa cautam solutii pentru interogatia: ? P(3)
                Nu s-au putut gasi solutii
Scopuri de demonstrat: ? Q(1)
        Încercăm sa cautam solutii pentru interogatia: ? Q(1)
                Nu s-au putut gasi solutii
Scopuri de demonstrat: ? P(X)
        Încercăm sa cautam solutii pentru interogatia: ? P(X)
                Nu s-au putut gasi solutii
Scopuri de demonstrat: ? t(1)
        Încercăm sa cautam solutii pentru interogatia: ? t(1)
                t(1) este un fapt adevarat
Scopuri de demonstrat: ? Q(?y)
        Încercăm sa cautam solutii pentru interogatia: ? Q(?y)
                Solutiile sunt:
                        y : 3
Scopuri de demonstrat: ? P(?X)
        Încercăm sa cautam solutii pentru interogatia: ? P(?X)
                Solutiile sunt:
                        X : 1
                        X : 2
Scopuri de demonstrat: ? pq(1, 3)
        Încercăm sa cautam solutii pentru interogatia: ? pq(1, 3)
                Interogatia este un fapt adevarat
Scopuri de demonstrat: ? pq(2, 3)
        Încercăm sa cautam solutii pentru interogatia: ? pq(2, 3)
                Interogatia este un fapt adevarat
Scopuri de demonstrat: ? pq(?a, 3)
        Încercăm sa cautam solutii pentru interogatia: ? pq(?a, 3)
                Nu s-au putut gasi solutii
Scopuri de demonstrat: ? pq(?x, 3)
        Încercăm sa cautam solutii pentru interogatia: ? pq(?x, 3)
                Nu s-au putut gasi solutii
Scopuri de demonstrat: ? pq(?y, 3)
        Încercăm sa cautam solutii pentru interogatia: ? pq(?y, 3)
                Nu s-au putut gasi solutii
Scopuri de demonstrat: ? pq(?a, ?b)
        Încercăm sa cautam solutii pentru interogatia: ? pq(?a, ?b)
                Nu s-au putut gasi solutii
Scopuri de demonstrat: ? s()
        Încercăm sa cautam solutii pentru interogatia: ? s()
                s() este un fapt adevarat
Gata.

```