from client import JevTypedStateActionRouter
import json

def test_router():
    router = JevTypedStateActionRouter()
    print("=== Testing Jev Typed State-Action Router MCP ===")
    
    # 1. Validate Schema
    val = router.validate_state_schema({
        "goal": "Find electric shaver",
        "budget": 8000,
        "currency": "USD"
    }, "user_intent")
    print("
[1] Schema Validation Result:")
    print(json.dumps(val, indent=2))
    
    # 2. Gatekeep Tool
    gate = router.gatekeep_tool_execution({
        "tool_name": "fetch_product_specs",
        "parameters": {"sku": "SHAVER-PRO-2026"}
    })
    print("
[2] Pre-flight Tool Gatekeeping:")
    print(json.dumps(gate, indent=2))

    # 3. Benchmark
    bench = router.run_benchmark_state_routing()
    print("
[3] Full State Routing Benchmark:")
    print(json.dumps(bench, indent=2))

if __name__ == "__main__":
    test_router()
