---
name: navigation-get
description: "Generic read: serialize any NavMesh `Component` (NavMeshSurface / NavMeshModifier / NavMeshModifierVolume / NavMeshLink / NavMeshAgent) on a GameObject via ReflectorNet. Pair with 'navigation-modify' to write changes back. Read-only."
metadata:
  generated-by: mcp-plugin-dotnet
---

# Navigation / Get Component

Serialize any NavMesh component on a GameObject using ReflectorNet. This is the generic escape hatch for fields not covered by the dedicated tools.

## Inputs

- `gameObjectRef` — the GameObject hosting the component (required).
- `componentRef` — optional. Resolves a specific component when the GameObject has more than one NavMesh component; otherwise the first recognized NavMesh component is used.
- `deepSerialization` — when `true`, recurses through nested objects; otherwise only top-level members.

## Behavior

Finds the target NavMesh component, serializes it via ReflectorNet, and returns the serialized member plus the resolved component type name. Read-only. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool navigation-get --input '{
  "gameObjectRef": "string_value",
  "componentRef": "string_value",
  "deepSerialization": false
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool navigation-get --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool navigation-get --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gameObjectRef` | `string` | Yes | Reference to the GameObject containing the NavMesh component. RQL: GameObjectRef |
| `componentRef` | `string` | No | Optional reference to a specific NavMesh component if the GameObject has multiple. RQL: ComponentRef |
| `deepSerialization` | `boolean` | No | Performs deep serialization including nested objects. Otherwise only top-level members. |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gameObjectRef": {
      "type": "string"
    },
    "componentRef": {
      "type": "string"
    },
    "deepSerialization": {
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

