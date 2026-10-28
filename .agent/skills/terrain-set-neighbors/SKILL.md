---
name: terrain-set-neighbors
description: Set the neighboring `Terrain`s of a center `Terrain` (left / top / right / bottom) so Unity blends seams and LOD across tiles. Omitted neighbors are treated as null.
metadata:
  generated-by: mcp-plugin-dotnet
---

# Terrain / Set Neighbors

Wire up the neighbor terrains of a center `Terrain` via `Terrain.SetNeighbors`.

## Inputs

- `gameObjectRef` — the center Terrain GameObject (required).
- `leftRef` / `topRef` / `rightRef` / `bottomRef` — optional GameObjects hosting the neighboring `Terrain`s. Any omitted side is set to null.

## Behavior

Resolves each provided neighbor GameObject to its `Terrain` component, calls `center.SetNeighbors(left, top, right, bottom)`, and triggers `Terrain.Flush()`. Marks the scene dirty and repaints. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool terrain-set-neighbors --input '{
  "gameObjectRef": "string_value",
  "leftRef": "string_value",
  "topRef": "string_value",
  "rightRef": "string_value",
  "bottomRef": "string_value"
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool terrain-set-neighbors --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool terrain-set-neighbors --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gameObjectRef` | `string` | Yes | Reference to the center Terrain GameObject. RQL: GameObjectRef |
| `leftRef` | `string` | No | Optional GameObject hosting the left neighbor Terrain. RQL: GameObjectRef |
| `topRef` | `string` | No | Optional GameObject hosting the top neighbor Terrain. RQL: GameObjectRef |
| `rightRef` | `string` | No | Optional GameObject hosting the right neighbor Terrain. RQL: GameObjectRef |
| `bottomRef` | `string` | No | Optional GameObject hosting the bottom neighbor Terrain. RQL: GameObjectRef |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gameObjectRef": {
      "type": "string"
    },
    "leftRef": {
      "type": "string"
    },
    "topRef": {
      "type": "string"
    },
    "rightRef": {
      "type": "string"
    },
    "bottomRef": {
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

