---
name: navigation-modify
description: "Generic write: apply a `SerializedMember` diff to any NavMesh `Component` on a GameObject via ReflectorNet `TryModify`. Use 'navigation-get' first to inspect the structure so the diff is targeted. Remember: fields go through the `fields` channel, properties through `props`."
metadata:
  generated-by: mcp-plugin-dotnet
---

# Navigation / Modify Component

Modify any NavMesh component on a GameObject by applying a `SerializedMember` diff via ReflectorNet. This is the generic escape hatch for fields not covered by the dedicated tools.

## Inputs

- `gameObjectRef` — the GameObject hosting the component (required).
- `data` — the `SerializedMember` diff to apply. Include only the members you want to change. C# fields must be supplied through the `fields` channel and properties through `props` (no cross-fallback).
- `componentRef` — optional. Resolves a specific component when the GameObject has more than one NavMesh component; otherwise the first recognized NavMesh component is used.

## Behavior

Finds the target NavMesh component, applies the diff via `Reflector.TryModify`, and on success marks the component + scene dirty and repaints. The applied logs are returned. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool navigation-modify --input '{
  "gameObjectRef": "string_value",
  "data": "string_value",
  "componentRef": "string_value"
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool navigation-modify --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool navigation-modify --input-file - <<'EOF'
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
| `data` | `string` | Yes | The SerializedMember diff to apply. Only include members you want to change. RQL: SerializedMember |
| `componentRef` | `string` | No | Optional reference to a specific NavMesh component if the GameObject has multiple. RQL: ComponentRef |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gameObjectRef": {
      "type": "string"
    },
    "data": {
      "type": "string"
    },
    "componentRef": {
      "type": "string"
    }
  },
  "required": [
    "gameObjectRef",
    "data"
  ]
}
```

## Output

This tool does not return structured output.

