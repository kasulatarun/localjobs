---
name: navigation-link-add
description: Add and configure a `NavMeshLink` on a GameObject. A NavMeshLink connects two points on (or off) the NavMesh — e.g. a jump-across or a doorway — so agents can traverse gaps the baked mesh does not cover. Points are local to the GameObject's transform.
metadata:
  generated-by: mcp-plugin-dotnet
---

# Navigation / Add NavMeshLink

Add a `NavMeshLink` to a GameObject. The link bridges `startPoint` and `endPoint` (in the GameObject's local space), letting agents cross between otherwise-disconnected NavMesh regions.

## Inputs

- `gameObjectRef` — the GameObject to add the link to (required).
- `startPoint` — local-space start of the link (default 0,0,-2.5).
- `endPoint` — local-space end of the link (default 0,0,2.5).
- `width` — link width in meters (default 0).
- `bidirectional` — when `true`, the link is traversable both ways (default true).
- `costModifier` — cost override; negative means use the default cost (default -1).
- `area` — NavMesh area index of the link (default 2 = Jump).

## Behavior

Adds (or reuses) a `NavMeshLink`, assigns the configured fields (which auto-rebuild the link), marks the scene dirty, and repaints. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool navigation-link-add --input '{
  "gameObjectRef": "string_value",
  "startPoint": "string_value",
  "endPoint": "string_value",
  "width": 0,
  "bidirectional": false,
  "costModifier": 0,
  "area": 0
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool navigation-link-add --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool navigation-link-add --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gameObjectRef` | `string` | Yes | Reference to the GameObject to add the NavMeshLink to. RQL: GameObjectRef |
| `startPoint` | `string` | No | Local-space start point of the link. RQL: Vector3 |
| `endPoint` | `string` | No | Local-space end point of the link. RQL: Vector3 |
| `width` | `number` | No | Link width in meters. |
| `bidirectional` | `boolean` | No | If true, the link is traversable in both directions. |
| `costModifier` | `integer` | No | Cost modifier for traversing the link; negative uses the default cost. |
| `area` | `integer` | No | NavMesh area index of the link (2 = Jump by default). |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gameObjectRef": {
      "type": "string"
    },
    "startPoint": {
      "type": "string"
    },
    "endPoint": {
      "type": "string"
    },
    "width": {
      "type": "number"
    },
    "bidirectional": {
      "type": "boolean"
    },
    "costModifier": {
      "type": "integer"
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

