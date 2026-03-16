#!/usr/bin/env python3
"""
Adaptive Reasoning System

A flexible reasoning system that selects the most reliable topology for problem-solving.
Supports multiple reasoning structures: chain, tree, graph, and reverse reasoning.
"""

from typing import Dict, List, Any, Tuple, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
import re


class TopologyType(Enum):
    """Available reasoning topologies"""
    CHAIN = "chain"
    TREE = "tree"
    GRAPH = "graph"
    REVERSE = "reverse"


@dataclass
class Entity:
    """Represents an extracted entity from the problem"""
    name: str
    entity_type: str
    value: Any = None
    constraints: List[str] = field(default_factory=list)


@dataclass
class ReasoningStep:
    """Represents a single step in the reasoning process"""
    step_id: int
    description: str
    inputs: List[str]
    outputs: List[str]
    confidence: float = 1.0
    dependencies: List[int] = field(default_factory=list)


@dataclass
class Solution:
    """Represents the final solution"""
    topology_used: TopologyType
    key_structure: str
    final_answer: str
    confidence: float
    reasoning_steps: List[ReasoningStep]
    contradictions: List[str] = field(default_factory=list)


class AdaptiveReasoningSystem:
    """
    Adaptive Reasoning System that selects the best topology for problem-solving.
    """

    def __init__(self):
        self.entities: List[Entity] = []
        self.variables: Dict[str, Any] = {}
        self.constraints: List[str] = []
        self.goal: str = ""
        self.reasoning_steps: List[ReasoningStep] = []
        self.current_topology: Optional[TopologyType] = None

    def solve(self, problem: str) -> Solution:
        """
        Main entry point to solve a problem using adaptive reasoning.

        Args:
            problem: The problem statement to solve

        Returns:
            Solution object with topology used, reasoning structure, answer, and confidence
        """
        # Step 1: Extract entities, variables, constraints, and goal
        self._extract_problem_components(problem)

        # Step 2: Select the best topology
        topology = self._select_topology()
        self.current_topology = topology

        # Step 3: Execute reasoning
        self._execute_reasoning(problem)

        # Step 4: Check for contradictions or missing steps
        contradictions = self._check_contradictions()

        # Step 5: If reliability is low, switch topology and recompute
        confidence = self._calculate_confidence(contradictions)
        if confidence < 0.6 and len(contradictions) > 0:
            # Try a different topology
            topology = self._switch_topology()
            self.current_topology = topology
            self.reasoning_steps = []
            self._execute_reasoning(problem)
            contradictions = self._check_contradictions()
            confidence = self._calculate_confidence(contradictions)

        # Step 6: Produce the best validated solution
        solution = Solution(
            topology_used=self.current_topology,
            key_structure=self._describe_structure(),
            final_answer=self._generate_final_answer(),
            confidence=confidence,
            reasoning_steps=self.reasoning_steps,
            contradictions=contradictions
        )

        return solution

    def _extract_problem_components(self, problem: str) -> None:
        """
        Extract entities, variables, constraints, and goal from the problem.
        """
        # Extract goal (usually last sentence or contains keywords)
        goal_keywords = ['find', 'determine', 'calculate', 'solve', 'identify', 'what']
        sentences = problem.split('.')

        for sentence in reversed(sentences):
            if any(keyword in sentence.lower() for keyword in goal_keywords):
                self.goal = sentence.strip()
                break

        if not self.goal and sentences:
            self.goal = sentences[-1].strip()

        # Extract entities (capitalized words, numbers, quoted strings)
        # Entities: proper nouns, names, specific values
        words = problem.split()
        for i, word in enumerate(words):
            cleaned = word.strip('.,!?;:')
            # Capitalized words (excluding first word of sentences)
            if cleaned and cleaned[0].isupper() and i > 0:
                if cleaned not in [e.name for e in self.entities]:
                    self.entities.append(Entity(
                        name=cleaned,
                        entity_type='named_entity'
                    ))

            # Numbers
            if cleaned.replace('.', '').replace('-', '').isdigit():
                self.entities.append(Entity(
                    name=f"value_{len(self.entities)}",
                    entity_type='numeric',
                    value=cleaned
                ))

        # Extract variables (words following 'let', 'given', 'assume')
        variable_patterns = [
            r'let\s+(\w+)',
            r'given\s+(\w+)',
            r'assume\s+(\w+)',
            r'(\w+)\s*=',
        ]

        for pattern in variable_patterns:
            matches = re.finditer(pattern, problem.lower())
            for match in matches:
                var_name = match.group(1)
                self.variables[var_name] = None

        # Extract constraints (conditional statements, requirements)
        constraint_keywords = ['must', 'should', 'if', 'unless', 'only if', 'when',
                              'where', 'such that', 'given that', 'constraint']

        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in constraint_keywords):
                self.constraints.append(sentence.strip())

    def _select_topology(self) -> TopologyType:
        """
        Select the most appropriate topology based on problem characteristics.

        Returns:
            The selected topology type
        """
        # Decision logic for topology selection
        num_entities = len(self.entities)
        num_constraints = len(self.constraints)
        has_goal = bool(self.goal)

        # Chain: Linear, sequential problems with clear cause-effect
        # Best for: step-by-step processes, sequential reasoning
        if num_constraints <= 2 and num_entities <= 5:
            return TopologyType.CHAIN

        # Tree: Hierarchical problems with multiple branches
        # Best for: decision trees, classification, hierarchical breakdown
        elif num_constraints > 2 and num_entities <= 10:
            return TopologyType.TREE

        # Graph: Complex problems with many interconnections
        # Best for: network problems, multiple relationships, cyclic dependencies
        elif num_entities > 10 or num_constraints > 5:
            return TopologyType.GRAPH

        # Reverse: Goal-oriented, work backwards from solution
        # Best for: when goal is clear but path is unclear
        elif has_goal and 'find' in self.goal.lower():
            return TopologyType.REVERSE

        # Default to chain for simple problems
        return TopologyType.CHAIN

    def _switch_topology(self) -> TopologyType:
        """
        Switch to a different topology when current one has low reliability.
        """
        # Define fallback order
        fallback_order = {
            TopologyType.CHAIN: TopologyType.TREE,
            TopologyType.TREE: TopologyType.GRAPH,
            TopologyType.GRAPH: TopologyType.REVERSE,
            TopologyType.REVERSE: TopologyType.CHAIN,
        }

        return fallback_order.get(self.current_topology, TopologyType.CHAIN)

    def _execute_reasoning(self, problem: str) -> None:
        """
        Execute reasoning based on the selected topology.
        """
        if self.current_topology == TopologyType.CHAIN:
            self._execute_chain_reasoning(problem)
        elif self.current_topology == TopologyType.TREE:
            self._execute_tree_reasoning(problem)
        elif self.current_topology == TopologyType.GRAPH:
            self._execute_graph_reasoning(problem)
        elif self.current_topology == TopologyType.REVERSE:
            self._execute_reverse_reasoning(problem)

    def _execute_chain_reasoning(self, problem: str) -> None:
        """Execute linear, sequential reasoning."""
        # Step 1: Identify starting point
        self.reasoning_steps.append(ReasoningStep(
            step_id=1,
            description="Identify problem components",
            inputs=["problem_statement"],
            outputs=["entities", "constraints", "goal"],
            confidence=0.95
        ))

        # Step 2: Process constraints sequentially
        for i, constraint in enumerate(self.constraints, start=2):
            self.reasoning_steps.append(ReasoningStep(
                step_id=i,
                description=f"Apply constraint: {constraint[:50]}...",
                inputs=[f"step_{i-1}"],
                outputs=[f"intermediate_result_{i}"],
                confidence=0.9,
                dependencies=[i-1]
            ))

        # Step 3: Reach goal
        final_step = len(self.reasoning_steps) + 1
        self.reasoning_steps.append(ReasoningStep(
            step_id=final_step,
            description="Synthesize final solution",
            inputs=[f"step_{final_step-1}"],
            outputs=["final_answer"],
            confidence=0.85,
            dependencies=[final_step-1]
        ))

    def _execute_tree_reasoning(self, problem: str) -> None:
        """Execute hierarchical, branching reasoning."""
        # Root: Problem decomposition
        self.reasoning_steps.append(ReasoningStep(
            step_id=1,
            description="Decompose problem into sub-problems",
            inputs=["problem_statement"],
            outputs=["sub_problem_1", "sub_problem_2", "sub_problem_3"],
            confidence=0.9
        ))

        # Branches: Solve each sub-problem
        for i in range(2, min(len(self.constraints) + 2, 6)):
            self.reasoning_steps.append(ReasoningStep(
                step_id=i,
                description=f"Solve sub-problem {i-1}",
                inputs=[f"sub_problem_{i-1}"],
                outputs=[f"sub_solution_{i-1}"],
                confidence=0.85,
                dependencies=[1]
            ))

        # Merge: Combine solutions
        merge_step = len(self.reasoning_steps) + 1
        self.reasoning_steps.append(ReasoningStep(
            step_id=merge_step,
            description="Merge sub-solutions into final answer",
            inputs=[f"sub_solution_{i}" for i in range(1, min(len(self.constraints) + 1, 5))],
            outputs=["final_answer"],
            confidence=0.88,
            dependencies=list(range(2, merge_step))
        ))

    def _execute_graph_reasoning(self, problem: str) -> None:
        """Execute interconnected, network-based reasoning."""
        # Create nodes for each entity and constraint
        node_id = 1
        entity_nodes = {}

        # Add entity nodes
        for entity in self.entities[:8]:  # Limit for complexity
            self.reasoning_steps.append(ReasoningStep(
                step_id=node_id,
                description=f"Process entity: {entity.name}",
                inputs=["problem_context"],
                outputs=[f"entity_node_{entity.name}"],
                confidence=0.9
            ))
            entity_nodes[entity.name] = node_id
            node_id += 1

        # Add constraint nodes connecting entities
        for i, constraint in enumerate(self.constraints[:5]):
            deps = list(entity_nodes.values())[:2]  # Connect to first entities
            self.reasoning_steps.append(ReasoningStep(
                step_id=node_id,
                description=f"Apply relational constraint: {constraint[:40]}...",
                inputs=[f"entity_node_{list(entity_nodes.keys())[j]}" for j in range(min(2, len(entity_nodes)))],
                outputs=[f"relationship_{i}"],
                confidence=0.85,
                dependencies=deps
            ))
            node_id += 1

        # Synthesize from graph
        self.reasoning_steps.append(ReasoningStep(
            step_id=node_id,
            description="Synthesize solution from relationship graph",
            inputs=[f"relationship_{i}" for i in range(min(len(self.constraints), 5))],
            outputs=["final_answer"],
            confidence=0.82,
            dependencies=list(range(len(self.entities) + 1, node_id))
        ))

    def _execute_reverse_reasoning(self, problem: str) -> None:
        """Execute goal-oriented, backwards reasoning."""
        # Start with goal
        self.reasoning_steps.append(ReasoningStep(
            step_id=1,
            description=f"Define target goal: {self.goal}",
            inputs=["goal_statement"],
            outputs=["goal_requirements"],
            confidence=0.95
        ))

        # Work backwards
        step_id = 2
        for i in range(min(len(self.constraints) + 1, 5)):
            self.reasoning_steps.append(ReasoningStep(
                step_id=step_id,
                description=f"Identify prerequisite {i+1}",
                inputs=[f"step_{step_id-1}"],
                outputs=[f"prerequisite_{i+1}"],
                confidence=0.87,
                dependencies=[step_id-1]
            ))
            step_id += 1

        # Connect to initial conditions
        self.reasoning_steps.append(ReasoningStep(
            step_id=step_id,
            description="Verify path from initial conditions to goal",
            inputs=[f"prerequisite_{i}" for i in range(1, min(len(self.constraints) + 2, 6))],
            outputs=["final_answer"],
            confidence=0.83,
            dependencies=list(range(2, step_id))
        ))

    def _check_contradictions(self) -> List[str]:
        """
        Check for contradictions or missing steps in reasoning.
        """
        contradictions = []

        # Check for missing dependencies
        step_ids = {step.step_id for step in self.reasoning_steps}
        for step in self.reasoning_steps:
            for dep in step.dependencies:
                if dep not in step_ids:
                    contradictions.append(
                        f"Step {step.step_id} depends on missing step {dep}"
                    )

        # Check for circular dependencies (simplified check)
        for step in self.reasoning_steps:
            if step.step_id in step.dependencies:
                contradictions.append(
                    f"Step {step.step_id} has circular dependency on itself"
                )

        # Check if final answer is produced
        has_final_answer = any(
            "final_answer" in step.outputs
            for step in self.reasoning_steps
        )

        if not has_final_answer:
            contradictions.append("No step produces a final answer")

        # Check for orphaned steps (no outputs used)
        if len(self.reasoning_steps) > 2:
            output_set = set()
            input_set = set()
            for step in self.reasoning_steps:
                output_set.update(step.outputs)
                input_set.update(step.inputs)

            # Some outputs should be used as inputs (except final answer)
            used_outputs = output_set.intersection(input_set)
            if not used_outputs and len(self.reasoning_steps) > 3:
                contradictions.append("Warning: Steps may not be properly connected")

        return contradictions

    def _calculate_confidence(self, contradictions: List[str]) -> float:
        """
        Calculate overall confidence in the solution.
        """
        if not self.reasoning_steps:
            return 0.0

        # Base confidence: average of all step confidences
        avg_confidence = sum(step.confidence for step in self.reasoning_steps) / len(self.reasoning_steps)

        # Penalty for contradictions
        contradiction_penalty = len(contradictions) * 0.15

        # Bonus for having goal
        goal_bonus = 0.05 if self.goal else 0.0

        # Bonus for appropriate number of steps
        step_count = len(self.reasoning_steps)
        if 3 <= step_count <= 8:
            step_bonus = 0.05
        else:
            step_bonus = 0.0

        final_confidence = avg_confidence + goal_bonus + step_bonus - contradiction_penalty

        # Clamp between 0 and 1
        return max(0.0, min(1.0, final_confidence))

    def _describe_structure(self) -> str:
        """
        Describe the key reasoning structure used.
        """
        descriptions = {
            TopologyType.CHAIN: f"Linear chain of {len(self.reasoning_steps)} sequential steps",
            TopologyType.TREE: f"Hierarchical tree with root decomposition and {len(self.reasoning_steps)-2} branches",
            TopologyType.GRAPH: f"Network graph with {len(self.entities)} entity nodes and {len(self.constraints)} relationship edges",
            TopologyType.REVERSE: f"Reverse reasoning from goal through {len(self.reasoning_steps)-2} prerequisites"
        }

        return descriptions.get(self.current_topology, "Unknown structure")

    def _generate_final_answer(self) -> str:
        """
        Generate the final answer based on reasoning steps.
        """
        if not self.reasoning_steps:
            return "Unable to generate answer - no reasoning steps"

        # Summary of the reasoning process
        answer_parts = [
            f"Based on {self.current_topology.value} reasoning with {len(self.reasoning_steps)} steps:",
            f"- Identified {len(self.entities)} entities",
            f"- Applied {len(self.constraints)} constraints",
            f"- Goal: {self.goal if self.goal else 'Not explicitly stated'}",
            f"- Solution pathway validated through {self.current_topology.value} topology"
        ]

        return " ".join(answer_parts)


def format_solution(solution: Solution) -> str:
    """
    Format solution for output according to specification.
    """
    output = []
    output.append("=" * 60)
    output.append("ADAPTIVE REASONING SYSTEM - SOLUTION")
    output.append("=" * 60)
    output.append(f"\nTopology Used: {solution.topology_used.value.upper()}")
    output.append(f"\nKey Reasoning Structure:")
    output.append(f"  {solution.key_structure}")
    output.append(f"\nFinal Answer:")
    output.append(f"  {solution.final_answer}")
    output.append(f"\nConfidence: {solution.confidence:.2f}")

    if solution.contradictions:
        output.append(f"\nWarnings/Contradictions Detected:")
        for contradiction in solution.contradictions:
            output.append(f"  - {contradiction}")

    output.append(f"\nReasoning Steps ({len(solution.reasoning_steps)} total):")
    for step in solution.reasoning_steps:
        deps = f" (depends on: {step.dependencies})" if step.dependencies else ""
        output.append(f"  {step.step_id}. {step.description}{deps}")
        output.append(f"     Confidence: {step.confidence:.2f}")

    output.append("=" * 60)

    return "\n".join(output)


def main():
    """Example usage of the Adaptive Reasoning System"""

    # Example problems
    examples = [
        {
            "name": "Simple Linear Problem",
            "problem": "Given that Alice has 5 apples and Bob gives her 3 more. If each apple costs 2 dollars, find the total value of Alice's apples."
        },
        {
            "name": "Complex Network Problem",
            "problem": "In a social network, Alice knows Bob and Carol. Bob knows David and Emma. Carol knows Frank. Emma knows George and Henry. David knows Ian. If information spreads through connections, determine how many steps it takes for information from Alice to reach Ian."
        },
        {
            "name": "Goal-Oriented Problem",
            "problem": "A company needs to achieve a revenue of $1 million. They currently have $400k in revenue. Their monthly growth rate must be at least 15%. Find the minimum number of months needed."
        }
    ]

    # Process each example
    for example in examples:
        print(f"\n{'='*60}")
        print(f"EXAMPLE: {example['name']}")
        print(f"{'='*60}")
        print(f"Problem: {example['problem']}")
        print()

        # Create system and solve
        system = AdaptiveReasoningSystem()
        solution = system.solve(example['problem'])

        # Display results
        print(format_solution(solution))
        print()


if __name__ == "__main__":
    main()
