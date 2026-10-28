---
name: terrain-set-heights
description: Set heightmap values over a rectangular region (or the whole terrain) of a `Terrain`. Either fill the region with a uniform normalized height, or supply an explicit row-major 2D heights array. Heights are normalized [0,1] of the terrain's Y size.
metadata:
  generated-by: mcp-plugin-dotnet
---

# Terrain / Set Heights

Write heightmap values into a `Terrain`'s `TerrainData`.

## Inputs

- `gameObjectRef` — the GameObject hosting the `Terrain` (required).
- `xBase` / `yBase` — top-left heightmap cell of the region (default 0,0).
- `width` / `height` — region size in heightmap cells. When &lt;= 0, the region spans to the edge of the heightmap from the base.
- `uniformHeight` — when `heights` is omitted, fill the whole region with this normalized [0,1] value (default 0).
- `heights` — optional explicit row-major `[height][width]` array of normalized [0,1] values. When provided, its dimensions define the region size (overriding width/height).

## Behavior

Resolves and clamps the region against `heightmapResolution`, builds a `[h,w]` height array (uniform fill or from `heights`), and calls `TerrainData.SetHeights(xBase, yBase, array)`. Destructive: overwrites existing heights in the region. Marks dirty + repaints. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool terrain-set-heights --input '{
  "gameObjectRef": "string_value",
  "xBase": 0,
  "yBase": 0,
  "width": 0,
  "height": 0,
  "uniformHeight": 0,
  "heights": []
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool terrain-set-heights --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool terrain-set-heights --input-file - <<'EOF'
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
| `uniformHeight` | `number` | No | Uniform normalized [0,1] height used to fill the region when 'heights' is omitted. |
| `heights` | `array` | No | Optional explicit row-major [height][width] array of normalized [0,1] heights. |

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
    "uniformHeight": {
      "type": "number"
    },
    "heights": {
      "type": "array",
      "items": {
        "type": "array",
        "items": {
          "type": "number"
        }
      }
    }
  },
  "required": [
    "gameObjectRef"
  ]
}
```

## Output

This tool does not return structured output.

