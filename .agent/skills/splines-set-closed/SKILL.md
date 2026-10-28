---
name: splines-set-closed
description: Toggle whether a spline is a closed loop. A closed spline connects its last knot back to its first, forming a continuous loop.
metadata:
  generated-by: mcp-plugin-dotnet
---

# Splines / Set Closed

Set the `Closed` flag of a spline.

## Inputs

- `gameObjectRef` — the GameObject hosting the `SplineContainer` (required).
- `closed` — true to close the loop, false to open it (default true).
- `splineIndex` — which spline in the container (default 0).

## Behavior

Assigns `Spline.Closed`, marks the scene dirty, repaints, and returns the resulting state. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool splines-set-closed --input '{
  "gameObjectRef": "string_value",
  "closed": false,
  "splineIndex": 0
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool splines-set-closed --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool splines-set-closed --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gameObjectRef` | `string` | Yes | Reference to the GameObject containing the SplineContainer component. RQL: GameObjectRef |
| `closed` | `boolean` | No | True to close the loop, false to open it. |
| `splineIndex` | `integer` | No | Index of the spline inside the container (default 0). |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gameObjectRef": {
      "type": "string"
    },
    "closed": {
      "type": "boolean"
    },
    "splineIndex": {
      "type": "integer"
    }
  },
  "required": [
    "gameObjectRef"
  ]
}
```

## Output

This tool does not return structured output.

