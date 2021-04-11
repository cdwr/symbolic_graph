import pyeda.inter as pyeda

render_graph = True

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

def joinEdgeList(edgeList):

    jointForm= ""

    # Add the OR between each formula
    for edgeForm in edgeList:
        jointForm += f"({edgeForm}) | "

    # Convert the formula string to a pyeda expression
    # chopping off the extra OR for formatting
    jointForm = pyeda.expr(jointForm[:-3])

    return jointForm

def doTC(R):
    
    i0, i1, i2, i3, i4 = pyeda.bddvars('i', 5)
    j0, j1, j2, j3, j4 = pyeda.bddvars('j', 5)
    k0, k1, k2, k3, k4 = pyeda.bddvars('k', 5)
    
    # Transitive closure alg
    H = R
    temp = None

    while True:

        temp = H
        
        ff1 = H.compose({j0:k0, j1:k1, j2:k2, j3:k3, j4:k4 })
        ff2 = R.compose({i0:k0, i1:k1, i2:k2, i3:k3, i4:k4 }) 
        ff3 = ff1 & ff2
        H = temp | ff3
        H = H.smoothing((k0, k1, k2, k3, k4))

        if H.equivalent(temp):
            break

    return H


def renderGraph(func):
    try:
        import graphviz
        from graphviz import Digraph
        import pydot
    except:
        print("Failed to import dependencies. No graph rendering for you!")
        return

    graph = pydot.graph_from_dot_data(func.to_dot())[0]
    graph.create_png('graph.png')


# MAIN, not gucci
if __name__ == '__main__':

    
    edgeList = []

    i0, i1, i2, i3, i4 = pyeda.bddvars('i', 5)
    j0, j1, j2, j3, j4 = pyeda.bddvars('j', 5)

    #build graph edges
    edgeList = [edge2Bool(i,j) for i in range(0,32) for j in range(0,32) if (((i+3) % 32) == (j % 32)) | (((i+7) % 32) == (j % 32))]

    function = joinEdgeList(edgeList)


    if(render_graph):
        try:
            renderGraph(function)
        except:
            print("Failed to render graph :(")

    # Convert the bool function into a BDD
    print("Converting function into BDD")
    BDD = pyeda.expr2bdd(function)

    # Compute the transitive closure R*
    print("Performing Transitive Closure")
    BDD_trans = doTC(BDD) 
    neg_BDD_trans = ~BDD_trans

    print("Smoothing... ")
    result = neg_BDD_trans.smoothing((i0, i1, i2, i3, i4, j0, j1, j2, j3, j4))

    result = ~result

    # Finally, assert the result
    print(f"\nfor all nodes i, j ∈ S,  i can reach j in one or more steps in G?: \n∴{result.equivalent(True)}\n")