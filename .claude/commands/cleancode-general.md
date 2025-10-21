---
description: Comprehensive analysis of general clean code principles and quality metrics
---

Perform a comprehensive analysis of general clean code principles throughout this project. Evaluate commenting practices, code duplication, error handling patterns, and overall code quality metrics.

## Analysis Scope
- **Source Files**: Scan all code files (.js, .ts, .jsx, .tsx, .py, .java, .cpp, .c, .go, .rs, .php, .rb, .cs, .swift, .kt, .scala, .clj, .ex, .dart, .lua, .r, .m, .pl, .sh, .sql, .html, .css, .scss, .less, etc.)
- **Project Structure**: Analyze documentation, configuration files, build scripts, and project organization
- **Cross-Cutting Concerns**: Assess overall codebase health, maintainability patterns, and architectural quality
- **Quality Metrics**: Evaluate technical debt, complexity, and maintainability indicators

## Comments Analysis

### Good Comments Detection
- **Legal Comments**: Verify copyright and license information placement
- **Informative Comments**: Identify helpful explanations of return values and behavior
- **Intent Explanation**: Find comments that clarify implementation reasoning
- **TODO Comments**: Catalog future tasks and improvement notes
- **Code Improvement**: Locate comments that could be replaced with better function names

### Bad Comments Identification
- **Compensating for Bad Code**: Find comments explaining poorly written code that should be refactored
- **Redundant Comments**: Detect comments that restate obvious code behavior
- **Closing Brace Comments**: Identify unnecessary brace markers in long functions
- **Commented-Out Code**: Find dead code that should be deleted (version control preserves history)
- **Noise Comments**: Locate obvious statements that add no value
- **Incorrect Comments**: Detect outdated or wrong comments that mislead readers
- **Journal Comments**: Find change logs that belong in version control, not comments

### Comment Quality Assessment
- **Self-documenting code opportunities**: Suggest where better naming eliminates comment needs
- **Comment-to-code ratio**: Analyze if comments are appropriately balanced
- **Comment maintenance**: Check for consistency between comments and actual code behavior

## DRY Principle Analysis

### Duplication Detection
- **Code Duplication**: Identify identical or near-identical code blocks across files
- **Logic Duplication**: Find repeated business rules and algorithms
- **Configuration Duplication**: Detect repeated settings and constants
- **Structure Duplication**: Identify similar class/function patterns

### Duplication Categories
- **Imposed Duplication**: Code required by standards or platform constraints
- **Inadvertent Duplication**: Unknowing repetition by developers
- **Impatient Duplication**: Shortcuts taken due to time pressure
- **Interdeveloper Duplication**: Multiple team members unknowingly duplicating work

### DRY Violation Assessment
- **Knowledge representation**: Check if each concept has single, authoritative representation
- **Change impact**: Identify areas where one logical change requires multiple code updates
- **Maintenance burden**: Assess effort required to keep duplicated code synchronized

### DRY Exceptions Evaluation
- **Performance optimizations**: Justified duplication for speed improvements
- **Coupling reduction**: Duplication to maintain component independence
- **Test readability**: Acceptable duplication for clear test cases
- **Generated code**: Auto-generated duplication that shouldn't be manually modified

## Error Handling Analysis

### Error Handling Principles
- **Root Cause Focus**: Check if errors are fixed at source vs. patched repeatedly
- **Error Context**: Verify errors include where, what, and why information
- **Proper Handling**: Assess distinction between real errors and false alarms
- **Exception Usage**: Evaluate preference for exceptions over error codes

### Exception vs Error Code Patterns
- **Return Code Analysis**: Find functions returning error codes instead of throwing exceptions
- **Error Code Clutter**: Identify complex error checking that obscures main logic
- **Exception Clarity**: Check if exceptions separate concerns from main algorithms
- **Error Propagation**: Assess how errors flow through the system

### Try-Catch-Finally Assessment
- **Exception Context**: Verify exceptions include enough information for debugging
- **Custom Exceptions**: Check for specific exception types vs. generic ones
- **Exception Wrapping**: Ensure stack traces are preserved when wrapping exceptions
- **Resource Management**: Verify proper cleanup in finally blocks

### Null Handling Evaluation
- **Null Returns**: Identify functions that return null unnecessarily
- **Null Parameters**: Find functions accepting null parameters
- **Null Checks**: Assess defensive programming against null values
- **Alternative Patterns**: Suggest Optional/Maybe patterns where appropriate

## Code Quality Metrics Assessment

### Static Analysis Metrics
- **Code Standards Compliance**: Evaluate adherence to coding standards and best practices
- **Style Consistency**: Check formatting, naming, and structural consistency
- **Rule Violations**: Identify violations of language-specific best practices

### Testing Metrics
- **Unit Test Coverage**: Assess percentage of code covered by tests
- **Test Success Rate**: Evaluate test reliability and failure patterns
- **Test Quality**: Check for meaningful assertions and edge case coverage

### Complexity Metrics
- **Cyclomatic Complexity**: Measure code path complexity (target: <10 per method)
- **Coupling Between Objects (CBO)**: Assess interdependency between classes
- **Lack of Cohesion in Methods (LCOM)**: Evaluate class internal consistency

### Maintainability Metrics
- **Technical Debt**: Assess accumulated shortcuts and maintenance burden
- **Code Duplication Percentage**: Measure repeated code structures
- **Comment Density**: Evaluate appropriate balance of comments to code

### Architecture Quality
- **Component Coupling**: Assess dependencies between major components
- **Abstraction Levels**: Check for appropriate separation of concerns
- **Design Pattern Usage**: Evaluate proper application of common patterns

## Report Output

After completing the analysis, create a comprehensive markdown report file named `cleancode-general-analysis.md` in the project's root directory containing:

### 1. Executive Summary
- **Overall Code Health Score** (0-100) with key metrics dashboard
- **Critical Issues Summary** requiring immediate attention (top 10)
- **Quality Trends** and patterns discovered across the codebase
- **Improvement Priority Matrix** (high impact vs. low effort)

### 2. Comments Analysis Report
- **Good Comments Inventory**: Well-written comments that add value
- **Bad Comments Catalog**: Comments that should be removed or refactored
- **Self-Documentation Opportunities**: Where better naming can replace comments
- **Comment Maintenance Issues**: Outdated or incorrect comments found

### 3. DRY Principle Violations
- **Code Duplication Hotspots**: Most critical duplication areas with impact assessment
- **Refactoring Opportunities**: Specific suggestions for eliminating duplication
- **Acceptable Duplication**: Cases where duplication is justified
- **Maintenance Risk Areas**: Code requiring synchronized updates

### 4. Error Handling Assessment
- **Exception Strategy**: Current patterns vs. clean code recommendations
- **Error Code Anti-patterns**: Functions that should throw exceptions instead
- **Null Safety Issues**: Areas prone to null pointer exceptions
- **Error Context Problems**: Exceptions lacking sufficient debugging information

### 5. Code Quality Metrics Dashboard
- **Complexity Analysis**: Methods/classes exceeding recommended thresholds
- **Coupling Assessment**: Highly interdependent components needing refactoring
- **Testing Gaps**: Areas with insufficient test coverage
- **Technical Debt Hotspots**: Code areas with highest maintenance burden

### 6. Detailed Findings by File
- **Critical Issues** (immediate attention required)
- **High Priority** (significant impact on maintainability)
- **Medium Priority** (improvement opportunities)
- **Low Priority** (minor enhancements)

Each finding includes:
- File path and line numbers
- Specific violation description
- Code examples demonstrating the issue
- Recommended solution with refactored examples
- Impact assessment and refactoring difficulty

### 7. Improvement Roadmap
- **Phase 1: Critical Fixes** (error handling, major duplications)
- **Phase 2: Quality Improvements** (comments, minor duplications)
- **Phase 3: Optimization** (metrics improvements, architectural refinements)

### 8. Team Guidelines & Best Practices
- **Commenting Standards** based on findings
- **DRY Implementation Strategy** for the project
- **Error Handling Conventions** to adopt
- **Code Review Checklist** incorporating all principles

### 9. Automated Tooling Recommendations
- **Static Analysis Tools** for ongoing quality monitoring
- **Linting Rules** to prevent future violations
- **Pre-commit Hooks** for quality gates
- **IDE Configurations** for consistent development

### 10. Quality Metrics & Tracking
- **Code Health Baseline**: Current state measurements and quality benchmarks
- **Progress Tracking**: KPIs for code quality improvements and technical debt reduction
- **Monitoring Dashboard**: Real-time quality metrics and trend analysis
- **Regular Assessment**: Schedule for ongoing quality reviews and improvement cycles

Focus on actionable insights that improve overall code maintainability, readability, and quality. Generate the report file immediately after analysis completion.