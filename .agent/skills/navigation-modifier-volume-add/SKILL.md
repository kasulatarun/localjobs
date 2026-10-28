---
name: navigation-modifier-volume-add
description: Add and configure a `NavMeshModifierVolume` on a GameObject. A modifier volume marks a box-shaped region of space so that any NavMesh baked inside it is assigned a specific area (e.g. a non-walkable or higher-cost zone).
metadata:
  generated-by: mcp-plugin-dotnet
---

# Navigation / Add NavMeshModifierVolume

Add a `NavMeshModifierVolume` to a GameObject. Unlike a NavMeshModifier (which is tied to geometry), a volume affects whatever NavMesh is generated inside its box region.

## Inputs

- `gameObjectRef` — the GameObject to add the volume to (required).
- `size` — the box size of the volume (default 4,4,4).
- `center` — the box center offset (default 0,0,0).
- `area` — the NavMesh area index assigned inside the volume (default 0 = Walkable).

## Behavior

Adds (or reuses) a `NavMeshModifierVolume`, assigns size / center / area, marks the scene dirty, and repaints. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool navigation-modifier-volume-add --input '{
  "gameObjectRef": "string_value",
  "size": "string_value",
  "center": "string_value",
  "area": 0
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool navigation-modifier-volume-add --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool navigation-modifier-volume-add --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gameObjectRef` | `string` | Yes | Reference to the GameObject to add the NavMeshModifierVolume to. RQL: GameObjectRef |
| `size` | `string` | No | Box size of the volume. RQL: Vector3 |
| `center` | `string` | No | Box center offset of the volume. RQL: Vector3 |
| `area` | `integer` | No | NavMesh area index assigned inside the volume (0 = Walkable). |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gameObjectRef": {
      "type": "string"
    },
    "size": {
      "type": "string"
    },
    "center": {
      "type": "string"
    },
    "area": {
      "type": "integer"
    }
  },
  "required": [
    "gameObjectRef"
  ]
}
```

## Output

This tool does not return structured output.

