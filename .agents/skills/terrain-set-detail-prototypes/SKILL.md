---
name: terrain-set-detail-prototypes
description: Replace the detail prototypes (grass / detail meshes) of a `Terrain` with a new set built from texture or prefab asset paths. Returns the resulting prototype count.
metadata:
  generated-by: mcp-plugin-dotnet
---

# Terrain / Set Detail Prototypes

Replace `TerrainData.detailPrototypes` with a new set.

## Inputs

- `gameObjectRef` — the GameObject hosting the `Terrain` (required).
- `textureAssetPaths` — optional list of `Texture2D` asset paths; each becomes a Grass-billboard detail prototype.
- `prefabAssetPaths` — optional list of prefab/GameObject asset paths; each becomes a VertexLit detail-mesh prototype.

At least one of the two lists must be non-empty.

## Behavior

Loads each asset, builds a `DetailPrototype` (texture → `usePrototypeMesh=false`+`prototypeTexture`, prefab → `usePrototypeMesh=true`+`prototype`), assigns the array to `TerrainData.detailPrototypes`, marks dirty + repaints, and returns the count. Destructive (replaces existing prototypes). Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool terrain-set-detail-prototypes --input '{
  "gameObjectRef": "string_value",
  "textureAssetPaths": [],
  "prefabAssetPaths": []
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool terrain-set-detail-prototypes --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool terrain-set-detail-prototypes --input-file - <<'EOF'
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
| `textureAssetPaths` | `array` | No | Optional Texture2D asset paths; each becomes a grass-billboard detail prototype. |
| `prefabAssetPaths` | `array` | No | Optional prefab/GameObject asset paths; each becomes a detail-mesh prototype. |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gameObjectRef": {
      "type": "string"
    },
    "textureAssetPaths": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "prefabAssetPaths": {
      "type": "array",
      "items": {
        "type": "string"
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

