import math

# return value, and uncertanties
def calculate(var, unc, func):
    value = func(var)
    uncertainty = 0

    for i in range(len(var)):
        x = var[i]
        dx = unc[i]

        var[i] = x + dx
        uncertainty += (func(var) - value)*(func(var) - value)
        var[i] = x

    uncertainty = math.sqrt(uncertainty)

    return value, uncertainty

def string_to_lambda(input_str):
    try:
        # Parse the input string
        lambda_str = f"lambda x: {input_str}"
        
        # Create a lambda function using eval
        lambda_func = eval(lambda_str)
        
        return lambda_func
    except Exception as e:
        print("Error:", e)
        return None


def getInput(var, unc, input_func, sig_fig):
    func = string_to_lambda(input_func)

    value, uncertainty = calculate(var, unc, func)

    result = str(str("%."+sig_fig+"f") % value)
    result += "±" + str(str("%."+sig_fig+"f") % uncertainty)
    
    return result

        