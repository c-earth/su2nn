from fractions import Fraction

class SU2PIrrep(tuple):
    def __new__(cls, dims, p):
        return super().__new__(cls, (dims, p))
    
    @property
    def dims(self):
        return self[0]
    
    @property
    def p(self):
        return self[1]
    
    @property
    def j(self):
        return Fraction(self[0] - 1, 2)
    
class Irreps(tuple):
    @property
    def dims(self):
        return