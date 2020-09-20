from copy import copy, deepcopy
import time
from sys import stdin

def parse(file):
    cnf = list()
    cnf.append(list())
    for line in file:
        tokens = line.split()
        if len(tokens) != 0 and tokens[0] not in ("p", "c"):
            for tok in tokens:
                lit = int(tok)
                if lit == 0:
                    cnf.append(list())
                else:
                    cnf[-1].append(lit)
    cnf.pop()
    return cnf



def assignLit(cnf, literal):
    for clause in copy(cnf):
        if literal in clause:
            cnf.remove(clause)
            if literal > 0:
                vars.append(literal)
        if -literal in clause:
            clause.remove(-literal)
    return cnf

def unitClauseRemoval(cnf):
  for clause in cnf:
      if len(clause) == 1:
          return clause[0]
  return 0


def pureLit(cnf):
    positive = []
    negative = []
    for clause in cnf:
        for literal in clause:
            if literal > 0:
                positive.append(literal)
            else:
                negative.append(literal)
    pureLiterals = []
    for clause in cnf:
        for literal in clause:
            if literal in positive and -literal not in negative:
                pureLiterals.append(literal)
            elif literal in negative and -literal not in positive:
                pureLiterals.append(literal)
    for literal in pureLiterals:
        cnf = assignLit(cnf, literal)
    #for literal in positive:
      #if -literal not in negative:
        #pureLiterals.append(literal)
    #for literal in negative:
      #if -literal not in positive:
        #pureLiterals.append(literal)
    #for literal in pureLiterals:
        #cnf = assignLit(cnf, literal)
    return cnf

def DPLL(cnf):
    literal = unitClauseRemoval(cnf)
    while (literal != 0):
        cnf = assignLit(cnf, literal)
        literal = unitClauseRemoval(cnf)
    cnf = pureLit(cnf)
    if len(cnf) == 0: # Check if all clauses are satisfied
        return True
    if [] in cnf: # Check for presence of empty clause
        return False
    cnf = deepcopy(cnf)
    literal = cnf[0][0]
    return DPLL(assignLit(cnf, literal)) or DPLL(assignLit(cnf, -literal))


def main():
    sudoku = open("sudoku-example.txt", "r")
    rules = open("sudoku-rules.txt", "r")
    sudoku_cnf = parse(sudoku)
    rules_cnf = parse(rules)
    sudoku_cnf.extend(rules_cnf)
    start_time = time.time()
    satisfied = DPLL(sudoku_cnf)
    if satisfied:
        print("Satisfiable")
    if not satisfied:
        print("Unsatisfiable")
    print("--- %s seconds ---" % (time.time() - start_time))

vars = []
main()
vars = set(vars)
print(vars)

