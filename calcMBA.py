import itertools as it 
import numpy as np
import sympy
field = [i for i in range(4)]
vars = []
ori_rank = 0
eq = sympy.Matrix([])
A = []

def gen_elements(vars: list, k:int):
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

n = 4
for t,x,y,z in it.product(field,field,field,field):
    new_eq = eq.col_join(sympy.Matrix([[1, t, x, y, z, (t&x), (t&y), (t&z), (x&y), (x&z), (y&z), (t&x&y), (t&x&z), (t&y&z), (x&y&z), (t&x&y&z), t*t, t*x, t*y, t*z, t*(t&x), t*(t&y), t*(t&z), t*(x&y), t*(x&z), t*(y&z), t*(t&x&y), t*(t&x&z), t*(t&y&z), t*(x&y&z), t*(t&x&y&z), x*x, x*y, x*z, x*(t&x), x*(t&y), x*(t&z), x*(x&y), x*(x&z), x*(y&z), x*(t&x&y), x*(t&x&z), x*(t&y&z), x*(x&y&z), x*(t&x&y&z), y*y, y*z, y*(t&x), y*(t&y), y*(t&z), y*(x&y), y*(x&z), y*(y&z), y*(t&x&y), y*(t&x&z), y*(t&y&z), y*(x&y&z), y*(t&x&y&z), z*z, z*(t&x), z*(t&y), z*(t&z), z*(x&y), z*(x&z), z*(y&z), z*(t&x&y), z*(t&x&z), z*(t&y&z), z*(x&y&z), z*(t&x&y&z), (t&x)*(t&x), (t&x)*(t&y), (t&x)*(t&z), (t&x)*(x&y), (t&x)*(x&z), (t&x)*(y&z), (t&x)*(t&x&y), (t&x)*(t&x&z), (t&x)*(t&y&z), (t&x)*(x&y&z), (t&x)*(t&x&y&z), (t&y)*(t&y), (t&y)*(t&z), (t&y)*(x&y), (t&y)*(x&z), (t&y)*(y&z), (t&y)*(t&x&y), (t&y)*(t&x&z), (t&y)*(t&y&z), (t&y)*(x&y&z), (t&y)*(t&x&y&z), (t&z)*(t&z), (t&z)*(x&y), (t&z)*(x&z), (t&z)*(y&z), (t&z)*(t&x&y), (t&z)*(t&x&z), (t&z)*(t&y&z), (t&z)*(x&y&z), (t&z)*(t&x&y&z), (x&y)*(x&y), (x&y)*(x&z), (x&y)*(y&z), (x&y)*(t&x&y), (x&y)*(t&x&z), (x&y)*(t&y&z), (x&y)*(x&y&z), (x&y)*(t&x&y&z), (x&z)*(x&z), (x&z)*(y&z), (x&z)*(t&x&y), (x&z)*(t&x&z), (x&z)*(t&y&z), (x&z)*(x&y&z), (x&z)*(t&x&y&z), (y&z)*(y&z), (y&z)*(t&x&y), (y&z)*(t&x&z), (y&z)*(t&y&z), (y&z)*(x&y&z), (y&z)*(t&x&y&z), (t&x&y)*(t&x&y), (t&x&y)*(t&x&z), (t&x&y)*(t&y&z), (t&x&y)*(x&y&z), (t&x&y)*(t&x&y&z), (t&x&z)*(t&x&z), (t&x&z)*(t&y&z), (t&x&z)*(x&y&z), (t&x&z)*(t&x&y&z), (t&y&z)*(t&y&z), (t&y&z)*(x&y&z), (t&y&z)*(t&x&y&z), (x&y&z)*(x&y&z), (x&y&z)*(t&x&y&z), (t&x&y&z)*(t&x&y&z)]]))
    new_rank = new_eq.rank()
    if(new_rank != ori_rank):
        ori_rank += 1
        eq = new_eq.echelon_form()
        A.append([1, t, x, y, z, (t&x), (t&y), (t&z), (x&y), (x&z), (y&z), (t&x&y), (t&x&z), (t&y&z), (x&y&z), (t&x&y&z), t*t, t*x, t*y, t*z, t*(t&x), t*(t&y), t*(t&z), t*(x&y), t*(x&z), t*(y&z), t*(t&x&y), t*(t&x&z), t*(t&y&z), t*(x&y&z), t*(t&x&y&z), x*x, x*y, x*z, x*(t&x), x*(t&y), x*(t&z), x*(x&y), x*(x&z), x*(y&z), x*(t&x&y), x*(t&x&z), x*(t&y&z), x*(x&y&z), x*(t&x&y&z), y*y, y*z, y*(t&x), y*(t&y), y*(t&z), y*(x&y), y*(x&z), y*(y&z), y*(t&x&y), y*(t&x&z), y*(t&y&z), y*(x&y&z), y*(t&x&y&z), z*z, z*(t&x), z*(t&y), z*(t&z), z*(x&y), z*(x&z), z*(y&z), z*(t&x&y), z*(t&x&z), z*(t&y&z), z*(x&y&z), z*(t&x&y&z), (t&x)*(t&x), (t&x)*(t&y), (t&x)*(t&z), (t&x)*(x&y), (t&x)*(x&z), (t&x)*(y&z), (t&x)*(t&x&y), (t&x)*(t&x&z), (t&x)*(t&y&z), (t&x)*(x&y&z), (t&x)*(t&x&y&z), (t&y)*(t&y), (t&y)*(t&z), (t&y)*(x&y), (t&y)*(x&z), (t&y)*(y&z), (t&y)*(t&x&y), (t&y)*(t&x&z), (t&y)*(t&y&z), (t&y)*(x&y&z), (t&y)*(t&x&y&z), (t&z)*(t&z), (t&z)*(x&y), (t&z)*(x&z), (t&z)*(y&z), (t&z)*(t&x&y), (t&z)*(t&x&z), (t&z)*(t&y&z), (t&z)*(x&y&z), (t&z)*(t&x&y&z), (x&y)*(x&y), (x&y)*(x&z), (x&y)*(y&z), (x&y)*(t&x&y), (x&y)*(t&x&z), (x&y)*(t&y&z), (x&y)*(x&y&z), (x&y)*(t&x&y&z), (x&z)*(x&z), (x&z)*(y&z), (x&z)*(t&x&y), (x&z)*(t&x&z), (x&z)*(t&y&z), (x&z)*(x&y&z), (x&z)*(t&x&y&z), (y&z)*(y&z), (y&z)*(t&x&y), (y&z)*(t&x&z), (y&z)*(t&y&z), (y&z)*(x&y&z), (y&z)*(t&x&y&z), (t&x&y)*(t&x&y), (t&x&y)*(t&x&z), (t&x&y)*(t&y&z), (t&x&y)*(x&y&z), (t&x&y)*(t&x&y&z), (t&x&z)*(t&x&z), (t&x&z)*(t&y&z), (t&x&z)*(x&y&z), (t&x&z)*(t&x&y&z), (t&y&z)*(t&y&z), (t&y&z)*(x&y&z), (t&y&z)*(t&x&y&z), (x&y&z)*(x&y&z), (x&y&z)*(t&x&y&z), (t&x&y&z)*(t&x&y&z)])
        vars.append([x,y,z])
        if(new_rank == 2**(2*n-1)+2**(n-1)):
            break

# print(vars)
print(np.matrix(A).I.tolist())