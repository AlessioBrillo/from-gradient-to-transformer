"""Micrograd: minimal autograd engine (pure Python, no NumPy).

Usage:
    from src.training.micrograd import Value

    a = Value(2.0, label='a')
    b = Value(3.0, label='b')
    c = a * b; c.label = 'c'
    d = c + Value(1.0); d.label = 'd'
    e = d.tanh(); e.label = 'e'
    e.backward()
    print(a.grad, b.grad)  # gradients of e w.r.t. a and b
"""

import math

try:
    from graphviz import Digraph
    _HAS_GRAPHVIZ = True
except ImportError:
    _HAS_GRAPHVIZ = False
    Digraph = None


class Value:
    """A scalar value with automatic differentiation support."""

    def __init__(self, data: float, _children: tuple = (), _op: str = "", label: str = "") -> None:
        self.data = data
        self.grad = 0.0
        self._backward = lambda: None
        self._prev = set(_children)
        self._op = _op
        self.label = label

    def __repr__(self) -> str:
        return f"Value(data={self.data:.4f}, grad={self.grad:.4f})"

    def __add__(self, other: "Value | float") -> "Value":
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), "+")

        def _backward() -> None:
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward
        return out

    def __radd__(self, other: float) -> "Value":
        return self + other

    def __mul__(self, other: "Value | float") -> "Value":
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), "*")

        def _backward() -> None:
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward
        return out

    def __rmul__(self, other: float) -> "Value":
        return self * other

    def __pow__(self, other: int | float) -> "Value":
        assert isinstance(other, (int, float)), "only int/float powers supported"
        out = Value(self.data ** other, (self,), f"**{other}")

        def _backward() -> None:
            self.grad += other * (self.data ** (other - 1)) * out.grad
        out._backward = _backward
        return out

    def __neg__(self) -> "Value":
        return self * (-1.0)

    def __sub__(self, other: "Value | float") -> "Value":
        return self + (-other)

    def __rsub__(self, other: float) -> "Value":
        return (-self) + other

    def __truediv__(self, other: "Value | float") -> "Value":
        return self * (other ** (-1.0))

    def tanh(self) -> "Value":
        x = self.data
        t = math.tanh(x)
        out = Value(t, (self,), "tanh")

        def _backward() -> None:
            self.grad += (1.0 - t ** 2) * out.grad
        out._backward = _backward
        return out

    def relu(self) -> "Value":
        out = Value(max(0.0, self.data), (self,), "relu")

        def _backward() -> None:
            self.grad += (out.data > 0.0) * out.grad
        out._backward = _backward
        return out

    def exp(self) -> "Value":
        x = self.data
        out = Value(math.exp(x), (self,), "exp")

        def _backward() -> None:
            self.grad += out.data * out.grad
        out._backward = _backward
        return out

    def log(self) -> "Value":
        x = self.data
        out = Value(math.log(x + 1e-15), (self,), "log")

        def _backward() -> None:
            self.grad += (1.0 / (x + 1e-15)) * out.grad
        out._backward = _backward
        return out

    def sigmoid(self) -> "Value":
        one = Value(1.0)
        return one / ((-self).exp() + one)

    def backward(self) -> None:
        topo = []
        visited = set()

        def _build_topo(v: Value) -> None:
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    _build_topo(child)
                topo.append(v)
        _build_topo(self)

        self.grad = 1.0
        for v in reversed(topo):
            v._backward()

    def draw(self, filename: str = "graph") -> "Digraph | None":
        if not _HAS_GRAPHVIZ or Digraph is None:
            return None
        dot = Digraph(filename=filename, format="png")
        nodes = set()

        def _add(v: Value) -> None:
            if v not in nodes:
                nodes.add(v)
                label = f"{{ {v.label or ''} | data {v.data:.4f} | grad {v.grad:.4f} }}"
                dot.node(str(id(v)), label, shape="record")
                if v._op:
                    op_node = str(id(v)) + v._op
                    dot.node(op_node, v._op, shape="circle")
                    dot.edge(op_node, str(id(v)))
                for child in v._prev:
                    dot.edge(str(id(child)), str(id(v)) + v._op if v._op else str(id(v)))
                    _add(child)
        _add(self)
        dot.render(view=False)
        return dot
