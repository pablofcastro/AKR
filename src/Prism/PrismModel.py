import re

class PrismCommand : 
    """
        Class that models Prism command: prob:(assign0)&(assign1)...
    """
    def __init__(self, text=None) :
        if text is not None :
            prob, assigns =  text.split(":", 1)  # split only on the first ":"
            self.prob = float(prob) 
            self.assigns = assigns.replace(";","")
        else :
            self.prob = None
            self.assigns = None

    def __str__(self) :
        return f"   {self.prob} : {self.assigns}"

class PrismAction :
    """
        This class model PRISM commands, and provides methods to manipulate them
    """
    def __init__(self, action=None) :
        """
            this creates the prism command by parsing the text
        """
        if action is not None :
            pattern = r'^\s*\[(.*?)\]\s*(.*?)\s*->\s*(.*)$'
            match = re.match(pattern, action)
            if not match:
                raise ValueError(f"Invalid format: {action}")
            label, guard, commands = match.groups()
            self.label = label.strip()
            self.guard = guard.strip()
            self.commands = [PrismCommand(part.strip()) for part in commands.split('+')]
        else :
            self.label = ""
            self.guard = ""
            self.commands = []
        
    def cross_product(self, action) :
        """
            Computes the crosss product between to actions
        """
        if not (self.label == action.label) :
            return None
        else :
            result_action = PrismAction()
            result_action.label = self.label
            result_action.guard = str(self.guard)+ " & " + str(action.guard)
            result_action.commands = []
            for c1 in self.commands :
                for c2 in action.commands : 
                    command = PrismCommand()
                    command.prob = c1.prob * c2.prob
                    command.assigns = c1.assigns + " & " + c2.assigns
                    result_action.commands.append(command)
                    
            return result_action
    
    def __str__(self) :
        result = f"""[{self.label}] {self.guard} -> {"+".join([str(command) for command in self.commands])};"""
        return result


class PrismModel :
    def __init__(self, text = None) :
        self.glob = ""
        self.name = ""
        if text is not None :
            self.decl = ""
            lines = text.splitlines()
            actions_str = []
            for line in lines :
                line = line.lstrip()
                if self.name == "" and not "module" in line :
                    self.glob = self.glob + line
                elif line.startswith("module") :
                    words = line.split()
                    self.name = words[1]
                elif actions_str == [] and  not line.startswith("[") :
                    self.decl = self.decl + line + "\n"
                elif line.startswith("[")  :
                    actions_str.append(line)
            self.actions = []
            for action in actions_str :
                self.actions.append(PrismAction(action))
        else :
            self.decl=""
            self.actions = []
    
    def cross_product(self, pmodel) :
        result_model = PrismModel()
        result_model.name = "product"
        result_model.glob = self.glob + pmodel.glob
        result_model.decl = self.decl + "\n" + pmodel.decl
        for action_left in self.actions :
            for action_right in pmodel.actions :
                new_action = action_left.cross_product(action_right)
                if new_action is not None :
                    result_model.actions.append(new_action)
        return result_model
    
    def __str__(self) :
        result = self.glob + "\n"
        result = result + f"module {self.name} \n"
        result = result + self.decl
        for action in self.actions :
            result = result + str(action) + "\n"
        result = result+"endmodule"
        return result
    
def test1() :
    model1 = f"""
    formula init = (s=0);
    module plts
    s : [0..10];   
    [lf] (s=0) -> 0.2:(s'=1) + 0.8:(s'=2);
    [st] (s=0) -> 0.9:(s'=4) + 0.1:(s'=5);
    [rm] (s=0) -> 0.5:(s'=4) + 0.5:(s'=5);   
    [st] (s=0) -> 0.1:(s'=4) + 0.9:(s'=5);
    [st] (s=0) -> 0.9:(s'=4) + 0.1:(s'=5);
    [mb] (s=2) -> 0.1:(s'=6) + 0.9:(s'=7);
    [pn] (s=4) -> 1:(s'=8);
    [mb] (s=5) -> 0.1:(s'=9) + 0.9:(s'=10);     
    endmodule
     """
    model2 = f"""module perception
      state : [0..3];
      accept : [0..1];
      [rm] (state=0) -> 1: (state' = 3) & (accept'=0);
      [mb] (state=3) -> 1: (state' = 2) & (accept'=1);
      [pn] (state=3) -> 1: (state' = 1) & (accept'=1);
 endmodule"""
    pm1 = PrismModel(model1)
    print(str(pm1))
    pm2 = PrismModel(model2)
    print(str(pm2))
    print(str(pm1.cross_product(pm2)))
    
if __name__ == "__main__" :
    test1()