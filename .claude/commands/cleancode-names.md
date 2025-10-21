---
description: Comprehensive analysis of naming conventions using clean code principles
---

Perform a comprehensive analysis of naming conventions throughout this project based on clean code principles. Evaluate all identifiers for clarity, consistency, and maintainability.

## Analysis Scope
- **Source Files**: Scan all code files (.js, .ts, .jsx, .tsx, .py, .java, .cpp, .c, .go, .rs, .php, .rb, .cs, .swift, .kt, .scala, .clj, .ex, .dart, .lua, .r, .m, .pl, .sh, .sql, .html, .css, .scss, .less, etc.)
- **Identifiers**: Analyze variables, functions, classes, interfaces, constants, enums, modules, packages, and file names
- **Cross-Reference Analysis**: Check naming consistency across the entire codebase
- **Context Evaluation**: Assess names within their usage context and domain

## Naming Convention Rules Assessment

### 1. Intention Revelation
- Identify names that require comments to understand their purpose
- Flag unclear or ambiguous names
- Suggest more descriptive alternatives

### 2. Clarity Over Cleverness  
- Find "cute" or overly clever names that sacrifice clarity
- Identify abbreviations that could be spelled out
- Flag misleading or confusing names

### 3. Searchability
- Check for single-letter variables outside appropriate contexts (loops, short methods)
- Identify names that would be hard to search for
- Flag overly generic names like "data", "info", "temp"

### 4. Encoding Issues
- Detect Hungarian notation usage
- Find unnecessary prefixes or suffixes
- Identify type encoding in names

### 5. Consistency
- Check if same concepts use different names across files
- Identify inconsistent naming patterns
- Flag similar names with different meanings

### 6. Meaningful Distinctions
- Find names that differ only by number series (data1, data2)
- Identify noise words that don't add meaning
- Check for spelling variations of the same concept

### 7. Pronunciation
- Flag unpronounceable abbreviations
- Identify names with unclear pronunciation
- Suggest more readable alternatives

## Length Rules Analysis

### Methods & Classes
- **Public APIs**: Check if names are appropriately short and well-defined
- **Private methods**: Verify long, descriptive names for single-use functions
- **Scope-appropriate naming**: Ensure name length correlates with scope

### Variables & Parameters  
- **Global/Instance variables**: Check for descriptive, long names
- **Local variables**: Verify appropriate short names in limited scopes
- **Constants**: Ensure descriptive, self-explanatory names

## Grammar Rules Check
- **Classes/Objects**: Verify noun phrases, no verbs
- **Methods**: Check for verb phrases
- **Solution domain**: Identify proper use of CS/programming terms
- **Problem domain**: Check for business-appropriate terminology

## Report Output

After completing the analysis, create a comprehensive markdown report file named `cleancode-names-analysis.md` in the project's root directory containing:

### 1. Executive Summary
- **Overall Naming Health Score** (0-100) with breakdown by category
- **Project Statistics**: Total files scanned, identifiers analyzed, violations found
- **Critical Issues Summary**: Top 5 violations requiring immediate attention
- **Quality Distribution**: Excellent, good, needs improvement, critical categories

### 2. Naming Rules Assessment
   - **Intention Revelation Issues**: Names requiring comments or clarification
   - **Clarity Problems**: Clever/cute names that sacrifice readability
   - **Searchability Issues**: Hard-to-find names and overly generic terms
   - **Encoding Problems**: Hungarian notation and unnecessary prefixes
   - **Consistency Violations**: Same concepts with different names
   - **Distinction Issues**: Meaningless number series and noise words
   - **Pronunciation Problems**: Unpronounceable abbreviations

### 3. Length Rules Assessment
- **Scope-Inappropriate Naming**: Methods/classes with wrong name lengths for their scope
- **Variable Length Issues**: Variables/parameters not following scope-length correlation
- **Constant Naming Problems**: Constants lacking descriptive, self-explanatory names

### 4. Grammar Rules Evaluation
- **Class Naming Violations**: Classes using verbs instead of noun phrases
- **Method Naming Issues**: Methods not using appropriate verb phrases
- **Domain Terminology Problems**: Improper use of technical vs. business terms

### 5. Detailed Findings by Priority
- **Critical Issues** (immediate attention required)
- **High Priority** (significant impact on maintainability)
- **Medium Priority** (improvement opportunities)
- **Low Priority** (minor enhancements)

Each finding includes:
- File path and line numbers
- Current identifier and context
- Specific violation description
- Recommended replacement with justification
- Impact assessment and refactoring difficulty

### 6. Cross-File Consistency Analysis
- **Inconsistent Concept Naming**: Same concepts using different names
- **Pattern Violations**: Deviations from established naming patterns
- **Domain Mixing**: Inappropriate mixing of technical and business terminology

### 7. Refactoring Roadmap
- **Phase 1: Critical Naming Fixes** (high impact, low effort)
- **Phase 2: Consistency Improvements** (medium impact, medium effort)
- **Phase 3: Architectural Naming** (high impact, high effort)

### 8. Team Guidelines & Standards
- **Naming Conventions**: Project-specific naming standards based on findings
- **Code Review Checklist**: Naming-focused review criteria
- **Onboarding Guidelines**: Naming best practices for new team members

### 9. Automated Tooling Recommendations
- **Linting Rules**: Naming-specific lint configurations
- **IDE Settings**: Auto-formatting and naming suggestions
- **Pre-commit Hooks**: Automated naming validation

### 10. Quality Metrics & Tracking
- **Naming Health Baseline**: Current state measurements
- **Progress Tracking**: KPIs for naming improvements
- **Regular Assessment**: Schedule for ongoing naming quality reviews

Focus on actionable insights that improve code maintainability, readability, and team productivity. Generate the report file immediately after analysis completion.