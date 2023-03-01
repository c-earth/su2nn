from fractions import Fraction

class Irrep(tuple):
    '''
    Irreducible representation of SU(2)

    Parameters:
        dim     : int
                  positive integer, dimension of representation
        phis    : iterable (optional)
                  sequence of phase in unit of pi for each discontinuous symmetry
    '''
    def __new__(cls, dim, *phis):
        if isinstance(dim, Irrep):
            return dim
        if isinstance(dim, str):
            tmp = dim[1:-1].split(',')
            tmp = [float(x) if float(x)%1.0 != 0 else int(float(x)) for x in tmp ]
            return Irrep(*tmp)
        if hasattr(dim, '__iter__'):
            return Irrep(*dim)
        if not isinstance(dim, int) or dim < 1:
            raise ValueError('Irrep must have positive dimension')
        for phi in phis:
            pass
        return super().__new__(cls, (dim, *phis))
    
    def __repr__(self):
        phis_str = ','.join([str(phis) for phis in self.phis])
        return f'({self.dim},{phis_str})'
    
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
        
    @property
    def dim(self):
        return self[0]
    
    @property
    def phis(self):
        return self[1:]
    
    @property
    def j(self):
        return Fraction(self[0] - 1, 2)
    
class MulIrrep(tuple):
    def __new__(cls, mul, irrep):
        return super().__new__(cls, (mul, irrep))
    
    def __repr__(self):
        return f'{self[0]}x{self[1]}'
    
class Irreps(tuple):
    def __new__(cls, mulirrep_list):
        irreps = mulirrep_list
        if isinstance(mulirrep_list, Irrep):
            irreps = [MulIrrep(1, mulirrep_list)]
        return super().__new__(cls, irreps)
    
    def __repr__(self):
        out = [str(mulirrep) for mulirrep in self]
        return '+'.join(out)
    
    def __mul__(self, other):
        if isinstance(other, Irreps):
            raise ValueError
        else:
            print(other)
            print(self)
            return Irreps(super().__mul__(other))
        
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def simplify(self):
        multi = dict()
        for mul, irrep in self:
            multi[irrep] = multi.get(irrep, 0) + mul
        return Irreps([MulIrrep(mul, irrep) for irrep, mul in multi.items()])
    
print(Fraction('1/2'))