import itertools as it 
def gen_elements(vars: list,k):
    elements = []
    for var in vars:
        elements.append(var)
    n = len(vars)
    # power 1 
    for i in range(2,n+1):
        for e in it.combinations(vars,i):
            elements.append("("+ "&".join(e) + ")")
    
    p1_elem = elements.copy()
    # power 2...k
    if(k > 1):
        for i in range(2,k+1):
            for e in it.combinations_with_replacement(p1_elem,i):
                elements.append("*".join(e))
    # power 0
    elements.insert(0,"1")
    return elements

res = gen_elements(["t","x","y","z"],2)
print(res)
print(len(res))