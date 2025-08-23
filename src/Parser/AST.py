"""
    This file constains the AST for the Knowing-Kow logic.
"""

from abc import ABC, abstractmethod

#class for Specifications
class Spec(ABC) :
    def __init__(self, prismmodel, perception, property) :
        self.prismmodel = prismmodel
        self.perception = perception
        self.property = property 
    
    def __str__(self) :
        return f"""
                PLTS: {str(self.prismmodel)}
                Perception: {str(self.perception)}
                Property: {str(self.property)}
                """

    def accept(self, visitor) :
        self.prismmodel.accept(visitor)
        self.perception.accept(visitor)
        self.property.accept(visitor)
  
# Class for the Prism model
class PrismModel(ABC) :
    def __init__(self, model) :
        self.model = model.replace('endplts','') # this is basically text passed to prism tool.
     
    def __str__(self) :
        return self.model
    
    def accept(self, visitor) : 
        pass

# class for the Perceptions
class Perception(ABC) :
    def __init__(self, *regexps) :
        self.regexps = regexps 

    def __str__(self) :
        return "\n".join(map(str, self.regexps))

    def accept(self, visitor) :
        for reg in self.regexps :
            visitor.visit(reg)

class Regex(ABC) :
    def __init__(self, expr) :
        self.expr = expr

    def __str__(self) :
        return str(self.expr)

    def accept(self, visitor) :
        visitor.visit(self.expr)

class RegexVar(Regex) :
    def __init__(self, var) :
        self.var = var

    def __str__(self) :
        return str(self.var)

    def accept(self, visitor) :
        visitor.visit_regexvar(self)

class Star(Regex) :
    def __init__(self, regex) :
        self.regex = regex
    
    def __str__(self) :
        return str(self.regex) + "*"

    def accept(self, visitor) :
        self.regex.accept(visitor)
        visitor.visit_star(self)

class BinaryRegex(Regex) :
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def accept(self, visitor) :
        self.left.accept(visitor)
        self.right.accept(visitor)

class Union(BinaryRegex) :
    def __str__(self):
        return f"({self.left} + {self.right})"

    def accept(self, visitor) :
        super().accept(visitor)
        visitor.visit_union(self)

class Concatenation(BinaryRegex) :
    def __str__(self):
        return f"({self.left} . {self.right})"

    def accept(self, visitor) :
        super().accept(visitor)
        visitor.visit_concatenation(self)
    
# class for property
class Property(ABC) :
    def __init__(self, form) :
        self.form = form
    
    def __str__(self) :
        str(self.form)

    def accept(self, visitor) :
        visitor.visit(self.form)

# Base class for all logical formulas
class Form(ABC):

    def __eq__(self, other) :
        return str(self) == str(other)

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def accept(self, visitor) :
        pass


# Represents a variable, e.g., "p" or "q"
class Var(Form):
    def __init__(self, name) :
        self.name = name

    def __str__(self):
        return str(self.name)
    
    def accept(self, visitor) :
        visitor.visit_var(self)


# Represents a constant (a number in [0,1])
class Constant(Form):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def accept(self, visitor) :
        visitor.visit_constant(self)


# Base class for unary operations
class UnaryOperation(Form):
    def __init__(self, operand):
        self.operand = operand

    def accept(self, visitor) :
        self.operand.accept(visitor)
       

# Unary operation for Luk. negation (lnot)
class Not(UnaryOperation):
    def __str__(self):
        return f"! {self.operand}"

    def accept(self, visitor) :
        super().accept(visitor)
        visitor.visit_not(self)


# Base class for binary operations
class BinaryOperation(Form):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def accept(self, visitor) :
        self.left.accept(visitor)
        self.right.accept(visitor)

# Binary operation for Luk. conjunction (land)
class And(BinaryOperation):
    def __str__(self):
        return f"({self.left} && {self.right})"

    def accept(self, visitor) :
        super().accept(visitor)
        visitor.visit_and(self)

# Binary operation for Luk. disjunction (lor)
class Or(BinaryOperation):
    def __str__(self):
        return f"({self.left} || {self.right})"

    def accept(self, visitor) :
        super().accept(visitor)
        visitor.visit_or(self)

# Modal operator. Knowing How
class Kh(Form):
    def __init__(self, left, right, lb) :
        self.left = left
        self.right = right
        self.lb = lb

    def __str__(self):
        return f"Kh({str(self.left)},{str(self.right)})>={self.lb}"

    def accept(self, visitor) :
        self.left.accept(visitor)
        self.right.accept(visitor)
        visitor.visit_kh(self)
