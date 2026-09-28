# Sample Python Code for Execution Sandbox
def calculate_fibonacci_sequence(n):
    """Generate Fibonacci series up to n terms with O(n) complexity."""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    
    sequence = [0, 1]
    while len(sequence) < n:
        sequence.append(sequence[-1] + sequence[-2])
    return sequence

# Execute function and output results
numbers = calculate_fibonacci_sequence(10)
print(f"Generated Fibonacci Series (10 terms): {numbers}")
print(f"Sum of series: {sum(numbers)}")
