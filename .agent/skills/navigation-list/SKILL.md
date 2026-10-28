---
name: navigation-list
description: List every `NavMeshSurface` and `NavMeshAgent` in the active scene with their key settings (agent type, baked-data presence for surfaces; speed, on-NavMesh state for agents). Read-only.
metadata:
  generated-by: mcp-plugin-dotnet
---

# Navigation / List Surfaces and Agents

Enumerate the NavMesh components in the active scene so you can inspect what is set up.

## Inputs

- `includeInactive` (bool, default true) — include components on inactive/disabled GameObjects.

## Behavior

Finds all `NavMeshSurface` and `NavMeshAgent` instances, reports each surface's agent-type id and whether it has baked NavMeshData, and each agent's agent-type id, speed, and whether it is currently on a NavMesh. Read-only. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool navigation-list --input '{
  "includeInactive": false
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool navigation-list --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool navigation-list --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `includeInactive` | `boolean` | No | If true (default), include components on inactive/disabled GameObjects. |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "includeInactive": {
      "type": "boolean"
    }
  }
}
```

## Output

This tool does not return structured output.

