from kivy.app import App
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
import math, ast, operator as op

class SafeCalc:
    ops = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv,
           ast.Pow: op.pow, ast.Mod: op.mod, ast.USub: op.neg, ast.UAdd: op.pos}
    funcs = {"sin": lambda x: math.sin(math.radians(x)), "cos": lambda x: math.cos(math.radians(x)),
             "tan": lambda x: math.tan(math.radians(x)), "log": math.log10, "ln": math.log,
             "sqrt": math.sqrt, "abs": abs}
    consts = {"pi": math.pi, "e": math.e}

    @classmethod
    def eval(cls, text):
        text = text.replace("×","*").replace("÷","/").replace("−","-").replace("^","**")
        tree = ast.parse(text, mode="eval")
        def walk(n):
            if isinstance(n, ast.Expression): return walk(n.body)
            if isinstance(n, ast.Constant) and isinstance(n.value,(int,float)): return n.value
            if isinstance(n, ast.BinOp):
                a,b=walk(n.left),walk(n.right); f=cls.ops.get(type(n.op))
                if not f: raise ValueError
                return f(a,b)
            if isinstance(n, ast.UnaryOp):
                f=cls.ops.get(type(n.op))
                if not f: raise ValueError
                return f(walk(n.operand))
            if isinstance(n, ast.Name) and n.id in cls.consts: return cls.consts[n.id]
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in cls.funcs:
                if len(n.args)!=1: raise ValueError
                return cls.funcs[n.func.id](walk(n.args[0]))
            raise ValueError
        result=walk(tree)
        if not math.isfinite(result): raise ValueError
        return result

class Calculator(BoxLayout):
    expression = StringProperty("")
    result = StringProperty("0")
    dark = BooleanProperty(True)
    memory = 0.0
    answer = 0.0
    history = []

    def press(self, value):
        if value == "AC":
            self.expression=""; self.result="0"
        elif value == "⌫":
            self.expression=self.expression[:-1]; self.update()
        elif value == "=":
            self.calculate()
        elif value == "±":
            self.expression = ("-("+self.expression+")") if self.expression else "-"
            self.update()
        elif value == "%":
            self.expression += "/100"; self.update()
        elif value == "√":
            self.expression += "sqrt("; self.update()
        elif value in ("sin","cos","tan","log","ln"):
            self.expression += value+"("; self.update()
        elif value == "x²":
            self.expression += "**2"; self.update()
        elif value == "xʸ":
            self.expression += "**"; self.update()
        elif value == "π":
            self.expression += "pi"; self.update()
        elif value == "e":
            self.expression += "e"; self.update()
        elif value == "!":
            try:
                n=int(SafeCalc.eval(self.expression))
                self.expression=str(math.factorial(n)); self.update()
            except: self.result="Error"
        elif value == "Ans":
            self.expression += str(self.answer); self.update()
        elif value == "M+":
            try: self.memory += SafeCalc.eval(self.expression)
            except: pass
        elif value == "M-":
            try: self.memory -= SafeCalc.eval(self.expression)
            except: pass
        elif value == "MR":
            self.expression += self.fmt(self.memory); self.update()
        elif value == "MC":
            self.memory=0.0
        elif value == "THEME":
            self.dark=not self.dark
        else:
            self.expression += value; self.update()

    def update(self):
        self.result = self.expression or "0"

    def calculate(self):
        if not self.expression: return
        try:
            r=SafeCalc.eval(self.expression)
            self.answer=r
            self.result=self.fmt(r)
            self.history.insert(0, f"{self.expression} = {self.result}")
            self.history=self.history[:30]
            self.expression=self.fmt(r)
        except:
            self.result="Error"

    @staticmethod
    def fmt(x):
        if abs(x-round(x)) < 1e-12: return str(int(round(x)))
        return f"{x:.12g}"

class CalculatorApp(App):
    def build(self):
        self.title="Calculator"
        return Calculator()

if __name__ == "__main__":
    CalculatorApp().run()
