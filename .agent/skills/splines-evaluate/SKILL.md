---
name: splines-evaluate
description: Evaluate a spline at normalized parameter `t` in [0,1], returning the local-space and world-space position, the tangent (direction of travel), and the up vector. Read-only.
metadata:
  generated-by: mcp-plugin-dotnet
---

# Splines / Evaluate

Sample a spline at a point along its length. `t` is normalized: 0 is the first knot, 1 is the last knot (or the loop point for a closed spline).

## Inputs

- `gameObjectRef` — the GameObject hosting the `SplineContainer` (required).
- `t` — normalized parameter in [0,1] (default 0.5). Values outside are clamped.
- `splineIndex` — which spline in the container (default 0).

## Behavior

Evaluates local position / tangent / up via `Spline.Evaluate`, transforms the position into world space using the container's transform, and returns all of them. The spline must have at least 2 knots. Read-only. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool splines-evaluate --input '{
  "gameObjectRef": "string_value",
  "t": 0,
  "splineIndex": 0
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool splines-evaluate --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool splines-evaluate --input-file - <<'EOF'
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
| `t` | `number` | No | Normalized parameter along the spline in [0,1] (clamped). Default 0.5. |
| `splineIndex` | `integer` | No | Index of the spline inside the container (default 0). |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gameObjectRef": {
      "type": "string"
    },
    "t": {
      "type": "number"
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

