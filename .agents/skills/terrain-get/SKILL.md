---
name: terrain-get
description: Inspect a `Terrain` — its `TerrainData` size, heightmap / alphamap / detail resolutions, the list of TerrainLayers, tree/detail prototype counts, tree-instance count, and neighbor terrains. Read-only.
metadata:
  generated-by: mcp-plugin-dotnet
---

# Terrain / Get Terrain

Inspect a `Terrain` component in the active scene and report its `TerrainData` configuration.

## Inputs

- `gameObjectRef` — the GameObject hosting the `Terrain` (required).

## Behavior

Reads `TerrainData.size`, `heightmapResolution`, `alphamapResolution`, `detailResolution`, the `terrainLayers` (with their diffuse-texture names), the tree- and detail-prototype counts, the number of placed tree instances, and the left/top/right/bottom neighbor terrains. Read-only — nothing is mutated. The whole call runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool terrain-get --input '{
  "gameObjectRef": "string_value"
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool terrain-get --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool terrain-get --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gameObjectRef` | `string` | Yes | Reference to the GameObject containing the Terrain component. RQL: GameObjectRef |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gameObjectRef": {
      "type": "string"
    }
  },
  "required": [
    "gameObjectRef"
  ]
}
```

## Output

This tool does not return structured output.

