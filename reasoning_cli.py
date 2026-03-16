#!/usr/bin/env python3
"""
Command-line interface for Adaptive Reasoning System
"""

import sys
import argparse
from adaptive_reasoning import AdaptiveReasoningSystem, format_solution, TopologyType


def solve_interactive():
    """Interactive mode - prompt user for problems"""
    print("=" * 60)
    print("ADAPTIVE REASONING SYSTEM - Interactive Mode")
    print("=" * 60)
    print("\nEnter your problem statement (or 'quit' to exit)")
    print("For multi-line input, end with an empty line\n")

    while True:
        print("\nProblem: ", end="")
        lines = []
        first_line = input()

        if first_line.lower() in ['quit', 'exit', 'q']:
            print("\nGoodbye!")
            break

        lines.append(first_line)

        # Allow multi-line input
        while True:
            line = input()
            if not line:
                break
            lines.append(line)

        problem = " ".join(lines).strip()

        if not problem:
            continue

        # Solve the problem
        print("\nSolving...")
        system = AdaptiveReasoningSystem()
        solution = system.solve(problem)

        # Display solution
        print()
        print(format_solution(solution))


def solve_from_file(filename):
    """Solve problems from a file"""
    try:
        with open(filename, 'r') as f:
            problems = f.read().split('\n\n')  # Problems separated by blank lines

        print(f"Found {len(problems)} problem(s) in {filename}\n")

        for i, problem in enumerate(problems, 1):
            problem = problem.strip()
            if not problem:
                continue

            print(f"\n{'='*60}")
            print(f"Problem {i}/{len(problems)}")
            print(f"{'='*60}")
            print(f"Input: {problem[:100]}...")

            system = AdaptiveReasoningSystem()
            solution = system.solve(problem)

            print(format_solution(solution))

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)


def solve_single(problem, topology=None):
    """Solve a single problem from command line"""
    system = AdaptiveReasoningSystem()

    # Force specific topology if requested
    if topology:
        try:
            forced_topology = TopologyType(topology.lower())
            solution = system.solve(problem)
            # Override the automatically selected topology
            if system.current_topology != forced_topology:
                print(f"Note: Forcing {forced_topology.value} topology "
                      f"(auto-selected: {system.current_topology.value})\n")
                system.current_topology = forced_topology
                system.reasoning_steps = []
                system._execute_reasoning(problem)
                contradictions = system._check_contradictions()
                confidence = system._calculate_confidence(contradictions)
                solution.topology_used = forced_topology
                solution.key_structure = system._describe_structure()
                solution.confidence = confidence
                solution.reasoning_steps = system.reasoning_steps
                solution.contradictions = contradictions
        except ValueError:
            print(f"Error: Unknown topology '{topology}'")
            print("Valid topologies: chain, tree, graph, reverse")
            sys.exit(1)
    else:
        solution = system.solve(problem)

    print(format_solution(solution))


def list_topologies():
    """List available topologies with descriptions"""
    print("=" * 60)
    print("AVAILABLE REASONING TOPOLOGIES")
    print("=" * 60)
    print()

    topologies = [
        ("chain", "Linear, sequential reasoning",
         "Step-by-step processes, simple cause-effect"),
        ("tree", "Hierarchical, branching reasoning",
         "Decision trees, classification problems"),
        ("graph", "Network-based, interconnected reasoning",
         "Complex relationships, many connections"),
        ("reverse", "Goal-oriented, backwards reasoning",
         "Working from desired outcome to prerequisites"),
    ]

    for name, desc, use_case in topologies:
        print(f"{name.upper()}")
        print(f"  Description: {desc}")
        print(f"  Best for: {use_case}")
        print()


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Adaptive Reasoning System - Intelligent problem solving",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  %(prog)s -i

  # Solve a single problem
  %(prog)s -p "Given x=5, find y where y=x+3"

  # Force a specific topology
  %(prog)s -p "Complex problem..." -t graph

  # Solve problems from a file
  %(prog)s -f problems.txt

  # List available topologies
  %(prog)s -l

  # Run example problems
  %(prog)s -e
        """
    )

    parser.add_argument('-i', '--interactive',
                        action='store_true',
                        help='Interactive mode')

    parser.add_argument('-p', '--problem',
                        type=str,
                        help='Problem statement to solve')

    parser.add_argument('-f', '--file',
                        type=str,
                        help='File containing problems (separated by blank lines)')

    parser.add_argument('-t', '--topology',
                        type=str,
                        choices=['chain', 'tree', 'graph', 'reverse'],
                        help='Force a specific reasoning topology')

    parser.add_argument('-l', '--list',
                        action='store_true',
                        help='List available topologies')

    parser.add_argument('-e', '--examples',
                        action='store_true',
                        help='Run example problems')

    args = parser.parse_args()

    # Handle different modes
    if args.list:
        list_topologies()
    elif args.interactive:
        solve_interactive()
    elif args.examples:
        # Import and run the examples from adaptive_reasoning module
        from adaptive_reasoning import main as run_examples
        run_examples()
    elif args.file:
        solve_from_file(args.file)
    elif args.problem:
        solve_single(args.problem, args.topology)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
