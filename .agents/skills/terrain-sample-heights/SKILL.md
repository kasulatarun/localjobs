---
name: terrain-sample-heights
description: Read heightmap values over a rectangular region (or the whole terrain) of a `Terrain`. Returns the normalized [0,1] heights plus min/max/average statistics. Read-only.
metadata:
  generated-by: mcp-plugin-dotnet
---

# Terrain / Sample Heights

Sample heightmap values from a `Terrain`'s `TerrainData`.

## Inputs

- `gameObjectRef` — the GameObject hosting the `Terrain` (required).
- `xBase` / `yBase` — top-left heightmap cell of the region (default 0,0).
- `width` / `height` — region size in heightmap cells. When &lt;= 0, the region spans to the edge of the heightmap from the base.
- `includeArray` — when `true`, include the full row-major `[height][width]` heights array in the response (can be large); otherwise only statistics are returned (default false).

## Behavior

Resolves and clamps the region against `heightmapResolution`, calls `TerrainData.GetHeights`, computes min/max/average over the sampled cells, and optionally returns the full array. Read-only. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool terrain-sample-heights --input '{
  "gameObjectRef": "string_value",
  "xBase": 0,
  "yBase": 0,
  "width": 0,
  "height": 0,
  "includeArray": false
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool terrain-sample-heights --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool terrain-sample-heights --input-file - <<'EOF'
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
| `xBase` | `integer` | No | Top-left heightmap X cell of the region. |
| `yBase` | `integer` | No | Top-left heightmap Y cell of the region. |
| `width` | `integer` | No | Region width in heightmap cells. <= 0 spans to the heightmap edge. |
| `height` | `integer` | No | Region height in heightmap cells. <= 0 spans to the heightmap edge. |
| `includeArray` | `boolean` | No | If true, include the full row-major [height][width] heights array in the response. |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gameObjectRef": {
      "type": "string"
    },
    "xBase": {
      "type": "integer"
    },
    "yBase": {
      "type": "integer"
    },
    "width": {
      "type": "integer"
    },
    "height": {
      "type": "integer"
    },
    "includeArray": {
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

