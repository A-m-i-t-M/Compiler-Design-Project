# Equality Saturation Optimizer

A Python implementation of an **Equality Saturation** based optimizer for arithmetic expressions using rewrite rules and Abstract Syntax Trees (AST).

## 📋 Table of Contents

- [Concept](#concept)
- [Aim](#aim)
- [Features](#features)
- [Implementation Details](#implementation-details)
- [Usage](#usage)
- [Testing](#testing)
- [Example Optimizations](#example-optimizations)
- [Project Structure](#project-structure)
- [Future Enhancements](#future-enhancements)

---

## 🎯 Concept

**Equality Saturation** is a compiler optimization technique that applies algebraic rewrite rules to expressions until a fixed point is reached (saturation). Unlike traditional optimizers that apply rules in a specific order and may miss optimization opportunities, equality saturation:

1. Represents multiple equivalent forms of an expression simultaneously
2. Applies rewrite rules exhaustively until no more transformations are possible
3. Selects the "best" representation based on a cost model

This implementation demonstrates the core principles of equality saturation by:
- Building an Abstract Syntax Tree (AST) from arithmetic expressions
- Applying algebraic rewrite rules iteratively
- Using a simple cost model to measure optimization effectiveness

---

## 🎓 Aim

The primary objectives of this project are to:

1. **Understand Compiler Optimization:** Explore how compilers optimize code using algebraic identities and rewrite rules
2. **Implement Equality Saturation:** Demonstrate the saturation approach where rules are applied until convergence
3. **Cost-Based Selection:** Show how a cost model can guide the selection of optimal expression forms
4. **Educational Tool:** Provide a simple, understandable implementation for learning compiler design concepts

---

## ✨ Features

### Supported Operations
- Addition (`+`)
- Multiplication (`*`)
- Parenthesized expressions

### Optimization Rules

#### 1. **Identity Laws**
- `x + 0 → x`
- `0 + x → x`
- `x * 1 → x`
- `1 * x → x`

#### 2. **Annihilation Law**
- `x * 0 → 0`
- `0 * x → 0`

#### 3. **Constant Folding**
- `2 + 3 → 5`
- `4 * 5 → 20`

#### 4. **Distributive Property**
- `a * (b + c) → (a * b) + (a * c)`

### Cost Model
- Measures expression complexity by counting AST nodes
- Lower cost indicates simpler expressions
- Used to evaluate optimization effectiveness

---

## 🔧 Implementation Details

### Architecture

```
┌─────────────┐
│   Input     │ "2*(x+0)"
│ Expression  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Tokenizer  │ ['2', '*', '(', 'x', '+', '0', ')']
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Parser    │ Builds AST with operator precedence
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Rewriter   │ Applies algebraic rules
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Saturation  │ Iterates until fixed point
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Cost Model  │ Evaluates optimization
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Optimized  │ "2*x"
│ Expression  │
└─────────────┘
```

### Components

#### 1. **Tokenizer** (`tokenize`)
- Uses regex to split expressions into tokens
- Recognizes: numbers, variables, operators, parentheses
- Pattern: `r'\d+|[a-zA-Z]+|[+*/()-]'`

#### 2. **AST Node** (`ASTNode`)
- Represents expression tree structure
- Properties: `value`, `left`, `right`
- Implements equality comparison for saturation detection

#### 3. **Parser** (`parse_expression`)
- Recursive descent parser
- Respects operator precedence (* before +)
- Handles parentheses for grouping
- Functions:
  - `parse_factor()`: Handles literals and parenthesized expressions
  - `parse_term()`: Handles multiplication chains
  - `parse_sum()`: Handles addition chains

#### 4. **Rewriter** (`rewrite`)
- Recursively applies transformation rules
- Bottom-up traversal (children before parents)
- Pattern matching on AST structure
- Returns transformed AST

#### 5. **Saturation Engine** (`saturation`)
- Iteratively applies rewrite rules
- Uses deep copy to preserve original AST
- Terminates when AST stops changing (fixed point)
- Implements the core equality saturation loop

#### 6. **Cost Model** (`cost`)
- Simple node-counting metric
- Leaf nodes: cost = 1
- Internal nodes: cost = 1 + cost(left) + cost(right)
- Lower cost = simpler expression

---

## 🚀 Usage

### Basic Usage

```bash
python eqsat.py
```

**Interactive mode:**
```
Enter expression: 2*(x+0)

Original: (2 * (x + 0))
Optimized: (2 * x)

Cost Before: 5
Cost After : 3
```

### Running Test Suite

```bash
python test_cases.py
```

This generates a `test_results.txt` file with detailed results for all 48 test cases.

### Testing Single Expression

```bash
python test_cases.py "a*(b+c)"
```

This creates `single_test_result.txt` with detailed analysis of the specific expression.

---

## 🧪 Testing

The project includes comprehensive test coverage across multiple categories:

### Test Categories (48 tests total)

| Category | Test Count | Description |
|----------|------------|-------------|
| **Identity Rules** | 6 | Tests `x+0`, `x*1` simplifications |
| **Annihilation Rules** | 4 | Tests `x*0` optimizations |
| **Constant Folding** | 6 | Tests numeric computation |
| **Distributive Property** | 4 | Tests expression expansion |
| **Combined Optimizations** | 6 | Tests multiple rule applications |
| **Complex Expressions** | 5 | Tests parser robustness |
| **Nested Expressions** | 3 | Tests deep tree structures |
| **Edge Cases** | 6 | Tests single values and trivial cases |
| **Performance Stress** | 5 | Tests long expression chains |
| **Realistic Expressions** | 3 | Tests practical scenarios |

### Test Results Summary
- **Optimization Rate:** ~70.8% (34/48 tests show cost reduction)
- **All tests pass** without errors
- Results saved to `test_results.txt`

---

## 💡 Example Optimizations

### Example 1: Identity Elimination
```
Input:     x + 0
Original:  (x + 0)  [cost: 3]
Optimized: x        [cost: 1]
Reduction: 2 nodes
```

### Example 2: Annihilation with Addition
```
Input:     a * 0 + b
Original:  ((a * 0) + b)  [cost: 5]
Optimized: b              [cost: 1]
Reduction: 4 nodes
```

### Example 3: Constant Folding
```
Input:     2 + 3
Original:  (2 + 3)  [cost: 3]
Optimized: 5        [cost: 1]
Reduction: 2 nodes
```

### Example 4: Distributive Expansion
```
Input:     2 * (3 + 4)
Original:  (2 * (3 + 4))      [cost: 5]
After:     ((2 * 3) + (2 * 4)) [cost: 7]
Final:     (6 + 8)             [cost: 3]
Optimized: 14                  [cost: 1]
Reduction: 4 nodes
```

### Example 5: Complex Optimization
```
Input:     1 * x + 0 * y
Original:  ((1 * x) + (0 * y))  [cost: 7]
Optimized: x                    [cost: 1]
Reduction: 6 nodes
```

---

## 📁 Project Structure

```
CD Project/
│
├── eqsat.py              # Main optimizer implementation
│   ├── tokenize()        # Expression tokenizer
│   ├── ASTNode           # AST node class
│   ├── parse_expression()# Recursive descent parser
│   ├── print_ast()       # AST pretty printer
│   ├── rewrite()         # Rewrite rule engine
│   ├── saturation()      # Saturation loop
│   └── cost()            # Cost model
│
├── test_cases.py         # Comprehensive test suite
│   ├── test_cases[]      # 48 test expressions
│   ├── run_tests()       # Batch test runner
│   └── run_single_test() # Single expression tester
│
├── test_results.txt      # Generated test results (396 lines)
│
└── README.md             # Project documentation
```

---

## 🔮 Future Enhancements

### Potential Extensions

1. **Additional Operators**
   - Subtraction (`-`)
   - Division (`/`)
   - Exponentiation (`^`)
   - Modulo (`%`)

2. **More Rewrite Rules**
   - Associativity: `(a + b) + c ↔ a + (b + c)`
   - Commutativity: `a + b ↔ b + a`
   - Absorption: `a + a * b → a`
   - De Morgan's Laws (for boolean expressions)

3. **Advanced Features**
   - E-graph data structure for true equality saturation
   - Multiple cost models (minimize operations, minimize depth, etc.)
   - User-defined custom rewrite rules
   - Visualization of AST transformations
   - Support for variables with known constraints

4. **Performance Improvements**
   - Memoization to avoid redundant rewrites
   - Rule ordering heuristics
   - Parallel rule application
   - Termination guarantees and cycle detection

5. **Extended Language Support**
   - Boolean expressions
   - Bitwise operations
   - Function calls
   - Array indexing

---

## 📚 References

- **Equality Saturation**: [Tate et al., "Equality Saturation: A New Approach to Optimization"](https://www.cs.cornell.edu/~ross/publications/eqsat/)
- **E-graphs**: Max Willsey et al., ["egg: Fast and Extensible Equality Saturation"](https://arxiv.org/abs/2004.03082)
- **Compiler Design**: Aho, Lam, Sethi, Ullman - "Compilers: Principles, Techniques, and Tools"

---

## 👥 Author

**Amit M**
- Repository: [Compiler-Design-Project](https://github.com/A-m-i-t-M/Compiler-Design-Project)

---

## 📄 License

This project is created for educational purposes as part of a Compiler Design course.

---

## 🙏 Acknowledgments

This project demonstrates fundamental compiler optimization techniques and serves as an educational tool for understanding:
- Abstract Syntax Trees
- Rewrite systems
- Term rewriting
- Cost-based optimization
- Compiler design principles

Feel free to explore, learn, and extend this implementation!
