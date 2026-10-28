---
name: splines-insert-knot
description: Insert a knot at a specific index in a spline, shifting later knots forward. Use this to add a control point in the middle of an existing path.
metadata:
  generated-by: mcp-plugin-dotnet
---

# Splines / Insert Knot

Insert a new knot at a given index in a spline. Knots at and after the index shift forward by one.

## Inputs

- `gameObjectRef` — the GameObject hosting the `SplineContainer` (required).
- `knotIndex` — the index to insert at (0..knotCount; required).
- `position` — local-space `Vector3` position of the knot (default zero).
- `tangentIn` / `tangentOut` — optional tangents (defaults `(0,0,-1)` / `(0,0,1)`).
- `rotation` — optional euler-degrees rotation (default zero).
- `splineIndex` — which spline in the container (default 0).

## Behavior

Validates the index range (0..count inclusive), builds a `BezierKnot`, inserts it, marks dirty, repaints, and returns the inserted knot index and the spline's new knot count. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool splines-insert-knot --input '{
  "gameObjectRef": "string_value",
  "knotIndex": 0,
  "position": "string_value",
  "tangentIn": "string_value",
  "tangentOut": "string_value",
  "rotation": "string_value",
  "splineIndex": 0
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool splines-insert-knot --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool splines-insert-knot --input-file - <<'EOF'
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
| `knotIndex` | `integer` | Yes | Index at which to insert the knot (0..knotCount). |
| `position` | `string` | No | Local-space position of the new knot. RQL: Vector3 |
| `tangentIn` | `string` | No | In tangent relative to the knot position. RQL: Vector3 |
| `tangentOut` | `string` | No | Out tangent relative to the knot position. RQL: Vector3 |
| `rotation` | `string` | No | Knot rotation in euler angles (degrees). RQL: Vector3 |
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
    "position": {
      "type": "string"
    },
    "tangentIn": {
      "type": "string"
    },
    "tangentOut": {
      "type": "string"
    },
    "rotation": {
      "type": "string"
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

