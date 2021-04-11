debugging = False
def debug(*s):
      if debugging:
           print(*s)

def toBinary():
    L = []
    i = 0
    while i < 32:
        L.append('{0:05b}'.format(i))
        i+=1
    return L

def is_prime(n):
    return n > 1 and all(n % i for i in islice(count(2), int(sqrt(n)-1)))

def findEdge():
    edges = {}
    i = 0
    while i < 31:
        j = 0
        while j < 31:
            if (i + 3) % 32 == j % 32:
                edges[i] = j
            elif (i + 8) % 32 == j % 32:
                edges[i] = j
            j+=1
        i+=1
    return edges

def appendEdges():
    eb = []
    L = toBinary()
    E = findEdge()
    for i in E.items():
        eb.append(L[i[0]] + L[i[1]])
    return eb

class edge:
    def __init__(self, i, j):
        seld.prime = 
        pass
    def 
    def 

class node:
    def __init__(self, n):
        self.prime = is_prime(n)
        self.even = (n%2) == 0
        self.bin = "{0:b}".format(n)
        self.edges = self.getEdges()
        pass
    def degEdges(self):

    def 


class BDD:
    def __init__(self, n, k):
        self.n = n
        self.k = k
        self.nodes = self.getNodes(n,k)
        self.edges = self.getEdges()

    def class edge:
        def __init__(self, i, j):
            self.prime = 
            pass

    def class node:
        def __init__(self, n):
            self.prime = is_prime(n)
            self.even = (n%2) == 0
            self.bin = "{0:b}".format(n)
            self.edges = self.getEdges()
            pass

        def getEdges(self):

        def 


    def __str__():
        pass
    
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

# 5 -> 00101 -> ~x1 & ~x2 & x3 & ~x4 & x5