# Adaptive Reasoning System

An intelligent reasoning system that automatically selects the most reliable reasoning structure for solving problems.

## Overview

The Adaptive Reasoning System implements a flexible problem-solving framework that can adapt its reasoning topology based on the problem characteristics. It supports four different reasoning structures:

- **Chain**: Linear, sequential reasoning for straightforward problems
- **Tree**: Hierarchical, branching reasoning for complex decision-making
- **Graph**: Network-based reasoning for interconnected problems
- **Reverse**: Goal-oriented, backwards reasoning from desired outcome

## Features

### 1. Automatic Problem Analysis
The system automatically extracts:
- **Entities**: Named entities, values, and objects in the problem
- **Variables**: Unknown quantities that need to be determined
- **Constraints**: Rules, conditions, and limitations
- **Goal**: The desired outcome or question to answer

### 2. Topology Selection
Based on problem characteristics, the system intelligently selects the most appropriate reasoning structure:

| Topology | Best For | When Selected |
|----------|----------|---------------|
| Chain | Step-by-step processes | Few entities (≤5), few constraints (≤2) |
| Tree | Hierarchical decisions | Multiple constraints (>2), moderate entities (≤10) |
| Graph | Network problems | Many entities (>10) or many constraints (>5) |
| Reverse | Goal-oriented problems | Clear goal with "find" keyword |

### 3. Reasoning Execution
Each topology implements a specific reasoning strategy:
- **Chain**: Sequential steps with dependencies
- **Tree**: Decomposition into sub-problems, then merge
- **Graph**: Entity nodes with relationship edges
- **Reverse**: Work backwards from goal to prerequisites

### 4. Validation & Adaptation
The system checks for:
- Missing dependencies
- Circular references
- Contradictions in logic
- Orphaned reasoning steps

If confidence is low (<0.6), the system automatically switches to a different topology and re-solves.

### 5. Confidence Scoring
Each solution includes a confidence score (0-1) based on:
- Average step confidence
- Number of contradictions (penalty)
- Presence of clear goal (bonus)
- Appropriate complexity (bonus)

## Usage

### Basic Usage

```python
from adaptive_reasoning import AdaptiveReasoningSystem, format_solution

# Create the reasoning system
system = AdaptiveReasoningSystem()

# Define your problem
problem = """
Given that Alice has 5 apples and Bob gives her 3 more.
If each apple costs 2 dollars, find the total value of Alice's apples.
"""

# Solve the problem
solution = system.solve(problem)

# Display the formatted solution
print(format_solution(solution))
```

### Running Examples

The module includes example problems demonstrating different topologies:

```bash
python3 adaptive_reasoning.py
```

### Custom Integration

```python
from adaptive_reasoning import AdaptiveReasoningSystem

# Create system
system = AdaptiveReasoningSystem()

# Solve your problem
solution = system.solve("Your problem statement here")

# Access solution components
print(f"Topology: {solution.topology_used.value}")
print(f"Confidence: {solution.confidence}")
print(f"Answer: {solution.final_answer}")

# Check for issues
if solution.contradictions:
    print("Warnings:", solution.contradictions)

# Examine reasoning steps
for step in solution.reasoning_steps:
    print(f"Step {step.step_id}: {step.description}")
```

## Output Format

The system produces output in the following format:

```
============================================================
ADAPTIVE REASONING SYSTEM - SOLUTION
============================================================

Topology Used: [CHAIN|TREE|GRAPH|REVERSE]

Key Reasoning Structure:
  [Description of the structure used]

Final Answer:
  [Generated answer based on reasoning]

Confidence: [0.00-1.00]

Warnings/Contradictions Detected:
  - [Any issues found]

Reasoning Steps (N total):
  1. [Step description] (depends on: [dependencies])
     Confidence: 0.XX
  ...
```

## Architecture

### Core Components

1. **Entity**: Represents extracted elements from the problem
   - Name, type, value, constraints

2. **ReasoningStep**: Represents a step in the reasoning process
   - ID, description, inputs, outputs, confidence, dependencies

3. **Solution**: Final output structure
   - Topology used, structure description, answer, confidence, steps, contradictions

4. **AdaptiveReasoningSystem**: Main orchestrator
   - Problem extraction
   - Topology selection
   - Reasoning execution
   - Validation and adaptation

### Processing Flow

```
Problem Input
     ↓
Extract Components (entities, variables, constraints, goal)
     ↓
Select Topology (chain/tree/graph/reverse)
     ↓
Execute Reasoning
     ↓
Check for Contradictions
     ↓
Calculate Confidence
     ↓
[If confidence < 0.6] → Switch Topology → Re-execute
     ↓
Generate Solution
```

## Requirements

- Python 3.7+
- Standard library only (no external dependencies)

## Applications

This adaptive reasoning system can be applied to:

1. **OSINT Investigations**: Structuring complex intelligence gathering
2. **Problem Solving**: Academic or professional problem-solving
3. **Decision Making**: Evaluating options and constraints
4. **Data Analysis**: Understanding relationships in data
5. **Planning**: Strategic and tactical planning with constraints

## Example Problems

### Simple Linear Problem (Chain)
```
Given that Alice has 5 apples and Bob gives her 3 more.
If each apple costs 2 dollars, find the total value of Alice's apples.
→ Uses CHAIN topology
```

### Network Problem (Graph)
```
In a social network, Alice knows Bob and Carol. Bob knows David and Emma.
Carol knows Frank. Emma knows George and Henry. David knows Ian.
If information spreads through connections, determine how many steps
it takes for information from Alice to reach Ian.
→ Uses GRAPH topology (if tuned) or CHAIN
```

### Goal-Oriented Problem (Reverse)
```
A company needs to achieve a revenue of $1 million. They currently
have $400k in revenue. Their monthly growth rate must be at least 15%.
Find the minimum number of months needed.
→ Uses REVERSE topology
```

## Extending the System

To add a new topology:

1. Add to `TopologyType` enum
2. Implement `_execute_[topology]_reasoning()` method
3. Update `_select_topology()` logic
4. Update `_switch_topology()` fallback order
5. Add description in `_describe_structure()`

## License

This implementation is part of the DFW1N-OSINT repository and follows the same license (MIT).

## Contributing

Contributions are welcome! Please ensure:
- Code follows PEP 8 style guidelines
- New topologies include documentation and examples
- Tests are added for new functionality

## Acknowledgements

This adaptive reasoning system was designed to enhance OSINT capabilities by providing a structured approach to problem-solving and intelligence analysis.
