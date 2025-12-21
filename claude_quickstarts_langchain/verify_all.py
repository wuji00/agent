import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

try:
    print("Verifying Customer Support Agent...")
    from customer_support_agent import graph as csa_graph
    assert csa_graph.app is not None
    print("OK")
except Exception as e:
    print(f"FAILED: {e}")
    sys.exit(1)

try:
    print("Verifying Financial Data Analyst...")
    from financial_data_analyst import graph as fda_graph
    assert fda_graph.app is not None
    print("OK")
except Exception as e:
    print(f"FAILED: {e}")
    sys.exit(1)

try:
    print("Verifying Autonomous Coding Agent...")
    from autonomous_coding_agent import graph as aca_graph
    assert aca_graph.app is not None
    print("OK")
except Exception as e:
    print(f"FAILED: {e}")
    sys.exit(1)

try:
    print("Verifying Computer Use Demo...")
    from computer_use_demo import graph as cud_graph
    assert cud_graph.app is not None
    print("OK")
except Exception as e:
    print(f"FAILED: {e}")
    sys.exit(1)
