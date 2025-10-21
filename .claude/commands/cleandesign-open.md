---
description: Comprehensive analysis of Open/Closed Principle (OCP) violations and extensibility improvements
---

Perform a comprehensive analysis of Open/Closed Principle (OCP) adherence throughout this project. Identify code that requires modification instead of extension for new functionality, assess abstraction layers, and provide refactoring recommendations for better extensibility.

## Analysis Scope
- **Source Files**: Scan all code files (.js, .ts, .jsx, .tsx, .py, .java, .cpp, .c, .go, .rs, .php, .rb, .cs, .swift, .kt, .scala, .clj, .ex, .dart, .lua, .r, .m, .pl, .sh, .sql, etc.)
- **Classes & Modules**: Analyze all classes, modules, functions, and architectural components
- **Extension Points**: Identify existing and missing extension mechanisms
- **Design Patterns**: Evaluate usage of extensibility patterns like Strategy, Template Method, and Plugin Architecture

## Open/Closed Principle Assessment

### 1. Shotgun Surgery Anti-Pattern Detection
- **Change Impact Analysis**: Identify areas where single feature changes require modifications across multiple files
- **Rigidity Assessment**: Find code changes that create ripple effects throughout the system
- **Modification Hotspots**: Locate classes that frequently require changes for new functionality
- **Coupling Issues**: Detect tight coupling that prevents extension without modification

### 2. Extension vs Modification Analysis
- **Open for Extension**: Identify areas that can be extended with new behavior without code changes
- **Closed for Modification**: Find existing code that should remain untouched when adding features
- **Abstraction Gaps**: Locate missing abstractions that force modification instead of extension
- **Binary Stability**: Assess if compiled/deployed code can remain unchanged when extending

### 3. Abstraction Layer Evaluation
- **API Design**: Evaluate module and component APIs for extensibility
- **Interface Completeness**: Check if interfaces provide sufficient extension points
- **Abstract Methods**: Identify appropriate use of abstract methods and virtual functions
- **Inheritance Hierarchies**: Assess class hierarchies for proper extensibility design

### 4. Extension Point Analysis
- **Virtual Methods**: Evaluate non-final methods that allow behavior override
- **Abstract Methods**: Check abstract method design for extension points
- **Interface Inheritance**: Assess interface-based extension mechanisms
- **Function Parameters**: Identify functions that accept behavior as parameters
- **Dependency Injection**: Evaluate setter-based and constructor-based extension points
- **Higher-Order Functions**: Check functional programming extension patterns

## Design Pattern Assessment

### Strategy Pattern Analysis
- **Algorithm Encapsulation**: Identify places where different algorithms should be interchangeable
- **Strategy Interface**: Evaluate existing strategy interfaces and missing opportunities
- **Context Isolation**: Check if clients are properly isolated from implementation details
- **Runtime Strategy Selection**: Assess dynamic strategy switching capabilities

### Template Method Pattern Analysis
- **Common Behavior**: Identify shared behavior that could use template methods
- **Abstract Step Definition**: Find operations that should be abstract in template hierarchies
- **Inheritance vs Delegation**: Evaluate when template method is preferred over strategy
- **Fixed Algorithm Structure**: Check for algorithms with invariant steps and variable implementations

### Plugin Architecture Pattern Analysis
- **Extension Points**: Identify architectural extension points for plugin systems
- **Plugin Contracts**: Evaluate interface definitions for plugin communication
- **Plugin Isolation**: Check if plugins can be developed and deployed independently
- **Configuration-Based Extension**: Assess configuration-driven extensibility mechanisms

### Factory Pattern Analysis
- **Object Creation**: Identify object creation that should be abstracted for extension
- **Type Registration**: Check for systems that should support dynamic type registration
- **Creation Logic**: Evaluate centralized vs distributed object creation patterns

## Violation Categories

### Critical OCP Violations
- **Shotgun Surgery**: Single changes requiring modifications across many files
- **Switch Statement Proliferation**: Type-checking code that grows with new types
- **Hard-Coded Dependencies**: Direct instantiation preventing extension
- **Monolithic Classes**: Large classes mixing multiple concerns without extension points

### Moderate OCP Issues
- **Missing Abstractions**: Concrete implementations where interfaces should exist
- **Tight Coupling**: Direct dependencies that prevent substitution
- **Configuration Rigidity**: Hard-coded values that should be configurable
- **Limited Polymorphism**: Missed opportunities for polymorphic behavior

### Subtle OCP Problems
- **Incomplete Interfaces**: Interfaces that don't provide sufficient extension points
- **Leaky Abstractions**: Abstractions that expose implementation details
- **Extension Limitations**: Systems that support some extensions but not others
- **Over-Specification**: Interfaces that are too specific for general extension

## Strategic OCP Application

### Change Prediction Analysis
- **Product Backlog Review**: Analyze planned features for extension requirements
- **Historical Change Patterns**: Identify recurring modification patterns
- **Business Domain Evolution**: Assess likely areas of business rule changes
- **Technology Evolution**: Consider technological changes requiring extensions

### Continuous Refactoring Assessment
- **First-Time Changes**: Identify areas experiencing first-time modifications
- **Recurring Modifications**: Find patterns of repeated changes in same directions
- **Refactoring Opportunities**: Locate code that should be refactored for future extensions
- **Technical Debt**: Assess accumulated rigidity from modification-based changes

### Over-Design Risk Evaluation
- **Abstraction Cost**: Evaluate complexity cost of current abstractions
- **YAGNI Violations**: Identify over-engineered extension points that aren't used
- **Simplicity Balance**: Assess balance between extensibility and simplicity
- **Maintenance Overhead**: Evaluate ongoing cost of abstraction layers

## Report Output

After completing the analysis, create a comprehensive markdown report file named `cleandesign-open-analysis.md` in the project's root directory containing:

### 1. Executive Summary
- **OCP Health Score** (0-100) with extensibility metrics dashboard
- **Critical Violations Summary** requiring immediate attention (top 10)
- **Extension Capability Assessment** across major system components
- **Refactoring Priority Matrix** (change frequency vs. modification impact)

### 2. Shotgun Surgery Analysis
- **Multi-File Change Patterns**: Changes that affect multiple files simultaneously
- **Ripple Effect Mapping**: How changes propagate through the system
- **Modification Hotspots**: Classes and modules that change most frequently
- **Coupling Dependencies**: Relationships that create modification chains

### 3. Extension Point Assessment
- **Existing Extension Mechanisms**: Current ways the system supports extension
- **Missing Extension Points**: Areas that should support extension but don't
- **Extension Point Quality**: Evaluation of existing extension interfaces
- **Architectural Extensibility**: System-level extension capabilities

### 4. Design Pattern Implementation
- **Strategy Pattern Opportunities**: Where algorithm variation should use strategy
- **Template Method Applications**: Common behaviors that need template methods
- **Plugin Architecture Potential**: Components that could benefit from plugin systems
- **Factory Pattern Needs**: Object creation that should be abstracted

### 5. OCP Violations by Severity
- **Critical Issues** (shotgun surgery, hard-coded dependencies)
- **High Priority** (missing abstractions, tight coupling)
- **Medium Priority** (incomplete interfaces, configuration rigidity)
- **Low Priority** (minor extension limitations, over-specification)

Each finding includes:
- File path and line numbers
- Current implementation description
- Specific OCP violation explanation
- Change impact analysis and risk assessment
- Recommended refactoring approach with examples
- Implementation effort and complexity estimation

### 6. Abstraction Strategy Roadmap
- **Phase 1: Critical Extensions** (eliminate shotgun surgery patterns)
- **Phase 2: Strategic Abstractions** (implement key extension points)
- **Phase 3: Architectural Enhancement** (plugin systems, advanced patterns)

### 7. Extension Pattern Implementation Guide
- **Strategy Pattern Examples**: Concrete implementations for identified opportunities
- **Template Method Designs**: Abstract class hierarchies for common behaviors
- **Plugin Architecture**: Extension point design and plugin contracts
- **Interface Segregation**: Focused interfaces for specific extension needs

### 8. Change Management Strategy
- **Continuous Refactoring Plan**: Approach for ongoing OCP improvements
- **Change Prediction Methods**: Techniques for anticipating extension needs
- **Risk Assessment**: Evaluating when to invest in abstraction vs. simple solutions
- **Stakeholder Communication**: Explaining extensibility benefits to business stakeholders

### 9. Quality Metrics & Monitoring
- **Extensibility Metrics**: Measurements for tracking OCP adherence
- **Change Impact Tracking**: Monitoring how changes affect system stability
- **Abstraction ROI**: Measuring return on investment for abstraction layers
- **Extension Usage Analytics**: Tracking which extension points are actually used

### 10. Team Guidelines & Best Practices
- **OCP Code Review Checklist**: Questions to ask during code reviews
- **Extension Design Guidelines**: Standards for creating extension points
- **Refactoring Standards**: Safe approaches for improving extensibility
- **Training Recommendations**: Skills development for OCP application

### 11. Tool Integration & Automation
- **Static Analysis Rules**: Configure tools to detect OCP violations
- **Architecture Testing**: Automated tests for extension point integrity
- **Refactoring Tools**: IDE support for safe extensibility improvements
- **CI/CD Integration**: Quality gates for extensibility requirements

### 12. Strategic Decision Framework
- **Extension Investment Criteria**: When to invest in abstraction vs. simple solutions
- **Business Value Assessment**: Connecting extensibility to business outcomes
- **Technical Debt Management**: Balancing OCP improvements with delivery pressure
- **Long-term Architecture Vision**: Planning extensible system evolution

Focus on actionable insights that improve system flexibility, reduce change costs, and enable sustainable feature development. Emphasize the strategic nature of OCP application and provide clear guidance on when and where to invest in extensibility. Generate the report file immediately after analysis completion.