---
name: splines-container-create
description: Create a new GameObject with a `SplineContainer` (and one initial empty `Spline`) in the active scene. Optionally set name, position and rotation. Returns the new GameObject reference and instanceId.
metadata:
  generated-by: mcp-plugin-dotnet
---

# Splines / Create Container

Create a new GameObject hosting a `SplineContainer` component in the active scene. The `SplineContainer` is the authoring component that holds one or more `Spline`s; this tool seeds it with a single empty spline ready for knots.

## Inputs

- `name` — optional GameObject name (default `Spline`).
- `position` — optional world `Vector3` position (default zero).
- `rotation` — optional euler-degrees `Vector3` rotation (default zero).
- `closed` — optional; when true the seeded spline is a closed loop (default false).

## Behavior

Creates the GameObject, adds a `SplineContainer` with one empty spline, applies transform and the `Closed` flag, marks the scene dirty, repaints the Editor, and returns the new GameObject reference and instanceId. The whole call runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool splines-container-create --input '{
  "name": "string_value",
  "position": "string_value",
  "rotation": "string_value",
  "closed": false
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool splines-container-create --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool splines-container-create --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `name` | `string` | No | Name of the new SplineContainer GameObject. |
| `position` | `string` | No | World-space position of the GameObject. RQL: Vector3 |
| `rotation` | `string` | No | World-space rotation of the GameObject in euler angles (degrees). RQL: Vector3 |
| `closed` | `boolean` | No | If true, the seeded spline is a closed loop. |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "name": {
      "type": "string"
    },
    "position": {
      "type": "string"
    },
    "rotation": {
      "type": "string"
    },
    "closed": {
      "type": "boolean"
    }
  }
}
```

## Output

This tool does not return structured output.

