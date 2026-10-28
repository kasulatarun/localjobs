---
name: splines-remove-knot
description: "Remove the knot at a given index from a spline, shifting later knots back. Destructive: the removed control point is gone."
metadata:
  generated-by: mcp-plugin-dotnet
---

# Splines / Remove Knot

Remove a knot at a specific index from a spline. Knots after the index shift back by one.

## Inputs

- `gameObjectRef` — the GameObject hosting the `SplineContainer` (required).
- `knotIndex` — the index of the knot to remove (0..knotCount-1; required).
- `splineIndex` — which spline in the container (default 0).

## Behavior

Validates the index range, removes the knot via `Spline.RemoveAt`, marks the scene dirty, repaints, and returns the spline's new knot count. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool splines-remove-knot --input '{
  "gameObjectRef": "string_value",
  "knotIndex": 0,
  "splineIndex": 0
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool splines-remove-knot --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool splines-remove-knot --input-file - <<'EOF'
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
| `knotIndex` | `integer` | Yes | Index of the knot to remove (0..knotCount-1). |
| `splineIndex` | `integer` | No | Index of the spline inside the container (default 0). |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gameObjectRef": {
      "type": "string"
    },
    "knotIndex": {
      "type": "integer"
    },
    "splineIndex": {
      "type": "integer"
    }
  },
  "required": [
    "gameObjectRef",
    "knotIndex"
  ]
}
```

## Output

This tool does not return structured output.

