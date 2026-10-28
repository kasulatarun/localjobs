---
name: terrain-paint-layer
description: Paint a `TerrainLayer` over a rectangular region (or the whole terrain) by writing the alphamap (splatmap) so the chosen layer has the given weight there and the other layers are reduced proportionally. Alphamap weights are normalized [0,1].
metadata:
  generated-by: mcp-plugin-dotnet
---

# Terrain / Paint Layer

Write the alphamap (splatmap) of a `Terrain` so one `TerrainLayer` dominates a region.

## Inputs

- `gameObjectRef` — the GameObject hosting the `Terrain` (required).
- `layerIndex` — index of the `TerrainLayer` to paint (required; must already be on the terrain).
- `xBase` / `yBase` — top-left alphamap cell of the region (default 0,0).
- `width` / `height` — region size in alphamap cells. When &lt;= 0, spans to the alphamap edge.
- `strength` — target normalized [0,1] weight for the chosen layer (default 1 = fully painted).

## Behavior

Reads the region alphamaps via `GetAlphamaps`, sets the chosen layer's weight to `strength` and scales the remaining layers so each cell's weights sum to 1, then writes back with `SetAlphamaps`. Destructive. Marks dirty + repaints. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool terrain-paint-layer --input '{
  "gameObjectRef": "string_value",
  "layerIndex": 0,
  "xBase": 0,
  "yBase": 0,
  "width": 0,
  "height": 0,
  "strength": 0
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool terrain-paint-layer --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool terrain-paint-layer --input-file - <<'EOF'
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
| `layerIndex` | `integer` | Yes | Index of the TerrainLayer to paint (must already be on the terrain). |
| `xBase` | `integer` | No | Top-left alphamap X cell of the region. |
| `yBase` | `integer` | No | Top-left alphamap Y cell of the region. |
| `width` | `integer` | No | Region width in alphamap cells. <= 0 spans to the alphamap edge. |
| `height` | `integer` | No | Region height in alphamap cells. <= 0 spans to the alphamap edge. |
| `strength` | `number` | No | Target normalized [0,1] weight for the chosen layer (1 = fully painted). |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gameObjectRef": {
      "type": "string"
    },
    "layerIndex": {
      "type": "integer"
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
    "strength": {
      "type": "number"
    }
  },
  "required": [
    "gameObjectRef",
    "layerIndex"
  ]
}
```

## Output

This tool does not return structured output.

