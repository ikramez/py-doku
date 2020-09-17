# sudokus = "4x4.txt"
# sudoku_rules = "sudoku-rules.txt"

import copy



def parse(cnf, file):
    cnf.append(list())
    for line in file:
        tokens = line.split()
        if len(tokens) != 0 and tokens[0] not in ("p", "c"):
            for tok in tokens:
                lit = int(tok)
                maxvar = max(maxvar, abs(lit))
            if lit == 0: cnf.append(list())
            else: cnf[-1].append(lit)
    return cnf

    assert len(cnf[-1]) == 0
    cnf.pop()
    print(cnf)
    print(maxvar)

def assignLit(cnf, lit):
    for clause in copy(cnf):
        for lit in clause:
            if lit in clause: cnf.remove(clause)
            if -lit in clause: clause.remove(lit)
    return cnf

def DPLL(cnf):
    # Test if no unsatisfied clauses remain
    if len(cnf) == 0: return True
    # Test for presense of empty clause
    if [] in cnf: return False
    cnf = deepcopy(cnf)
    return DPLL(assignLit(cnf, lit)) or DPLL(assignLit(cnf, lit))




def main():
    sudokus = "4x4.txt"
    # sudoku_rules = "sudoku-rules.txt"
    # cnf = parse([], sudoku_rules)
    cnf = parse([], sudokus)
    DPLL(cnf)


main()






