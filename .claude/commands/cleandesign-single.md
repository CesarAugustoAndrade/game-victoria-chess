---
description: Comprehensive analysis of Single Responsibility Principle (SRP) violations and design improvements
---

Perform a comprehensive analysis of Single Responsibility Principle (SRP) adherence throughout this project. Identify classes and modules with multiple responsibilities, assess cohesion levels, and provide refactoring recommendations.

## Analysis Scope
- **Source Files**: Scan all code files (.js, .ts, .jsx, .tsx, .py, .java, .cpp, .c, .go, .rs, .php, .rb, .cs, .swift, .kt, .scala, .clj, .ex, .dart, .lua, .r, .m, .pl, .sh, .sql, etc.)
- **Classes & Modules**: Analyze all classes, modules, functions, and components
- **Responsibility Identification**: Map different reasons for change to specific actors/users
- **Cohesion Assessment**: Evaluate method-field relationships within classes

## Single Responsibility Principle Assessment

### 1. Class Size and Description Analysis
- **Single Sentence Test**: Check if each class can be described in one sentence
- **Word Count Validation**: Verify descriptions are fewer than 25 words
- **Conjunction Detection**: Flag descriptions containing "if," "or," "and," or "but"
- **Clarity Assessment**: Ensure classes explain themselves without additional comments

### 2. Responsibility Identification
- **Reason to Change Analysis**: Identify all potential reasons each class might need modification
- **Actor Mapping**: Connect each responsibility to specific user groups or stakeholders
- **Change Source Tracking**: Map different types of changes (UI, business logic, data access, reporting) to their origins
- **Responsibility Families**: Group related functions that serve the same actor

### 3. Cohesion Analysis
- **High Cohesion Detection**: Identify classes where most methods use most fields
- **Low Cohesion Identification**: Find classes with subsets of methods using subsets of fields
- **Maximum Cohesive Methods**: Detect methods that use all class fields
- **Field-Method Correlation**: Analyze relationships between class members

### 4. Mixed Responsibilities Detection
- **Multi-Actor Classes**: Find classes serving multiple user groups
- **Cross-Concern Coupling**: Identify classes mixing different types of functionality
- **Fragile Design Patterns**: Detect designs prone to unexpected breakage from changes
- **Responsibility Accumulation**: Find areas where functionality mixing has grown over time

## Violation Categories

### Critical SRP Violations
- **God Classes**: Classes with excessive responsibilities and reasons to change
- **Manager Classes**: Classes that delegate without clear single purpose
- **Utility Classes**: Grab-bag classes mixing unrelated functionality
- **Data Classes**: Classes mixing data storage with business logic

### Moderate SRP Issues
- **Feature Envy**: Methods more interested in other classes than their own
- **Large Class**: Classes exceeding reasonable size limits
- **Long Parameter Lists**: Methods requiring too much external data
- **Divergent Change**: Classes changed for different reasons

### Subtle SRP Problems
- **Shotgun Surgery**: Changes requiring modifications in many classes
- **Message Chains**: Long chains of method calls indicating responsibility misplacement
- **Middle Man**: Classes that only delegate to other classes
- **Data Clumps**: Repeated groups of parameters suggesting missing abstractions

## Refactoring Strategies

### Extract Class Pattern
- **Responsibility Separation**: Split classes by identifying distinct responsibility families
- **Actor-Based Separation**: Create separate classes for each user group served
- **Cohesion Improvement**: Group highly related methods and fields together
- **Interface Extraction**: Define clear contracts between separated responsibilities

### Move Method Pattern
- **Method Placement**: Move methods to classes where they belong based on data usage
- **Responsibility Alignment**: Ensure methods serve the same actor as their containing class
- **Dependency Reduction**: Minimize dependencies between different responsibility areas
- **Encapsulation Enhancement**: Keep related data and behavior together

### Facade Pattern Application
- **Complexity Hiding**: Create simple interfaces for complex subsystems
- **Responsibility Coordination**: Coordinate between multiple responsibility-focused classes
- **Client Simplification**: Provide unified access to related functionality
- **Subsystem Decoupling**: Reduce dependencies between client code and implementation details

## Report Output

After completing the analysis, create a comprehensive markdown report file named `cleandesign-single-analysis.md` in the project's root directory containing:

### 1. Executive Summary
- **SRP Health Score** (0-100) with key metrics dashboard
- **Critical Violations Summary** requiring immediate attention (top 10)
- **Responsibility Distribution** across the codebase
- **Refactoring Priority Matrix** (high impact vs. low effort)

### 2. Class-by-Class SRP Assessment
- **Single Sentence Test Results**: Classes failing the description test
- **Responsibility Count**: Number of distinct reasons each class might change
- **Actor Mapping**: Which user groups each class serves
- **Cohesion Metrics**: High vs. low cohesion classification

### 3. Responsibility Analysis
- **Actor Identification**: Different user groups served by the system
- **Responsibility Families**: Groups of functions serving each actor
- **Cross-Actor Dependencies**: Cases where different actors share functionality
- **Change Impact Assessment**: How changes from one actor affect others

### 4. Cohesion Assessment Results
- **High Cohesion Classes**: Well-designed classes with strong internal relationships
- **Low Cohesion Classes**: Classes needing responsibility separation
- **Field-Method Correlation**: Detailed analysis of internal class relationships
- **Cohesion Improvement Opportunities**: Specific areas for refactoring

### 5. SRP Violations by Severity
- **Critical Issues** (multiple actors, god classes)
- **High Priority** (mixed responsibilities, low cohesion)
- **Medium Priority** (large classes, feature envy)
- **Low Priority** (minor responsibility leaks)

Each finding includes:
- File path and line numbers
- Class/method name and current responsibilities
- Specific SRP violation description
- Actor analysis and change impact
- Recommended refactoring approach with examples
- Complexity assessment and effort estimation

### 6. Refactoring Roadmap
- **Phase 1: Critical Separations** (god classes, multi-actor classes)
- **Phase 2: Cohesion Improvements** (extract class, move method)
- **Phase 3: Architecture Refinement** (facade patterns, interface extraction)

### 7. Design Patterns & Best Practices
- **Extract Class Examples**: Concrete refactoring examples for major violations
- **Interface Segregation**: How to separate different actor concerns
- **Facade Implementation**: Simplifying complex multi-class interactions
- **Dependency Injection**: Reducing coupling between separated responsibilities

### 8. Team Guidelines & Code Review
- **SRP Checklist**: Questions to ask during code reviews
- **Class Design Guidelines**: Standards for new class creation
- **Refactoring Standards**: Safe approaches for responsibility separation
- **Testing Strategy**: How to test single-responsibility classes

### 9. Quality Metrics & Monitoring
- **Cohesion Tracking**: Metrics for measuring class internal consistency
- **Responsibility Counting**: Methods for tracking class purpose clarity
- **Change Impact Analysis**: Measuring the blast radius of modifications
- **Actor Satisfaction**: Ensuring each user group's needs are well-served

### 10. Automated Detection Tools
- **Static Analysis Rules**: Configure tools to detect SRP violations
- **Code Metrics**: Cohesion and coupling measurements
- **Design Quality Gates**: Prevent new SRP violations in CI/CD
- **Refactoring Tools**: IDE support for safe responsibility separation

Focus on actionable insights that improve code maintainability, reduce change impact, and create more focused, cohesive classes. Emphasize the connection between responsibilities and real users/actors who request changes. Generate the report file immediately after analysis completion.