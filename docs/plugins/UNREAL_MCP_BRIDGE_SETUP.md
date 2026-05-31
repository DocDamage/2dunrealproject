# Unreal MCP Bridge Setup

**Repository:** `https://github.com/DocDamage/ue5-mcp-bridge`
**Project plugin:** `F:\Nocturne Signal\2dunrealproject\Plugins\UnrealMCPBridge`
**Plugin name:** `UnrealMCPBridge`
**Editor endpoint:** `127.0.0.1:30020`

## Unreal Project Entry

```json
{
  "Name": "UnrealMCPBridge",
  "Enabled": true
}
```

## Codex MCP Wrapper

The UE plugin exposes a TCP JSON bridge from the editor. Codex uses a local stdio MCP wrapper to forward calls into that TCP bridge:

```text
C:\Users\Doc\.codex\external\ue5-mcp-bridge-mcp
```

Codex config:

```toml
[mcp_servers.unreal-mcp-bridge]
command = "uv"
args = ["--directory", "C:\\Users\\Doc\\.codex\\external\\ue5-mcp-bridge-mcp", "run", "ue5_mcp_bridge_server.py"]
startup_timeout_sec = 30
```

## Verification

1. Restart Unreal Editor so the new project plugin can compile/load.
2. Confirm the editor log reports that the MCP bridge is listening on `127.0.0.1:30020`.
3. Restart Codex so the new MCP config is loaded.
4. Use the `unreal_mcp_ping` tool to verify editor connectivity.

## Current Verified State

Verified on 2026-05-30:

```text
Editor process: UnrealEditor.exe
Project: F:\Nocturne Signal\2dunrealproject\NocturneSignal.uproject
Bridge listeners: 127.0.0.1:30020, 0.0.0.0:30020, 127.0.0.1:30010
Engine: 5.7.4-51494982+++UE5+Release-5.7
Project name reported by MCP: 2dunrealproject
```

Known-good smoke calls:

```text
unreal_mcp_ping
editor.engine_version {}
editor.project_name {}
level.current_map {}
asset.exists {"path": "/Game/NocturneSignal/Characters/Jacob/SK_Jacob.SK_Jacob"}
```

For paginated asset queries, use the bridge's expected filter object shape:

```json
{
  "filter": {
    "package_paths": ["/Game/NocturneSignal/Characters/Jacob"],
    "recursive_paths": true
  },
  "page_size": 20
}
```

For animation sequence listings, keep the query narrow and paginated:

```json
{
  "path_prefix": "/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/RamsterZ",
  "page_size": 10
}
```

Avoid broad or incorrectly shaped calls such as `anim.list_sequences` over all Jacob retargeted animations without `page_size`, or `asset.list` with a top-level `path` field. Those can appear as MCP timeouts even when the bridge itself is healthy.

If Unreal is open while large `.uasset` folders are copied into `Content/`, the asset registry can log temporary `OpenFile failed` warnings for locked files. Restarting the editor or rescanning after the copy is complete is the clean recovery path.
