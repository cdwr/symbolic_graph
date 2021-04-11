import pyeda.inter as pyeda
from functools import reduce
from math import sqrt
from itertools import count, islice

render_graph = True

def edge2Bool(i, j):

    c = 0
    iLogic = ""
    jLogic = ""
    iBin = '{0:05b}'.format(i)
    jBin = '{0:05b}'.format(j)
    
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

    # create final Formula with both i and j formulas
    edgeBool = f"({iLogic}) & ({jLogic})"

    return edgeBool


def num2Bool(i):

    c = 0
    iLogic = ""
    iBin = '{0:05b}'.format(i)
    
    for digit in iBin:
        if int(digit):
            iLogic += "i[" + str(c) + "] & "
        else:
            iLogic += "~i[" + str(c) + "] & "
        c += 1    
    iLogic = iLogic[:-3]

    # create final Formula with both i and j formulas

    return iLogic

def joinEdgeList(edgeList):

    jointForm= ""

    # Add the ORs
    for edgeForm in edgeList:
        jointForm += f"({edgeForm}) | "

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

def is_prime(n):
    return n > 1 and all(n % i for i in islice(count(2), int(sqrt(n)-1)))


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

    primes = list(filter(is_prime, range(0,32)))
    evens = list(filter(lambda x: x % 2 == 0, range(0,32)))

    try:
        pList = [num2Bool(p) for p in primes]
        eList = [num2Bool(e) for e in evens]

        pForms = joinEdgeList(pList)
        eForms = joinEdgeList(eList)

        P = pyeda.expr2bdd(pForms)
        E = pyeda.expr2bdd(eForms)

        print("Success!")
        print(str(P))
        print(str(E))

    except Exception as e:
        print("!!!!!\n" + str(e))


    #build graph edges
    print("Building edges for G...")
    edgeList = [edge2Bool(i,j) for i in range(0,32) for j in range(0,32) if (((i+3) % 32) == (j % 32)) | (((i+8) % 32) == (j % 32))]

    print("Joining edges for G...")
    Gforms = joinEdgeList(edgeList)


    if(render_graph):
        print("Attempting to render graph from joined edge formula...")
        try:
            renderGraph(Gforms)
        except:
            print("Failed to render graph :(")

    # Convert the bool function into a BDD
    print("Converting function into BDD")
    R = pyeda.expr2bdd(Gforms)

    # Compute the transitive closure
    print("Performing Transitive Closure")
    Rs = doTC(R) 
    neg_Rs = ~Rs

    print("Smoothing... ")
    result = neg_Rs.smoothing((i0, i1, i2, i3, i4, j0, j1, j2, j3, j4))

    result = ~result

    # Finally, assert the result
    #print(f"\n → for all nodes i, j ∈ S,  i can reach j in one or more steps in G?: \n∴{result.equivalent(True)}\n")
    print(f"\n → for all nodes i ∈ Prime there is a node j ∈ Even, such that i can reach j in one or more steps in G?: \n∴{result.equivalent(True)}\n")