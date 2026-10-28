---
name: navigation-agent-add
description: Add and configure a `NavMeshAgent` (from the built-in `com.unity.modules.ai`) on a GameObject — or create a new GameObject to host it. Configure agent type, speed, acceleration, angular speed, stopping distance, and the area mask. Returns the GameObject reference and instanceId.
metadata:
  generated-by: mcp-plugin-dotnet
---

# Navigation / Add NavMeshAgent

Add a `NavMeshAgent` to a GameObject so it can pathfind across a baked NavMesh. Use 'navigation-agent-set-destination' to move it.

## Inputs

- `gameObjectRef` — optional GameObject to add the agent to. When omitted, a new GameObject is created.
- `name` — optional name for the new GameObject (default `NavMeshAgent`); ignored when `gameObjectRef` is given.
- `agentTypeId` — optional NavMesh agent-type id (default 0 = Humanoid).
- `speed` — optional max movement speed (default 3.5).
- `acceleration` — optional max acceleration (default 8).
- `angularSpeed` — optional max turning speed in deg/s (default 120).
- `stoppingDistance` — optional stop distance from the destination (default 0).
- `areaMask` — optional traversable-area bitmask (default -1 = all areas).

## Behavior

Adds (or reuses) a `NavMeshAgent`, assigns the configured properties, marks the scene dirty, repaints, and returns the GameObject reference, the agent component reference, and the instanceId. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool navigation-agent-add --input '{
  "gameObjectRef": "string_value",
  "name": "string_value",
  "agentTypeId": 0,
  "speed": 0,
  "acceleration": 0,
  "angularSpeed": 0,
  "stoppingDistance": 0,
  "areaMask": 0
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool navigation-agent-add --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool navigation-agent-add --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gameObjectRef` | `string` | No | Optional GameObject to add the NavMeshAgent to. When omitted, a new GameObject is created. RQL: GameObjectRef |
| `name` | `string` | No | Name for the new GameObject (ignored when gameObjectRef is provided). |
| `agentTypeId` | `integer` | No | NavMesh agent-type id (0 = Humanoid by default). |
| `speed` | `number` | No | Maximum movement speed. |
| `acceleration` | `number` | No | Maximum acceleration. |
| `angularSpeed` | `number` | No | Maximum turning speed in degrees per second. |
| `stoppingDistance` | `number` | No | Distance from the destination at which the agent stops. |
| `areaMask` | `integer` | No | Traversable-area bitmask (-1 = all areas). |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gameObjectRef": {
      "type": "string"
    },
    "name": {
      "type": "string"
    },
    "agentTypeId": {
      "type": "integer"
    },
    "speed": {
      "type": "number"
    },
    "acceleration": {
      "type": "number"
    },
    "angularSpeed": {
      "type": "number"
    },
    "stoppingDistance": {
      "type": "number"
    },
    "areaMask": {
      "type": "integer"
    }
  }
}
```

## Output

This tool does not return structured output.

