---
name: timeline-director-bind
description: Bind a `TimelineAsset` to a scene GameObject's `PlayableDirector` (adding the component if missing). Optionally set the play-on-awake flag. Returns the director's GameObject and instanceId.
metadata:
  generated-by: mcp-plugin-dotnet
---

# Timeline / Bind PlayableDirector

Assign a `TimelineAsset` as the playable of a scene `PlayableDirector` so the timeline can be played at runtime/in the editor. If the GameObject has no `PlayableDirector`, one is added.

## Inputs

- `gameObjectRef` — the scene GameObject to host/own the `PlayableDirector` (required).
- `assetPath` — the `.playable` TimelineAsset to bind (required).
- `playOnAwake` — optional flag to set `PlayableDirector.playOnAwake`.

## Behavior

Resolves the GameObject, ensures a `PlayableDirector`, sets `playableAsset` to the loaded `TimelineAsset`, applies `playOnAwake` when provided, marks the scene dirty, and returns the director GameObject reference + instanceId. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool timeline-director-bind --input '{
  "gameObjectRef": "string_value",
  "assetPath": "string_value",
  "playOnAwake": false
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool timeline-director-bind --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool timeline-director-bind --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gameObjectRef` | `string` | Yes | Reference to the scene GameObject that should own the PlayableDirector. RQL: GameObjectRef |
| `assetPath` | `string` | Yes | Assets-rooted path to the TimelineAsset (.playable) to bind. |
| `playOnAwake` | `boolean` | No | Optional value for PlayableDirector.playOnAwake. |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gameObjectRef": {
      "type": "string"
    },
    "assetPath": {
      "type": "string"
    },
    "playOnAwake": {
      "type": "boolean"
    }
  },
  "required": [
    "gameObjectRef",
    "assetPath"
  ]
}
```

## Output

This tool does not return structured output.

