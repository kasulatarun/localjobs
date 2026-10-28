---
name: terrain-set-tree-prototypes
description: Replace the tree prototypes of a `Terrain` with a new set built from prefab/GameObject asset paths. Returns the resulting prototype count.
metadata:
  generated-by: mcp-plugin-dotnet
---

# Terrain / Set Tree Prototypes

Replace `TerrainData.treePrototypes` with a new set built from prefab asset paths.

## Inputs

- `gameObjectRef` — the GameObject hosting the `Terrain` (required).
- `prefabAssetPaths` — list of prefab/GameObject asset paths; each becomes a `TreePrototype` (required, non-empty).

## Behavior

Loads each prefab, builds a `TreePrototype` with `prefab` set, assigns the array to `TerrainData.treePrototypes`, marks dirty + repaints, and returns the count. Destructive (replaces existing prototypes; existing placed tree instances may need re-placing). Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool terrain-set-tree-prototypes --input '{
  "gameObjectRef": "string_value",
  "prefabAssetPaths": []
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool terrain-set-tree-prototypes --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool terrain-set-tree-prototypes --input-file - <<'EOF'
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
| `prefabAssetPaths` | `array` | Yes | Prefab/GameObject asset paths; each becomes a TreePrototype. |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gameObjectRef": {
      "type": "string"
    },
    "prefabAssetPaths": {
      "type": "array",
      "items": {
        "type": "string"
      }
    }
  },
  "required": [
    "gameObjectRef",
    "prefabAssetPaths"
  ]
}
```

## Output

This tool does not return structured output.

