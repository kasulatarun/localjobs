---
name: terrain-set-size
description: Set the world-space size of a `Terrain`'s `TerrainData` — width (X), height (Y), and length (Z). Omitted components keep their current value.
metadata:
  generated-by: mcp-plugin-dotnet
---

# Terrain / Set Size

Set the world-space size of a `Terrain`'s `TerrainData`.

## Inputs

- `gameObjectRef` — the GameObject hosting the `Terrain` (required).
- `width` — optional new width in world units (X). When omitted, the current width is kept.
- `height` — optional new height in world units (Y). When omitted, the current height is kept.
- `length` — optional new length in world units (Z). When omitted, the current length is kept.

## Behavior

Assigns `TerrainData.size` from the provided components (falling back to the current value for any omitted axis). Marks the asset + scene dirty and repaints. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool terrain-set-size --input '{
  "gameObjectRef": "string_value",
  "width": 0,
  "height": 0,
  "length": 0
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool terrain-set-size --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool terrain-set-size --input-file - <<'EOF'
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
| `width` | `number` | No | Optional new terrain width in world units (X axis). |
| `height` | `number` | No | Optional new terrain height in world units (Y axis). |
| `length` | `number` | No | Optional new terrain length in world units (Z axis). |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gameObjectRef": {
      "type": "string"
    },
    "width": {
      "type": "number"
    },
    "height": {
      "type": "number"
    },
    "length": {
      "type": "number"
    }
  },
  "required": [
    "gameObjectRef"
  ]
}
```

## Output

This tool does not return structured output.

