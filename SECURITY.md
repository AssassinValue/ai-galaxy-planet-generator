# Security Policy

## Supported versions

| Version | Supported |
| ------- | --------- |
| 0.9.x   | yes       |
| 0.8.x   | no        |

## Scope

`ai-galaxy-planet-generator` is an offline desktop tool. It does not
open network sockets, does not phone home, and does not auto-update.
The only external surface is the filesystem: it reads preset YAML and
writes `.gfp` / `.gfx` / `.hmap` artifacts to a user-chosen directory.

Linux and macOS builds are unsupported and untested.

## Threat model

- **Malicious preset YAML.** Presets are parsed with `yaml.safe_load`
  only. Never `yaml.load`. If you find a code path using `yaml.load`,
  open a security issue immediately.
- **Malicious `.gfp` / `.gfx` files.** These are loaded via
  `pickle`-free parsing — the format is a length-prefixed binary blob
  with a JSON header. Report any deserialization path that touches
  `pickle`, `marshal`, or `torch.load(weights_only=False)`.
- **Model weight files.** `.pt` files are loaded with
  `torch.load(..., weights_only=True)`. Do not disable this.
- **Path traversal.** All export paths go through
  `adapters/win_paths.safe_join`. Report any service writing to a
  path built from unvalidated user input.

## Reporting a vulnerability

Email `security@potatolabs.dev` with a reproducer. Do not open a
public issue for deserialization or path-traversal bugs.

We aim to respond within 72 hours.