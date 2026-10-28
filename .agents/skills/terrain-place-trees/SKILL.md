---
name: terrain-place-trees
description: Place trees on a `Terrain` using an existing tree prototype. Either scatter `count` trees randomly across a normalized [0,1] sub-rectangle, or place trees at explicit normalized positions. Optionally clear existing trees first.
metadata:
  generated-by: mcp-plugin-dotnet
---

# Terrain / Place Trees

Add `TreeInstance`s to a `Terrain`. Tree positions are normalized [0,1] across the terrain.

## Inputs

- `gameObjectRef` — the GameObject hosting the `Terrain` (required).
- `prototypeIndex` — index of the tree prototype to place (must already be on the terrain, default 0).
- `count` — number of trees to scatter randomly (used when `positions` is omitted; default 100).
- `minX` / `minZ` / `maxX` / `maxZ` — normalized [0,1] sub-rectangle to scatter within (default 0..1 on both axes).
- `positions` — optional explicit normalized [0,1] XZ positions (each a `Vector2`, x→X, y→Z). When provided, overrides random scatter.
- `heightScale` / `widthScale` — per-instance scale (default 1).
- `clearExisting` — when `true`, removes existing trees before placing (default false).

## Behavior

Validates the prototype index, builds `TreeInstance`s (sampling the terrain height at each normalized position), and assigns them via `TerrainData.SetTreeInstances(..., snapToHeightmap:true)`. Marks dirty + repaints. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool terrain-place-trees --input '{
  "gameObjectRef": "string_value",
  "prototypeIndex": 0,
  "count": 0,
  "minX": 0,
  "minZ": 0,
  "maxX": 0,
  "maxZ": 0,
  "positions": "string_value",
  "heightScale": 0,
  "widthScale": 0,
  "clearExisting": false
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool terrain-place-trees --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool terrain-place-trees --input-file - <<'EOF'
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
| `prototypeIndex` | `integer` | No | Index of the tree prototype to place (must already be on the terrain). |
| `count` | `integer` | No | Number of trees to scatter randomly when 'positions' is omitted. |
| `minX` | `number` | No | Normalized [0,1] minimum X of the scatter sub-rectangle. |
| `minZ` | `number` | No | Normalized [0,1] minimum Z of the scatter sub-rectangle. |
| `maxX` | `number` | No | Normalized [0,1] maximum X of the scatter sub-rectangle. |
| `maxZ` | `number` | No | Normalized [0,1] maximum Z of the scatter sub-rectangle. |
| `positions` | `string` | No | Optional explicit normalized [0,1] XZ positions (Vector2: x->X, y->Z). RQL: [Vector2] |
| `heightScale` | `number` | No | Per-instance height scale. |
| `widthScale` | `number` | No | Per-instance width scale. |
| `clearExisting` | `boolean` | No | If true, removes existing trees before placing. |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gameObjectRef": {
      "type": "string"
    },
    "prototypeIndex": {
      "type": "integer"
    },
    "count": {
      "type": "integer"
    },
    "minX": {
      "type": "number"
    },
    "minZ": {
      "type": "number"
    },
    "maxX": {
      "type": "number"
    },
    "maxZ": {
      "type": "number"
    },
    "positions": {
      "type": "string"
    },
    "heightScale": {
      "type": "number"
    },
    "widthScale": {
      "type": "number"
    },
    "clearExisting": {
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

