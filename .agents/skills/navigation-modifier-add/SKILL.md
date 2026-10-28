---
name: navigation-modifier-add
description: Add and configure a `NavMeshModifier` on a GameObject. A NavMeshModifier overrides how that object (and optionally its children) is treated during baking — its NavMesh area, whether it is ignored, and link generation.
metadata:
  generated-by: mcp-plugin-dotnet
---

# Navigation / Add NavMeshModifier

Add a `NavMeshModifier` to a GameObject so its geometry is baked with overridden parameters.

## Inputs

- `gameObjectRef` — the GameObject to add the modifier to (required).
- `overrideArea` — when `true`, the object's NavMesh area is overridden with `area`.
- `area` — the NavMesh area index to assign when `overrideArea` is true (default 0 = Walkable).
- `ignoreFromBuild` — when `true`, the object is excluded from the bake entirely.
- `applyToChildren` — when `true`, the override also applies to child objects.

## Behavior

Adds (or reuses) a `NavMeshModifier`, assigns the configured flags, marks the scene dirty, and repaints. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool navigation-modifier-add --input '{
  "gameObjectRef": "string_value",
  "overrideArea": false,
  "area": 0,
  "ignoreFromBuild": false,
  "applyToChildren": false
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool navigation-modifier-add --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool navigation-modifier-add --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gameObjectRef` | `string` | Yes | Reference to the GameObject to add the NavMeshModifier to. RQL: GameObjectRef |
| `overrideArea` | `boolean` | No | If true, override the NavMesh area of this object with 'area'. |
| `area` | `integer` | No | NavMesh area index to assign when overrideArea is true (0 = Walkable). |
| `ignoreFromBuild` | `boolean` | No | If true, exclude this object from the NavMesh bake. |
| `applyToChildren` | `boolean` | No | If true, apply the override to child objects as well. |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gameObjectRef": {
      "type": "string"
    },
    "overrideArea": {
      "type": "boolean"
    },
    "area": {
      "type": "integer"
    },
    "ignoreFromBuild": {
      "type": "boolean"
    },
    "applyToChildren": {
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

