---
name: splines-list
description: List every `SplineContainer` in the active scene with its name, spline count, and the knot count of each spline. Read-only.
metadata:
  generated-by: mcp-plugin-dotnet
---

# Splines / List Containers

Enumerate the `SplineContainer`s in the active scene. For each, returns a reference, the name, the number of splines, and per-spline knot counts and closed flags.

## Inputs

- `includeInactive` (bool, default true) — include containers on inactive/disabled GameObjects.

## Behavior

Finds all `SplineContainer` instances and summarizes them. Read-only. The whole call runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool splines-list --input '{
  "includeInactive": false
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool splines-list --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool splines-list --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `includeInactive` | `boolean` | No | If true (default), include containers on inactive/disabled GameObjects. |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "includeInactive": {
      "type": "boolean"
    }
  }
}
```

## Output

This tool does not return structured output.

