#!/usr/bin/env python3
"""
Test suite for Adaptive Reasoning System
"""

from adaptive_reasoning import (
    AdaptiveReasoningSystem,
    TopologyType,
    format_solution,
    Entity
)


def test_entity_extraction():
    """Test entity extraction from problem statements"""
    print("Testing Entity Extraction...")

    system = AdaptiveReasoningSystem()
    problem = "Alice has 5 apples. Bob has 3 oranges. Find the total fruit count."

    system._extract_problem_components(problem)

    assert len(system.entities) > 0, "Should extract entities"
    assert system.goal, "Should identify goal"

    print(f"  ✓ Extracted {len(system.entities)} entities")
    print(f"  ✓ Goal identified: {system.goal[:50]}...")
    print()


def test_topology_selection():
    """Test topology selection logic"""
    print("Testing Topology Selection...")

    # Test chain selection (simple problem)
    system1 = AdaptiveReasoningSystem()
    problem1 = "If x = 5, find y where y = x + 3."
    system1._extract_problem_components(problem1)
    topology1 = system1._select_topology()

    print(f"  ✓ Simple problem → {topology1.value} topology")

    # Test with more complex problem
    system2 = AdaptiveReasoningSystem()
    problem2 = """
    In a network, Alice connects to Bob, Carol, David, Emma, Frank,
    George, Harry, Ian, Jack, and Kate. Each person must satisfy
    at least 3 connection rules. Find the optimal network structure.
    """
    system2._extract_problem_components(problem2)
    topology2 = system2._select_topology()

    print(f"  ✓ Complex problem → {topology2.value} topology")
    print()


def test_chain_reasoning():
    """Test chain topology reasoning"""
    print("Testing Chain Reasoning...")

    system = AdaptiveReasoningSystem()
    system.current_topology = TopologyType.CHAIN
    system.constraints = ["constraint1", "constraint2"]

    system._execute_chain_reasoning("test problem")

    assert len(system.reasoning_steps) > 0, "Should generate steps"
    assert any("final_answer" in step.outputs for step in system.reasoning_steps), \
        "Should produce final answer"

    print(f"  ✓ Generated {len(system.reasoning_steps)} reasoning steps")
    print(f"  ✓ Final answer step included")
    print()


def test_tree_reasoning():
    """Test tree topology reasoning"""
    print("Testing Tree Reasoning...")

    system = AdaptiveReasoningSystem()
    system.current_topology = TopologyType.TREE
    system.constraints = ["c1", "c2", "c3"]

    system._execute_tree_reasoning("test problem")

    assert len(system.reasoning_steps) > 0, "Should generate steps"

    # Check for decomposition
    first_step = system.reasoning_steps[0]
    assert "decompose" in first_step.description.lower() or \
           "sub" in first_step.description.lower(), \
           "First step should decompose problem"

    print(f"  ✓ Generated {len(system.reasoning_steps)} reasoning steps")
    print(f"  ✓ Decomposition step included")
    print()


def test_graph_reasoning():
    """Test graph topology reasoning"""
    print("Testing Graph Reasoning...")

    system = AdaptiveReasoningSystem()
    system.current_topology = TopologyType.GRAPH
    system.entities = [
        Entity(name="A", entity_type="test"),
        Entity(name="B", entity_type="test"),
        Entity(name="C", entity_type="test"),
    ]
    system.constraints = ["c1", "c2"]

    system._execute_graph_reasoning("test problem")

    assert len(system.reasoning_steps) > 0, "Should generate steps"

    print(f"  ✓ Generated {len(system.reasoning_steps)} reasoning steps")
    print(f"  ✓ Graph structure created")
    print()


def test_reverse_reasoning():
    """Test reverse topology reasoning"""
    print("Testing Reverse Reasoning...")

    system = AdaptiveReasoningSystem()
    system.current_topology = TopologyType.REVERSE
    system.goal = "Find the solution"
    system.constraints = ["c1", "c2"]

    system._execute_reverse_reasoning("test problem")

    assert len(system.reasoning_steps) > 0, "Should generate steps"

    # Check for goal-first approach
    first_step = system.reasoning_steps[0]
    assert "goal" in first_step.description.lower(), \
        "First step should define goal"

    print(f"  ✓ Generated {len(system.reasoning_steps)} reasoning steps")
    print(f"  ✓ Goal-oriented structure created")
    print()


def test_contradiction_detection():
    """Test contradiction detection"""
    print("Testing Contradiction Detection...")

    system = AdaptiveReasoningSystem()
    from adaptive_reasoning import ReasoningStep

    # Create steps with missing dependency
    system.reasoning_steps = [
        ReasoningStep(1, "step 1", [], ["out1"], 0.9),
        ReasoningStep(2, "step 2", ["out1"], ["out2"], 0.9, dependencies=[1]),
        ReasoningStep(3, "step 3", ["out2"], ["out3"], 0.9, dependencies=[99]),  # Missing!
    ]

    contradictions = system._check_contradictions()

    assert len(contradictions) > 0, "Should detect missing dependency"

    print(f"  ✓ Detected {len(contradictions)} contradiction(s)")
    for c in contradictions:
        print(f"    - {c}")
    print()


def test_confidence_calculation():
    """Test confidence score calculation"""
    print("Testing Confidence Calculation...")

    system = AdaptiveReasoningSystem()
    from adaptive_reasoning import ReasoningStep

    # High confidence scenario
    system.reasoning_steps = [
        ReasoningStep(1, "step 1", [], ["out1"], 0.95),
        ReasoningStep(2, "step 2", ["out1"], ["out2"], 0.90),
        ReasoningStep(3, "step 3", ["out2"], ["final_answer"], 0.85),
    ]
    system.goal = "Find x"

    confidence = system._calculate_confidence([])
    print(f"  ✓ High confidence (no issues): {confidence:.2f}")

    # Low confidence scenario
    contradictions = ["issue1", "issue2", "issue3"]
    confidence_low = system._calculate_confidence(contradictions)
    print(f"  ✓ Low confidence (with issues): {confidence_low:.2f}")

    assert confidence > confidence_low, "Confidence should decrease with contradictions"
    print()


def test_topology_switching():
    """Test topology switching mechanism"""
    print("Testing Topology Switching...")

    system = AdaptiveReasoningSystem()

    # Test each topology's fallback
    topologies = [TopologyType.CHAIN, TopologyType.TREE,
                  TopologyType.GRAPH, TopologyType.REVERSE]

    for topo in topologies:
        system.current_topology = topo
        new_topo = system._switch_topology()
        print(f"  ✓ {topo.value} → {new_topo.value}")

    print()


def test_full_solution():
    """Test complete solution generation"""
    print("Testing Full Solution Generation...")

    problems = [
        "Given x = 5 and y = 3, find z where z = x + y.",
        "Alice, Bob, Carol, and David are connected. Find shortest path.",
        "A company needs $1M revenue. Currently at $500K. Find months needed."
    ]

    for i, problem in enumerate(problems, 1):
        print(f"\n  Problem {i}: {problem[:60]}...")

        system = AdaptiveReasoningSystem()
        solution = system.solve(problem)

        print(f"    ✓ Topology: {solution.topology_used.value}")
        print(f"    ✓ Confidence: {solution.confidence:.2f}")
        print(f"    ✓ Steps: {len(solution.reasoning_steps)}")

        if solution.contradictions:
            print(f"    ⚠ Contradictions: {len(solution.contradictions)}")

    print()


def test_output_formatting():
    """Test solution output formatting"""
    print("Testing Output Formatting...")

    system = AdaptiveReasoningSystem()
    solution = system.solve("Simple test problem: find x where x = 5 + 3")

    formatted = format_solution(solution)

    assert "Topology Used:" in formatted, "Should include topology"
    assert "Confidence:" in formatted, "Should include confidence"
    assert "Final Answer:" in formatted, "Should include answer"

    print(f"  ✓ Formatted output generated ({len(formatted)} chars)")
    print()


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("ADAPTIVE REASONING SYSTEM - TEST SUITE")
    print("=" * 60)
    print()

    tests = [
        test_entity_extraction,
        test_topology_selection,
        test_chain_reasoning,
        test_tree_reasoning,
        test_graph_reasoning,
        test_reverse_reasoning,
        test_contradiction_detection,
        test_confidence_calculation,
        test_topology_switching,
        test_full_solution,
        test_output_formatting,
    ]

    passed = 0
    failed = 0

    for test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            failed += 1

    print("=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
