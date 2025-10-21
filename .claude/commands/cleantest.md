# CleanTest - Unit Test Quality Analyzer

Analyze unit tests for readability, maintainability, and best practices based on "Writing Readable Unit Tests" principles.

## Usage
```
/cleantest [project_path]
```

## What it does

Performs comprehensive analysis of unit tests following Robert C. Martin's principle: *"The ratio of time spent reading vs. writing is well over 10:1... making it easy to read actually makes it easier to write."*

The command analyzes test files and generates a detailed markdown report covering:

### 1. Test Naming Convention Analysis
Evaluates test names against recommended patterns that answer "Why are you writing this test?":

#### JavaScript/TypeScript Projects
For JS/TS projects, follows the specific naming convention:
- **should [behavior] when/if [condition]**
  - `should return error when user is not authenticated`
  - `should calculate total if all items are valid`
  - `should throw exception when account is blocked`
  - `should update state if payment succeeds`

#### General Language Patterns
- **MethodName_StateUnderTest_ExpectedBehavior**
  - `rejectPayment_BlockedAccount_ExceptionThrown`
  - `isFallingBehindTheSchedule_EmployeeInVacation_False`

- **Should_ExpectedBehavior_When_StateUnderTest**
  - `Should_ThrowException_When_ExpirationDateIsLessThanToday`
  - `When_InvalidID_Expect_FailToAuthenticate`

- **Given_Preconditions_When_StateUnderTest_Then_ExpectedBehavior**
  - `Given_UserIsPowerUser_When_RequestAdminAccess_Then_ThrowException`
  - `Given_PartIsInStock_When_AddToOrder_Then_ChangeInvoiceSuccess`

- **testFeatureBeingTested**
  - `testFailToWithdrawMoneyIfAccountBalanceIsNegative`
  - `testFormIsNotSubmittedIfMandatoryFieldsAreMissing`

### 2. AAA Pattern Compliance
Verifies tests follow the three logical steps:

1. **Arrange Inputs**: Test setup and object property definition
2. **Act On the Target Behavior**: Execute the code being tested
3. **Assert an Expected Output**: Verify results match expectations

### 3. Code Isolation Assessment
**Code isolation** is a simple yet effective concept that greatly simplifies unit testing. The analysis checks adherence to two basic rules:

1. One piece of code should not know about another piece of code or affect it in any way
2. **A** should not be aware of **B**, **C**, or anything else. If **A** uses **B**, it should not know where **B** came from or where **B** is going

#### SOLID Principles Validation
1. **Single Responsibility Principle:** A class, method, or module should have only one responsibility
2. **Open Closed Principle:** Software entities should be open for extension but closed for modification
3. **Liskov Substitution Principle:** Objects should be replaceable with instances of their subtypes without altering correctness
4. **Interface Segregation Principle:** Multiple client-specific interfaces are better than one general-purpose interface
5. **Dependency Inversion Principle:** High-level modules should not depend on low-level modules. Both should depend on abstractions

### 4. Test Doubles Usage Analysis
A **test double** is anything that replaces a production entity in a test scenario. The analysis evaluates proper usage of:

1. **Dummy**: Test double with no behavior that returns default values for all methods. Serves as placeholders, often used to create parameter lists so code compiles

2. **Fake**: Object with complete working implementation but bypasses certain behaviors. Uses shortcuts that help unit testing (e.g., in-memory database for testing vs. real database in production)

3. **Stub**: Hardcoded object providing predefined responses when specific methods are called. Has predefined, controlled behavior - returns the same value every time called. Used to simulate API returning correct values

4. **Spy**: Stub that records information based on how it's called. Keeps logs about usage that can be checked after testing to make assumptions about interactions

5. **Mock**: Object programmed for expected interactions. Focuses on verifying interactions rather than state. Validates provided arguments or order/number of interactions. Usually trained to:
   - Return a specific value when input is a specific value
   - Throw an exception when input is a specific value

## Supported Test Patterns
- JavaScript/TypeScript: `*.test.js`, `*.spec.ts`, etc.
- Python: `*_test.py`, `test_*.py`
- Java: `*Test.java`, `*Tests.java`
- Go: `*_test.go`
- C#: `*Test.cs`, `*Tests.cs`
- PHP: `*Test.php`, `*.test.php`
- Ruby: `*_test.rb`

## Analysis Output
Creates `test-quality-report.md` in project root containing:

### Executive Summary
- Total test files and tests analyzed
- Quality score with color-coded rating
- Issue breakdown by category

### Detailed Issue Analysis
- **Naming Issues**: Tests with unclear or non-descriptive names
- **Structure Issues**: AAA pattern violations
- **Isolation Issues**: Hard dependencies and external calls
- **Readability Issues**: Long methods, magic numbers, complex assertions

### Best Practices Guide
Complete reference including:
- All four naming convention patterns with examples
- AAA pattern implementation examples
- SOLID principles in testing
- Test doubles usage patterns
- Code isolation techniques

## Quality Scoring
- **85%+**: 🟢 Excellent - Following best practices
- **70-84%**: 🟡 Good - Minor improvements needed  
- **50-69%**: 🟠 Fair - Several areas need attention
- **<50%**: 🔴 Needs Improvement - Significant issues found

## Benefits
- **Improves maintainability** through readable test structure
- **Reduces debugging time** with clear test intent
- **Enforces team standards** with automated quality checks
- **Educational tool** teaching clean testing principles
- **Objective code review** metrics for test quality

The setup logic of readable unit tests becomes visible right away, making it easy to figure out how code works and fix problems without debugging when tests fail.