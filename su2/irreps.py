from fractions import Fraction

class Irrep(tuple):
    def __new__(cls, dim, *phis):
        return super().__new__(cls, (dim, *phis))
    
    @property
    def dim(self):
        return self[0]
    
    @property
    def phis(self):
        return self[1:]
    
    @property
    def j(self):
        return Fraction(self[0] - 1, 2)
    
    def __mul__(self, other):
        dmin = int(2 * abs(self.j - other.j) + 1)
        dmax = int(2 * (self.j + other.j) + 1)
        phi_y = []
        for phi_s, phi_o in zip(self.phis, other.phis):
            phi_y.append((phi_s + phi_o) % 1)
        for d in range(dmin, dmax + 1, 2):
            yield Irrep(d, *phi_y)

    def __rmul__(self, mul):
        return Irreps([(mul, self)])
    
class Irreps(tuple):
    pass

print(Fraction(1, 3)+Fraction(1, 3))