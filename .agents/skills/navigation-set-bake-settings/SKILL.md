---
name: navigation-set-bake-settings
description: Tune NavMesh bake settings. Agent radius / height / max-slope / step-height belong to a NavMesh agent type (in project NavMesh settings) and apply to every surface baking for that type. The voxel size is a per-surface override; pass `gameObjectRef` (a NavMeshSurface) with `voxelSize` to set it.
metadata:
  generated-by: mcp-plugin-dotnet
---

# Navigation / Set Bake Settings

Configure the parameters that control how a NavMesh is voxelized and baked.

Agent radius / height / max-slope / step-height are stored on the **agent type** (id `agentTypeId`, default 0 = Humanoid) in the project's NavMesh settings, so they affect all surfaces baking for that type. The **voxel size** is a per-`NavMeshSurface` override.

## Inputs

- `agentTypeId` — the NavMesh agent type to edit (default 0 = Humanoid).
- `agentRadius` — optional agent radius (meters).
- `agentHeight` — optional agent height (meters).
- `maxSlope` — optional maximum walkable slope (degrees, 0–60).
- `stepHeight` — optional maximum step / climb height (meters).
- `gameObjectRef` — optional NavMeshSurface GameObject whose voxel-size override to set.
- `voxelSize` — optional voxel size for that surface (only applied when `gameObjectRef` is provided; sets `overrideVoxelSize = true`).

## Behavior

Edits the agent type's bake settings via the `NavMeshProjectSettings` serialized object (only the provided values change), and optionally enables and sets the surface voxel-size override. Marks dirty and repaints. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool navigation-set-bake-settings --input '{
  "agentTypeId": 0,
  "agentRadius": 0,
  "agentHeight": 0,
  "maxSlope": 0,
  "stepHeight": 0,
  "gameObjectRef": "string_value",
  "voxelSize": 0
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool navigation-set-bake-settings --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool navigation-set-bake-settings --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `agentTypeId` | `integer` | No | NavMesh agent-type id to edit (0 = Humanoid by default). |
| `agentRadius` | `number` | No | Agent radius in meters. |
| `agentHeight` | `number` | No | Agent height in meters. |
| `maxSlope` | `number` | No | Maximum walkable slope in degrees (0-60). |
| `stepHeight` | `number` | No | Maximum step / climb height in meters. |
| `gameObjectRef` | `string` | No | Optional NavMeshSurface GameObject whose voxel-size override to set. RQL: GameObjectRef |
| `voxelSize` | `number` | No | Voxel size for the surface (applied only when gameObjectRef is provided). |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "agentTypeId": {
      "type": "integer"
    },
    "agentRadius": {
      "type": "number"
    },
    "agentHeight": {
      "type": "number"
    },
    "maxSlope": {
      "type": "number"
    },
    "stepHeight": {
      "type": "number"
    },
    "gameObjectRef": {
      "type": "string"
    },
    "voxelSize": {
      "type": "number"
    }
  }
}
```

## Output

This tool does not return structured output.

