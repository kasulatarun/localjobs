---
name: navigation-surface-add
description: Add and configure a `NavMeshSurface` component (from `com.unity.ai.navigation`) on a GameObject — or create a new GameObject to host it. Configure agent type, geometry-collection mode, layer mask, default area, and the box volume (size/center). Returns the GameObject reference and instanceId.
metadata:
  generated-by: mcp-plugin-dotnet
---

# Navigation / Add NavMeshSurface

Add a `NavMeshSurface` to a GameObject. A NavMeshSurface defines a region of the scene that is baked into a runtime NavMesh that agents can traverse. Use 'navigation-set-bake-settings' to tune the agent radius/height/slope/step and voxel size, then 'navigation-surface-bake' to bake.

## Inputs

- `gameObjectRef` — optional GameObject to add the surface to. When omitted, a new GameObject is created.
- `name` — optional name for the new GameObject (default `NavMesh Surface`); ignored when `gameObjectRef` is given.
- `agentTypeId` — optional NavMesh agent-type id this surface bakes for (default 0 = Humanoid).
- `collectObjects` — optional geometry collection mode: `0` All, `1` Volume, `2` Children (default 0 All).
- `defaultArea` — optional default NavMesh area index applied to collected geometry (default 0 = Walkable).
- `layerMask` — optional include-layers bitmask for geometry collection (default -1 = Everything).
- `size` — optional box volume size (only used when `collectObjects` = Volume).
- `center` — optional box volume center offset.

## Behavior

Adds (or reuses) a `NavMeshSurface`, assigns the configured properties, marks the scene dirty, repaints, and returns the GameObject reference, the surface component reference, and the instanceId. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool navigation-surface-add --input '{
  "gameObjectRef": "string_value",
  "name": "string_value",
  "agentTypeId": 0,
  "collectObjects": 0,
  "defaultArea": 0,
  "layerMask": 0,
  "size": "string_value",
  "center": "string_value"
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool navigation-surface-add --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool navigation-surface-add --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gameObjectRef` | `string` | No | Optional GameObject to add the NavMeshSurface to. When omitted, a new GameObject is created. RQL: GameObjectRef |
| `name` | `string` | No | Name for the new GameObject (ignored when gameObjectRef is provided). |
| `agentTypeId` | `integer` | No | NavMesh agent-type id this surface bakes for (0 = Humanoid by default). |
| `collectObjects` | `integer` | No | Geometry collection mode: 0 = All, 1 = Volume, 2 = Children. |
| `defaultArea` | `integer` | No | Default NavMesh area index applied to collected geometry (0 = Walkable). |
| `layerMask` | `integer` | No | Include-layers bitmask for geometry collection (-1 = Everything). |
| `size` | `string` | No | Box volume size (used only when collectObjects = Volume). RQL: Vector3 |
| `center` | `string` | No | Box volume center offset. RQL: Vector3 |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gameObjectRef": {
      "type": "string"
    },
    "name": {
      "type": "string"
    },
    "agentTypeId": {
      "type": "integer"
    },
    "collectObjects": {
      "type": "integer"
    },
    "defaultArea": {
      "type": "integer"
    },
    "layerMask": {
      "type": "integer"
    },
    "size": {
      "type": "string"
    },
    "center": {
      "type": "string"
    }
  }
}
```

## Output

This tool does not return structured output.

