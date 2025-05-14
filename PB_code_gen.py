digits = [6, 2, 0, 4, 5, 9, 3, 7, 5, 6, 6, 0, 1, 5, 4, 3, 8, 10, 18, 5]
operators = ['+', '*', '-', '/', '+', '-', '+', '+', '-', '*', '+', '/', '+', '*', '-', '-', '*', '/', '+']

# case with 20 digits & 19 operators -- extreme case

def evaluate(a, b, op):
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '/':
        return a/b
    else:  # op == '*'
        return a * b

def max_min_expression_with_parens(digits, operators): 
    # dynamic programming to explore all valid parenthizations & find min/max values
    n = len(digits)
    dp_min = [[0] * n for _ in range(n)]
    dp_max = [[0] * n for _ in range(n)]
    paren_min = [[''] * n for _ in range(n)]
    paren_max = [[''] * n for _ in range(n)]

    # Step 1: Initialize diagonals
    for i in range(n):
        dp_min[i][i] = dp_max[i][i] = digits[i]
        paren_min[i][i] = paren_max[i][i] = str(digits[i])

    # Step 2: Fill DP tables
    for length in range(2, n + 1):  # subexpression length
        for i in range(n - length + 1):
            j = i + length - 1
            dp_min[i][j] = float('inf')
            dp_max[i][j] = float('-inf')
            for k in range(i, j):
                op = operators[k]

                # evaluate all 4 combination of left/right min/max values at each partition k
                a = evaluate(dp_min[i][k], dp_min[k+1][j], op)
                b = evaluate(dp_min[i][k], dp_max[k+1][j], op)
                c = evaluate(dp_max[i][k], dp_min[k+1][j], op)
                d = evaluate(dp_max[i][k], dp_max[k+1][j], op)

                min_candidates = [(a, f"({paren_min[i][k]}{op}{paren_min[k+1][j]})"),
                                  (b, f"({paren_min[i][k]}{op}{paren_max[k+1][j]})"),
                                  (c, f"({paren_max[i][k]}{op}{paren_min[k+1][j]})"),
                                  (d, f"({paren_max[i][k]}{op}{paren_max[k+1][j]})")]

                max_candidates = min_candidates

                # update min and max tables and record the corresponding expression strings
                for val, expr in min_candidates:
                    if val < dp_min[i][j]:
                        dp_min[i][j] = val
                        paren_min[i][j] = expr

                for val, expr in max_candidates:
                    if val > dp_max[i][j]:
                        dp_max[i][j] = val
                        paren_max[i][j] = expr

    return dp_max[0][n-1], paren_max[0][n-1] # return max value and corresponding expression string that gives that value 

max_value, max_expr = max_min_expression_with_parens(digits, operators)

print("Maximum Value:", max_value) # 117751.82222222222
print("Optimal Parenthesization:", max_expr) # ((6+2)*(((((0-((4/5)+9))-(3+(7+5)))-6)*(6+((0/1)+5)))*((4-3)-(8*((10/18)+5)))))
