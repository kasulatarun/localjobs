---
name: terrain-create
description: Create a new GameObject with a `Terrain` + `TerrainCollider` backed by a freshly created `TerrainData` asset. Set heightmap resolution and the terrain world size (width/height/length). Returns the new GameObject reference and instanceId.
metadata:
  generated-by: mcp-plugin-dotnet
---

# Terrain / Create Terrain

Create a new GameObject hosting a `Terrain` and a `TerrainCollider` in the active scene, backed by a new `TerrainData` asset saved to the project.

## Inputs

- `name` — optional GameObject name (default `Terrain`).
- `terrainDataAssetPath` — project path for the new `TerrainData` asset (default `Assets/TerrainData_<name>.asset`). Must start with `Assets/` and end with `.asset`.
- `heightmapResolution` — heightmap resolution; rounded to a valid `2^n + 1` value (default 513).
- `width` / `length` — horizontal terrain size in world units (X / Z, default 1000 each).
- `height` — vertical terrain size in world units (Y, default 600).
- `position` — optional world position of the terrain GameObject (default zero).

## Behavior

Creates the `TerrainData`, sets its `heightmapResolution` and `size`, writes it as an asset, then creates the GameObject via `Terrain.CreateTerrainGameObject`, positions it, marks the scene dirty, repaints, and returns the new GameObject reference and instanceId. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool terrain-create --input '{
  "name": "string_value",
  "terrainDataAssetPath": "string_value",
  "heightmapResolution": 0,
  "width": 0,
  "length": 0,
  "height": 0,
  "position": "string_value"
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool terrain-create --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool terrain-create --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `name` | `string` | No | Name of the new Terrain GameObject. |
| `terrainDataAssetPath` | `string` | No | Project path for the new TerrainData asset (Assets/...asset). Defaults to Assets/TerrainData_<name>.asset. |
| `heightmapResolution` | `integer` | No | Heightmap resolution. Rounded up to a valid (2^n + 1) value. |
| `width` | `number` | No | Terrain width in world units (X axis). |
| `length` | `number` | No | Terrain length in world units (Z axis). |
| `height` | `number` | No | Terrain height in world units (Y axis). |
| `position` | `string` | No | World-space position of the terrain GameObject. RQL: Vector3 |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "name": {
      "type": "string"
    },
    "terrainDataAssetPath": {
      "type": "string"
    },
    "heightmapResolution": {
      "type": "integer"
    },
    "width": {
      "type": "number"
    },
    "length": {
      "type": "number"
    },
    "height": {
      "type": "number"
    },
    "position": {
      "type": "string"
    }
  }
}
```

## Output

This tool does not return structured output.

