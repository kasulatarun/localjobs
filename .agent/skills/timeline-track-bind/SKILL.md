---
name: timeline-track-bind
description: Bind a scene object to a Timeline output track via a `PlayableDirector` generic binding — e.g. point an AnimationTrack at an `Animator`, or an ActivationTrack at a GameObject. The director must already play the timeline that owns the track.
metadata:
  generated-by: mcp-plugin-dotnet
---

# Timeline / Bind Track

Set the scene-object binding for a specific output track on a `PlayableDirector`. The director's `playableAsset` must be the `TimelineAsset` that owns the track. For an `AnimationTrack` the binding is typically an `Animator`; for an `ActivationTrack`/`AudioTrack` it is the GameObject / AudioSource that the track drives.

## Inputs

- `directorRef` — GameObject hosting the `PlayableDirector` that plays the timeline (required).
- `trackName` / `trackIndex` — which output track to bind (name wins; index default 0).
- `targetRef` — the scene GameObject to bind to the track. When the track expects a `Component` (e.g. Animator/AudioSource), the matching component on this GameObject is used; otherwise the GameObject itself is bound.
- `clearBinding` — when true, clears the binding instead of setting it (ignored if `targetRef` is given).

## Behavior

Resolves the director and its timeline, finds the track, computes the binding object (component when the track output type is a Component, else the GameObject), calls `SetGenericBinding`, marks the scene dirty, and returns the bound object's name. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool timeline-track-bind --input '{
  "directorRef": "string_value",
  "trackName": "string_value",
  "trackIndex": 0,
  "targetRef": "string_value",
  "clearBinding": false
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool timeline-track-bind --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool timeline-track-bind --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `directorRef` | `string` | Yes | Reference to the GameObject hosting the PlayableDirector that plays the timeline. RQL: GameObjectRef |
| `trackName` | `string` | No | Name of the output track to bind. Takes precedence over trackIndex. |
| `trackIndex` | `integer` | No | Zero-based root-track index, used when trackName is null/empty. |
| `targetRef` | `string` | No | Scene GameObject to bind to the track (its matching component is used when the track expects one). RQL: GameObjectRef |
| `clearBinding` | `boolean` | No | If true, clears the track binding (ignored when targetRef is provided). |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "directorRef": {
      "type": "string"
    },
    "trackName": {
      "type": "string"
    },
    "trackIndex": {
      "type": "integer"
    },
    "targetRef": {
      "type": "string"
    },
    "clearBinding": {
      "type": "boolean"
    }
  },
  "required": [
    "directorRef"
  ]
}
```

## Output

This tool does not return structured output.

