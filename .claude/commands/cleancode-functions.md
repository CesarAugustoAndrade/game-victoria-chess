---
description: Comprehensive analysis of function quality using clean code principles
---

Perform a comprehensive analysis of all functions in this project based on clean code principles. Evaluate function design, structure, parameters, and adherence to best practices.

## Analysis Scope
- **Source Files**: Scan all code files (.js, .ts, .jsx, .tsx, .py, .java, .cpp, .c, .go, .rs, .php, .rb, .cs, .swift, .kt, .scala, .clj, .ex, .dart, .lua, .r, .m, .pl, .sh, .sql, etc.)
- **Function Analysis**: Identify all function/method definitions, lambdas, and closures
- **Usage Patterns**: Analyze function signatures, bodies, calls, and dependency relationships
- **Cross-Reference**: Check function interactions and coupling across the codebase

## Function Size & Structure Analysis

### Small Functions Assessment
- **Line count analysis**: Flag functions exceeding 20 lines (ideal: 5-10 lines)
- **Block complexity**: Check for excessive nesting (max 1-2 levels)  
- **Extractable code**: Identify functions that can be broken down further
- **Single responsibility**: Verify each function does only one thing

### Abstraction Level Consistency
- **Mixed abstraction detection**: Find functions mixing high-level and low-level operations
- **Stepdown rule compliance**: Check if functions follow top-down narrative flow
- **Extraction opportunities**: Suggest where code blocks should become separate functions

## Function Behavior Analysis

### Single Responsibility Principle
- **One thing rule**: Identify functions performing multiple unrelated tasks
- **Extraction test**: Flag functions where additional functions can be extracted
- **Cohesion analysis**: Check if all statements operate at the same abstraction level

### Command-Query Separation
- **Dual-purpose detection**: Find functions that both modify state AND return values
- **Side effect identification**: Locate functions with hidden state changes
- **Separation suggestions**: Recommend splitting command/query functions

### Descriptive Naming
- **Clarity assessment**: Check if function names clearly describe their purpose
- **Action representation**: Verify names accurately reflect what functions do
- **Consistency check**: Ensure naming patterns align across similar functions

## Parameter Analysis

### Parameter Count Assessment
- **Golden rule compliance**: Flag functions with >2 parameters (ideal: 0-2)
- **Readability impact**: Assess how parameter count affects code comprehension
- **Refactoring suggestions**: Recommend parameter reduction strategies

### Parameter Quality Issues
- **Boolean flags**: Identify functions using boolean parameters (anti-pattern)
- **Null parameters**: Find functions accepting/returning null values
- **Output parameters**: Detect confusing output parameter usage
- **Parameter object opportunities**: Suggest grouping related parameters

## Error Handling Analysis

### Exception vs Error Codes
- **Error code usage**: Find functions returning error codes instead of throwing exceptions
- **Exception handling**: Verify proper try-catch implementation
- **Error propagation**: Check if errors are handled at appropriate levels

### Try-Catch Structure
- **Block extraction**: Identify try-catch blocks that should be separate functions
- **Single purpose**: Ensure error-handling functions only handle errors
- **Clean separation**: Verify try is first word with nothing after catch/finally

## Side Effects & Temporal Coupling

### Side Effect Detection
- **Hidden modifications**: Find functions with undocumented state changes
- **Temporal coupling**: Identify function pairs requiring specific call order
- **Pure function opportunities**: Suggest functions that could be made pure

### State Management Issues
- **Global state modification**: Track functions modifying global variables
- **Unexpected mutations**: Find functions changing inputs or external state
- **Dependency clarity**: Check if side effects are clearly documented

## Code Structure & Formatting

### Modern Structure Assessment
- **Switch statement analysis**: Identify switch statements that should use polymorphism
- **GoTo detection**: Find any goto-like patterns that violate structured programming
- **Control flow clarity**: Assess single entrance/exit compliance

### File & Function Organization
- **File length**: Check for oversized files (flag >500 lines)
- **Line length**: Verify lines stay within 120-140 characters
- **Function grouping**: Assess logical organization within files

## Report Output

After completing the analysis, create a comprehensive markdown report file named `cleancode-functions-analysis.md` in the project's root directory containing:

### 1. Executive Summary
- **Overall Function Health Score** (0-100) with breakdown by analysis category
- **Project Statistics**: Total functions analyzed, average metrics, violation counts
- **Critical Issues Summary**: Top 5 violations requiring immediate attention
- **Quality Distribution**: Excellent, good, needs improvement, critical categories
- **Key Metrics Dashboard**: Average function length, parameter counts, complexity scores

### 2. Function Size & Structure Findings
- **Oversized functions** (>20 lines) with refactoring suggestions
- **Excessive nesting** violations with simplification recommendations
- **Single responsibility failures** with extraction opportunities
- **Abstraction level mixing** with stepdown rule violations

### 3. Function Behavior Analysis
- **Command-Query separation violations** with split function suggestions
- **Side effect issues** with pure function opportunities
- **Naming clarity problems** with descriptive alternatives
- **State management concerns** with isolation recommendations

### 4. Parameter Quality Assessment
- **Parameter count violations** (>2 parameters) with reduction strategies
- **Boolean flag anti-patterns** with multiple method suggestions
- **Null parameter issues** with validation recommendations
- **Parameter object opportunities** for grouped related parameters

### 5. Error Handling Evaluation
- **Error code anti-patterns** with exception conversion suggestions
- **Try-catch structure problems** with extraction recommendations
- **Error propagation issues** with proper handling strategies
- **Exception clarity problems** with specific error type suggestions

### 6. Code Structure & Organization
- **Switch statement candidates** for polymorphism refactoring
- **File organization issues** with logical grouping suggestions
- **Line length violations** with formatting recommendations
- **Control flow clarity problems** with structured programming fixes

### 7. Detailed Function-by-Function Breakdown
- **Critical issues** (immediate attention required)
- **High priority** (significant impact on maintainability)
- **Medium priority** (improvement opportunities)
- **Low priority** (minor enhancements)

Each entry includes:
- File path and line numbers
- Current code example
- Specific violation description
- Recommended fix with after example
- Impact assessment and difficulty level

### 8. Refactoring Roadmap
- **Phase 1: Quick Wins** (high impact, low effort)
- **Phase 2: Structural Improvements** (medium impact, medium effort)
- **Phase 3: Architectural Changes** (high impact, high effort)

### 9. Team Guidelines & Standards
- **Function size standards** for the project
- **Parameter guidelines** and exceptions
- **Error handling patterns** to adopt
- **Naming conventions** for functions
- **Code review checklist** based on findings

### 10. Metrics Dashboard
- **Function size distribution** histogram
- **Parameter complexity trends** by module
- **Error handling patterns** analysis
- **Code quality hotspots** requiring attention
- **Progress tracking metrics** for future assessments

### 10. Automated Tooling Recommendations
- **Linting Rules**: Function-specific lint configurations and complexity thresholds
- **IDE Settings**: Auto-formatting, refactoring suggestions, and complexity warnings
- **Pre-commit Hooks**: Automated function quality validation and testing requirements
- **Testing Strategies**: Coverage requirements and testing patterns for complex functions

### 11. Quality Metrics & Tracking
- **Function Health Baseline**: Current state measurements and benchmarks
- **Progress Tracking**: KPIs for function quality improvements and technical debt reduction
- **Regular Assessment**: Schedule for ongoing function quality reviews and refactoring

Focus on actionable insights that improve maintainability, readability, and testability. Generate the report file immediately after analysis completion.