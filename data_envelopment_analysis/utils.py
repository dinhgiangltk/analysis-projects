# Source: https://github.com/gary60405/Data-Envelopment-Analysis-Tutorial

from pulp import LpProblem, LpMinimize, LpMaximize, LpVariable, lpSum, value
      
def getMinOE(r:int,K:list,I:list,J:list,X:dict,Y:dict):
    """
    # CRS_DEA_Model with LpMinimize
    r: the index of DMUs
    K: list of DMUs
    I: list of inputs
    J: list of outputs
    X: dict of input values
    Y: dict of output values
    """
    # Model Building
    model = LpProblem('CRS_model_Min', LpMinimize)
    
    # Decision variables Building
    theta_r = LpVariable(f'theta_r')
    lambda_k = LpVariable.dicts(f'lambda_k', lowBound=0, indexs=K)
    
    # Objective Function setting
    model += theta_r
    
    # Constraints setting
    for i in I:
        model += lpSum([
                lambda_k[k] * X[i][k]
            for k in K]) <= theta_r * float(X[i][K[r]])
    for j in J:
        model += lpSum([
                lambda_k[k] * Y[j][k]
            for k in K]) >= float(Y[j][K[r]])
    
    # Model solving
    model.solve()
    
    return f'{K[r]}:{round(value(model.objective), 3)}\n', value(model.objective)


def getMinTE(r:int,K:list,I:list,J:list,X:dict,Y:dict):
    """
    # VRS_DEA_Model with LpMinimize
    r: the index of DMUs
    K: list of DMUs
    I: list of inputs
    J: list of outputs
    X: dict of input values
    Y: dict of output values
    """
    # Model Building 
    model = LpProblem('VRS_model_Min', LpMinimize)
    
    # Decision variables Building 
    theta_r = LpVariable(f'theta_r')
    lambda_k = LpVariable.dicts(f'lambda_k', lowBound=0, indexs = K)
    
    # Objective Function setting
    model += theta_r
    
    # Constraints setting
    for i in I:
        model += lpSum([
                lambda_k[k] * X[i][k]
            for k in K]) <= theta_r * float(X[i][K[r]])
    for j in J:
        model += lpSum([
                lambda_k[k] * Y[j][k]
            for k in K]) >= float(Y[j][K[r]])
    model += lpSum([ lambda_k[k] for k in K]) == 1
    
    # model solving 
    model.solve()  
    
    return f'{K[r]}:{round(value(model.objective), 3)}\n', value(model.objective)


def getMaxOE(r:int,K:list,I:list,J:list,X:dict,Y:dict):
    """
    # CRS_DEA_Model with LpMaximize
    r: the index of DMUs
    K: list of DMUs
    I: list of inputs
    J: list of outputs
    X: dict of input values
    Y: dict of output values
    """
    # Model Building
    model = LpProblem('CRS_model_Max', LpMaximize)
    
    # Decision variables Building
    # theta_r = LpVariable(f'theta_r')
    v = LpVariable.dicts(f'lambda_v', lowBound=0, indexs=I)
    u = LpVariable.dicts(f'lambda_u', lowBound=0, indexs=J)
    
    # Objective Function setting
    model += lpSum([u[j] * Y[j][K[r]] for j in J])
    
    # Constraints setting
    model += lpSum([v[i] * X[i][K[r]] for i in I]) == 1

    for k in K:
        model += lpSum([u[j] * Y[j][k] for j in J]) <= lpSum([v[i] * X[i][k] for i in I])
    
    # Model solving
    model.solve()
    
    return f'{K[r]}:{round(value(model.objective), 3)}\n', value(model.objective)