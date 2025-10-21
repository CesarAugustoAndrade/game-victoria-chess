---
description: Comprehensive analysis of Objects vs Data Structures design principles and anti-symmetry patterns
---

Perform a comprehensive analysis of Objects vs Data Structures design throughout this project. Identify hybrid structures, evaluate data/object anti-symmetry patterns, assess appropriate use of objects vs data structures, and provide recommendations for proper abstraction levels.

## Analysis Scope
- **Source Files**: Scan all code files (.js, .ts, .jsx, .tsx, .py, .java, .cpp, .c, .go, .rs, .php, .rb, .cs, .swift, .kt, .scala, .clj, .ex, .dart, .lua, .r, .m, .pl, .sh, .sql, etc.)
- **Classes & Structures**: Analyze all classes, objects, data structures, and data containers
- **Design Patterns**: Evaluate object-oriented vs procedural programming approaches
- **Abstraction Levels**: Assess appropriate data exposure and encapsulation strategies

## Objects vs Data Structures Assessment

### 1. Object Classification Analysis
- **True Objects**: Classes that hide data behind abstractions and expose behavior-focused methods
- **Data Structures**: Classes that expose data and have minimal or no meaningful functions
- **Hybrid Structures**: Classes mixing object and data structure characteristics (anti-pattern)
- **Appropriate Usage**: Evaluate whether each class serves its intended purpose correctly

### 2. Data/Object Anti-Symmetry Evaluation
- **Object-Oriented Benefits**: Assess ease of adding new object types vs. new functions
- **Procedural Benefits**: Evaluate ease of adding new functions vs. new data types
- **Design Trade-offs**: Identify where each approach is most appropriate
- **Evolution Patterns**: Analyze how the codebase handles changes over time

### 3. Hybrid Structure Detection
- **Mixed Characteristics**: Find classes with both significant operations and public data access
- **Public Variables**: Identify objects with public fields that should be encapsulated
- **Accessor/Mutator Overuse**: Detect excessive getters/setters in behavioral classes
- **External Data Manipulation**: Find external functions treating objects as data structures

### 4. Abstraction Level Assessment
- **Data Exposure Quality**: Evaluate how data is exposed (concrete vs. abstract)
- **Implementation Detail Leakage**: Find cases where internal structure is exposed
- **Polymorphism Opportunities**: Identify missed abstraction opportunities
- **Interface Design**: Assess quality of public interfaces and abstractions

## Design Pattern Analysis

### Object-Oriented Patterns
- **Strategy Pattern**: Evaluate algorithm encapsulation and behavioral variation
- **Command Pattern**: Assess operation encapsulation and behavioral objects
- **State Pattern**: Check state-dependent behavior encapsulation
- **Template Method**: Analyze behavioral inheritance patterns

### Data Structure Patterns
- **Data Transfer Objects (DTOs)**: Evaluate pure data carriers for serialization/transport
- **Value Objects**: Assess immutable data containers with minimal behavior
- **Configuration Objects**: Check read-only data structures for settings
- **Record Types**: Evaluate simple data aggregation structures

### Anti-Pattern Detection
- **Anemic Domain Model**: Find domain objects with only getters/setters
- **Feature Envy**: Detect objects more interested in other objects' data
- **God Objects**: Identify objects trying to be both data structures and behavioral entities
- **Inappropriate Intimacy**: Find classes exposing too much internal structure

## Getter/Setter Analysis

### Appropriate Getter/Setter Usage
- **Data Structures**: Legitimate use in pure data containers
- **Framework Requirements**: Necessary for serialization/ORM frameworks
- **Value Objects**: Appropriate for immutable data access
- **Configuration Access**: Legitimate for read-only configuration data

### Inappropriate Getter/Setter Usage
- **Behavioral Objects**: Objects that should expose behavior, not data
- **Business Logic Bypass**: Getters/setters that circumvent proper encapsulation
- **Tell, Don't Ask Violations**: Data access patterns that should be behavioral methods
- **Implementation Exposure**: Getters/setters that leak internal structure

### Abstraction Quality Assessment
- **Concrete vs Abstract**: Evaluate level of abstraction in data exposure
- **Implementation Independence**: Check if interfaces depend on implementation details
- **Polymorphism Support**: Assess whether data exposure supports polymorphic behavior
- **Evolution Resilience**: Evaluate whether abstractions can handle future changes

## Procedural vs Object-Oriented Analysis

### Procedural Code Identification
- **Data + Services Pattern**: Find data structures with separate service classes
- **Function-Centric Design**: Identify code organized around functions rather than objects
- **External Data Manipulation**: Detect functions operating on external data structures
- **Stateless Service Classes**: Find classes that primarily contain static methods

### Object-Oriented Code Identification
- **Behavior-Centric Design**: Find code organized around object responsibilities
- **Encapsulated State**: Identify proper data hiding with behavioral interfaces
- **Message Passing**: Assess object-to-object communication patterns
- **Polymorphic Behavior**: Evaluate proper use of inheritance and interfaces

### Design Trade-off Analysis
- **Change Frequency**: Assess whether data types or functions change more often
- **Extension Patterns**: Evaluate whether new types or new operations are added more frequently
- **Business Domain**: Analyze whether the domain favors object-oriented or procedural approaches
- **Team Expertise**: Consider team familiarity with different paradigms

## Report Output

After completing the analysis, create a comprehensive markdown report file named `cleandesign-objects-analysis.md` in the project's root directory containing:

### 1. Executive Summary
- **Objects vs Data Structures Health Score** (0-100) with design quality metrics
- **Critical Issues Summary** requiring immediate attention (top 10)
- **Design Paradigm Distribution** (OO vs Procedural vs Hybrid)
- **Refactoring Priority Matrix** (impact vs. effort for hybrid elimination)

### 2. Object Classification Results
- **True Objects**: Well-designed behavioral classes with proper encapsulation
- **Pure Data Structures**: Legitimate data containers with minimal behavior
- **Hybrid Structures**: Problematic classes mixing objects and data structures
- **Misclassified Entities**: Classes serving the wrong purpose

### 3. Data/Object Anti-Symmetry Analysis
- **OO Advantages**: Areas where object-oriented design excels
- **Procedural Advantages**: Areas where procedural design is more appropriate
- **Evolution Patterns**: How the codebase handles adding new types vs. new functions
- **Design Consistency**: Whether the chosen approach is applied consistently

### 4. Hybrid Structure Assessment
- **Critical Hybrids**: Classes that are worst of both worlds
- **Behavioral Contamination**: Objects polluted with data structure characteristics
- **Data Structure Pollution**: Data structures contaminated with inappropriate behavior
- **Refactoring Opportunities**: Clear separation strategies for hybrid classes

### 5. Abstraction Quality Evaluation
- **Appropriate Abstractions**: Well-designed interfaces hiding implementation details
- **Abstraction Leaks**: Cases where implementation details are exposed
- **Polymorphism Opportunities**: Missed chances for polymorphic design
- **Interface Design Quality**: Assessment of public API design

### 6. Getter/Setter Usage Assessment
- **Legitimate Usage**: Appropriate use in data structures and value objects
- **Anti-Pattern Usage**: Inappropriate getters/setters in behavioral objects
- **Abstraction Violations**: Cases where getters/setters expose implementation details
- **Refactoring Recommendations**: Converting getters/setters to behavioral methods

### 7. Design Issues by Severity
- **Critical Issues** (hybrid structures, major abstraction violations)
- **High Priority** (inappropriate getter/setter usage, design inconsistencies)
- **Medium Priority** (missed polymorphism opportunities, minor abstraction leaks)
- **Low Priority** (naming improvements, documentation gaps)

Each finding includes:
- File path and line numbers
- Current implementation description
- Specific design issue explanation with examples
- Object vs data structure classification
- Recommended refactoring approach with before/after code
- Implementation complexity and effort estimation

### 8. Design Pattern Refactoring Roadmap
- **Phase 1: Hybrid Elimination** (separate objects from data structures)
- **Phase 2: Abstraction Improvement** (proper data hiding and behavior encapsulation)
- **Phase 3: Pattern Application** (appropriate use of OO and procedural patterns)

### 9. Objects vs Data Structures Strategy Guide
- **Decision Framework**: When to use objects vs. data structures
- **Hybrid Avoidance**: Strategies for preventing mixed designs
- **Abstraction Design**: Creating appropriate abstraction levels
- **Evolution Planning**: Preparing for future changes in types vs. functions

### 10. Paradigm-Specific Best Practices
- **Object-Oriented Guidelines**: Proper encapsulation and behavior design
- **Data Structure Guidelines**: Appropriate use of pure data containers
- **Interface Design**: Creating clean abstractions and APIs
- **Evolution Strategies**: Handling changes in object-oriented vs. procedural code

### 11. Quality Metrics & Monitoring
- **Encapsulation Quality**: Measuring data hiding effectiveness
- **Behavioral Cohesion**: Assessing how well behavior is encapsulated
- **Abstraction Stability**: Tracking interface changes over time
- **Design Consistency**: Monitoring adherence to chosen paradigms

### 12. Team Guidelines & Training
- **Design Decision Framework**: Criteria for choosing objects vs. data structures
- **Code Review Checklist**: Questions for identifying design issues
- **Refactoring Safety**: Safe approaches for paradigm improvements
- **Architecture Evolution**: Long-term strategies for design consistency

### 13. Anti-Pattern Prevention
- **Hybrid Structure Detection**: Early warning signs and prevention strategies
- **Abstraction Leak Prevention**: Maintaining proper encapsulation boundaries
- **Design Consistency**: Ensuring paradigm alignment across the codebase
- **Quality Gates**: Preventing design violations in new code

Focus on actionable insights that improve design clarity, eliminate hybrid structures, and promote appropriate use of objects vs. data structures. Emphasize the trade-offs between object-oriented and procedural approaches and provide clear guidance on when each is most appropriate. Generate the report file immediately after analysis completion.