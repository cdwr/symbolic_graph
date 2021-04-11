import pyeda.inter as pyeda

def edgeToBooleanFormula(i, j):

    index = 0
    xFormula = ""
    yFormula = ""
    xBin = '{0:05b}'.format(i)
    yBin = '{0:05b}'.format(j)

    # iterate over the bits in binary i to create xFormula
    # produces "x[i] & ".. to match pyEDA style expression and indexed vars
    for digit in xBin:
        
        if int(digit) == 0:
            xFormula += f"~x[{index}] & "
        elif int(digit) == 1:
            xFormula += f"x[{index}] & "
        
        index += 1    

    # reset the indexer
    index = 0

    # iterate over the bits in binary j to formulate the yFormula
    for digit in yBin:
        
        if int(digit) == 0:
            yFormula += f"~y[{index}] & "
        elif int(digit) == 1:
            yFormula += f"y[{index}] & "
        
        index += 1  
    
    # pop the last 3 chars from the expressions
    xFormula = xFormula[:-3]
    yFormula = yFormula[:-3]

    # create a new Formula with both x and y expressions
    E_i_j = f"({xFormula}) & ({yFormula})"


    return E_i_j

def joinEdgeFormulaList(edgeFormulaList):

    jointFormula = ""

    # Add the OR between each formula
    for edgeFormula in edgeFormulaList:
        
        jointFormula += f"({edgeFormula}) | "

    # Convert the formula string to a pyeda expression
    # chopping off the extra OR for formatting
    jointFormula = pyeda.expr(jointFormula[:-3])

    return jointFormula

def computeTransitiveClosure(R):
    
    x0, x1, x2, x3, x4 = pyeda.bddvars('x', 5)
    y0, y1, y2, y3, y4 = pyeda.bddvars('y', 5)
    z0, z1, z2, z3, z4 = pyeda.bddvars('z', 5)
    
    # Transitive closure alg
    H = R
    HPrime = None

    while True:

        HPrime = H
        
        # H
        ff1 = H.compose({y0:z0, y1:z1, y2:z2, y3:z3, y4:z4 })

        # R
        ff2 = R.compose({x0:z0, x1:z1, x2:z2, x3:z3, x4:z4 }) 

        # H x R
        ff3 = ff1 & ff2

        # H = H v (H x R)
        H = HPrime | ff3

        # apply smoothing over all z BDD Vars to rid them from the graph
        H = H.smoothing((z0, z1, z2, z3, z4))

        if H.equivalent(HPrime):
            break

    return H

# MAIN, not gucci
if __name__ == '__main__':

    
    edgeFormulaList = []

    x0, x1, x2, x3, x4 = pyeda.bddvars('x', 5)
    y0, y1, y2, y3, y4 = pyeda.bddvars('y', 5)

    print("Building the graph, G..")
    # for (i, j) in G:
    for i in range(0, 32):

        for j in range(0,32):

            if (((i+3) % 32) == (j % 32)) | (((i+7) % 32) == (j % 32)):

                # send the edge to to formula creation function
                newFormula = edgeToBooleanFormula(i, j)

                # add the formula to the list
                edgeFormulaList.append(newFormula)
    print("Done")

    
    # Create a big boolean expression, F, for the entire graph G
    print("Building the boolean expression, F, from the graph G..")
    F = joinEdgeFormulaList(edgeFormulaList)
    print("Done")

    # Convert F into BDD: R 
    print("Converting F to a BDD, R..")
    R = pyeda.expr2bdd(F)
    print("Done")

    # Compute the transitive closure R*
    print("Computing the transitive closure, R*..")
    RStar = computeTransitiveClosure(R) 
    print("Done")


    # for all i, j ∈ S, node i can reach node j in one or more steps in G
    # first we negate R*
    print("Negating the transitive closure, R*..")
    negRStar = ~RStar
    print("Done")

    # Then apply smoothing over all BDD vars
    print("Smoothing over all x[0]..x[4] and y[0]..y[4]")
    result = negRStar.smoothing((x0, x1, x2, x3, x4, y0, y1, y2, y3, y4))
    print("Done")

    # take the negation of the result
    print("Negating the result..")
    result = ~result
    print("Done")

    # Finally, assert the result
    print(f"\nfor all i, j ∈ S, can node i can reach node j in one or more steps in G?: {result.equivalent(True)}\n")