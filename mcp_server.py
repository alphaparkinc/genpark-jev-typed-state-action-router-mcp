import sys, json
from client import JevTypedStateActionRouter

def handle_mcp():
    router = JevTypedStateActionRouter()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(router.run_benchmark_state_routing(), indent=2))
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            
            if method == "initialize":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {"name": "genpark-jev-typed-state-action-router-mcp", "version": "1.0.0"},
                    "capabilities": {"tools": {}}
                }}
            elif method == "tools/list":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [
                    {"name": "validate_state_schema", "description": "Verify state payload conformity against strict schema.", "inputSchema": {"type": "object", "properties": {"state_dict": {"type": "object"}, "schema_name": {"type": "string"}}}},
                    {"name": "route_action_payload", "description": "Determine optimal dispatch pipeline based on state entropy.", "inputSchema": {"type": "object", "properties": {"state_payload": {"type": "object"}}}},
                    {"name": "gatekeep_tool_execution", "description": "Pre-flight safety inspection for external tool executions.", "inputSchema": {"type": "object", "properties": {"tool_call_spec": {"type": "object"}}}},
                    {"name": "run_benchmark_state_routing", "description": "Execute comprehensive state routing benchmark.", "inputSchema": {"type": "object"}}
                ]}}
            elif method == "tools/call":
                tname = req.get("params", {}).get("name")
                args = req.get("params", {}).get("arguments", {})
                if tname == "validate_state_schema":
                    res = router.validate_state_schema(args.get("state_dict", {}), args.get("schema_name", "user_intent"))
                elif tname == "route_action_payload":
                    res = router.route_action_payload(args.get("state_payload", {}))
                elif tname == "gatekeep_tool_execution":
                    res = router.gatekeep_tool_execution(args.get("tool_call_spec", {}))
                else:
                    res = router.run_benchmark_state_routing()
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}
            
            sys.stdout.write(json.dumps(resp) + "
")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "
")
            sys.stdout.flush()

if __name__ == "__main__":
    handle_mcp()
