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

