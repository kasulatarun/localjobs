---
name: splines-get-knots
description: "Read all knots of a spline in a `SplineContainer`: per-knot position, in/out tangents, rotation, and tangent mode, plus the closed flag. Read-only."
metadata:
  generated-by: mcp-plugin-dotnet
---

# Splines / Get Knots

Inspect the knots of a specific spline. Useful before editing to know the indices, positions, and tangent modes.

## Inputs

- `gameObjectRef` — the GameObject hosting the `SplineContainer` (required).
- `splineIndex` — which spline in the container (default 0).

## Behavior

Enumerates every knot of the chosen spline and returns a per-knot summary plus the spline's `Closed` flag. Read-only. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool splines-get-knots --input '{
  "gameObjectRef": "string_value",
  "splineIndex": 0
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool splines-get-knots --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool splines-get-knots --input-file - <<'EOF'
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
| `splineIndex` | `integer` | No | Index of the spline inside the container (default 0). |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gameObjectRef": {
      "type": "string"
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

