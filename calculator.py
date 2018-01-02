
import logging
from fractions import Fraction
from decimal import Decimal

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def _get_operator (input_str='', seperator=['+','-']):

    if not input_str:
        return []
    ret = []
    tmp=''
    for i in input_str:
        if i not in seperator:
            tmp += i
        else:
            if tmp:
                ret.append(tmp)
            ret.append(i)
            tmp = ''
    if tmp:
        ret.append(tmp)
    return ret

    ret = [input_str]
    for op in seperator:
        tmp = []
        for item in ret:
            tmp.extend(item.split(op))
        ret = tmp
    return ret

def _to_rational_num (input=''):
    import re
    if not input:
        return None
    if not isinstance(input, str):
        return input
    match = None
    try:
        digit_pattern = re.compile('\d+')
        match =  digit_pattern.match(input)
    except Exception as ex:
        print ('input is',input)
    if match:
        return Fraction(input)
    return None

def calculation(expr=[]):
    while len(expr) >= 3:
        input1, op, input2 = expr[:3]
        ret = _cal(input1, input2, op)
        tmp_lst = [ret]
        tmp_lst.extend(expr[3:])
        expr = tmp_lst

def _cal (input1=None, input2=None, op='+'):
    if not input1 or not input2:
        return None
    #print ('to be calculated', input1, op,  input2)
    #print (input1/input2)
    def _divide(x, y):
        return  x if y in [Fraction(1,1), Decimal(1), 1, '1'] else x/y
        #num, denom = Fraction (r).numerator, Fraction(r).denominator
        #print ('num,denom',num,denom)
        #return r if denom == 1 else r
    #print ('num1,op,num2', input1, input2, op)
    try:
        ret = {'+':lambda x,y:x+y,
             '-':lambda x,y:x+y,
             '*':lambda x,y:x*y,
             '/':_divide
             }.get(op)(input1, input2)
    except Exception as ex:
        logger.info('cal error for {0},{1},{2},{3}'.format(input1, op, input2, ex))
    #print ('cal val is:',ret)
    return ret

def _resolve_stack_calc(input_stack=[]):

    if not input_stack or len(input_stack) < 3:
        return input_stack
    #print (input_stack)
    num2 = input_stack.pop()
    if num2 == '(':
        num2 = input_stack.pop()
    op = input_stack.pop()
    if op == '(':
        op = input_stack.pop()
    num1 = input_stack.pop()
    if num1 == '(':
        num1 = input_stack.pop()

    ret = _cal(_to_rational_num (num1),_to_rational_num ( num2), op)
    #tmp = Fraction(ret)
    #num, denom = tmp.numerator, tmp.denominator
    #print ('to be cal', num1, op, num2)
    #print('before convert', ret,num, denom, tmp)
    #if denom == 1:
        #ret = Decimal(num)
    #print ('before cal', num1, num2,op )
    #print ('to calculation',_to_rational_num(num1),_to_rational_num(num2),op,ret )
    input_stack.append(ret)
    #print ('after each calculation:',input_stack)
    return input_stack


def bh_calc (*args, **kwargs):
    if args:
        expr = args[0]
    else:
        expr = kwargs.get('expr')
    PRECISION = kwargs.get('precision') or 100000000
    if not expr:
        return None
    expr_lst = _get_operator(input_str=expr, seperator=['+','-','*','/','(',')'])
    #print (expr_lst)
    stack = []
    for item in expr_lst:
        if item != ')':
            stack.append(item)
            continue
        top = stack.pop()
        if top == '(':
            continue
        stack.append(top)
        while len(stack) > 3:
           _resolve_stack_calc(stack)
           top = stack.pop()
           if top == '(':
                break
           stack.append(top)
    while len(stack) >= 3:
        _resolve_stack_calc(stack)
    #print ('result is:000000000000',stack)
    #print (stack)
    if len(stack) == 1:
        top = stack.pop()
        #num, denom = top.numerator, top.denominator
        return '{0}/{1}'.format(top.numerator, top.denominator)
        return Fraction(stack.pop()).limit_denominator(PRECISION)
    raise ValueError('input expr is invalid:{0}'.format(expr))

print (calculation([Fraction (1,2),'*',Fraction(1,2),'/',Fraction(2,1)]))
#print('999999999/1000000000',bh_calc('999999999/1000000000'))
#print('1/7+1/7+1/7+1/7+1/7+1/7+1/7',bh_calc('1/7+1/7+1/7+1/7+1/7+1/7+1/7', precision=100000000000000))
#print('1/(1/(3+4))',bh_calc('1/(1/(3+4))'))
#print('case4',bh_calc('1/(1+)'))
#print('case5',bh_calc('1+(2*3'))
#print(_to_rational_num('1.2'))
#print (_cal(Decimal('1.2'),Decimal('3.4'),'+'))
#print (_get_operator(input_str='3+4-6'))


