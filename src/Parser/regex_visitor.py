from abc import ABC, abstractmethod

#Visitor interface for regular expressions

class RegexVisitor(ABC):

    @abstractmethod
    def visit_regexvar(self, var) :
        pass

    @abstractmethod
    def visit_union(self, union) :
        pass

    @abstractmethod
    def visit_concatenation(self, concat) :
        pass

    @abstractmethod
    def visit_star(self, star) :
        pass
    