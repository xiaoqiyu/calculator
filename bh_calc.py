
import logging
from fractions import Fraction
from decimal import Decimal
import re
import sys

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def _resolve_signal(val=''):
    if not (val.startswith('+') or val.startswith('-')):
        return val
    op_cnt = {'+':0,'-':0}
    cnt = 0
    while val[cnt] in ['+','-']:
        num = (op_cnt.get(val[cnt]) or 0)+1
        op_cnt.update({val[cnt]:num})
        cnt += 1
    if not op_cnt.get('-'):
        sig = '+'
    neg  = op_cnt.get('-')
    sig = '+' if neg % 2 == 0 else '-'
    return sig+val[cnt:]


def _get_operator (input_str='', seperator=['+','-']):
    if not input_str:
        return []
    ret = []
    tmp=''
    for idx, i in enumerate(input_str):
        if i not in seperator:
            tmp += i
        else:
            if idx == 0 and i in ['+','-']:
                tmp += i
                continue
            try:
                pre_ch = input_str[idx-1]
                if pre_ch in ['e','E'] or (pre_ch in seperator and i in ['+','-']):
                    tmp += i
                    continue
            except Exception as ex:
                raise ValueError('invalid expr:{0}'.format(input_str))
            if tmp:
                ret.append(tmp)
            ret.append(i)
            tmp = ''
    if tmp:
        ret.append(_resolve_signal(tmp))
    return ret

def _to_rational_num (input=''):
    if not input:
        return None
    if not isinstance(input, str):
        return input
    ret = None
    try:
        ret = Fraction(input)
    except Exception as ex:
        raise ValueError('invalid rational num:{0}'.format(input))
    return ret

def _cal (input1=None, input2=None, op='+'):
    if not input1 or not input2:
        return None
    def _divide(x, y):
        return  x if y in [Fraction(1,1), Decimal(1), 1, '1'] else x/y
    ret = None
    #print ('to cal...',input1, op, input2)
    logger.info('to cal...{0},{1},{2}'.format( input1, op, input2))
    try:
        ret = {'+':lambda x,y:x+y,
             '-':lambda x,y:x+y,
             '*':lambda x,y:x*y,
             '/':_divide
             }.get(op)(input1, input2)

    except Exception as ex:
        logger.info('cal error for {0},{1},{2},{3}'.format(input1, op, input2, ex))
    #print ('cal ret', ret)
    logger.info('cal ret:{0}'.format(ret))
    return ret

def get_opertor_priority(val=''):
    if val in ['+','-','*','/']:
        return {'+':1, '-':1, '*':2, '/':2}.get(val)
    return None

def rpn_evaluate(rpn_expr=[]):
     stack_num =  []
     if not rpn_expr:
         return None
     for item in rpn_expr:
         pri = get_opertor_priority(item)
         if not pri:
            stack_num.append(item)
            continue
         try:
            num2 = stack_num.pop()
            num1 = stack_num.pop()
            ret = _cal(_to_rational_num (num1), _to_rational_num (num2), item)
            stack_num.append(ret)
         except Exception as ex:
            raise ValueError('Invalid rpn expr:{0}'.format(rpn_expr))
         #print ('stack_num', stack_num)
     if len(stack_num) !=  1:
         raise ValueError('Invalid expr:{0}'.format(rpn_expr))
     return stack_num[0]

def get_rpn_expr(expr=[], operators=['+','-','*','/','(',')']):
    stack_num = []
    stack_op =[]
    if not expr:
        return []
    for item in expr:
        if item not in operators:
            stack_num.append(item)
            continue
        if item == '(':
            stack_op.append(item)
        elif item == ')':
            top = stack_op.pop()
            while top != '(':
                stack_num.append(top)
                top = stack_op.pop()
        elif get_opertor_priority(item):
            if not stack_op:
                stack_op.append(item)
                continue
            top = stack_op.pop()
            if top == '(':
                stack_op.append(top)
                stack_op.append(item)
                continue
            if get_opertor_priority(item) >= get_opertor_priority(top):
                stack_op.append(top)
                stack_op.append(item)
            else:
                stack_num.append(top)
                stack_op.append(item)
    while stack_op:
        stack_num.append(stack_op.pop())
    return stack_num


def bh_calc(*args, **kwargs):
    '''
    @param expr, the calculation folumar
    @type expr, string
    '''
    logger.info('start, args is:{0}'.format(args))
    if args:
        expr = args[0]
    else:
        expr = kwargs.get('expr')
    if not expr:
        return None
    expr_lst = _get_operator(input_str=expr, seperator=['+','-','*','/','(',')'])
    #print ('expr lst is', expr_lst)
    rpn_expr = get_rpn_expr(expr_lst, operators=['+','-','*','/','(',')'])
    #print ('rpn_expr',rpn_expr)
    ret = rpn_evaluate(rpn_expr)
    if not ret:
        return None
    num, denom  = ret.numerator, ret.denominator
    return ('{0}/{1}'.format(num, denom)) if denom != 1 else '{0}'.format(num)

if __name__  == '__main__':
    if len(sys.argv) > 1:
        expr = sys.argv[1]
        print (expr, '=', bh_calc(expr))
    else:
        print ('Usage: bh_calc.py 9999/1000')
        print ('Support Rational Calculation for Interger:')
        print ('e.g."1/3+1/3","3*(4+6)"')


