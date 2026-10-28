---
name: splines-modify
description: "Generic write: apply a `SerializedMember` diff to any Splines `Component` on a GameObject via ReflectorNet `TryModify`. Use 'splines-get' first to inspect the structure so the diff is targeted. Fields go through the `fields` channel, properties through `props` (no cross-fallback)."
metadata:
  generated-by: mcp-plugin-dotnet
---

# Splines / Modify Component

Modify any Splines component on a GameObject by applying a `SerializedMember` diff via ReflectorNet. This is the generic escape hatch for fields not covered by the dedicated tools.

## Inputs

- `gameObjectRef` — the GameObject hosting the component (required).
- `data` — the `SerializedMember` diff to apply. Public fields MUST be supplied through the `fields` channel and properties through `props`; ReflectorNet does not cross-fall-back.
- `componentRef` — optional. Resolves a specific component when the GameObject has more than one Splines component; otherwise the first component in the `UnityEngine.Splines` namespace is used.

## Behavior

Finds the target Splines component, applies the diff via `Reflector.TryModify`, and on success marks the component + scene dirty and repaints. The applied logs are returned. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool splines-modify --input '{
  "gameObjectRef": "string_value",
  "data": "string_value",
  "componentRef": "string_value"
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool splines-modify --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool splines-modify --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gameObjectRef` | `string` | Yes | Reference to the GameObject containing the Splines component. RQL: GameObjectRef |
| `data` | `string` | Yes | The SerializedMember diff to apply. Only include members you want to change. RQL: SerializedMember |
| `componentRef` | `string` | No | Optional reference to a specific Splines component if the GameObject has multiple. RQL: ComponentRef |

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

