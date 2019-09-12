import operator

from peewee import OP, Expression

EQ = operator.eq
GT = operator.gt
GE = operator.ge
LT = operator.lt
LE = operator.le
NOT = operator.ne
LIKE = lambda l, r: Expression(l, OP.LIKE, r)
ILIKE = lambda l, r: Expression(l, OP.ILIKE, r)
REGEXP = lambda l, r: Expression(l, OP.REGEXP, r)
IEGEXP = lambda l, r: Expression(l, OP.IREGEXP, r)
