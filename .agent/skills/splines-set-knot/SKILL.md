---
name: splines-set-knot
description: Set position, in/out tangents, and/or rotation of an existing knot in a spline. Only the fields you pass are changed; the rest are preserved.
metadata:
  generated-by: mcp-plugin-dotnet
---

# Splines / Set Knot

Edit an existing knot in place. `BezierKnot` is a value type, so this reads the current knot, applies only the provided fields, and writes it back through the spline indexer (which rebuilds the cached curve).

## Inputs

- `gameObjectRef` — the GameObject hosting the `SplineContainer` (required).
- `knotIndex` — the index of the knot to edit (required).
- `position` — optional new local-space position.
- `tangentIn` / `tangentOut` — optional new tangents.
- `rotation` — optional new euler-degrees rotation.
- `splineIndex` — which spline in the container (default 0).

## Behavior

Reads the knot, overrides only the supplied fields, writes it back, marks the scene dirty, repaints, and returns the resulting knot summary. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool splines-set-knot --input '{
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
> unity-mcp-cli run-tool splines-set-knot --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool splines-set-knot --input-file - <<'EOF'
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
| `position` | `string` | No | New local-space position of the knot. RQL: Vector3 |
| `tangentIn` | `string` | No | New in tangent relative to the knot position. RQL: Vector3 |
| `tangentOut` | `string` | No | New out tangent relative to the knot position. RQL: Vector3 |
| `rotation` | `string` | No | New knot rotation in euler angles (degrees). RQL: Vector3 |
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

