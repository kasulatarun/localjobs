---
name: terrain-list
description: List every `Terrain` in the active scene with its name, world size, heightmap resolution, and TerrainLayer count. Read-only.
metadata:
  generated-by: mcp-plugin-dotnet
---

# Terrain / List Terrains

List every `Terrain` in the active scene.

## Inputs

- `includeInactive` (bool, default true) — include Terrains on inactive/disabled GameObjects.

## Behavior

Finds all `Terrain` instances, and for each returns the GameObject reference, the name, the `TerrainData.size`, the heightmap resolution, and the number of TerrainLayers. Read-only. The whole call runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool terrain-list --input '{
  "includeInactive": false
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool terrain-list --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool terrain-list --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `includeInactive` | `boolean` | No | If true (default), include Terrains on inactive/disabled GameObjects; if false, only active ones. |

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

