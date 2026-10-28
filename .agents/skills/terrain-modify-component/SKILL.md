---
name: terrain-modify-component
description: "Generic write: apply a `SerializedMember` diff to a terrain-related `Component` (`Terrain` or `TerrainCollider`) via ReflectorNet `TryModify`. Use 'terrain-get-component' first to inspect the structure. Route fields through the `fields` channel and properties through `props`."
metadata:
  generated-by: mcp-plugin-dotnet
---

# Terrain / Modify Component (generic)

Modify a terrain component by applying a `SerializedMember` diff via ReflectorNet.

## Inputs

- `gameObjectRef` — the GameObject hosting the component (required).
- `data` — the `SerializedMember` diff to apply. Put C# *fields* in the `fields` channel and *properties* in the `props` channel (ReflectorNet resolves them separately — no cross-fallback).
- `componentRef` — optional. Resolves a specific component when the GameObject has more than one; otherwise the first `Terrain` (or `TerrainCollider`) is used.

## Behavior

Finds the target terrain component, applies the diff via `Reflector.TryModify`, and on success marks the component + scene dirty and repaints. The applied logs are returned. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool terrain-modify-component --input '{
  "gameObjectRef": "string_value",
  "data": "string_value",
  "componentRef": "string_value"
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool terrain-modify-component --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool terrain-modify-component --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gameObjectRef` | `string` | Yes | Reference to the GameObject containing the terrain component. RQL: GameObjectRef |
| `data` | `string` | Yes | The SerializedMember diff to apply. Fields via the 'fields' channel, properties via 'props'. RQL: SerializedMember |
| `componentRef` | `string` | No | Optional reference to a specific component if the GameObject has multiple. RQL: ComponentRef |

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

