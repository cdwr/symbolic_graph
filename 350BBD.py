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
    def __init__():
        pass

    def __str__():
        pass
    def 

# 5 -> 00101 -> ~x1 & ~x2 & x3 & ~x4 & x5