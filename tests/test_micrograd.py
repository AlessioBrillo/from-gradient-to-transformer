"""Tests for micrograd autograd engine."""

import math

from src.training.micrograd import Value


def test_addition() -> None:
    a = Value(2.0)
    b = Value(3.0)
    c = a + b
    assert c.data == 5.0
    c.backward()
    assert a.grad == 1.0
    assert b.grad == 1.0


def test_multiplication() -> None:
    a = Value(2.0)
    b = Value(3.0)
    c = a * b
    assert c.data == 6.0
    c.backward()
    assert a.grad == 3.0
    assert b.grad == 2.0


def test_power() -> None:
    a = Value(3.0)
    b = a ** 2
    assert b.data == 9.0
    b.backward()
    assert a.grad == 6.0


def test_tanh() -> None:
    a = Value(0.5)
    b = a.tanh()
    expected = math.tanh(0.5)
    assert abs(b.data - expected) < 1e-10
    b.backward()
    expected_grad = 1.0 - math.tanh(0.5) ** 2
    assert abs(a.grad - expected_grad) < 1e-10


def test_relu() -> None:
    a = Value(-1.0)
    b = a.relu()
    assert b.data == 0.0
    b.backward()
    assert a.grad == 0.0


def test_chain_rule() -> None:
    x = Value(2.0)
    y = (x ** 2) + (x * 3) + Value(1.0)
    y.backward()
    # dy/dx = 2x + 3 = 7 at x=2
    assert abs(x.grad - 7.0) < 1e-10


def test_scalar_mul() -> None:
    a = Value(2.0)
    b = a * 3.0
    assert b.data == 6.0
    b.backward()
    assert a.grad == 3.0


def test_scalar_add() -> None:
    a = Value(2.0)
    b = a + 1.0
    assert b.data == 3.0
    b.backward()
    assert a.grad == 1.0


def test_subtraction() -> None:
    a = Value(5.0)
    b = Value(3.0)
    c = a - b
    assert c.data == 2.0
    c.backward()
    assert a.grad == 1.0
    assert b.grad == -1.0


def test_division() -> None:
    a = Value(6.0)
    b = Value(3.0)
    c = a / b
    assert abs(c.data - 2.0) < 1e-10
    c.backward()
    assert abs(a.grad - 1.0/3.0) < 1e-10


def test_sigmoid() -> None:
    a = Value(0.0)
    b = a.sigmoid()
    assert abs(b.data - 0.5) < 1e-10
    # sigmoid(0) = 0.5; gradient via (1 - sigmoid) * sigmoid = 0.25
    b.backward()
    assert abs(a.grad - 0.25) < 1e-10


def test_neuron_forward() -> None:
    x1 = Value(2.0)
    x2 = Value(-1.0)
    w1 = Value(0.5)
    w2 = Value(-0.3)
    b = Value(0.1)
    out = (w1 * x1 + w2 * x2 + b).tanh()
    expected = math.tanh(0.5 * 2.0 + (-0.3) * (-1.0) + 0.1)
    assert abs(out.data - expected) < 1e-10
