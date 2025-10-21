---
description: Comprehensive analysis of Tell, Don't Ask Principle violations and object-oriented design improvements
---

Perform a comprehensive analysis of Tell, Don't Ask Principle adherence throughout this project. Identify procedural code patterns, data exposure issues, anemic domain models, and provide refactoring recommendations for better object-oriented design.

## Analysis Scope
- **Source Files**: Scan all code files (.js, .ts, .jsx, .tsx, .py, .java, .cpp, .c, .go, .rs, .php, .rb, .cs, .swift, .kt, .scala, .clj, .ex, .dart, .lua, .r, .m, .pl, .sh, .sql, etc.)
- **Classes & Objects**: Analyze all classes, objects, and data structures
- **Method Calls**: Examine patterns of data access vs. behavior delegation
- **Encapsulation**: Assess data hiding and behavior encapsulation quality

## Tell, Don't Ask Principle Assessment

### 1. Procedural vs Object-Oriented Code Analysis
- **Information Gathering Patterns**: Identify code that gets information then makes decisions
- **Decision-Making Location**: Find where business logic operates on external object data
- **Message Passing**: Evaluate proper object-to-object communication patterns
- **Behavior Delegation**: Check if objects tell other objects what to do vs. asking for data

### 2. Data Exposure Detection
- **Getter/Setter Overuse**: Identify excessive use of accessor methods
- **Public Data Members**: Find public fields that should be encapsulated
- **Data Structure Leakage**: Detect internal data structures exposed to clients
- **State Interrogation**: Locate patterns where objects are queried for state information

### 3. Anemic Domain Model Analysis
- **Behavior-less Classes**: Identify classes that are primarily data containers
- **Getter/Setter Dominance**: Find classes with mostly accessor methods
- **External Logic Concentration**: Locate business logic operating on anemic objects
- **Data-Procedure Separation**: Detect where data and operations are artificially separated

### 4. Encapsulation Violations
- **Direct State Access**: Find direct manipulation of object internal state
- **Inappropriate Intimacy**: Identify classes that know too much about others' internals
- **Feature Envy**: Detect methods more interested in other classes' data
- **Temporal Coupling**: Find operations that must be called in specific sequences

## Violation Categories

### Critical Tell, Don't Ask Violations
- **Train Wrecks**: Long chains of method calls traversing object graphs (obj.getA().getB().getC())
- **Anemic Domain Models**: Classes with no behavior, only getters/setters
- **External Business Logic**: Domain logic implemented outside domain objects
- **State Interrogation**: Complex conditional logic based on object state queries

### Moderate Violations
- **Excessive Getters**: Classes with more getters than behavioral methods
- **Data Exposure**: Internal data structures accessible to external classes
- **Procedural Methods**: Methods that gather data from multiple objects then process
- **Inappropriate Delegation**: Objects asking others to perform operations they should do themselves

### Subtle Violations
- **Property-Based Logic**: Business decisions based on object properties
- **State-Dependent Behavior**: External control of object behavior based on state
- **Indirect Data Access**: Accessing data through multiple intermediary objects
- **Primitive Obsession**: Using primitives instead of meaningful object types

## Object-Oriented Design Patterns

### Command Pattern Analysis
- **Action Encapsulation**: Identify where commands should encapsulate operations
- **Request as Object**: Find places where requests should be objectified
- **Undo Operations**: Evaluate support for reversible operations
- **Macro Commands**: Check for composite command opportunities

### Strategy Pattern for Behavior
- **Conditional Logic**: Find switch/if statements that should use strategy objects
- **Algorithm Variation**: Identify varying algorithms that should be encapsulated
- **Runtime Behavior**: Check for behavior that changes at runtime
- **Policy Objects**: Evaluate need for policy-based decision making

### State Pattern Applications
- **State-Dependent Behavior**: Find objects with behavior varying by state
- **State Machines**: Identify implicit state machines that should be explicit
- **Conditional Complexity**: Locate complex state-based conditional logic
- **State Transitions**: Check for proper state change management

### Factory Pattern for Creation
- **Object Creation Logic**: Find complex object creation that should be encapsulated
- **Type-Based Creation**: Identify creation patterns based on type parameters
- **Configuration-Based Creation**: Check for objects created from configuration
- **Family Creation**: Evaluate related object creation patterns

## Refactoring Strategies

### Move Method Pattern
- **Data Usage Analysis**: Move methods to classes where they use most data
- **Behavior Relocation**: Place operations with the data they manipulate
- **Responsibility Alignment**: Ensure methods belong to appropriate classes
- **Coupling Reduction**: Minimize data access across class boundaries

### Extract Method for Behavior
- **Local Operations**: Extract operations that work on local data
- **Cohesion Improvement**: Group related operations together
- **Complexity Reduction**: Break down complex procedural methods
- **Reusability Enhancement**: Create reusable behavioral methods

### Replace Getter with Method
- **Calculated Properties**: Replace getters with meaningful behavioral methods
- **Business Operations**: Convert data access into business operations
- **State Queries**: Transform state checks into behavioral queries
- **Intention Revealing**: Make method names express business intent

### Introduce Parameter Object
- **Data Clumps**: Group related parameters into meaningful objects
- **Primitive Parameters**: Replace primitive parameters with rich objects
- **Parameter Reduction**: Reduce long parameter lists with objects
- **Behavior Addition**: Add behavior to parameter objects

## Design Quality Assessment

### Encapsulation Quality
- **Data Hiding**: Evaluate how well internal data is protected
- **Interface Design**: Assess quality of public interfaces
- **Abstraction Level**: Check appropriate abstraction levels
- **Information Hiding**: Verify implementation details are hidden

### Cohesion Analysis
- **Class Cohesion**: Measure how well class members work together
- **Method Cohesion**: Evaluate single responsibility within methods
- **Data-Behavior Relationship**: Check alignment between data and operations
- **Functional Cohesion**: Assess focus on single, well-defined tasks

### Coupling Assessment
- **Data Coupling**: Measure dependencies through data sharing
- **Control Coupling**: Identify control flow dependencies
- **Content Coupling**: Find inappropriate access to internal details
- **Interface Coupling**: Evaluate dependencies through interfaces

## Report Output

After completing the analysis, create a comprehensive markdown report file named `cleandesign-tell-analysis.md` in the project's root directory containing:

### 1. Executive Summary
- **Tell, Don't Ask Health Score** (0-100) with object-oriented design metrics
- **Critical Violations Summary** requiring immediate attention (top 10)
- **Procedural vs OO Code Ratio** across the codebase
- **Refactoring Priority Matrix** (coupling impact vs. effort required)

### 2. Procedural Code Analysis
- **Information-Decision Patterns**: Code that gathers data then makes decisions
- **External Logic Concentration**: Business logic outside domain objects
- **Data-Centric Operations**: Methods that primarily manipulate external data
- **Control Flow Dependencies**: Inappropriate control coupling between objects

### 3. Data Exposure Assessment
- **Getter/Setter Analysis**: Classes with excessive accessor methods
- **Public Data Members**: Fields that should be encapsulated
- **Data Structure Leakage**: Internal structures exposed to clients
- **State Interrogation Patterns**: Objects queried for state information

### 4. Anemic Domain Model Detection
- **Behavior-less Classes**: Classes serving as data containers only
- **Logic Distribution**: Where business logic resides vs. where it should be
- **Data-Procedure Separation**: Artificial separation of data and operations
- **Rich Domain Opportunities**: Places where behavior should be added

### 5. Encapsulation Violations
- **Direct State Access**: External manipulation of object internals
- **Inappropriate Intimacy**: Classes knowing too much about others
- **Feature Envy**: Methods more interested in other classes' data
- **Train Wreck Patterns**: Long method call chains traversing object graphs

### 6. Tell, Don't Ask Violations by Severity
- **Critical Issues** (anemic models, train wrecks, external business logic)
- **High Priority** (excessive getters, data exposure, procedural methods)
- **Medium Priority** (property-based logic, state interrogation)
- **Low Priority** (minor encapsulation issues, primitive obsession)

Each finding includes:
- File path and line numbers
- Current implementation description
- Specific violation explanation with examples
- Object-oriented design impact assessment
- Recommended refactoring approach with before/after code
- Implementation complexity and effort estimation

### 7. Object-Oriented Refactoring Roadmap
- **Phase 1: Critical Behavior Movement** (eliminate anemic models)
- **Phase 2: Data Encapsulation** (hide internal state, add behavior)
- **Phase 3: Design Pattern Application** (strategy, command, state patterns)

### 8. Design Pattern Implementation Guide
- **Move Method Examples**: Concrete refactoring for behavior placement
- **Command Pattern Applications**: Encapsulating operations as objects
- **Strategy Pattern Implementations**: Replacing conditional logic with objects
- **State Pattern Usage**: Managing state-dependent behavior properly

### 9. Encapsulation Best Practices
- **Interface Design Guidelines**: Creating meaningful object interfaces
- **Data Hiding Strategies**: Protecting internal object state
- **Behavior Encapsulation**: Keeping data and operations together
- **Abstraction Techniques**: Providing appropriate abstraction levels

### 10. Quality Metrics & Monitoring
- **Cohesion Measurements**: Tracking class and method cohesion
- **Coupling Analysis**: Monitoring dependencies between classes
- **Behavioral Method Ratio**: Measuring behavior vs. accessor methods
- **Encapsulation Quality**: Assessing data hiding effectiveness

### 11. Code Review Guidelines
- **Tell, Don't Ask Checklist**: Questions for code review sessions
- **Object-Oriented Design Standards**: Guidelines for proper OO design
- **Refactoring Safety**: Safe approaches for behavior movement
- **Design Quality Gates**: Preventing procedural code introduction

### 12. Team Training & Best Practices
- **Object-Oriented Thinking**: Shifting from procedural to OO mindset
- **Behavior Identification**: Recognizing where behavior belongs
- **Encapsulation Techniques**: Proper data hiding and behavior placement
- **Message Passing Patterns**: Effective object communication strategies

Focus on actionable insights that improve object-oriented design quality, enhance encapsulation, and promote proper behavior placement. Emphasize the shift from procedural thinking to object-oriented message passing. Generate the report file immediately after analysis completion.