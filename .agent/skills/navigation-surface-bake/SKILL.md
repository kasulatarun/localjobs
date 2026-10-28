---
name: navigation-surface-bake
description: Bake (build) the NavMesh for a `NavMeshSurface`, or clear its existing baked data. Pass `clear = true` to remove the baked NavMeshData instead of building it.
metadata:
  generated-by: mcp-plugin-dotnet
---

# Navigation / Bake or Clear NavMeshSurface

Build or clear the runtime NavMesh for a `NavMeshSurface`.

## Inputs

- `gameObjectRef` — the GameObject hosting the `NavMeshSurface` (required).
- `clear` — when `true`, removes the surface's baked NavMeshData (`RemoveData`) instead of baking. Default `false` (bake via `BuildNavMesh`).

## Behavior

When baking, collects the surface's geometry sources and builds the NavMeshData, then marks the surface dirty so the result is saved. When clearing, removes the active NavMeshData from the surface. Marks the scene dirty and repaints. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool navigation-surface-bake --input '{
  "gameObjectRef": "string_value",
  "clear": false
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool navigation-surface-bake --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool navigation-surface-bake --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gameObjectRef` | `string` | Yes | Reference to the GameObject containing the NavMeshSurface component. RQL: GameObjectRef |
| `clear` | `boolean` | No | If true, clears the baked NavMeshData instead of baking it. |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gameObjectRef": {
      "type": "string"
    },
    "clear": {
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

