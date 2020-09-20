from copy import copy, deepcopy
import time
from sys import stdin




vars = []  # List to save variables that are true and not negated.

#Parse file, to get clauses.
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
    cnf.pop() #Remove item from list and returns it.
    return cnf


#Assign, remove, and add values.
def assignLit(cnf, literal):
    for clause in copy(cnf):
        if literal in clause:
            cnf.remove(clause)
            if literal > 0:
                vars.append(literal) #Add positive literal to vars list.
        if -literal in clause:
            clause.remove(-literal) #Remove negative literal.
    return cnf


#If one literal in clause, remove.
def unitClauseRemoval(cnf):
  for clause in cnf:
      if len(clause) == 1:
          return clause[0]
  return 0

#Check for pure literals, always positive or always negative.
def pureLit(cnf):
    positive = []
    negative = []
    for clause in cnf:
        for literal in clause:
            if literal > 0:
                positive.append(literal) #Add positive literals to positive list.
            else:
                negative.append(literal) #Add negative literals to negative list.
    pureLiterals = []
    for clause in cnf:
        for literal in clause:
            # Check if literal is only positive or negative.
            if literal in positive and -literal not in negative:
                pureLiterals.append(literal)
            elif literal in negative and -literal not in positive:
                pureLiterals.append(literal)
    for literal in pureLiterals:
        cnf = assignLit(cnf, literal)
    return cnf

def DPLL(cnf):
    literal = unitClauseRemoval(cnf) #Call unitClauseRemoval function.
    while (literal != 0): #While a unit clause is found.
        cnf = assignLit(cnf, literal)
        literal = unitClauseRemoval(cnf)
    cnf = pureLit(cnf) #Call pureLit funtion.
    if len(cnf) == 0: # Check if all clauses are satisfied
        return True
    if [] in cnf: # Check for presence of empty clause
        return False
    cnf = deepcopy(cnf)
    literal = cnf[0][0]
    return DPLL(assignLit(cnf, literal)) or DPLL(assignLit(cnf, -literal))



def main():
    sudokus = open("sudoku-example.txt", "r") #Open sudokus file.
    rules = open("sudoku-rules.txt", "r") #Open sudoku rules file.
    sudoku_cnf = parse(sudokus) #Call parse function, sudokus in cnf.
    rules_cnf = parse(rules) #Get rules in cnf.
    sudoku_cnf.extend(rules_cnf) #Add rules cnf clauses to sudoku cnf clauses.
    start_time = time.time() #Run time.
    #Check if satisfied or unsatisfiable.
    satisfied = DPLL(sudoku_cnf)
    if satisfied:
        print("Satisfiable")
    if not satisfied:
        print("Unsatisfiable")
    print("--- %s seconds ---" % (time.time() - start_time)) #Print run time.


main() #Call main function.
print(vars)

