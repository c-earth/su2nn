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
        return MulIrrep(mul, self)
    
class MulIrrep(tuple):
    def __new__(cls, mul, irrep):
        return super().__new__(mul, irrep)
    
class Irreps(tuple):
    def __new__(cls, mulirrep_list):
        irreps = mulirrep_list
        if isinstance(mulirrep_list, Irrep):
            irreps = [MulIrrep(1, mulirrep_list)]
        return super().__new__(cls, *irreps)
    
    def simplify(self):
        multi = dict()
        for mul, irrep in self:
            multi[irrep] = multi.get(irrep, 0) + mul
        return Irreps([MulIrrep(mul, irrep) for mul, irrep in multi.items()])