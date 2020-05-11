#TODO
"""
class make:
    @staticmethod
    def _SELECT(col,out):

        pass
    @staticmethod
    def _FROM(table,out):
        pass
    @staticmethod
    def _WHERE(cond,out):
        pass
    @staticmethod
    def _COL(col,out):
        pass
    @staticmethod
    def _DISTINCT(col,out):
        pass
    @staticmethod
    def _F(col,out):
        pass
    @staticmethod
    def _BCOND(cond,out):
        pass
    @staticmethod
    def _ORDERBY(col_cond,out):
        pass
    @staticmethod
    def _LIMIT(nos,out):
        pass
    @staticmethod
    def _IN(vals,out):
        pass
    @staticmethod
    def _BETWEEN(val,out):
        pass
    methd = {
        "SELECT":_SELECT,
        "FROM" : _FROM,
        "WHERE": _WHERE,
        "COL" : _COL,
        "DISTINCT" :_DISTINCT,
        "F": _F,
        "BCOND" : _BCOND, # AND OR NOT LIKE
        "ORDER BY" : _ORDERBY,
        "LIMIT" : _LIMIT,
        "IN" : _IN,
        "BETWEEN" : _BETWEEN
    }
    def __init__(self):
        pass
    @staticmethod
    def parseList(lst,out):
        if len(lst) == 0:
            raise Exception
        while len(lst) > 0:
            tup = lst.pop(0)
            make.methd[tup[0]](tup[1],out)


"""