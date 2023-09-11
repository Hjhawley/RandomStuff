import numpy as np

# Define the function
def f(x):
    return np.sin(1/x)

# Define the limits
a = 0.001
b = 0.01

# Midpoint Rule
def midpoint_rule(a, b, n):
    h = (b-a)/n
    integral = 0
    for i in range(n):
        x = a + h*(i + 0.5)
        integral += f(x)
    return h * integral

# Trapezoidal Rule
def trapezoidal_rule(a, b, n):
    h = (b-a)/n
    integral = f(a)/2 + f(b)/2
    for i in range(1, n):
        x = a + i*h
        integral += f(x)
    return h * integral

# Simpson's Rule
def simpson_rule(a, b, n):
    if n % 2 != 0:
        raise ValueError("n must be an even integer")
    
    h = (b-a)/n
    integral = f(a) + f(b)
    
    for i in range(1, n, 2):
        x = a + i*h
        integral += 4 * f(x)
    
    for i in range(2, n-1, 2):
        x = a + i*h
        integral += 2 * f(x)
        
    return (h/3) * integral

# Number of subintervals
n_midpoint = 100000  # Modify as needed
n_trapezoidal = 100000  # Modify as needed
n_simpson = 100000  # Must be even, modify as needed

# Calculations
midpoint_result = midpoint_rule(a, b, n_midpoint)
trapezoidal_result = trapezoidal_rule(a, b, n_trapezoidal)
simpson_result = simpson_rule(a, b, n_simpson)

# Display results
print(f"Midpoint Rule with {n_midpoint} subintervals: {midpoint_result:.12f}")
print(f"Trapezoidal Rule with {n_trapezoidal} subintervals: {trapezoidal_result:.12f}")
print(f"Simpson's Rule with {n_simpson} subintervals: {simpson_result:.12f}")
