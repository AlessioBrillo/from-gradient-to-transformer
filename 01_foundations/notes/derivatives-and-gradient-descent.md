---
tags: [type/lesson, phase/1]
state: review
created: 2026-06-18
---

> **Series**: [Essence of Calculus — 3Blue1Brown](https://youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr&si=UrW_Qk2DDRi0K3PQ) — Chapters 1-3: *The essence of calculus*, *The paradox of the derivative*, *Derivative formulas through geometry*
>
> **Also**: [StatQuest — Gradient Descent, Step-by-Step](https://youtu.be/sDv4f4s2SB8) | [StatQuest — Stochastic Gradient Descent](https://youtu.be/vMh0zPT0tLI)

## What it is
The derivative measures how fast a function changes at a point; the gradient assembles all partial derivatives into a vector pointing in the direction of steepest ascent.

## Why it exists / what problem it solves
Optimization is the central problem in machine learning: find the parameters θ that minimize a loss function L(θ). The gradient tells you which direction to move θ to reduce L most quickly. Gradient descent — repeatedly stepping in the negative gradient direction — is the algorithm that trains nearly every neural network.

## How it works

### Derivative of a scalar function
The derivative f'(x) is the limit of the difference quotient:

f'(x) = lim_{h→0} (f(x + h) − f(x)) / h

Geometrically: the slope of the tangent line at x. The steeper the slope, the more a small change in x changes f(x).

### Partial derivatives
For a multivariable function f(x₁, x₂, ..., xₙ), the partial derivative ∂f/∂x_i measures how f changes when only x_i changes — holding all other variables constant.

### The gradient
The gradient ∇f is the vector of all partial derivatives:

∇f = [∂f/∂x₁, ∂f/∂x₂, ..., ∂f/∂xₙ]

Key properties:
- ∇f points in the direction of **steepest increase** at the current point.
- −∇f points in the direction of **steepest decrease** — this is the direction we follow in gradient descent.
- The magnitude ‖∇f‖ tells you how steep the slope is.

### Gradient descent
The update rule:

θ_{t+1} = θ_t − η · ∇L(θ_t)

where η is the learning rate (step size). If η is too large, you overshoot; if too small, training is slow.

```python
import numpy as np

def gradient_descent(grad_fn, init, lr=0.01, n_steps=100):
    """Minimize a function given its gradient."""
    theta = np.array(init, dtype=float)
    for step in range(n_steps):
        grad = grad_fn(theta)
        theta -= lr * grad
        if step % 20 == 0:
            print(f"step {step}: θ = {theta}, grad norm = {np.linalg.norm(grad):.6f}")
    return theta

# Example: minimize f(x) = x², gradient f'(x) = 2x
grad_f = lambda x: np.array([2 * x[0]])
minimum = gradient_descent(grad_f, init=[10.0], lr=0.1, n_steps=100)
print(f"Minimum at x = {minimum[0]:.6f} (expected 0)")
```

### The learning rate problem
If the learning rate is too high, gradient descent diverges. If too low, convergence is slow. The relationship between curvature (second derivative) and optimal learning rate is governed by the condition number — a preview of why adaptive optimizers like Adam exist.

## Links
- [[01_foundations/notes/chain-rule-and-backpropagation|Chain Rule and Backpropagation]]
- [[01_foundations/notes/numerical-gradient-check|Numerical Gradient Check]]
- [[01_foundations/notes/key-activation-functions-and-derivatives|Key Activation Functions and Their Derivatives]]

## Insight
The gradient of a function at a point is **not** a vector in the original input space — it lives in the dual space. The conversion from dual vector to direction vector requires an inner product (a metric). In standard gradient descent, we implicitly use the Euclidean inner product, which is why preconditioning (like Adam's adaptive learning rates) can be seen as changing the metric.
