---
name: splines-add-spline
description: Add an additional empty `Spline` to an existing `SplineContainer`. A container can hold many splines; this appends one and returns its new index.
metadata:
  generated-by: mcp-plugin-dotnet
---

# Splines / Add Spline

Add a new empty `Spline` to a `SplineContainer`. Use this when you need more than one spline on the same GameObject (e.g. a multi-path container).

## Inputs

- `gameObjectRef` — the GameObject hosting the `SplineContainer` (required).
- `closed` — optional; when true the new spline is a closed loop (default false).

## Behavior

Appends a new empty spline to the container, applies the `Closed` flag, marks the scene dirty, repaints, and returns the index of the new spline and the resulting spline count. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool splines-add-spline --input '{
  "gameObjectRef": "string_value",
  "closed": false
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool splines-add-spline --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool splines-add-spline --input-file - <<'EOF'
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
| `closed` | `boolean` | No | If true, the new spline is a closed loop. |

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
    }
  },
  "required": [
    "gameObjectRef"
  ]
}
```

## Output

This tool does not return structured output.

