---
name: splines-set-tangent-mode
description: "Set the `TangentMode` of a knot in a spline. Valid modes: Linear, Continuous, Broken, AutoSmooth, Mirrored. The mode controls how the knot's in/out tangents are computed."
metadata:
  generated-by: mcp-plugin-dotnet
---

# Splines / Set Tangent Mode

Change how a knot's tangents behave by setting its `TangentMode`.

## Inputs

- `gameObjectRef` — the GameObject hosting the `SplineContainer` (required).
- `knotIndex` — the index of the knot (required).
- `tangentMode` — one of `Linear`, `Continuous`, `Broken`, `AutoSmooth`, `Mirrored` (case-insensitive, required).
- `splineIndex` — which spline in the container (default 0).

## Behavior

Parses the mode, applies it via `Spline.SetTangentMode(index, mode)`, marks the scene dirty, repaints, and returns the resulting knot summary. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool splines-set-tangent-mode --input '{
  "gameObjectRef": "string_value",
  "knotIndex": 0,
  "tangentMode": "string_value",
  "splineIndex": 0
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool splines-set-tangent-mode --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool splines-set-tangent-mode --input-file - <<'EOF'
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
| `knotIndex` | `integer` | Yes | Index of the knot to edit (0..knotCount-1). |
| `tangentMode` | `string` | Yes | Tangent mode: Linear, Continuous, Broken, AutoSmooth, or Mirrored (case-insensitive). |
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
    "tangentMode": {
      "type": "string"
    },
    "splineIndex": {
      "type": "integer"
    }
  },
  "required": [
    "gameObjectRef",
    "knotIndex",
    "tangentMode"
  ]
}
```

## Output

This tool does not return structured output.

