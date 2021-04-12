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
    Hprime = None

    while True:

        Hprime = H
        
        p1 = H.compose({j0:k0, j1:k1, j2:k2, j3:k3, j4:k4 })
        p2 = R.compose({i0:k0, i1:k1, i2:k2, i3:k3, i4:k4 }) 
        p = p1 & p2
        H = Hprime | p
        H = H.smoothing((k0, k1, k2, k3, k4))

        if H.equivalent(Hprime):
            break

    return H

def is_prime(n):
    return n > 1 and all(n % i for i in islice(count(2), int(sqrt(n)-1)))


def renderGraph(func):
    try:
        import graphviz
        from graphviz import Digraph
        import pydot

        graph = pydot.graph_from_dot_data(func.to_dot())[0]
        graph.create_png('graph.png')
    except Exception as e:
        print("Failed to graph. No graph rendering for you! <" + type(e) + ">")



if __name__ == '__main__':

    i0, i1, i2, i3, i4 = pyeda.bddvars('i', 5)
    j0, j1, j2, j3, j4 = pyeda.bddvars('j', 5)
    k0, k1, k2, k3, k4 = pyeda.bddvars('k', 5)

    primes = list(filter(is_prime, range(0,32)))
    evens = list(filter(lambda x: x % 2 == 0, range(0,32)))


    print("Building boolean expressions...")
    rList = [edge2Bool(i,j) for i in range(0,32) for j in range(0,32) if (((i+3) % 32) == (j % 32)) | (((i+8) % 32) == (j % 32))]
    pList = [num2Bool(p) for p in primes]
    eList = [num2Bool(e) for e in evens]

    print("Joining edges for boolean expressions...")
    rForms = joinEdgeList(rList)
    pForms = joinEdgeList(pList)
    eForms = joinEdgeList(eList)

    if(render_graph):
        print("Attempting to render graph from R formula...")
        try:
            renderGraph(rForms)
        except:
            print("Failed to render graph :(")

    print("Converting boolean functions into BDDs RR, PP, and EE")
    RR = pyeda.expr2bdd(rForms)
    PP = pyeda.expr2bdd(pForms)
    EE = pyeda.expr2bdd(eForms)

    print("Computing BDD RR2 from BDD RR")
    RR2 = RR.compose({j0:k0, j1:k1, j2:k2, j3:k3, j4:k4 }) & RR.compose({i0:k0, i1:k1, i2:k2, i3:k3, i4:k4 })

    print("Performing Transitive Closure on RR2")
    RR2s = doTC(RR2) 
    neg_RR2s = ~RR2s

    print("Finalizing... ")
    JJ = (~RR2s & EE).smoothing((j0, j1, j2, j3, j4))
    QQ = ~( ~( JJ | ~PP).smoothing((i0, i1, i2, i3, i4)) )
    print(f"\n → for all nodes i ∈ Prime there is a node j ∈ Even, such that i can reach j in an even number of steps: \n∴{QQ.equivalent(True)}\n")

        