#!/usr/bin/python2.7 

from z3 import *
from register_convert import register
from instruction import instruction


class SymbolicExecutionEngine(instruction):
    def __init__(self, file_disass):
        self.ctx = register()
        self.disass = open(file_disass)
        self.mem = {}
        self.idx = 0
        self.sym_variables = []
        self.equations = {}

    def _push_equation(self, e):
        self.equations[self.idx] = e
        self.idx += 1
        return (self.idx - 1)

    def set_reg_with_equation(self, r, e):
        self.ctx[r] = self._push_equation(e)

    def get_reg_equation(self, r):
        return self.equations[self.ctx[r]]

    
    def run(self):
        for line in self.disass:
            address, mnemonic, dst, src = line.split(" ")
            # print(mnemonic, dst, src)
            eval("self._{0}('{1}', '{2}')".format(mnemonic, dst, src[:-1]))
            
    def get_solution(self, reg, value):
        s = Solver()
        eq = self.get_reg_equation(reg)
        s.add(eq == value)
        s.check()
        return s.model()

    def get_solver(self, output, value):
        s = Solver()
        eq = [self.equations[self.mem[i]] for i in output]
        s.add(*[ x == ord(y) for x, y in zip(eq, value)])
        return s

    def get_string_solution(self, output, value):
        s = self.get_solver(output, value)
        s.check()
        return s.model()
