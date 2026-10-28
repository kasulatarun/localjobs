---
name: navigation-agent-set-destination
description: Set the destination of a `NavMeshAgent` so it pathfinds toward a world-space point. Optionally provide a target GameObject instead of explicit coordinates. The agent must be on a baked NavMesh for a path to be computed (most relevant in play mode).
metadata:
  generated-by: mcp-plugin-dotnet
---

# Navigation / Set Agent Destination

Set a `NavMeshAgent`'s destination. The agent computes a path across the baked NavMesh and begins moving toward the destination (path computation/movement happens in play mode; in edit mode the destination is still assigned).

## Inputs

- `gameObjectRef` — the GameObject hosting the `NavMeshAgent` (required).
- `destination` — the world-space destination point. Ignored when `targetRef` is provided.
- `targetRef` — optional GameObject whose position is used as the destination.

## Behavior

Resolves the agent, computes the destination (from `targetRef` if given, else `destination`), and — when the agent is active and placed on a NavMesh — calls `SetDestination`. Off the NavMesh (e.g. before baking, in edit mode) it reports the intended destination without mutating, so the call is always safe. Returns `accepted` plus the agent's `hasPath` / `pathPending` state. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool navigation-agent-set-destination --input '{
  "gameObjectRef": "string_value",
  "destination": "string_value",
  "targetRef": "string_value"
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool navigation-agent-set-destination --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool navigation-agent-set-destination --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gameObjectRef` | `string` | Yes | Reference to the GameObject containing the NavMeshAgent component. RQL: GameObjectRef |
| `destination` | `string` | No | World-space destination point (ignored when targetRef is provided). RQL: Vector3 |
| `targetRef` | `string` | No | Optional GameObject whose position is used as the destination. RQL: GameObjectRef |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gameObjectRef": {
      "type": "string"
    },
    "destination": {
      "type": "string"
    },
    "targetRef": {
      "type": "string"
    }
  },
  "required": [
    "gameObjectRef"
  ]
}
```

## Output

This tool does not return structured output.

