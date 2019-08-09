import operator

from peewee import OP, Expression

EQUAL = operator.eq
GREATER_THAN = operator.gt
GREATER_THAN_OR_EQUAL = operator.ge
LESS_THAN = operator.lt
LESS_THAN_OR_EQUAL = operator.le
NOT = operator.ne
LIKE = lambda l, r: Expression(l, OP.LIKE, r)
ILIKE = lambda l, r: Expression(l, OP.ILIKE, r)
REGEXP = lambda l, r: Expression(l, OP.REGEXP, r)
