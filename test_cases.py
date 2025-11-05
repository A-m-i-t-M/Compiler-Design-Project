"""
Test Cases for Equality Saturation Optimizer (eqsat.py)

This file contains comprehensive test expressions to verify the optimizer's performance.
Each test case includes:
- Input expression
- Expected optimization behavior
- Category of test
"""

import sys
from eqsat import tokenize, parse_expression, saturation, print_ast, cost

# Test case format: (expression, description, expected_behavior)
test_cases = [
    # ========== IDENTITY RULES ==========
    ("x+0", "Identity: x + 0", "Should simplify to: x"),
    ("0+x", "Identity: 0 + x", "Should simplify to: x"),
    ("x*1", "Identity: x * 1", "Should simplify to: x"),
    ("1*x", "Identity: 1 * x", "Should simplify to: x"),
    ("a+0+0", "Multiple identity: a + 0 + 0", "Should simplify to: a"),
    ("a*1*1", "Multiple identity: a * 1 * 1", "Should simplify to: a"),
    
    # ========== ANNIHILATION RULES ==========
    ("x*0", "Annihilation: x * 0", "Should simplify to: 0"),
    ("0*x", "Annihilation: 0 * x", "Should simplify to: 0"),
    ("a*0+b", "Mixed: a * 0 + b", "Should simplify to: b"),
    ("x*0*y", "Chain annihilation: x * 0 * y", "Should simplify to: 0"),
    
    # ========== CONSTANT FOLDING ==========
    ("2+3", "Constant folding: 2 + 3", "Should simplify to: 5"),
    ("5*4", "Constant folding: 5 * 4", "Should simplify to: 20"),
    ("1+2+3", "Multiple constants: 1 + 2 + 3", "Should fold to: 6"),
    ("2*3*4", "Multiple constants: 2 * 3 * 4", "Should fold to: 24"),
    ("10+0", "Constant with identity: 10 + 0", "Should simplify to: 10"),
    ("7*1", "Constant with identity: 7 * 1", "Should simplify to: 7"),
    
    # ========== DISTRIBUTIVE PROPERTY ==========
    ("a*(b+c)", "Distributive: a * (b + c)", "Should expand to: a*b + a*c"),
    ("2*(x+y)", "Distributive with constant: 2 * (x + y)", "Should expand to: 2*x + 2*y"),
    ("x*(3+4)", "Distributive with constants: x * (3 + 4)", "Should simplify to: 7*x or x*7"),
    ("a*(b+0)", "Distributive with identity: a * (b + 0)", "Should simplify to: a*b"),
    
    # ========== COMBINED OPTIMIZATIONS ==========
    ("x+0*y", "Combined: x + 0 * y", "Should simplify to: x"),
    ("a*1+b*0", "Combined: a * 1 + b * 0", "Should simplify to: a"),
    ("2*(3+4)", "Combined: 2 * (3 + 4)", "Should fully simplify to: 14"),
    ("x*(y+0)", "Combined: x * (y + 0)", "Should simplify to: x*y"),
    ("0+a*1", "Combined: 0 + a * 1", "Should simplify to: a"),
    ("1*x+0*y", "Combined: 1 * x + 0 * y", "Should simplify to: x"),
    
    # ========== COMPLEX EXPRESSIONS ==========
    ("a+b+c", "No optimization: a + b + c", "Should remain unchanged"),
    ("a*b*c", "No optimization: a * b * c", "Should remain unchanged"),
    ("(a+b)*(c+d)", "Complex: (a + b) * (c + d)", "No direct optimization available"),
    ("a*(b+c)+d", "Complex: a * (b + c) + d", "Distributive applies: a*b + a*c + d"),
    ("2*x+3*y", "Complex: 2 * x + 3 * y", "Should remain unchanged"),
    
    # ========== NESTED EXPRESSIONS ==========
    ("a*(b*(c+d))", "Nested: a * (b * (c + d))", "Distributive may apply multiple times"),
    ("(x+0)*(y+0)", "Nested identities: (x + 0) * (y + 0)", "Should simplify to: x*y"),
    ("((a+0)*1)+0", "Triple nested identity", "Should simplify to: a"),
    
    # ========== EDGE CASES ==========
    ("0", "Single constant: 0", "Should remain: 0"),
    ("x", "Single variable: x", "Should remain: x"),
    ("42", "Single constant: 42", "Should remain: 42"),
    ("0+0", "Constant identities: 0 + 0", "Should simplify to: 0"),
    ("0*0", "Constant annihilation: 0 * 0", "Should simplify to: 0"),
    ("1+1", "Constants: 1 + 1", "Should fold to: 2"),
    
    # ========== PERFORMANCE STRESS TESTS ==========
    ("a+b+c+d+e", "Long chain addition", "Tests parser and optimizer performance"),
    ("a*b*c*d*e", "Long chain multiplication", "Tests parser and optimizer performance"),
    ("1*2*3*4*5", "Long constant chain", "Should fold to: 120"),
    ("a+0+0+0+0", "Multiple identities", "Should simplify to: a"),
    ("x*(a+b+c)", "Distributive with multiple terms", "Limited by current implementation"),
    
    # ========== REALISTIC EXPRESSIONS ==========
    ("2*x+0*y+3*z", "Realistic: 2*x + 0*y + 3*z", "Should simplify to: 2*x + 3*z"),
    ("a*1*b*1*c", "Realistic: a * 1 * b * 1 * c", "Should simplify to: a*b*c"),
    ("100*0+x", "Realistic: 100 * 0 + x", "Should simplify to: x"),
]


def run_tests(output_file="test_results.txt"):
    """Run all test cases and save results to a file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("EQUALITY SATURATION OPTIMIZER - TEST SUITE\n")
        f.write("=" * 80 + "\n\n")
        
        total_tests = len(test_cases)
        successful_optimizations = 0
        
        for i, (expr, description, expected) in enumerate(test_cases, 1):
            f.write(f"Test {i}/{total_tests}: {description}\n")
            f.write(f"Input:    {expr}\n")
            
            try:
                # Parse and optimize
                tokens = tokenize(expr)
                ast = parse_expression(tokens)
                original_str = print_ast(ast)
                original_cost = cost(ast)
                
                optimized = saturation(ast)
                optimized_str = print_ast(optimized)
                optimized_cost = cost(optimized)
                
                # Display results
                f.write(f"Original:  {original_str} (cost: {original_cost})\n")
                f.write(f"Optimized: {optimized_str} (cost: {optimized_cost})\n")
                f.write(f"Expected:  {expected}\n")
                
                # Check if optimization occurred
                if original_cost > optimized_cost:
                    f.write(f"✓ OPTIMIZED - Cost reduced by {original_cost - optimized_cost}\n")
                    successful_optimizations += 1
                elif original_str != optimized_str:
                    f.write(f"⟳ TRANSFORMED - Cost unchanged\n")
                else:
                    f.write(f"→ NO CHANGE\n")
                
            except Exception as e:
                f.write(f"✗ ERROR: {e}\n")
            
            f.write("-" * 80 + "\n\n")
        
        # Summary
        f.write("=" * 80 + "\n")
        f.write("SUMMARY\n")
        f.write("=" * 80 + "\n")
        f.write(f"Total tests: {total_tests}\n")
        f.write(f"Expressions with cost reduction: {successful_optimizations}\n")
        f.write(f"Optimization rate: {successful_optimizations/total_tests*100:.1f}%\n\n")
    
    print(f"✓ Test results saved to: {output_file}")
    print(f"  Total tests: {total_tests}")
    print(f"  Optimizations: {successful_optimizations}")


def run_single_test(expr, output_file="single_test_result.txt"):
    """Run a single test expression and save to file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write(f"Testing: {expr}\n")
        f.write("=" * 80 + "\n\n")
        
        try:
            tokens = tokenize(expr)
            f.write(f"Tokens: {tokens}\n\n")
            
            ast = parse_expression(tokens)
            original_str = print_ast(ast)
            original_cost = cost(ast)
            
            optimized = saturation(ast)
            optimized_str = print_ast(optimized)
            optimized_cost = cost(optimized)
            
            f.write(f"Original:  {original_str}\n")
            f.write(f"Optimized: {optimized_str}\n\n")
            f.write(f"Cost Before: {original_cost}\n")
            f.write(f"Cost After:  {optimized_cost}\n")
            f.write(f"Reduction:   {original_cost - optimized_cost}\n")
            
            print(f"✓ Test result saved to: {output_file}")
            
        except Exception as e:
            f.write(f"Error: {e}\n")
            print(f"✗ Error occurred: {e}")
            print(f"  Details saved to: {output_file}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run specific test expression from command line
        expr = sys.argv[1]
        run_single_test(expr)
    else:
        # Run all tests
        run_tests()
