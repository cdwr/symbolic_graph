import pyeda.inter as pyeda

def edge2Bool(i, j):

    c = 0
    iLogic = ""
    jLogic = ""
    iBin = '{0:05b}'.format(i)
    jBin = '{0:05b}'.format(j)

    # iterate over the bits in binary i to create xFormula
    # produces "x[i] & ".. to match pyEDA style expression and indexed vars
    
    for digit in iBin:
        if int(digit):
            iLogic += "i[" + str(c) + "] & "
        else:
            iLogic += "~i[" + str(c) + "] & "
        c += 1    
    iLogic = iLogic[:-3]

    c = 0

    for digit in jBin:
        if int(digit):
            jLogic += "j[" + str(c) + "] & "
        else:
            jLogic += "~j[" + str(c) + "] & "
        c += 1     
    jLogic = jLogic[:-3] 

    # create a new Formula with both x and y expressions
    edgeBool = f"({iLogic}) & ({jLogic})"


    return edgeBool

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
    
    i0, i1, i2, i3, i4 = pyeda.bddvars('i', 5)
    j0, j1, j2, j3, j4 = pyeda.bddvars('j', 5)
    k0, k1, k2, k3, k4 = pyeda.bddvars('k', 5)
    
    # Transitive closure alg
    H = R
    temp = None

    while True:

        temp = H
        
        # H
        ff1 = H.compose({j0:k0, j1:k1, j2:k2, j3:k3, j4:k4 })

        # R
        ff2 = R.compose({i0:k0, i1:k1, i2:k2, i3:k3, i4:k4 }) 

        # H x R
        ff3 = ff1 & ff2

        # H = H v (H x R)
        H = temp | ff3

        # apply smoothing over all z BDD Vars to rid them from the graph
        H = H.smoothing((k0, k1, k2, k3, k4))

        if H.equivalent(temp):
            break

    return H

# MAIN, not gucci
if __name__ == '__main__':

    
    edgeList = []

    i0, i1, i2, i3, i4 = pyeda.bddvars('i', 5)
    j0, j1, j2, j3, j4 = pyeda.bddvars('j', 5)

    print("Building the graph, G..")
    # for (i, j) in G:

    edgeList = [edge2Bool(i,j) for i in range(0,32) for j in range(0,32) if (((i+3) % 32) == (j % 32)) | (((i+7) % 32) == (j % 32))]

    # for i in range(0, 32):

    #     for j in range(0,32):

    #         if (((i+3) % 32) == (j % 32)) | (((i+7) % 32) == (j % 32)):

    #             # send the edge to to formula creation function
    #             newFormula = edgeToBooleanFormula(i, j)

    #             # add the formula to the list
    #             edgeFormulaList.append(newFormula)
    # print("Done")

    
    # Create a big boolean expression, F, for the entire graph G
    print("Building the boolean expression, F, from the graph G..")
    F = joinEdgeFormulaList(edgeList)
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
    result = negRStar.smoothing((i0, i1, i2, i3, i4, j0, j1, j2, j3, j4))
    print("Done")

    # take the negation of the result
    print("Negating the result..")
    result = ~result
    print("Done")

    # Finally, assert the result
    print(f"\nfor all i, j ∈ S, can node i can reach node j in one or more steps in G?: {result.equivalent(True)}\n")