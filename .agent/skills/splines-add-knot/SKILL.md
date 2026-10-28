---
name: splines-add-knot
description: Append a knot to a spline in a `SplineContainer`. A knot is a `BezierKnot` with a local position plus in/out tangents and a rotation. Returns the index of the appended knot.
metadata:
  generated-by: mcp-plugin-dotnet
---

# Splines / Add Knot

Append a new knot to the end of a spline. Knots define the control points the spline curve passes through.

## Inputs

- `gameObjectRef` — the GameObject hosting the `SplineContainer` (required).
- `position` — local-space `Vector3` position of the knot (default zero).
- `tangentIn` — optional in tangent relative to the position (default `(0,0,-1)`).
- `tangentOut` — optional out tangent relative to the position (default `(0,0,1)`).
- `rotation` — optional euler-degrees rotation of the knot (default zero).
- `splineIndex` — which spline in the container to append to (default 0).

## Behavior

Builds a `BezierKnot` from the inputs, appends it to the chosen spline, marks the scene dirty, repaints, and returns the appended knot index plus the spline's new knot count. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool splines-add-knot --input '{
  "gameObjectRef": "string_value",
  "position": "string_value",
  "tangentIn": "string_value",
  "tangentOut": "string_value",
  "rotation": "string_value",
  "splineIndex": 0
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool splines-add-knot --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool splines-add-knot --input-file - <<'EOF'
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
| `position` | `string` | No | Local-space position of the new knot. RQL: Vector3 |
| `tangentIn` | `string` | No | In tangent relative to the knot position. RQL: Vector3 |
| `tangentOut` | `string` | No | Out tangent relative to the knot position. RQL: Vector3 |
| `rotation` | `string` | No | Knot rotation in euler angles (degrees). RQL: Vector3 |
| `splineIndex` | `integer` | No | Index of the spline inside the container to append to (default 0). |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gameObjectRef": {
      "type": "string"
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
    "gameObjectRef"
  ]
}
```

## Output

This tool does not return structured output.

