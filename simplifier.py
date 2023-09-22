import time
import re
from linv import *
import itertools as it 
import ast
import sys

def get_degree(ast_tree):
    if isinstance(ast_tree, ast.Expr):
        ast_tree = ast_tree.value

    if isinstance(ast_tree, ast.Constant):
        return 0

    if isinstance(ast_tree, ast.Name):
        return 1
    if isinstance(ast_tree, ast.UnaryOp):
        if isinstance(ast_tree.operand, ast.Name):
            return 1
        else:
            return get_degree(ast_tree.operand)
    if isinstance(ast_tree, ast.BinOp) and isinstance(ast_tree.op, ast.Mult):
        return get_degree(ast_tree.left) + get_degree(ast_tree.right)

    if isinstance(ast_tree, ast.BinOp):
        return max(get_degree(ast_tree.left), get_degree(ast_tree.right))

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

def calc_n_k(MBA_exp: str):
    # 求n元k次MBA的具体n与k值    
    vars = []
    
    k = get_degree(ast.parse(MBA_exp).body[0])

    vars = list(set(re.findall(r"[v]\d+",MBA_exp)))
    if (not vars):
        for ch in MBA_exp:
            if(ch.isalpha() and ch not in vars):
                vars.append(ch)
    
       
    vars.sort()
    # print(vars,k)
    return (vars,k)

def judge_equal(MBA_exp1: str, MBA_exp2:str, num_of_bits:int):
    MBA_exp3 = f"{MBA_exp1}-({MBA_exp2})"
    vars,k = calc_n_k(MBA_exp3)  
    n = len(vars)  
    if(k==1):
        if(n == 1):
            domain = [0,1]
        else:
            domain = list(it.product(*[[i for i in range(2)] for _ in range(n)]))
    else:
        domain = p2_domain[n-1] 
    eval_code = f"[{MBA_exp3} for "+ ",".join(vars) +" in domain]"
    result = eval(eval_code)
    # print(result)
    for item in result:
        if((item % 2**num_of_bits) != 0):
            return False
    return True
    


def simplify(MBA_exp: str, num_of_bits: int, sign=True):
    vars,k = calc_n_k(MBA_exp)    # vars is a list and k is power
    n = len(vars)
    
    if(k==1):
        elements = 	gen_elements(vars,k)  # elements is a list of all possible combinations of the variables.
        if(n == 1):
            domain = [0,1]
        else:
            domain = list(it.product(*[[i for i in range(2)] for _ in range(n)]))
        inv = p1_inv[n-1]

    else:
        elements = gen_elements(vars,k)
        domain = p2_domain[n-1] 
        inv = p2_inv[n-1]
    
    # domain variable used here
    eval_code = f"[{MBA_exp} for "+ ",".join(vars) +" in domain]"
    exp_range = eval(eval_code)

    len_elements = len(elements)
    result = {}
    coefficents = []
    count = 0
    for j in range(len_elements):
        tmp = 0
        for i in range(len_elements):
            tmp += inv[count][i] * exp_range[i]
        if(k>1):
            tmp = round(tmp)
        tmp %= (2**num_of_bits) # convert into unsigned number
        if (tmp > 2**(num_of_bits-1)-1) and sign:
            tmp = tmp - 2**num_of_bits
        coefficents.append(tmp)
        count += 1
    
    for i in range(len(coefficents)):
        if(coefficents[i] != 0):
            result[elements[i]] = coefficents[i]

    return result

def MBAdict2str(MBA_dict: dict):
    if not bool(MBA_dict):
        return "0"
    MBA_str = ""
    for k,v in MBA_dict.items():
        if(k=="1"):
            MBA_str+=str(v)
            continue
        if(v>0):
            if not bool(MBA_str):
                MBA_str+=f"{str(v)+'*' if v!=1 else ''}"+k
            else:    
                MBA_str+=f"+{str(v)+'*' if v!=1 else ''}"+k
        else:
            MBA_str+=f"{str(v)+'*' if v!=-1 else '-'}"+k
    return MBA_str

if __name__ == '__main__':
    num_of_bits = 64 # Number of bits. default 64.
    sign = True
    

    if "-u" in sys.argv:
        sign = False  # If the user specified the option -u.  represent result in unsigned number

    if "-n" in sys.argv:
        num_of_bits = int(sys.argv[sys.argv.index("-n")+1]) 
    
    if "-s" in sys.argv: # simply a MBA string
        print("simplified result:")
        print(MBAdict2str(simplify(sys.argv[sys.argv.index("-s")+1].strip(),num_of_bits,sign)))

    if "-f" in sys.argv: # verify a file with MBA and simplified result.
        right_num = 0
        len_examples = 0
        with open(sys.argv[sys.argv.index("-f")+1].strip(),"r") as f:
            examples = f.readlines()
            len_examples = len(examples)        
            t1 = time.perf_counter()
            for example in examples: 
                if(example.find("#") != -1):
                    continue
                exps = example.split(",")
                if judge_equal(exps[0].strip(),exps[1].strip(), num_of_bits):
                    right_num += 1
                else:
                    print(f"wrong result: {exps[0]} != {exps[1]}")
                    
            t2 = time.perf_counter()


        print(f"total right: {right_num}")
        print(f"used time(per example): {(t2-t1)/len_examples}s")