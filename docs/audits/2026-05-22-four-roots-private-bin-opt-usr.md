# Forensic Context Map — `/private`, `/bin`, `/opt`, `/usr`

**Captured:** 2026-05-22 · macOS 26.5 Tahoe Beta · ARM64 (M5) · 16 GB RAM
**Scope:** every package source, every shell, every PATH contributor, every drift from CLAUDE.md.

## TL;DR — the disaster, ranked

| # | Severity | Finding | Where |
|---|---|---|---|
| 1 | **P0 SEC** | `com.jupyter.server.plist` LaunchAgent runs on boot with **empty token + `allow_origin=*` + XSRF disabled** on `:8888`. Any browser tab can spawn a Python kernel → arbitrary RCE. Also a Rule #9 hard-rule violation. | `~/Library/LaunchAgents/com.jupyter.server.plist` (target: `~/.local/share/uv/tools/jupyter-core/bin/jupyter-server`) |
| 2 | P1 GOV | Home `CLAUDE.md` says "Python: Anaconda at `/opt/anaconda3/`". **`/opt/anaconda3` does not exist. `conda` is not on PATH.** Constitution lies. | `~/CLAUDE.md` §"Development Environment" |
| 3 | P1 GOV | **Three brew-managed LaunchAgents exist** (`jupyter`, `atuin`, `ollama`) directly contradicting Rule #9's "no LaunchAgents anywhere" HARD RULE. Either the rule needs a brew-services exemption or these are unauthorized survivals. `ollama` is in error state (PID 1, exit 9). | `~/Library/LaunchAgents/homebrew.mxcl.{atuin,ollama}.plist` |
| 4 | P2 OPS | **pkgx ghost install at `/opt/pkg`** — `/etc/paths.d/10-pmk-global` adds `/pkg/env/global/bin` to every shell's PATH, but **`/pkg` doesn't exist at root** (it's `/opt/pkg`, and even there `inv/envs/<sha>/bin` is missing). Dead PATH entry since 2025-02-17. | `/etc/paths.d/10-pmk-global` → `/pkg/env/global/bin` |
| 5 | P2 OPS | **16 dead symlinks in `/usr/local/bin`** pointing at `PythonT.framework` (free-threaded CPython variant) — the framework itself does not exist. Probably uninstalled but symlinks orphaned. | `/usr/local/bin/python3{,.13}t*` (×16) |
| 6 | P2 OPS | **Five+ Pythons coexisting** with PATH-ordering ambiguity (active: brew `python@3.14`; second-on-PATH: python.org framework 3.13 via `/usr/local/bin`; third: Apple `/usr/bin/python3` 3.9.6). | See §3 below |
| 7 | P2 OPS | Brew cask `klatexformula` deprecated (already tracked as **IRF-OPS-060**). Brew cask `ngrok` outdated. | `brew doctor` / `brew outdated` |
| 8 | P3 INF | **Ghostty in PATH via AppTranslocation** — `/private/var/folders/l9/zn9x070d4xqb1qb5wfzr9tjr0000gn/T/AppTranslocation/.../Ghostty.app/Contents/MacOS` on PATH. Means Ghostty was opened from quarantine (Downloads) and never moved to `/Applications`. Path is ephemeral. | This shell's PATH |
| 9 | P3 STA | `/private/var/db/diagnostics` = 2.6 G + `uuidtext` 715 M + `receipts` 183 M + `locationd` 130 M. Unified-logging persistent store dominates. Normal for macOS Beta but worth knowing on a 16 GB box. | `/private/var/db/*` |
| 10 | P3 STA | **`/private/var/folders/l9/.../...` user temp = 2.7 G**, **`/private/var/vm/sleepimage` = 2.0 G**. Combined ~5 G of OS state pinned to disk. | `/private/var/folders`, `/private/var/vm` |

## 1. `/bin` — Apple sealed shells (read-only, signed)

`/bin` is on the **sealed system volume** (`/dev/disk3s1s1`, `apfs, sealed, local, read-only`). Cryptographically signed; SIP enabled; cannot be modified without disabling SIP + booting recovery + remounting r/w. 37 binaries, all timestamped `Apr 30 15:33` (Tahoe 26.5 OS-install epoch). The full inventory:

```
[ bash cat chmod cp csh dash date dd df echo ed expr hostname kill ksh
launchctl link ln ls mkdir mv pax ps pwd realpath rm rmdir sh sleep
stty sync tcsh test unlink wait4path zsh
```

**Shell-relevant facts:**

- `/bin/sh` and `/bin/bash` are **the same physical bash 3.2.57** (Apple's last legal GPLv2 bash). `/bin/sh` runs bash in POSIX mode.
- `/bin/zsh` is **zsh 5.9** — the same version as `/opt/homebrew/bin/zsh`. User's login shell is the Apple one (`dscl . -read /Users/[user] UserShell` → `/bin/zsh`), not the Homebrew copy.
- `/bin/csh` and `/bin/tcsh` are both `tcsh 6.21.00` (one binary, two names; old).
- `/bin/dash` exists for `#!/bin/dash` scripts but is not in `/etc/shells` for login.
- `/bin/ksh` is AT&T ksh93 (`93u+ 2012-08-01`). Old, but present.

`/etc/shells` (legal login shells) lists `bash, csh, dash, ksh, sh, tcsh, zsh` — all the `/bin` shells. **No Homebrew or fish shells are blessed** for login. To use brew zsh/fish/bash as login shell, would need `sudo` edit of `/etc/shells` (Apple cleared `/etc/sudoers.d/` so no privilege-escalation shim exists).

`/bin` also carries `launchctl` — the only client for `launchd`, the system's process-1 supervisor. (`launchd` itself is in `/sbin/launchd`.)

## 2. `/usr` — sealed system + writable `/usr/local`

### Sealed-volume children (read-only)

| Path | Entries | What it is |
|---|---|---|
| `/usr/bin` | 924 binaries | Apple-shipped userland: `python3` (3.9.6), `ruby` (3.x system), `perl`, `git`, `ssh`, every standard Unix tool. SIP-protected. |
| `/usr/sbin` | 228 binaries | System-admin tools (`networksetup`, `nvram`, `softwareupdate`, `system_profiler`, …). |
| `/usr/libexec` | 429 binaries/bundles | Daemons & helpers — `airportd`, `amfid` (Apple Mobile File Integrity Daemon), `apfsd`, `appleaccountd`, MLModelC files for power-management ML. The OS's internal service mesh. |
| `/usr/lib` | 32 entries | System dynamic libs visible at this level. **Note:** the real shared-library cache is `dyld_shared_cache` baked into the cryptex, not loose `.dylib` files anymore. `/usr/lib` here is mostly bridge/legacy: `libpcre2-8.dylib`, `libffi-trampolines.dylib`, etc. |
| `/usr/share` | 45 dirs | Man pages, locale data, terminfo, ssl certs (read-only). |
| `/usr/standalone` | 5 entries | Recovery/boot helpers. |

### `/usr/local` — Intel-era Homebrew prefix, now a junk drawer (18 MB total)

On Apple Silicon, Homebrew uses `/opt/homebrew`, not `/usr/local`. The `/usr/local` tree should be near-empty. Yours has only `/usr/local/bin` with **33 entries**, and they're almost all symlinks to other locations — app-bundled CLIs, the python.org framework Pythons, and the Docker.app-shipped `docker`/`kubectl`/`docker-compose` shim set.

Breakdown (`/usr/local/bin`):

- **Docker.app-shipped (5)**: `docker`, `docker-compose`, `docker-credential-{desktop,osxkeychain}`, `hub-tool`, `kubectl`, `kubectl.docker`, `cagent` → all symlinks into `/Applications/Docker.app/Contents/Resources/`.
- **VS Code variants (2)**: `code-insiders`, `cursor` → app-bundle `code` binaries.
- **App-bundle escapes (3)**: `github` (GitHub Desktop), `ollama` (Ollama.app), `oz` (Warp.app — labeled "stable").
- **Real binaries (2)**: `cht.sh` (22 KB shell script, last touched 2026-05-21), `newrelic` (19 MB arm64 binary — sole large non-symlink).
- **python.org framework symlinks (16)** — to `/Library/Frameworks/Python.framework/Versions/3.13/bin/{python3,python3.13,pip3,pydoc3,idle3}` and **eight broken targets** in `PythonT.framework` (free-threaded variant) — the framework dir does not exist. **Dead symlinks.**

**Disaster classification of `/usr/local`:** apps that bypass Homebrew (Docker, VS Code, GitHub Desktop, Ollama, Warp) install their CLI shims directly here, sidestepping `brew shellenv`'s path management. The python.org installer adds its own. Net effect: `/usr/local/bin` is on PATH ahead of `/usr/bin` (per `/etc/paths`), so these app-bundle CLIs shadow any same-named Apple binary, **and the python.org `python3.13` shadows the Apple `/usr/bin/python3` 3.9.6**.

## 3. `/opt` — third-party prefixes

```
/opt
├── homebrew/    12 GB  (ARM Homebrew prefix)
└── pkg/          0 B    (pkgx graveyard — see below)
```

### `/opt/homebrew` — 12 GB, 230 formulae, 16 casks, 0 taps

Itself a git repository (HEAD: `bc4c8a83ec Merge pull request #22369 from Homebrew/ask-default-for-developers`, 0 commits behind upstream, no uncommitted changes). Composition:

| Tree | Size | Contents |
|---|---|---|
| `Cellar/` | 6.6 G | The actual installed formula payloads, 230 dirs |
| `lib/` | 2.8 G | Shared libs from Cellar packages, linked into prefix |
| `share/` | 1.3 G | Man pages, docs, data files |
| `Caskroom/` | 1.0 G | Cask installer cache (mostly metadata; the big one is `plugdata` 737 M) |
| `var/` | 151 M | Service state (`brew services` runtime data) |
| `Library/` | 66 M | Homebrew's own internal formula/cask source |

**Top 10 disk hogs in Cellar:**

| Formula | Size | Notes |
|---|---|---|
| `llvm` | 1.7 G | Full LLVM toolchain |
| `qemu` | 679 M | VM emulator |
| `rust` | 365 M | Compiler + std |
| `block-goose-cli` | 275 M | Block (Cash App) Goose AI assistant |
| `go` | 258 M | Go SDK |
| `trivy` | 189 M | Container security scanner |
| `mlx` | 171 M | Apple's MLX ML framework |
| `kimi-cli` | 159 M | Moonshot Kimi CLI |
| `emacs`, `k9s` | 134 M each | |
| `ruby` | 119 M | brew ruby 4.0.5 |

**Top Caskroom hogs:** `plugdata` 737 M, `codex` 185 M (OpenAI Codex cask kept post-claude-code-cask-removal), `1password-cli` 37 M, `ngrok` 29 M.

**84 user-installed leaves, 245 total installed.** Net 161 are transitive dependencies — healthy ratio (~2:1 deps:leaves, no orphan candidates flagged by `brew autoremove --dry-run`).

**No third-party taps registered** (`brew tap` empty). Everything comes from `homebrew/core` and `homebrew/cask`.

**Symlink alias farm — `/opt/homebrew/opt/*`:** brew uses `opt/` to alias formula-version-pin dirs. Multiple symlinks can point to the same Cellar tree — these are **not duplicate installs**:

- `python`, `python@3`, `python3` → `Cellar/python@3.14/3.14.5` (one canonical install, three aliases)
- `node`, `node.js`, `nodejs`, `node@25`, `node@26` → `Cellar/node/26.0.0` (one install, five aliases — `node@25` lying about being v25)
- `ruby`, `ruby@3`, `ruby@3.4`, `ruby@4`, `ruby@4.0` → `Cellar/ruby/4.0.5` (one install, five aliases — `ruby@3.4` lying about being 3.4.x)

The aliases are how callers expecting `node@25` find a binary — at the cost of `node@25` actually being node 26.0.0. Mostly harmless; surprising if you script against `readlink`.

**Heavy AI-CLI cluster** (relevant to the multi-agent fleet system): `block-goose-cli`, `kimi-cli`, `gemini-cli`, `opencode`, `huggingface-cli`, `hf`, `ollama`, `llm`, plus cask `codex` and (outside brew) native `~/.local/share/claude` — **8+ agent/model CLIs locally**.

### `/opt/pkg` — pkgx graveyard

```
/opt/pkg/
├── env/active -> global
├── env/global -> /opt/pkg/inv/envs/454eea274ef715bed0aef364fec823e04318850d28eb04f1c16a03a5127c071c
├── etc/  (empty)
├── inv/   (the content-addressable env target dir IS missing or empty — fails glob expansion)
└── var/   (empty)
```

This is **pkgx** (formerly tea/pkx) — a content-addressed third package manager. Installed 2025-02-17 (root-owned), abandoned. **`/etc/paths.d/10-pmk-global` adds `/pkg/env/global/bin` to PATH** — but:

1. `/pkg` doesn't exist at filesystem root (the install is at `/opt/pkg`).
2. Even at the real prefix, `inv/envs/<sha>/bin` doesn't exist.

So **every shell session you've started since Feb 2025 has had a dead PATH entry**. The error is silent — `PATH` lookups skip nonexistent dirs — so it's been invisible. Two ways out: delete the file (sudo required) or relocate pkgx properly. The user has never invoked `pkgx`/`pkx` (no binary on PATH).

## 4. `/private` — the real backing for `/etc`, `/var`, `/tmp`

`/etc`, `/var`, `/tmp` at root are firmlinks (symlinks-with-special-semantics) to `/private/etc`, `/private/var`, `/private/tmp`. Owned by root.

### `/private/etc` — 79 entries, the system-config canon

Relevant for this audit:

| File / dir | What it does | Notes |
|---|---|---|
| `/etc/shells` | Legal login shells | 7 entries, all sealed `/bin/*` shells; no brew/fish blessed |
| `/etc/paths` | Base PATH ordering | `/usr/local/bin:/System/Cryptexes/App/usr/bin:/usr/bin:/bin:/usr/sbin:/sbin` |
| `/etc/paths.d/` | Path additions | 4 files: `10-cryptex` (Apple security update PATH), `10-pmk-global` (**dead pkgx**), `100-rvictl` (`/Library/Apple/usr/bin`), `homebrew` (`/opt/homebrew/bin`) |
| `/etc/zshrc` | System zsh init | Clobbers `HISTFILE`, `HISTSIZE=2000`, `SAVEHIST=1000`. User's `~/.config/zsh/01-history.zsh` overrides per `feedback_histfile_override`. |
| `/etc/zprofile` | System zsh login init | 304 bytes; runs `path_helper` to assemble `/etc/paths` + `/etc/paths.d/*` into `$PATH` |
| `/etc/bashrc`, `/etc/profile`, `/etc/bashrc_Apple_Terminal` | bash equivalents | Apple's Terminal.app injects session-restore code from `bashrc_Apple_Terminal` |
| `/etc/sudoers` | sudo config | Standard Apple defaults |
| `/etc/sudoers.d/` | sudo overrides | **Empty** — no privilege grants beyond default `%admin` |
| `/etc/ssh/` | SSH client/server config | `ssh_config` includes `/etc/ssh/ssh_config.d/*` |
| `/etc/pam.d/` | PAM auth modules | Apple-default |

**No `/etc/zshenv`, no `/etc/zlogin`** — Apple only ships `zprofile` and `zshrc` at system scope. The shell init order for the user's interactive login zsh:

```
/etc/zshenv (absent)  →  ~/.zshenv  →  /etc/zprofile  →  ~/.zprofile  →
/etc/zshrc            →  ~/.zshrc   →  /etc/zlogin (absent)  →  ~/.zlogin
```

The user's `~/.zshrc` is the last word for interactive vars (including the `01-history.zsh` re-assertion).

### `/private/var` — system + user state (≈7.3 G)

| Subdir | Size | What it holds |
|---|---|---|
| `db/diagnostics` | 2.6 G | Unified-logging persistent store (`/var/db/diagnostics/{Persist,Special,Live}`) |
| `db/uuidtext` | 715 M | Symbol files for unified-log decoding |
| `db/receipts` | 183 M | `/var/db/receipts/*.{plist,bom}` — every `.pkg` install's manifest, going back forever |
| `db/locationd` | 130 M | Core Location service state |
| `db/KernelExtensionManagement` | 115 M | KEXT staging (Tahoe still tracks the legacy KEXT bundle even with system extensions) |
| `db/powerlog` | 112 M | Battery + power telemetry |
| `db/accessoryupdater` | 86 M | USB/Bluetooth accessory firmware |
| `db/systemstats` | 75 M | `system_profiler`/`sysdiagnose` data |
| `db/cmiodalassistants` | 73 M | Camera/microphone (CMIO) framework state |
| `db/SystemPolicyConfiguration` | 59 M | Gatekeeper, KEXT policy, system-extension policy DB |
| `db/biome` | 55 M | Spotlight/Knowledge Graph "Biome" |
| `db/DiagnosticPipeline` | 47 M | Modern crash/diag pipeline |
| `db/CoreDuet` | 36 M | Suggestions engine (Siri/Spotlight) |
| `db/analyticsd` | 35 M | Apple analytics queue |
| `folders/l9/zn9x070d4xqb1qb5wfzr9tjr0000gn` | 2.7 G | **User [user]'s per-user temp/cache** ($TMPDIR + DerivedData area) |
| `vm/sleepimage` | 2.0 G | Hibernation RAM dump (`hibernatemode 3 + standby 1`) |
| `log/com.apple.xpc.launchd` | 19 M | launchd's own log |
| `log/install.log` | 18 M | Every package install since 2025 |

**`/private/var/db/com.apple.xpc.launchd/`** — `config/`, `disabled.501.plist` (user [user]'s disabled-services map), `disabled.plist`, `disabled.migrated`. This is where `launchctl disable user/501/com.foo.bar` writes.

### `/private/tmp` — world-writable scratch

Mostly the current and recent Claude Code session log scaffolding:
- `cc-daemon-501/` — the Claude Code daemon's tmp dir
- `claude-501/` — current session tmp dir
- `claude-mcp-browser-bridge-[user]/` — MCP browser bridge state
- `claude-session-*.unpushed.log` — 5+ zero-byte log files from today's session-start hooks
- `audit-log-queries.sh`, `audit-log-timeline.sh` — current session artifacts

Plus the recent `a-i-skills-workspace-audit.md` (11 KB, today). Routine working state; no foreign processes.

## 5. The shell layer — what runs when you type a command

### Default login shell

`dscl . -read /Users/[user] UserShell` → **`/bin/zsh`** (Apple's sealed zsh 5.9, **not** the brew zsh).

### Init cascade as it actually fires for an interactive zsh

| Stage | File | What it does on this system |
|---|---|---|
| 1 | `/etc/zshenv` | (absent) |
| 2 | `~/.zshenv` | (varies — chezmoi-managed; sets `XDG_*` per memory) |
| 3 | `/etc/zprofile` | Runs `path_helper` to merge `/etc/paths` + `/etc/paths.d/*` into `$PATH`. **Includes the dead `/pkg/env/global/bin`.** |
| 4 | `~/.zprofile` | chezmoi-managed |
| 5 | `/etc/zshrc` | Clobbers `HISTFILE` (XDG-violating), `HISTSIZE=2000`, `SAVEHIST=1000`. Disables `log` builtin. Sets `setopt BEEP`. |
| 6 | `~/.zshrc` | chezmoi-managed; includes `~/.config/zsh/01-history.zsh` to re-assert `HISTFILE` post-clobber |

### PATH as composed in this shell (39 entries — leading order matters)

```
1.  ~/.config/carapace/bin
2.  /opt/homebrew/opt/python@3/libexec/bin     ← python.python3 wins here
3.  ~/Workspace/4444J99/.../_agents/bin
4.  ~/.local/bin                       ← claude, build-contract, domus-memory-sync, etc.
5.  ~/.local/share/npm/bin
6.  ~/.local/share/cargo/bin           ← rustup, rustc, cargo
7.  ~/.local/share/go/bin
8.  /opt/homebrew/lib/ruby/gems/3.4.0/bin       ← ⚠ stale: brew ruby is 4.0.5 now
9.  /opt/homebrew/opt/ruby/bin                  ← brew ruby 4.0.5
10. /opt/homebrew/opt/file-formula/bin
11. /opt/homebrew/bin                           ← 866 brew symlinks
12. /opt/homebrew/sbin
13. /usr/local/bin                              ← 33 entries (python.org, app bundles, broken PythonT symlinks)
14. /System/Cryptexes/App/usr/bin
15. /usr/bin                                    ← Apple system
16. /bin
17. /usr/sbin
18. /sbin
19-21. /var/run/com.apple.security.cryptexd/codex.system/bootstrap/{usr/local/bin,usr/bin,usr/appleinternal/bin}
22. /pkg/env/global/bin                         ← ⚠ DEAD (pkgx ghost, see §3)
23. /Library/Apple/usr/bin
24. /private/var/folders/.../AppTranslocation/.../Ghostty.app/Contents/MacOS   ← ⚠ ephemeral
25-39. ~/.claude/plugins/cache/.../bin          ← per-plugin bin dirs from Claude Code plugin cache
```

**Three PATH problems in one place:**

- Entry 8 (`gems/3.4.0/bin`) is pinned to gems-version `3.4.0`, but brew ruby is now `4.0.5` (ATM-000258 ruby-bump backlog item visible from session startup). Likely producing missing-gem errors silently.
- Entry 22 (`/pkg/env/global/bin`) has been dead since pkgx was abandoned in Feb 2025.
- Entry 24 (Ghostty AppTranslocation) is in `$TMPDIR`-equivalent territory; vanishes when macOS rotates the translocation root.

## 6. Languages and their package managers

| Runtime | Active version | Source on disk | Manager(s) overlapping |
|---|---|---|---|
| **Python** (active) | 3.14.5 | `/opt/homebrew/Cellar/python@3.14/3.14.5` via `/opt/homebrew/opt/python@3/libexec/bin/python` | brew formula |
| Python | 3.13.x | `/opt/homebrew/Cellar/python@3.13` (transitive dep) | brew |
| Python | 3.11.x | `/opt/homebrew/Cellar/python@3.11` (transitive dep) | brew |
| Python | 3.13.x | `/Library/Frameworks/Python.framework/Versions/3.13` | python.org installer (Dec 2025) |
| Python | 3.9.6 | `/usr/bin/python3` | Apple sealed |
| **PythonT (free-threaded)** 3.13 | **MISSING** | `/Library/Frameworks/PythonT.framework` — directory does not exist | python.org installer once dropped it, now gone, **16 dangling `/usr/local/bin/python*t*` symlinks** |
| **Conda** | — | (none) | **CLAUDE.md still claims `/opt/anaconda3` but it's gone**; sole residue is `~/.conda/aau_token{,_host}` (30 B) |
| **Node** | 26.0.0 | `/opt/homebrew/Cellar/node/26.0.0` | brew |
| **npm** | (bundled with node) | `~/.local/share/npm/bin/npm` (XDG layout) | brew node + user-XDG global prefix |
| **pnpm** | (active) | `/opt/homebrew/bin/pnpm` | brew |
| **yarn / deno / bun** | — | (not installed) | — |
| **Go** | (active) | `/opt/homebrew/bin/go` → Cellar `go` 258 M | brew |
| **Rust** | (active) | `~/.local/share/cargo/bin/{rustc,cargo,rustup}` | **rustup** (not brew; brew has rust formula 365 M but PATH order puts cargo-bin first) |
| **Ruby** | 4.0.5 (brew, active) | `/opt/homebrew/opt/ruby/bin/{ruby,gem,bundle}` | brew, **plus** mise tracks ruby 3.4.8 (shadowed) |
| **Java/javac** | system | `/usr/bin/java`, `/usr/bin/javac` (Apple shims) | Apple-system |
| **pkgx** | abandoned | `/opt/pkg` (no binary on PATH; PATH entry broken) | — |

**Python tool environments:**

- `pipx`/`uv` installed via brew (user prefers them over conda).
- `uv tool list` shows **3 user-tools**: `jupyter-core 5.9.1` (provides `jupyter`, `jupyter-migrate`, `jupyter-troubleshoot`), `jupyterlab 4.5.7` (`jlpm`, `jupyter-lab`, `jupyter-labextension`, `jupyter-labhub`), `openai-whisper 20250625` (`whisper`).
- `mise` (modern asdf replacement) installed; tracks **only ruby 3.4.8** — and even that is shadowed by brew ruby's PATH precedence.
- Apple `pip3 --user` has just `PyYAML 6.0.3`.

## 7. launchd surface — the LaunchAgent disaster, in detail

**Counts:** 424 system jobs (root scope) + 533 user jobs ([user] scope).

### Active brew-services state

```
Name    Status User File
atuin   started        [user]  ~/Library/LaunchAgents/homebrew.mxcl.atuin.plist
emacs   none           
ollama  error  1       [user]  ~/Library/LaunchAgents/homebrew.mxcl.ollama.plist
unbound none
```

### The Jupyter LaunchAgent (FULL plist) — sysdiagnose's P0 SEC finding

```xml
<dict>
    <key>Label</key>
    <string>com.jupyter.server</string>
    <key>ProgramArguments</key>
    <array>
        <string>~/.local/share/uv/tools/jupyter-core/bin/jupyter-server</string>
        <string>--no-browser</string>
        <string>--port=8888</string>
        <string>--IdentityProvider.token=</string>            <!-- ⚠ EMPTY TOKEN -->
        <string>--ServerApp.allow_origin=*</string>          <!-- ⚠ ANY ORIGIN -->
        <string>--ServerApp.disable_check_xsrf=True</string> <!-- ⚠ NO CSRF GUARD -->
    </array>
    <key>RunAtLoad</key><true/>
    <key>KeepAlive</key><true/>
    <key>StandardOutPath</key><string>~/.local/var/log/jupyter-server.out.log</string>
    <key>StandardErrorPath</key><string>~/.local/var/log/jupyter-server.err.log</string>
    <key>WorkingDirectory</key><string>/Users/[user]</string>
</dict>
```

**Threat model:** any browser tab the user opens — including a tab opened by a Markdown preview, an email signature image-load, an XSS payload on any visited site — can POST to `http://localhost:8888/api/sessions` and spawn a kernel. Kernel = arbitrary Python = arbitrary code with the user's UID. CORS `*` defeats the same-origin protection; empty token defeats Jupyter's primary auth; disabled XSRF defeats the secondary one. The `WorkingDirectory=/Users/[user]` means the spawned kernel starts in the home directory — full access to chezmoi source, SSH keys, `.codex/`, memory tree, everything.

Mitigation options (in increasing order of restraint):

1. **Unload immediately**: `launchctl unload ~/Library/LaunchAgents/com.jupyter.server.plist && rm ~/Library/LaunchAgents/com.jupyter.server.plist`.
2. **Tighten if must keep**: replace `--IdentityProvider.token=` with a generated token; remove `--ServerApp.allow_origin=*` (default is same-origin); remove `--ServerApp.disable_check_xsrf=True`.
3. **Switch to on-demand**: invoke `uv tool run --from jupyter-core jupyter-server` from a wrapper when actually needed, per Rule #9.

### The other two brew LaunchAgents (Rule #9 sibling violations)

- `homebrew.mxcl.atuin.plist` — running, healthy. Atuin maintains the encrypted shell-history sync daemon.
- `homebrew.mxcl.ollama.plist` — **error state, exit code 9**. Ollama daemon failing to start; needs investigation. Matches the "Ollama throttle loop" finding from the sysdiagnose audit.

### Vendor LaunchAgents in `~/Library/LaunchAgents/` (non-brew)

- `com.backblaze.bzbmenu.plist`
- `com.DigiDNA.iMazing2Mac.Mini.plist`
- `com.google.GoogleUpdater.wake.plist`
- `com.google.keystone.{agent,xpcservice}.plist` (×2 Google Updater)
- `com.microsoft.EdgeUpdater.wake.plist`
- `com.openai.atlas.update-helper.plist` (the OpenAI Atlas browser auto-updater — Atlas itself is not in this audit's scope but the helper is here)

Plus the Jupyter agent. **Total: 11 LaunchAgents in user scope, 8 of which were installed by third-party apps without user-visible consent.**

## 8. Drift summary against CLAUDE.md claims

| Claim in home `CLAUDE.md` | Reality on disk | Action |
|---|---|---|
| "Python: Anaconda at `/opt/anaconda3/`" | Anaconda absent; only `~/.conda/aau_token{,_host}` residue | Update CLAUDE.md (via chezmoi source); delete `~/.conda` |
| "Memory-constrained (16 GB RAM)" | Confirmed; combined with `/var/db/diagnostics` 2.6 G + `var/folders` 2.7 G + sleepimage 2.0 G = ~7.3 G OS state on a 460 G volume | No drift |
| Hard Rule #9 "No LaunchAgents" | 3 brew-managed + 8 vendor = **11 LaunchAgents** in user scope. Plus 533 active user-scope jobs at `launchctl list`. | Either rule needs amendment or 3+ targeted removals |
| `~/seed.yaml` "misplaced byte-identical copy" (IRF-OPS-040) | Still pending (out of scope here but lives in home dir) | Tracked |
| "Brew cask `claude-code` removed; never re-install" | Confirmed gone; only Caskroom entries for the *other* tools | No drift |

## 9. What's safe to act on without further input

1. **`/etc/paths.d/10-pmk-global`** — dead pkgx PATH entry; safe to `sudo rm` (only mutation needed; pkgx itself is harmless). Verify no shell function imports it.
2. **`/usr/local/bin/python*t*`** — 16 dangling symlinks to missing `PythonT.framework`. Safe to remove with `sudo find /usr/local/bin -name 'python*t*' -type l ! -execdir test -e {} \; -print` to first list them.
3. **`~/.conda`** — Anaconda residue. Safe to `rm -rf ~/.conda` (only contains 30 B of `aau_token` files).
4. **`com.jupyter.server.plist`** — security-critical, but a *user* decision: do you actually need always-on Jupyter, and if so under what auth model? Until decided, at minimum `launchctl unload` to stop the always-on RCE surface without losing the file.
5. **`ollama` LaunchAgent in error state** — restart attempt or unload; understand why exit 9.
6. **`brew upgrade ngrok`** — single outdated cask.
7. **CLAUDE.md update** — replace the Anaconda line. Goes via chezmoi source `dot_config/ai-context/*.md.tmpl`, not the deployed file.

Items 1–6 are local and reversible. Item 7 routes through chezmoi's autoCommit+autoPush, so it ships to GitHub when applied.

## 10. Per-directory enumeration (depth 1, every child of every root)

Comprehensive sweep so the "100% context" claim is defensible. Sizes, owners, child counts, and role for **every** directory under the four roots.

### `/bin` — 37 sealed binaries (no subdirectories)

Already fully enumerated in §1. Flat dir; every entry is a binary file, all `root:wheel`, all signed.

### `/opt` — 2 children

| Path | Size | Owner | Entries | Role |
|---|---|---|---|---|
| `/opt/homebrew` | 12 G | `[user]:staff` | 24 | ARM Homebrew prefix **and** brew source git-repo checkout (both at once — `brew update` pulls into this dir). User-owned. |
| `/opt/pkg` | 0 B | `root:wheel` | 4 | pkgx graveyard (§3). Root-owned, abandoned. |

#### `/opt/homebrew` — 16 subdirs + 15 root files (the brew git-repo files)

| Path | Size | Entries | Role |
|---|---|---|---|
| `bin/` | 20 M | 866 | Symlinks to Cellar binaries — the active CLI surface (`brew`, `git`, `python3`, every brew-installed command) |
| `sbin/` | 0 B | 8 | Symlinks to Cellar admin binaries |
| `Cellar/` | 6.6 G | 230 | Actual installed formula payloads |
| `Caskroom/` | 1.0 G | 16 | Cask installer cache + metadata |
| `opt/` | 0 B | 280 | Alias-symlink farm for version-pin keys (`python@3.14`, `ruby@4.0`, etc.). 280 aliases over 230 formulae because some formulae carry multiple aliases (e.g. `node@25`, `node@26`, `nodejs`, `node.js`, `node` all → `Cellar/node/26.0.0`) |
| `lib/` | 2.8 G | 1000 | Shared libs (`.dylib`, `.a`) symlinked from Cellar formulae |
| `include/` | 0 B | 223 | Symlinks to Cellar header files (size 0 because du counts the symlink, not target) |
| `share/` | 1.3 G | 72 | Man pages, locale data, fonts, brew formula tap source under `share/Homebrew/Library/` (?) |
| `etc/` | 2.1 M | 30 | Per-formula config (ssl certs, GPG dirmngr config, gnupg keys, etc.) |
| `var/` | 152 M | 5 | Service state for `brew services` (atuin DB lives here) |
| `Library/` | 66 M | 3 | Brew's own Ruby source code + tap source (formula `.rb` files) |
| `Frameworks/` | 0 B | 1 | Empty placeholder for `.framework` bundles |
| `completions/` | 420 K | 5 | bash/zsh/fish completion scripts |
| `docs/` | 1.5 M | 82 | Brew's own contributor docs |
| `manpages/` | 148 K | 2 | brew(1), brew-bundle(5) |
| `package/` | 96 K | 3 | Packaging-build artifacts (used by brew releases) |

**Root files (brew project source — confirms `/opt/homebrew` is the brew git repo):**
`AGENTS.md` (5 KB), `CLAUDE.md` (11 B — stub), `CHANGELOG.md`, `CODEOWNERS`, `CONTRIBUTING.md`, `Dockerfile`, `LICENSE.txt`, `README.md`, plus dev tooling: `.gitignore`, `.gitattributes`, `.shellcheckrc`, `.vale.ini`, `.editorconfig`, `.dockerignore`, `.DS_Store`. This is the upstream `Homebrew/brew` repository, checked out at the prefix — standard but worth knowing: editing any of these would dirty the brew git tree.

### `/usr` — 7 subdirs (+ 2 X11 symlinks)

| Path | Size | Entries | Role |
|---|---|---|---|
| `bin/` | 80 M | 924 | Apple-shipped userland CLIs. Sealed. Includes `python3` (3.9.6), `ruby` (2.6.10 system), `perl` (5.34), `git`, `ssh`, `curl`, `gcc` (clang shim), every standard Unix tool. |
| `sbin/` | 47 M | 228 | System admin tools — `networksetup`, `nvram`, `softwareupdate`, `system_profiler`, `installer`, `diskutil`. |
| `lib/` | 13 M | 32 | System libs not baked into dyld_shared_cache (see breakdown below) |
| `libexec/` | 230 M | 429 | Daemons and helpers — `apfsd`, `airportd`, `amfid`, etc. (samples in §2) |
| `local/` | 18 M | 1 | Intel-era Homebrew prefix, now junk drawer (`bin/` only; §2) |
| `share/` | 253 M | 43 | OS data (see breakdown below) |
| `standalone/` | 152 M | 3 | `bootcaches.plist` (22 KB), `firmware/` (firmware blobs for FaceTime camera, T2, etc. — though T2 is intel-only; on Apple Silicon may be vestigial), `i386/` (legacy Intel kernel-cache structure for Rosetta) |
| `X11`, `X11R6` | symlinks | — | → `/private/var/select/X11` — X11 has been ripped from macOS; these point to whatever XQuartz set up, if anything (probably dangling) |

#### `/usr/lib` (32 entries) — what each is

- **Subdirs**: `cron/` (legacy cron job scratch), `dtrace/` (DTrace provider definitions), `dyld/` (dyld closure cache structure), `i18n/`, `ignition/` (boot helper), `log/` (log archive support), `pam/` (PAM auth modules — Touch ID PAM plugin is here), `pkgconfig/` (system `.pc` files), `rdma/` (RDMA support; vestigial on Mac), `rpcsvc/`, `ruby/` (system Ruby's stdlib path), `sasl2/` (auth modules), `sqlite3/`, `swift/` (Swift system libs — Apple ships Swift here), `system/` (low-level glue), `updaters/`, `usd/` (Universal Scene Description for ARKit/RealityKit), `zsh/` (system zsh modules path)
- **Loose dylibs**: `libc++.modules.json`, `libffi-trampolines.dylib`, `libgmalloc.dylib`, `libipconfig.dylib`, `libLeaksAtExit.dylib`, `libnetquality.dylib`, `libnetwork.dylib`, `libobjc-trampolines.dylib`, `libpcre2-8.dylib`, `libpcre2-posix.dylib`, `libRPAC.dylib`, `libz.1.2.12.dylib`, `ssh-keychain.dylib`

  These are the libs that **don't** fit in the dyld shared cache — diagnostic-mode libs like `libgmalloc` and `libLeaksAtExit`, the libobjc trampolines (called dynamically), and a couple of legacy libs.

#### `/usr/share` (43 dirs) — OS-data tree

Notable subdirs:

- **Shell/editor support**: `terminfo/` (every terminal's capabilities), `tabset/`, `vim/`, `zsh/`
- **Locale & language**: `locale/`, `i18n/`, `langid/`, `langid/` (text language ID models), `mecabra/`, `morphun/`, `tokenizer/`, `germantok/` (German tokenizer!), `dict/` (system dictionaries)
- **Time data**: `zoneinfo/`, `zoneinfo.default/` (tzdata)
- **System config**: `firmlinks` (the firmlink table — defines `/Applications` → `/System/Volumes/Data/Applications`, etc.), `sandbox/` (App Sandbox profiles)
- **Frameworks/runtimes data**: `swift/`, `libc++/`, `ri/` (Ruby `ri` doc store), `httpd/`, `cups/`, `openssh/`, `snmp/`, `screen/`, `skel/`
- **System extensions data**: `CoreDuetDaemonConfig.bundle/`, `kdrl.bundle/`, `thermald.bundle/`, `kpep/` (kernel power events), `pmenergy/`
- **Other**: `man/`, `doc/`, `examples/`, `misc/`, `firmware/`, `hiutil/`, `CSI/`, `cracklib/`, `file/` (file(1)'s magic db), `ans2_dummy_dir/` (test fixture leak from Apple internals), `com.apple.languageassetd/`, `icu/` (ICU data), `ucupdate/`

### `/private` — 4 children

| Path | Size | Owner | Entries | Role |
|---|---|---|---|---|
| `etc` | 1.5 M | `root:wheel` | 77 | All system configuration (firmlink target of `/etc`); enumerated below |
| `tftpboot` | 0 B | `root:wheel` | 0 | Reserved for legacy TFTP boot server; never used here |
| `tmp` | 7.6 M | `root:wheel` | 42 | World-writable scratch (firmlink target of `/tmp`); §4 |
| `var` | 8.8 G | `root:wheel` | 34 | System mutable state (firmlink target of `/var`); 34 children below |

#### `/private/etc` — 77 entries, every single one

(Most are tiny config files. Bold = directly material to this audit.)

Files: `afpovertcp.cfg`, `aliases` (→ postfix/aliases), `aliases.db`, **`asl.conf`** (Apple System Log), `auto_home`, `auto_master`, `autofs.conf`, **`bashrc`**, **`bashrc_Apple_Terminal`**, `bootpd.plist`, `com.apple.mis.rtadvd.conf`, `com.apple.screensharing.agent.launchd`, `csh.cshrc`, `csh.login`, `csh.logout`, `find.codes`, `ftpusers`, `gettytab`, **`group`**, **`hosts`**, `hosts.equiv`, `irbrc`, `kern_loader.conf`, `krb5.keytab`, `localtime`, `locate.rc`, `mail.rc`, `man.conf`, **`manpaths`**, `master.passwd`, `networks`, `newsyslog.conf`, `nfs.conf`, `notify.conf`, `ntp_opendirectory.conf`, `ntp.conf`, **`passwd`**, **`paths`** (§5), **`profile`**, `protocols`, `rc.common`, `rc.netboot`, `resolv.conf`, `rmtab`, `rpc`, `rtadvd.conf`, **`services`**, **`shells`** (§1), `sudo_lecture`, **`sudoers`**, `syslog.conf`, `ttys`, `uucp`, `xtab`, **`zprofile`**, **`zshrc`** (§5), `zshrc_Apple_Terminal`

Subdirs: `apache2/`, `asl/`, `cups/`, `manpaths.d/`, `newsyslog.d/`, `openldap/`, `pam.d/`, **`paths.d/`** (§3, §5), `pf.anchors/`, `postfix/`, `ppp/`, `racoon/`, `security/`, `snmp/`, `ssh/`, `ssl/`, **`sudoers.d/`** (empty), `wfs/`

**Highlights worth knowing exist (not all explored exhaustively):**

- `manpaths` + `manpaths.d/` — equivalent of `paths`/`paths.d` for `man`. Could harbor a stale entry pointing at Anaconda's man dir; worth checking if `apropos` ever errors. (Not investigated in this pass.)
- `pf.anchors/`, `pf.conf` — `pfctl` (the macOS firewall) anchor + config. Not customized.
- `racoon/` — IPsec daemon config (legacy; macOS uses newer IKE daemons now).
- `apache2/` — Apple ships Apache 2.4 but doesn't run it; config is upstream defaults.
- `openldap/`, `snmp/` — present but unused.
- `wfs/` — WebDAV-FS config (legacy).

#### `/private/var` — 34 children, every one

**The 13 with measurable size:** (already itemized in §4 table)

`db` (3.9 G) · `folders` (2.7 G) · `vm` (2.0 G — sleepimage) · `log` (92 M) · `protected` (42 M) · `logs` (3.9 M) · `run` (44 K) · `tmp` (4 K) · `sntpd` (4 K) · `lib` (effectively 0) · `msgs` (0) · `personalized_factory` (0) · `select` (0)

**The 21 zero-size / effectively-empty system-reserved dirs (purpose annotated):**

| Path | Owner | Role |
|---|---|---|
| `agentx` | `root:wheel` | SNMP AgentX subagent socket dir |
| `at` | `daemon:wheel` | `at`/`atrun` job queue (6 sub-spool dirs, empty) |
| `audit` | `root:wheel` | BSM audit trail (auditd off — empty) |
| `backups` | `root:wheel` | Reserved for system backups |
| `boot` | `root:daemon` | Boot-cooperative scratch |
| `containers` | `root:wheel` | App-sandbox container metadata (containers themselves live under `~/Library/Containers/`) |
| `dextcores` | `_driverkit:_driverkit` | DriverKit extension crash cores |
| `dirs_cleaner` | `root:wheel` | `dirs_cleaner` daemon scratch |
| `empty` | `root:sys` | Reserved-empty for daemons that `chroot()` |
| `install` | `root:wheel` | `Installer.app`/macOS installer scratch |
| `jabberd` | `_jabber:_jabber` | Legacy XMPP server (removed years ago; dir survives) |
| `lib` | `root:wheel` | 1 entry (legacy path; mostly unused on macOS) |
| `ma` | `_mobileasset:_mobileasset` | Mobile assets (Apple downloadable resources) |
| `mail` | `root:mail` | Legacy `/var/mail` mbox spool |
| `msgs` | `root:wheel` | `msgs(1)` system-message spool (vestigial) |
| `netboot` | `root:wheel` | NetBoot server spool |
| `networkd` | `_networkd:_networkd` | networkd state (2 entries) |
| `OOPJit` | `root:admin` | Out-of-Process JIT scratch (modern WebKit) |
| `recovery` | `root:wheel` | Recovery boot state |
| `root` | `root:wheel` | root user's home (per BSD layout; permissions-blocked from stat as user [user]) |
| `rpc` | `root:wheel` | RPC service state |
| `spool` | `root:wheel` | Print/mail spool aliases (4 sub-dirs, all empty) |
| `yp` | `root:wheel` | NIS/YP (defunct since OS X 10.5; dir survives) |

**The active ones in detail:**

- **`db` (3.9 G, 123 entries)** — system databases. The 14 largest subdirs were enumerated in §4. The remaining 109 are smaller per-service state stores (TCC, ConfigurationProfiles, mds — Spotlight, MobileMeAccounts, OpenDirectory, etc.). **`com.apple.xpc.launchd/`** lives here: holds `config/`, `disabled.501.plist`, `disabled.plist`, `disabled.migrated` — i.e. the launchd configuration state the user has modified via `launchctl disable`.
- **`folders` (2.7 G, 2 entries)** — exactly 2 subtrees: `zz/` (system-account scratch — small) and `l9/zn9x070d4xqb1qb5wfzr9tjr0000gn/` (user [user]'s `$TMPDIR` + per-user caches — 2.7 G).
- **`log` (92 M, 41 entries)** — Apple-style log files. Top entries: `install.log` (18 M), `com.apple.xpc.launchd` (19 M log archive — separate from `db/com.apple.xpc.launchd/` config), `powermanagement` (38 M), `DiagnosticMessages` (8.3 M), `asl/` (3.1 M ASL archive), `fsck_apfs.log`, multiple `wifi.log*.bz2` rotations.
- **`logs` (3.9 M, 5 entries)** — distinct from `log/`: older syslog-style. `CoreDuet/`, `DiagnosticMessages/`, `CrashReporter/`, `CDIS.log`, `Bluetooth/`.
- **`protected` (42 M, 3 entries)** — system-protected data with hardware-backed access controls (T2/Secure Enclave); not user-readable.
- **`run` (44 K, 32 entries)** — runtime sockets and PIDs (containerd-style ephemeral). Includes `com.apple.security.cryptexd/` (the cryptex bootstrap — see PATH §5).
- **`sntpd` (4 K)** — Simple NTP daemon state.
- **`tmp` (4 K)** — reserved-clean tmp distinct from `/private/tmp`.
- **`vm` (2.0 G)** — sole entry is `sleepimage` (hibernation RAM dump).

#### `/private/tmp` — 42 entries

World-writable; current Claude Code session scratch. Inventoried in §4. Sample size 7.6 M — small because zero-byte session log files dominate.

#### `/private/tftpboot` — 0 entries

Empty. Reserved for TFTP boot server (e.g., NetBoot/network install). Not used here.

### Summary table — every directory under each root

```
ROOT       | DIR                    | SIZE  | OWNER         | NOTES
-----------|------------------------|-------|---------------|---------------------------
/bin       | (37 files, no dirs)    | 9.4M  | root:wheel    | Sealed shells + utilities
-----------|------------------------|-------|---------------|---------------------------
/opt       | homebrew/              | 12G   | [user]:staff     | ARM brew prefix + git repo
/opt       | pkg/                   | 0B    | root:wheel    | pkgx graveyard
-----------|------------------------|-------|---------------|---------------------------
/usr       | bin/                   | 80M   | root:wheel    | 924 Apple binaries, sealed
/usr       | sbin/                  | 47M   | root:wheel    | 228 admin tools, sealed
/usr       | lib/                   | 13M   | root:wheel    | 32 libs/dirs, sealed
/usr       | libexec/               | 230M  | root:wheel    | 429 daemons, sealed
/usr       | local/                 | 18M   | root:wheel    | Intel-era junk drawer
/usr       | share/                 | 253M  | root:wheel    | 43 data dirs, sealed
/usr       | standalone/            | 152M  | root:wheel    | Boot caches + firmware
/usr       | X11, X11R6             | sym   | root:wheel    | Dangling X11 symlinks
-----------|------------------------|-------|---------------|---------------------------
/private   | etc/                   | 1.5M  | root:wheel    | 77 entries; system config
/private   | tftpboot/              | 0B    | root:wheel    | Unused (legacy)
/private   | tmp/                   | 7.6M  | root:wheel    | World-writable scratch
/private   | var/                   | 8.8G  | root:wheel    | 34 entries; system state
```

## 11. Depth 2 + 3 — every directory's children

### `/opt/homebrew/etc` — orphan-config audit (depth 2)

True orphans (formula uninstalled, config retained):

| Entry | Formula status | Note |
|---|---|---|
| `redis.conf`, `redis-sentinel.conf` | `redis` **uninstalled** | Stale; safe to delete |
| `php/` (1 entry) | `php` **uninstalled** | Stale |
| `freetds.conf` | `freetds` **uninstalled** | Stale |
| `newrelic-infra/` (1 entry) | `newrelic-infra` **uninstalled** | Stale; partner `/opt/homebrew/var/log/newrelic-infra/` is 107 MB |
| `pkcs11/`, `pkcs11.conf.example` | `pkcs11-helper` **uninstalled** | Stale |
| `openldap/` (9 entries) | `openldap` **uninstalled** | Stale; slapd configs preserved |
| `slsh.rc` | `s-lang` interactive **uninstalled** | Stale |
| `odbc.ini`, `odbcinst.ini` | `unixodbc` **uninstalled** | Stale |

Shared-dir false positives (not actual orphans — populated by multiple formulae): `bash_completion.d/` (51 entries from many formulae), `clang/` (72 entries from llvm-tools), `fonts/`, `gitconfig`/`gitconfig.default` (brew's git glue), `paths`, `profile.d/`, `target-spec-json-schema.json*` (rust).

Live configs (formula installed): `byobu/` (byobu 6.15), `unbound/` (unbound 1.25.1), `fish/` (fish 4.7.1), `gnupg/` (2.5.20), `gnutls/` (3.8.13_2), `ca-certificates/`, `openssl@3/` (8 entries), `vde2/` (2 entries — vde 4.2.x).

### `/opt/homebrew/var` — service state (depth 2 + 3)

| Path | Size | Role |
|---|---|---|
| `var/cache` | 6.0 M | Brew formula tarball cache (downloaded source archives) |
| `var/db` | 120 K | Brew internal state DB |
| `var/homebrew/{linked,locks,tmp}` | 0 B | Linked-formula tracking; install locks; scratch |
| `var/log/atuin.log` | 12 K | Atuin daemon log (active service) |
| `var/log/ollama.log` | **39 M** | Ollama daemon spam (error-state LaunchAgent — see §7) |
| `var/log/newrelic-infra/` | **107 M** | **Orphan — formula uninstalled, logs retained** |
| `var/log/php-fpm.log`, `redis.log` | 0–8 K | Orphan logs |
| `var/run` | 0 B | Empty |

### `/opt/homebrew/bin` — anatomy of the 866 symlinks (samples)

Every entry is a symlink into `../Cellar/<formula>/<version>/bin/<binary>`. Verified key tools and their pinned versions:

```
brew      -> Cellar/<homebrew-itself-via-Library>
git       -> Cellar/git/2.54.0/bin/git
python3   -> Cellar/python@3.14/3.14.5/bin/python3
node      -> Cellar/node/26.0.0/bin/node
go        -> Cellar/go/1.26.3/bin/go
cargo     -> Cellar/rust/1.95.0/bin/cargo
gh        -> Cellar/gh/2.92.0/bin/gh
chezmoi   -> Cellar/chezmoi/2.70.4/bin/chezmoi
atuin     -> Cellar/atuin/18.16.1/bin/atuin
starship  -> Cellar/starship/1.25.1/bin/starship
eza       -> Cellar/eza/0.23.4/bin/eza
bat       -> Cellar/bat/0.26.1/bin/bat
fd        -> Cellar/fd/10.4.2/bin/fd
rg        -> Cellar/ripgrep/15.1.0/bin/rg
fzf       -> Cellar/fzf/0.72.0/bin/fzf
jq        -> Cellar/jq/1.8.1/bin/jq
yq        -> Cellar/yq/4.53.2/bin/yq
just      -> Cellar/just/1.51.0/bin/just
k9s       -> Cellar/k9s/0.50.18/bin/k9s
ollama    -> Cellar/ollama/0.24.0/bin/ollama
llm       -> Cellar/llm/0.31_1/bin/llm
```

Random samples from the other 846 symlinks: `addbuiltin` (gnu), `icc_simplify`, `gtac`, `msgcomm`, `gcsplit`, `nnsd`, `git-upload-pack`, `crlutil`, `ttx`, `gdbus-codegen`, `byobu-export`, `httpx`, `gettext`, `byobu-disable`, `lame`, `critcl`, `qemu-system-ppc`, `glib-compile-schemas`, `progress`, `code` (probably VS Code's CLI), `fdtoverlay`, `brotli`, `aviocat`, `vdecmd`, `vfychain`, `gwc`, `crypto_bench`, `lt`, `target_dec_fate.sh`, `whiptail`.

### `/opt/homebrew/Cellar/<formula>/<version>/` — anatomy of one install (atuin 18.16.1)

This is the depth-3 structure every brew formula produces:

```
atuin/
└── 18.16.1/
    ├── INSTALL_RECEIPT.json          ← install metadata (deps, options, bottle source)
    ├── sbom.spdx.json                ← Software Bill of Materials (SPDX format)
    ├── .brew/atuin.rb                ← pinned formula source at install time
    ├── .bottle (if bottled)          ← bottle metadata
    ├── .crates.toml, .crates2.json   ← cargo-install metadata (rust formula)
    ├── LICENSE
    ├── CHANGELOG.md
    ├── README.md
    ├── homebrew.atuin.service        ← systemd unit (unused on macOS but bundled)
    ├── homebrew.mxcl.atuin.plist     ← LaunchAgent template — copied here, then symlinked
    │                                   to ~/Library/LaunchAgents/ by brew services
    ├── bin/atuin
    ├── etc/bash_completion.d/
    └── share/{pwsh,zsh,fish}/        ← shell completions
```

**Where the brew-managed LaunchAgents come from:** `~/Library/LaunchAgents/homebrew.mxcl.atuin.plist` is a symlink (or copy) of `/opt/homebrew/Cellar/atuin/18.16.1/homebrew.mxcl.atuin.plist`. Same pattern for `homebrew.mxcl.ollama.plist`. **Removing the LaunchAgent file requires either `brew services stop <formula>` or manual `launchctl unload && rm`** — direct deletion without `brew services` makes brew think the service is still installed.

### `/opt/homebrew/Caskroom/<cask>/` — anatomy (depth 2)

Each cask is shallow: a single version dir + a `.metadata/` dir holding 3 files (install receipt, cask source, manifest):

| Cask | Installed version | .metadata files |
|---|---|---|
| 1password-cli | 2.34.0 | 3 |
| block-goose | 1.35.0 | 3 |
| codex | 0.133.0 | 3 |
| font-jetbrains-mono-nerd-font | 3.4.0 | 3 |
| gcloud-cli | 569.0.0 + `latest` symlink | 3 |
| gitkraken-cli | 3.1.64 | 3 |
| keyclu | 0.31 | 3 |
| kitty | 0.47.0 | 3 |
| klatexformula | 4.1.0 | 3 (deprecated — IRF-OPS-060) |
| latexit | 2.16.6 | 3 |
| mailmate | 5673 | 3 |
| ngrok | 3.39.3,2vZur35asZP,a | 3 (outdated — brew flagged) |
| plugdata | 0.9.3 | 3 |
| visual-studio-code | 1.121.0 | 3 |
| visual-studio-code@insiders | 1.122.0-insider,... | 3 |
| warp | 0.2026.05.20.09.21.stable_02 | 3 |

### `/opt/homebrew/Library/` — brew's own source (depth 2)

```
Library/
├── .rubocop.yml          ← brew's Ruby linter config
├── README.md
├── Homebrew/             ← 227 entries — brew's internal Ruby source
└── Taps/                 ← empty (matches `brew tap` output)
```

### `/opt/homebrew/share/` — depth 2 highlights (72 dirs)

Notable: `qemu/` (71 entries — VM data files), `zsh-completions/` (180 entries), `tessdata/` (Tesseract OCR data), `WebP/` (codec data), `pwsh/` (PowerShell glue), `slsh/` (45 entries — left after s-lang uninstall? actually this is a formula brew share dir generated by slsh-the-lib-not-the-bin, possibly), `tmux/`, `trivy/`, `z3/`, `X11/`, `xml/`, `sounds/`, `pixmaps/`, `pkgconfig/` (31 entries — `.pc` files for brew formulae).

### `/opt/pkg/` — full depth-3 (the pkgx graveyard)

```
/opt/pkg
├── env/
│   ├── active -> global
│   └── global -> /opt/pkg/inv/envs/454eea274ef715bed0aef364fec823e04318850d28eb04f1c16a03a5127c071c
├── etc/                              (empty)
├── inv/
│   ├── envs/
│   │   └── 454eea274ef715bed0aef364fec823e04318850d28eb04f1c16a03a5127c071c/  (no bin/ child)
│   └── pkgs/                         (empty)
└── var/                              (empty)
```

The SHA-named env target directory exists but is empty (no `bin/` child). **Confirmed: `/etc/paths.d/10-pmk-global` → `/pkg/env/global/bin` is broken on TWO axes**: wrong root prefix AND missing leaf.

### `/private/etc/<subdir>/` — full depth-2 enumeration

**`apache2/` (7 entries)**: `httpd.conf`, `magic`, `mime.types`, plus subdirs `extra/`, `original/`, `other/`, `users/`. Apple ships Apache config but doesn't run the server.

**`asl/` (14 entries)**: 14 Apple System Log filter files for various daemons — `com.apple.authd`, `com.apple.MessageTracer`, `com.apple.networking.boringssl`, etc.

**`cups/` (12 entries)**: `cupsd.conf`, `cups-files.conf`, `printers.conf` (+ `.default`, `.O`, `.pre-update` backups). Subdirs `certs/`, `ppd/`. Standard CUPS print server config.

**`newsyslog.d/` (5 entries)**: log-rotation configs — `wifi.conf`, `files.conf`, three Apple slapconfig files.

**`openldap/` (6 entries)**: `AppleOpenLDAP.plist`, `DB_CONFIG.example`, `ldap.conf`, `ldap.conf.default`, `slapd.conf.default`, `schema/`. Apple ships ldap.conf even though slapd isn't running.

**`pam.d/` (26 entries)** — the auth modules:
`authorization`, `authorization_aks`, `authorization_ctk`, `authorization_la`, `authorization_lacont`, `checkpw`, `chkpasswd`, `cups`, `login`, `login.term`, `other`, `passwd`, `screensaver`, `screensaver_aks`, `screensaver_ctk`, `screensaver_la`, `screensaver_new`, `screensaver_new_aks`, `screensaver_new_ctk`, `screensaver_new_la`, `smbd`, `sshd`, `su`, `sudo`, `sudo_local`, `sudo_local.template`.

The `aks`/`ctk`/`la` variants are auth-cascade tail files for Apple Key Store, Cryptotokenkit, and Login Authority. **`sudo_local`** is Apple's blessed extension point — it's where you'd add `pam_tid.so` for Touch ID + sudo (in Sequoia/Tahoe, Touch ID for sudo is built into `sudo_local.template`, requires copying to `sudo_local`).

`/etc/pam.d/sudo` actually reads:
```
auth       include        sudo_local       ← reads sudo_local first
auth       sufficient     pam_smartcard.so
auth       required       pam_opendirectory.so
account    required       pam_permit.so
password   required       pam_deny.so
session    required       pam_permit.so
```

**`paths.d/` (4 entries)**: `10-cryptex`, `10-pmk-global` (**dead pkgx**), `100-rvictl`, `homebrew`.

**`pf.anchors/` (1)**: `com.apple` — Apple's packet-filter anchor file.

**`postfix/` (21 entries)**: `main.cf`, `master.cf` (+ `.default`, `.proto`), `aliases`, `access`, `bounce.cf.default`, `canonical`, `custom_header_checks`, `generic`, `header_checks`, `LICENSE`, `makedefs.out`, `postfix-files`, `postfix-files.d/`, `relocated`, `TLS_LICENSE`, `transport`. **Postfix configured but not running** — Apple ships full config.

**`racoon/` (2)**: `psk.txt`, `racoon.conf` — legacy IPsec daemon (removed years ago, configs survive).

**`security/` (5)**: `audit_class`, `audit_control.example`, `audit_event`, `audit_user`, `audit_warn` — BSM audit framework templates (not active).

**`snmp/` (2)**: `snmpd.conf`, `snmpd.conf.default`.

**`ssh/` (7)**: `crypto`, `crypto.conf`, `moduli`, `ssh_config`, `ssh_config.d/`, `sshd_config`, `sshd_config.d/`. Both `ssh_config.d` and `sshd_config.d` contain a single file: **`100-macos.conf`** — Apple's macOS-specific SSH defaults.

**`ssl/` (4)**: `cert.pem`, `certs/`, `openssl.cnf`, `x509v3.cnf` — system OpenSSL config.

**`sudoers.d/`** — empty (no custom sudo grants).

**`uucp/` (3)**: `passwd`, `port`, `sys` — legacy UUCP (Unix-to-Unix Copy Protocol) configs. Last used in the 1990s.

**`wfs/` (4)**: WebDAV File Sharing configs — `httpd_webdavsharing*` files + `wfs.plist`.

**Empty subdirs**: `manpaths.d/`, `ppp/`.

### `/private/var/db/` — all 123 children (categorized)

**14 actually contain data** (totaling 3.9 G):

| Path | Size | Children | Role |
|---|---|---|---|
| `diagnostics/` | 2.6 G | 14 | Unified-logging persistent store (Apple's `os_log` archive) |
| `uuidtext/` | 715 M | 257 | Symbol files for log decoding (UUID-keyed) |
| `receipts/` | 183 M | 94 | `.bom` + `.plist` pairs for 47 installed `.pkg` packages — Apple iWork (Keynote/Pages/Numbers), iLife (iMovie/GarageBand), Final Cut, Compressor, etc. |
| `KernelExtensionManagement/` | 115 M | 3 | KEXT staging (Tahoe still tracks legacy KEXTs) |
| `powerlog/` | 113 M | 1 | Power-management telemetry SQLite DB |
| `systemstats/` | 75 M | 462 | Per-process statistics archives (system_profiler/sysdiagnose source) |
| `SystemPolicyConfiguration/` | 59 M | 20 | Gatekeeper / KEXT policy / system-extension policy |
| `DiagnosticPipeline/` | 47 M | 10 | Modern crash/diag pipeline |
| `CoreDuet/` | 34 M | 3 | Suggestions engine (Siri/Spotlight) |
| `gkopaque.bundle/` | 6.1 M | 1 | Gatekeeper opaque-policy bundle |
| `GridData/` | 4.6 M | 1 | Spotlight grid metadata |
| `DuetActivityScheduler/` | 4.2 M | 4 | CoreDuet activity scheduler state |
| `eligibilityd/` | 4.1 M | 6 | Apple Intelligence/feature eligibility tracking |
| `timezone/` | 2.7 M | 4 | Timezone resolution state |

**70 are empty preallocated** (Apple creates these on first boot so daemons have a known mount-point even before they've written anything): `Accessibility/`, `accessoryupdater/`, `analyticsd/`, `aonsensed/`, `appinstalld/`, `AppleIntelligencePlatform/`, `applepay/`, `appstore/`, `astris/`, `biome/`, `cmiodalassistants/`, `com.apple.dt.automationmode/`, `com.apple.findmy.findmybeaconingd/`, `com.apple.naturallanguaged/`, `com.apple.threadradiod/`, `com.apple.xpc.roleaccountd.staging/`, `ConnectivityPowerTableUpdates/`, `coreml/`, `ctkd/`, `CVMS/`, `darwindaemon/`, `datadetectors/`, `dhcpclient/`, `DiagnosticsReporter/`, `diskimagesiod/`, `displaypolicyd/`, `DumpPanic/`, `ExtensibleSSO/`, `findmydevice/`, `fpsd/`, `fseventsd/`, `geod/`, `GPURestartReporter/`, `hidd/`, `installcoordinationd/`, `knowledgegraphd/`, `locationd/`, `lockdown/`, `ManagedConfigurationFiles/`, `mmaintenanced/`, `MobileIdentityService/`, `modelmanagerd/`, `nearbyd/`, `neuralengine/`, `nsurlsessiond/`, `nsurlstoraged/`, `oah/`, `ondemand/`, `PanicReporter/`, `RemoteManagement/`, `reportmemoryexception/`, `rmd/`, `Sandbox/`, `searchparty/`, `securityagent/`, `SoC/`, `Spotlight/`, `Spotlight-V100/`, `sudo/`, `swtransparencyd/`, `sysdiagnose/`, `system-override/`, `SystemKeys/`, `terminus/`, `timed/`, `UpdateMetrics/`.

**~39 contain small amounts** (4 KB – 256 KB): `audiomxd/`, `BootCaches/`, `caches/`, `com.apple.backgroundtaskmanagement/`, `com.apple.countryd/`, `com.apple.modelcatalog/`, `com.apple.security.cryptexd/`, `ConfigurationProfiles/`, `DarwinDirectory/`, `dslocal/`, `factory_installs/`, `keybags/`, `launchd.db/`, `mds/`, `NANDTelemetryServices/`, `openldap/`, `os_eligibility/`, `softwareupdate/`, `spindump/`, `Wallpapers/`, `amfid/`, `assetsubscriptiond/`, `Battery/`, `dscsym/`, **`com.apple.xpc.launchd/`** (4 entries — the launchd config tree, detailed below).

#### `/private/var/db/com.apple.xpc.launchd/` — depth 3 (launchd's own state)

```
com.apple.xpc.launchd/
├── config/                 ← (empty — launchd reads /Library/Apple/System/Library/LaunchAgents/* and ~/Library/LaunchAgents/* directly)
├── disabled.501.plist      ← [user]'s per-user disabled-services map (UID 501)
├── disabled.migrated       ← migration marker (zero bytes; touched once)
└── disabled.plist          ← system-scope disabled-services map
```

**`disabled.501.plist` excerpt — what [user] has explicitly toggled:**

```xml
<dict>
  <key>com.docker.helper</key><false/>                           ← enabled (runs)
  <key>com.apple.ManagedClientAgent.enrollagent</key><true/>     ← DISABLED
  <key>com.ollama.ollama</key><false/>                           ← enabled
  <key>com.fiplab.tasktabhelper</key><false/>
  <key>homebrew.mxcl.newrelic-infra-agent</key><false/>          ← enabled but formula uninstalled!
  <key>com.apple.Siri.agent</key><false/>
  <key>2BUA8C4S2C.com.agilebits.onepassword7-helper</key><false/>
  <key>com.apple.Passwords.MenuBarExtra</key><false/>
  <key>com.1password.1password-launcher</key><false/>
  <key>com.apple.weather.menu</key><false/>
  <key>com.dropbox.DropboxUpdater.wake</key><false/>
  <key>com.microsoft.OneDriveLauncher</key><false/>
  <key>com.pyloggy.startup</key><false/>
  <key>com.spotify.client.startuphelper</key><false/>
  <key>com.apple.FolderActionsDispatcher</key><true/>            ← DISABLED
  <key>com.fiplab.clipboardhelper</key><false/>
  <key>com.microsoft.EdgeUpdater.wake</key><false/>
  <key>com.jetbrains.toolbox</key><false/>
  ...
</dict>
```

Read semantically: `<true/>` = the service IS in the disabled set (will not run); `<false/>` = it's been **explicitly re-enabled** (overriding a default disable, or explicitly marked enabled). Two services are user-disabled here: `ManagedClientAgent.enrollagent` (MDM enrollment — appropriate for a non-managed Mac) and `FolderActionsDispatcher`. **A reference to `homebrew.mxcl.newrelic-infra-agent` is in the enabled set even though newrelic-infra is uninstalled — confirms the orphan story (and means the disable-state itself is stale).**

#### `/private/var/db/diagnostics/` — depth 2 (the 2.6 G unified-log store)

```
diagnostics/
├── Persist/        ← 54 entries — primary persisted tracepoints (the main bulk)
├── Signpost/       ← 372 entries — signpost trace marks (os_signpost)
├── Special/        ← 1003 entries — high-priority log entries (the LARGE one — most files)
├── HighVolume/     ← 10 entries — high-rate-source overflow
├── timesync/       ← 5 entries — clock-sync state
├── diagnosticd.0.log       — 562 B
├── logd_helper.0.log       — 941 KB
├── logd.0.log              — 661 KB
├── logdata.statistics.0.jsonl — 4.7 MB (most recent)
├── logdata.statistics.0.txt   — 36 KB
├── logdata.statistics.1.jsonl — 5.0 MB (previous rotation)
├── logdata.statistics.1.txt   — 1.0 MB
├── shutdown.0.log          — 1.0 MB
└── version.plist           — 505 B
```

`Special/` with 1003 individual files is what dominates the file count; `Persist/` has fewer but larger tracefiles. Apple's `log show`/`log stream` reads from these.

### `/private/var/log/` — depth 2 (full file/dir listing)

| Path | Size | Type |
|---|---|---|
| `powermanagement/` | 38 M | dir |
| `install.log` | 18 M | file |
| `com.apple.xpc.launchd/` | 19 M | dir (launchd log archive — distinct from db tree) |
| `DiagnosticMessages/` | 8.3 M | dir |
| `asl/` | 3.1 M | dir (legacy ASL archive) |
| `wifi.log` | 2.0 M | file (active) |
| `wifi.log.{0..10}.bz2` | 180–420 K each | files (11 rotations) |
| `system.log` | 348 K | file (active) |
| `system.log.{0..6}.gz` | 4–36 K | files (7 rotations) |
| `fsck_apfs.log` | 536 K | file |
| `shutdown_monitor.log` | 16 K | file |
| `com.apple.wifi.analytics/` | 400 K | dir |
| `ppp/`, `uucp/`, `PrivacyPreservingMeasurement/` | 0 B | empty dirs |

### `/private/var/folders/l9/zn9x070d4xqb1qb5wfzr9tjr0000gn/` — [user]'s `$TMPDIR` (depth 2)

The macOS confinement model: every user gets a `/private/var/folders/<two-char>/<long-hash>/` tree. Four subdirs by convention:

| Subdir | Size | Role |
|---|---|---|
| `0/` | 34 M | Reserved for special use (varies; often code-signing scratch) |
| `T/` | 138 M | The actual `$TMPDIR` — `mktemp`, app scratch |
| `C/` | 244 M | Per-user XDG-style cache (`NSCachesDirectory` for sandboxed apps) |
| `X/` | **2.3 G** | **Per-user app data — see breakdown** |

**`X/` — the 2.3 G hog, depth 3:**

```
X/com.google.Chrome.code_sign_clone        → 1.3 G  ← orphaned code-sign clone
X/com.openai.atlas.web.code_sign_clone     → 956 M  ← orphaned code-sign clone
X/com.microsoft.edgemac.code_sign_clone    → 0 B    ← drained successfully
```

These are macOS code-signing sandbox clones created when each browser self-updates. The kernel's codesign verifier asks the updater to materialize a separate clone in `$TMPDIR/X/` to confirm signature integrity. **The updater is supposed to remove it after.** Chrome and Atlas didn't. Safe to `rm -rf` both directories — the browsers will recreate them on next update if needed. Frees **2.3 G immediately**.

### `/private/var/run/` — depth 1 (32 entries) — runtime sockets and "didRunThisBoot" flags

`automount.initialized`, `bootSessionMA.txt`, `com.apple.AssetCache`, `com.apple.DumpPanic.{finishedPMUFaultHandling,finishedThisBoot}`, `com.apple.launchd.K49S15ITPA`, `com.apple.logind.didRunThisBoot`, `com.apple.loginwindow.didRunThisBoot`, `com.apple.mdmclient.daemon.didRunThisBoot`, `com.apple.security.cryptexd/`, `com.apple.wifivelocity`, `com.apple.WindowServer.didRunThisBoot`, `cupsd`, `diskarbitrationd.pid`, `filesystemui.socket`, `hdiejectd.pid`, `kdc.pid`, `mDNSResponder`, `mds`, `MobileAssetCriticalDomainsUpdated.plist`, `MobileAssetStartupActivation.doneThisBoot`, `portmap.socket`, `pppconfd`, `resolv.conf` (resolver-derived snapshot), `syslog`, `syslog.pid`, `systemkeychaincheck.{done,socket}`, `usbmuxd`, `utmpx`, `vpncontrol.sock`, `wifi`.

### `/usr/bin` — 924 binaries categorized

Categorical breakdown (named-pattern counts, ~133 matched out of 924):

| Category | Count | Examples |
|---|---|---|
| Authentication/identity | 16 | `login`, `passwd`, `chpass`, `sudo`, `su`, `id`, `whoami`, `users`, `who`, `groups`, `kinit`, `klist`, `kpasswd`, `kdestroy` |
| Networking clients | 12 | `curl`, `ssh`, `scp`, `sftp`, `nc`, `host`, `dig`, `nslookup`, `dscacheutil`, `ping`, `traceroute`, `whois` |
| Archive/compression | 12 | `tar`, `gzip`, `gunzip`, `bzip2`, `xz`, `zip`, `unzip`, `compress`, `zcat`, `zless`, `zgrep` |
| Dev/build (toolchain) | 21 | `make`, `gcc`, `clang`, `ld`, `as`, `ar`, `nm`, `strip`, `otool`, `lipo`, `dsymutil`, `install_name_tool`, `codesign`, `xcrun`, `xcodebuild`, `swift`, `swiftc`, `git`, `hg`, `cvs`, `svn` |
| Scripting runtimes | 6 | `python3`, `ruby`, `perl`, `perl5`, `php` (system has no node here), `awk` |
| Text/data tools | 26 | `grep`, `sed`, `cut`, `tr`, `sort`, `uniq`, `wc`, `head`, `tail`, `less`, `more`, `cat`, `tac`, `paste`, `join`, `comm`, `tee`, `column`, `fold`, `fmt`, `nl`, `pr`, `expand`, `unexpand`, `tabs`, etc. |
| Process/system | 16 | `top`, `ps`, `kill`, `killall`, `nice`, `renice`, `nohup`, `time`, `env`, `printenv`, `ulimit`, `hostid`, `uname`, `sysctl`, `locale`, `defaults`, `launchctl` |
| File ops | 18 | `file`, `stat`, `find`, `locate`, `which`, `whereis`, `type`, `readlink`, `du`, `df`, `mount`, `umount`, `diskutil`, `hdiutil`, `chflags`, `mktemp`, `truncate`, `touch`, `split`, `cmp`, `diff`, `patch` |
| Crypto/hashing | 6 | `openssl`, `gpg`, `md5`, `shasum`, `base64`, `security` |
| **Apple-internal** | ~120 | `sysdiagnose`, `syslog`, `systemextensionsctl`, `tccutil`, `swift-inspect`, `app-sso`, `kextutil`, `sw_vers`, `swcutil`, `syspolicy_check`, `apropos`, plus DTrace probes (`syscallbypid.d`, `syscallbyproc.d`, `syscallbysysc.d`) — these are pre-shipped DTrace scripts |
| **Remaining ~660** | — | Apple framework support binaries — Cocoa runtime helpers, accessibility tools, AppleScript bridges, Mach utilities, debug helpers, `AssetCacheLocatorUtil`, `mdfind`, `mdimport`, `mdutil`, `tmutil` (Time Machine), `caffeinate`, `pbcopy`/`pbpaste`, `say`, `qlmanage`, `pluginkit`, etc. |

### `/usr/libexec` — 429 entries, depth 2

- **225 daemon binaries** (filename ending in `d`): `airportd`, `apfsd`, `amfid`, `appleaccountd`, `aned` (Apple Neural Engine daemon), `aneuserd`, `aonsensed`, `appleh13camerad`, `appleh16camerad`, `appleidsetupd`, `applekeystored`, `adprivacyd`, …
- **37 subdirectories** — purpose-grouped helpers:
  - **`apache2/`** (115 entries) — full Apache module + helper tree (`httpd-foreground`, `envvars`, `apxs`, mod_*.so, etc.)
  - **`postfix/`** (43) — Postfix MTA helper binaries (`smtp`, `qmgr`, `local`, `pickup`, `cleanup`, etc.)
  - **`AssetCacheAgent/`** (43) — Content Caching service helpers
  - **`apple2/`** — (none found — typo)
  - **`ApplicationFirewall/`** (7) — `socketfilterfw` + helpers
  - **`AssetCache/`** (2) — Content Caching daemon binaries
  - **`BiomeSync/`** (1)
  - **`cups/`** (9) — `cups-{deviced,driverd,exec,lpd}` etc.
  - **`dtrace/`** (7) — DTrace USDT provider definitions
  - **`fax/`** (1) — legacy fax daemon (lol)
  - **`feedback/`** (5) — feedback assistant helpers
  - **`MiniTerm.app/`** (1) — embedded miniature Terminal app used by `pppd` chat scripts
  - **`pmudiagnose/`** (1) — PMU diagnostic
  - **8 `.mlmodelc` bundles** — **on-device ML models for system decisions**:
    - `_OSDischargeETA.mlmodelc` — predicts battery discharge time
    - `_OSHighBatteryDrainHighChargeDurationModel.mlmodelc` — high-drain pattern recognition
    - `_OSHighBatteryDrainLowChargeDurationModel.mlmodelc` — sibling
    - `dynamic_scheduling.mlmodelc` — CPU/process scheduler ML model
    - `engageOnPlugin.mlmodelc` — engagement detection
    - `freezer_app_ranking_model.mlmodelc` — which apps to suspend first
    - `longDurationModel.mlmodelc`, `Prev12Next12Drain.mlmodelc` — battery-life forecasting
    - `Recipe.mlmodelc`, `Recipe_CJK.mlmodelc` — text recognition recipes
  - **`DuetActivityScheduler.momd/`** (5), **`GKCentralCache.momd/`** (3) — Core Data `.momd` model bundles
  - **`com.apple.cmio.videodriverkithostextension.systemextension/`** (1) — CMIO video driver system-extension

- **11 explicitly Apple-namespaced** entries

### `/usr/share/` — depth 2 highlights

**`firmlinks`** (19 lines, file not dir) — the firmlink table mapping. Critical to understand macOS APFS dual-volume architecture:

```
/AppleInternal                             AppleInternal
/Applications                              Applications
/Library                                   Library
/System/Library/Caches                     System/Library/Caches
/System/Library/Assets                     System/Library/Assets
/System/Library/PreinstalledAssets         System/Library/PreinstalledAssets
/System/Library/AssetsV2                   System/Library/AssetsV2
/System/Library/PreinstalledAssetsV2       System/Library/PreinstalledAssetsV2
/System/Library/CoreServices/CoreTypes.bundle/Contents/Library   System/Library/CoreServices/CoreTypes.bundle/Contents/Library
/System/Library/Speech                     System/Library/Speech
... (9 more)
```

Each row maps a path on the **sealed System volume** (left) to its writable counterpart on the **Data volume** (right). The kernel transparently redirects writes to the right side; reads see a merged view. This is **how `/Applications` can be writable when `/System` (its container) is sealed** — `/Applications` is firmlinked to the Data volume.

**`zoneinfo/`** (67 entries) — `Africa/`, `America/`, `Antarctica/`, `Arctic/`, `Asia/`, `Atlantic/`, `Australia/`, `Brazil/`, `Canada/`, `Etc/`, `Europe/`, … (Olson tzdata).

**`sandbox/`** (59 .sb files) — Apple's per-daemon sandbox profiles in TinyScheme syntax: `airportd.sb`, `bluetoothd.sb`, `BTLEServer.sb`, `com.apple.bootinstalld.sb`, `com.apple.ckdiscretionaryd.sb`, `com.apple.cloudd.sb`, `com.apple.CommCenter.sb`, `com.apple.corespotlightservice.sb`, `com.apple.fontd.internal.sb`, `com.apple.fontd.support.sb`, …

**`zsh/`** (2): `5.9/` (zsh standard function path for sealed-volume zsh 5.9), `site-functions/`.

**`man/`** (8): `man1`, `man4`, `man5`, `man6`, `man7`, `man8`, `man9`, `mann`. **Curiously no `man2`/`man3`** — those are in `/usr/share/man/manl` or accessed via cryptex paths in modern macOS.

### `/private/var/db/receipts/` — depth 1 (94 entries = 47 packages)

47 `.pkg` install receipts in `.bom` (Bill of Materials, binary format) + `.plist` (metadata) pairs. The first 10 alphabetically:

`com.apple.cdm.pkg.{GarageBand,iMovie,Keynote,Numbers,Pages}_MASReceipt` (Mac App Store update receipts), `com.apple.pkg.Compressor_AppStore`, `com.apple.pkg.FinalCut_AppStore`, `com.apple.pkg.GarageBand_AppStore`, `com.apple.pkg.iMovie_AppStore`, `com.apple.pkg.Keynote14`, …

These are how macOS knows which Apple `.pkg` payloads have been applied — Software Update writes here.

## 12. Depth 4 + 5 — file-type identification and structural anatomy

### `/private/var/db/receipts/` — full 47-package install autobiography

Every `.pkg` ever installed on this Mac that didn't go through the Mac App Store delta-update channel left a receipt here. Sorted by install epoch (the 47 .bom + 47 .plist pairs):

**Apple iWork / iLife (Mac App Store)** (10 receipts):
`com.apple.cdm.pkg.{GarageBand,iMovie,Keynote,Numbers,Pages}_MASReceipt`, `com.apple.pkg.{GarageBand,iMovie,Keynote14,Numbers14,Pages14,Pages15}`.

**Apple Pro Apps / Developer** (8 receipts):
`com.apple.pkg.Compressor_AppStore`, `com.apple.pkg.FinalCut_AppStore`, `com.apple.pkg.LogicPro_AppStore`, `com.apple.pkg.MainStageAppStore`, `com.apple.pkg.Xcode`, `com.apple.pkg.TestFlight`, `com.apple.pkg.Playgrounds`, `com.apple.pkg.WWDC_Catalyst`.

**Anaconda — the forensic trail** (5 receipts, payload gone):
`io.continuum.pkg.prepare_installation`, `io.continuum.pkg.run_conda_init`, `io.continuum.pkg.run_installation`, `io.continuum.pkg.shortcuts`, `io.continuum.pkg.user_post_install`. Combined with `~/.conda/aau_token{,_host}` residue and the still-stale `CLAUDE.md` claim, this is now a triple-witnessed historical install.

**python.org full installer** (4 receipts — confirms the `/Library/Frameworks/Python.framework/Versions/3.13` story):
`org.python.Python.Python{Applications,Documentation,Framework,UnixTools}-3.13`.

**Java** (1):
`net.temurin.25.jdk` — Eclipse Temurin Java 25 JDK is installed (not just the `/usr/bin/java` shim — there's a real JDK somewhere, likely under `/Library/Java/JavaVirtualMachines/temurin-25.jdk/`).

**Music/creative production** (15 receipts):
- **Cardinal modular synth** × 8: `studio.kx.distrho.cardinal.resources`, `studio.kx.distrho.plugins.cardinal.{clapbundles,components,jack,lv2bundles,native,vst2bundles,vst3bundles}`
- **plugdata** (matches brew cask) × 5 plugin format receipts: `com.plugdata.{app,au,clap,lv2,vst3}.pkg.plugdata`
- `com.pixelmatorteam.pixelmator.touch.x.photo` — Pixelmator Photo (Catalyst)
- `com.quoteunquoteapps.highlandapp2` — Highland 2 (screenwriting)

**Auxiliary** (4): `com.backblaze.modern.pkg`, `com.google.Keystone`, `com.pieces.pkg`.

### `/private/var/db/diagnostics/` — depth 4 (1434 files in 5 subdirs, all binary)

All trace files are Apple's compressed unified-log format. `file(1)` returns just "data" — they're not text:

| Subdir | Count | Pattern | Format |
|---|---|---|---|
| `Persist/` | 52 | `00000000000049e4.tracev3` etc. | `.tracev3` (compressed log chunk) |
| `Special/` | 1001 | `0000000000003768.tracev3` etc. | `.tracev3` |
| `Signpost/` | 370 | `00000000000018d5.tracev3` etc. | `.tracev3` |
| `HighVolume/` | 8 | `0000000000001595.tracev3` etc. | `.tracev3` |
| `timesync/` | 3 | `000000000000004a.timesync` etc. | `.timesync` (clock-skew chunks) |

Filenames are sequence numbers (16-digit hex). The buckets reflect log-priority routing:
- **Persist** — Apple's `os_log` calls with `OS_LOG_TYPE_DEFAULT` or higher when the subsystem has persistent retention configured.
- **Special** — high-priority/system-critical signals (errors, faults, security events). 1001 files = largest by count.
- **Signpost** — `os_signpost` API trace points (used for instrumented timing intervals — Instruments.app reads these).
- **HighVolume** — overflow bucket for sources that exceeded normal rate limits.
- **timesync** — clock-correction state across boots (allows merging logs from different time domains).

To read these, use `log show --predicate '<filter>' --start <date>` — never grep them directly.

### `/private/var/db/uuidtext/` — depth 4 (715 MB, content-addressed)

Two-character hex bucketing (00–FF). Each two-char dir holds files named by the rest of the UUID (32 chars total). Sample: `uuidtext/A1/B2C3D4E5F6...`. Each file is the **symbol table for a single Mach-O binary** — when `log show` decodes a tracepoint, it looks up the binary's UUID in here to translate addresses to symbols. **257 buckets present** out of 256 possible (extra entries are likely `dsc/` and `dsc.shared_cache/` subdirs for dyld shared cache symbols).

### `/private/var/db/SystemPolicyConfiguration/` — depth 3 (20 entries, the Gatekeeper brain)

**SQLite database family** (each has main file + `-shm` shared-memory + `-wal` write-ahead-log):

| File | Size | Role |
|---|---|---|
| `SystemPolicy` (+wal/shm) | 589 KB | Master Gatekeeper policy — every app/binary's quarantine status, dev-id allow/deny |
| `ExecPolicy` (+wal/shm) | 4.8 M (+ 3.5 M wal) | Modern execution-quarantine policy (Big Sur+) |
| `KextPolicy` (+wal/shm) | 4 KB (+ 890 KB wal) | KEXT load authorization |
| `Tickets` (+wal/shm) | 1.1 M (+ 3.0 M wal) | Stapled notarization tickets for installed apps |
| `.SystemPolicy-default` | 61 KB | The SIP-baked default policy (root-only readable) |

**Plist configurations**: `Default.plist`, `gatekeeper-migration.plist` (265 KB — migration record from older formats), `migration.plist`, `KextClassification.plist` (20 KB — KEXT trust classes), `TamperExceptions.plist` (12 KB — apps allowed to modify protected paths).

**Subdirs**: `gke/`, `gke.bundle/` (Gatekeeper Engine), `XProtect.app/`, `XProtect.bundle/` (**Apple's bundled malware scanner**, updated separately from OS), `SamplingStaging/`.

**`.LastGKReject` — 181 bytes, modified `May 22 12:16` (today!)** — the most recent Gatekeeper rejection. This is updated when something tries to execute and Gatekeeper says no. Worth a `cat` to see what was rejected. (Did not view in this audit to avoid noise on routine sysadmin scripts.)

### `/private/var/db/KernelExtensionManagement/` — depth 3 (115 MB)

```
KernelExtensionManagement/
├── DextRecordTable.plist     (257 B — registered DriverKit extensions)
├── KernelCollections/         (the 115 MB hog — prelinked KEXT boot blob)
└── Staging/                   (KEXT staging area for newly-installed kexts pending reboot)
```

The 115 MB is essentially the **prelinked boot kernel collection** — every loaded KEXT pre-merged into one blob for fast boot. Rebuilt by `kmutil` after every kext install/uninstall.

### `/private/var/db/CoreDuet/` — depth 3 (34 MB)

```
CoreDuet/
├── Caches/      (3 entries — predictive engine caches)
└── People/      (6 entries — contact-graph state for Siri Suggestions)
```

CoreDuet is Apple's behavioral-prediction service — feeds Spotlight, Siri Suggestions, app-prelaunch hints, and the freezer model in `/usr/libexec/freezer_app_ranking_model.mlmodelc`.

### `/opt/homebrew/Cellar/<formula>/<version>/` — typical anatomy (depth 4 via git 2.54.0)

The canonical brew-bottle install layout:

```
git/2.54.0/
├── .brew/atuin.rb-equivalent             ← pinned formula source at install time
├── .bottle/etc/                          ← bottle install manifest
├── INSTALL_RECEIPT.json
├── sbom.spdx.json                        ← SPDX SBOM for security scanning
├── bin/git                               ← THE binary (just one)
├── etc/bash_completion.d/
├── libexec/git-core/                     ← 181 git subcommand binaries
│   ├── git, git-add, git-am, git-apply,
│   ├── git-bisect, git-blame, git-branch,
│   ├── git-cherry-pick, git-clone, …
│   └── mergetools/                       ← merge driver scripts
└── share/
    ├── man/{man1,man5,man7}/             ← per-section manpages
    ├── locale/{ca,de,el,es,fr,ga,id,is,it,ko,pl,pt_PT,ru,sv,tr,uk,vi,zh_CN,zh_TW,…}/
    │                                     ← 24 language localizations
    ├── perl5/{Authen,FromCPAN,Git,Net}/  ← Perl libs for git-svn etc.
    ├── gitweb/static/
    ├── git-core/{contrib,templates}/
    ├── doc/git-doc/
    ├── zsh/site-functions/
    └── bash-completion/completions/
```

**Brew's two-tier binary strategy:** `bin/git` is the user-facing dispatcher; the actual subcommand implementations are in `libexec/git-core/`. Only `bin/git` is symlinked into `/opt/homebrew/bin`; the 181 subcommands are reached internally via `$GIT_EXEC_PATH`.

### `/opt/homebrew/Cellar/python@3.14/3.14.5/` — depth 4-5 (Python via macOS framework)

```
python@3.14/3.14.5/
├── .brew/                                ← pinned formula
├── bin/                                  ← python3, python3.14, pip3, pip3.14, pydoc3, idle3, ...
├── libexec/bin/                          ← unversioned aliases (python, pip, pydoc, idle)
├── lib/
│   ├── pkgconfig/                        ← python-3.14.pc, python3-embed.pc
│   └── python3.14/
│       ├── site-packages/                ← only pip 26.1.1 + wheel 0.47.0 here
│       └── (standard library)
├── Frameworks/Python.framework/Versions/ ← brew installs in framework mode for IDLE.app
├── IDLE 3.app/                           ← bundled IDLE GUI
├── Python Launcher 3.app/                ← bundled launcher
└── share/man/man1/
```

**Brew Python is "stdlib-only" at the global level** — `site-packages` carries just pip + wheel. Real Python tools are isolated:
- `pipx`-managed under `~/.local/pipx/` (if any installed; user prefers `uv`)
- `uv tool`-managed under `~/.local/share/uv/tools/` (jupyter-core, jupyterlab, openai-whisper)
- per-project virtualenvs

This matches the user's "no `sudo pip install`" hygiene and aligns with PEP 668's externally-managed-environment lock that newer brew Pythons enforce.

### `/opt/homebrew/Cellar/node/26.0.0/` — depth 3-4 (node anatomy)

```
node/26.0.0/
├── bin/                                  ← node, npm, npx, corepack
├── libexec/
│   ├── bin/                              ← versioned binaries
│   └── lib/node_modules/                 ← npm's "global" install root (unused here — user uses ~/.local/share/npm)
├── include/node/                         ← C++ headers for native modules
│   ├── libplatform/                      ← V8 platform abstraction
│   └── cppgc/                            ← V8 garbage collector headers
├── etc/bash_completion.d/
└── share/{man/man1,doc/node}/
```

### `/opt/homebrew/Caskroom/<cask>/<version>/` — two distinct cask shapes

**Shape A — "Symlink-to-/Applications" (the standard cask):**

```
visual-studio-code/1.121.0/
└── Visual Studio Code.app -> /Applications/Visual Studio Code.app
```

The actual `.app` lives in `/Applications`. The Caskroom version dir holds **only a symlink**. This is why the cask Caskroom dirs reported sizes of 12-20 KB — they're metadata-only.

**Shape B — "Self-contained binary in Caskroom":**

```
codex/0.133.0/
└── codex-aarch64-apple-darwin           (193 MB native ARM64 binary)
```

The OpenAI Codex cask stores the binary inside Caskroom and creates a symlink at `/opt/homebrew/bin/codex` pointing here. This is why `Caskroom/codex` is the second-largest at 185 MB. Same pattern likely for `gcloud-cli` (569 MB), `plugdata` (737 MB — the DAW bundles its full payload).

### `/opt/homebrew/Library/Homebrew/` — depth 3 (brew's own source, 218 entries)

```
Library/Homebrew/
├── brew.sh, brew.rb                      ← entry points (bash wrapper + Ruby main)
├── abstract_command.rb, abstract_subcommand.rb
├── analytics/, analytics.rb              ← anonymous usage metrics
├── api/, api.rb, api_hashable.rb         ← formulae.brew.sh API client
├── attestation.rb, autobump_constants.rb
├── bottle.rb, bottle_specification.rb    ← bottle handling
├── brew_irb_helpers, brew_irb_helpers.rb, brew_irbrc
├── build.rb, build_environment.rb, build_options.rb
├── bump.rb, bump_version_parser.rb
├── bundle/, bundle.rb, bundle_version.rb ← brew bundle (Brewfile)
├── cachable.rb
├── cache_store/, cache_store.rb
├── cask/, cask_dependent.rb              ← cask handling
├── cmd/                                  ← 87 user-facing subcommands
├── dev-cmd/                              ← maintainer-facing subcommands
└── … (190+ more .rb modules)
```

**`cmd/` highlights (the 87 `brew <subcommand>` surface):**
`--cache.rb`, `--caskroom.rb`, `--cellar.rb`, `--env.rb`, `--prefix.rb`, `--repository.rb`, `--taps.rb`, `--version.rb`, `alias.rb`, `analytics.rb`, `as-console-user.rb`, `autoremove.rb`, `bundle.rb`, `casks.rb`, `cleanup.rb`, `command-not-found-init.rb`, `command.rb`, `commands.rb`, `completions.rb`, `config.rb`, …

**`dev-cmd/` highlights** (developer/maintainer-only): `audit.rb`, `bottle.rb`, `bump-cask-pr.rb`, `bump-formula-pr.rb`, `bump-revision.rb`, `bump-unversioned-casks.rb`, `cat.rb`, `contributions.rb`, `create.rb`, `debugger.rb`, `determine-test-runners.rb`, `dispatch-build-bottle.rb`, `edit.rb`, `extract.rb`, …

### `/opt/homebrew/share/zsh-completions/` — depth 2 (180 completion functions)

All named `_<command>` per zsh convention. Sample alphabetic head: `_afew`, `_age`, `_archlinux-java`, `_atach`, `_augmatch`, `_augparse`, `_augprint`, `_avdmanager`, `_bento4`, `_bitcoin-cli`, `_blkid`, `_bower`, `_bundle`, `_cap`, `_cask`, `_ccache`, `_certbot`, `_cf`, `_chatblade`, `_chcpu`, …

These are loaded into zsh's `fpath`. Each one handles tab-completion for one external command (most installed by their respective brew formulae, dropped here).

### `/usr/libexec/apache2/` — depth 2 (115 `.so` Apache modules)

The complete Apache 2.4 module library is staged here, ready to load on `apachectl start`:

- **Auth modules** (16): `mod_auth_basic.so`, `mod_auth_digest.so`, `mod_auth_form.so`, `mod_authn_anon.so`, `mod_authn_core.so`, `mod_authn_dbd.so`, `mod_authn_dbm.so`, `mod_authn_file.so`, `mod_authn_socache.so`, `mod_authnz_ldap.so`, **`mod_authnz_od_apple.so`** (Apple OpenDirectory auth), `mod_authz_core.so`, `mod_authz_dbd.so`, `mod_authz_dbm.so`, `mod_authz_groupfile.so`, `mod_authz_host.so`, `mod_authz_owner.so`, `mod_authz_user.so`
- **Caching**: `mod_cache.so`, `mod_cache_disk.so`, `mod_cache_socache.so`, `mod_buffer.so`
- **Content-generation**: `mod_actions.so`, `mod_alias.so`, `mod_allowmethods.so`, `mod_asis.so`, `mod_autoindex.so`, `mod_cgi.so`, …
- Plus 80 more modules covering proxy, SSL/TLS, headers, env, logging, dav, lua, rewrite, etc.
- **`httpd.exp`** — the symbol-export file used by the Apache runtime to link modules.

**Apache is staged but not running.** Apple ships this complete because `apachectl` is a documented and supported control point, just not auto-started.

### `/usr/libexec/postfix/` — depth 2 (43 entries, full MTA)

A complete Postfix mail transport agent is staged:

**Daemons / delivery agents**: `master` (supervisor), `pickup`, `cleanup`, `qmgr`, `nqmgr`, `oqmgr`, `smtp`, `smtpd`, `local`, `virtual`, `lmtp`, `pipe`, `discard`, `error`, `bounce`, `flush`, `verify`, `proxymap`, `scache`, `anvil` (rate-limiting), `dnsblog` (DNS blacklists), `tlsmgr`, `tlsproxy`, `postscreen` (anti-spam triage), `qmqpd`, `qmqp-sink`, `qmqp-source`, `smtp-sink`, `smtp-source`, `showq`, `spawn`, `trivial-rewrite`.

**Helper scripts**: `post-install`, `postfix-script`, `postfix-tls-script`, `postfix-wrapper`, `postmulti-script`, `postfixsetup`, `mk_postfix_spool.sh`, `set_credentials.sh`, `greylist.pl`, `bind_unix_socket`, `scripts/`.

**Postfix is staged but not running.** Local mail delivery (e.g., cron job notifications) silently goes nowhere.

### `/usr/libexec/AssetCacheAgent/` — depth 2 (43 entries, Content Caching)

The Apple Content Caching service (used by `AssetCache` daemon). Contents are the agent's `.app`-style bundle:
- `AssetCacheAgent` (binary)
- `AssetCacheAgent.icns` (icon)
- Plus 41 `.lproj/` localization dirs: `ar.lproj`, `ca.lproj`, `cs.lproj`, `da.lproj`, `de.lproj`, `el.lproj`, `en_AU.lproj`, `en_GB.lproj`, `en.lproj`, `es_419.lproj`, `es.lproj`, `fi.lproj`, `fr_CA.lproj`, … (40+ languages)

### `/usr/share/zoneinfo/` — depth 3 (147 entries under `America/` alone)

Olson tzdata at full resolution. Sample `America/`:
`Adak`, `Anchorage`, `Anguilla`, `Antigua`, `Araguaina`, `Argentina/` (further subdir for city-level Argentine zones), `Aruba`, `Asuncion`, `Atikokan`, `Atka`, `Bahia`, `Bahia_Banderas`, `Barbados`, `Belem`, `Belize`, `Blanc-Sablon`, `Boa_Vista`, `Bogota`, `Boise`, `Buenos_Aires`, `Cambridge_Bay`, `Campo_Grande`, `Cancun`, `Caracas`, `Catamarca`, … (147 total).

`Argentina/` (depth 4) further enumerates Argentine sub-zones: `Buenos_Aires`, `Catamarca`, `Cordoba`, `Jujuy`, `La_Rioja`, `Mendoza`, `Rio_Gallegos`, `Salta`, `San_Juan`, `San_Luis`, `Tucuman`, `Ushuaia`.

### `/usr/share/sandbox/` — depth 3 sample (one `.sb` profile)

The TinyScheme sandbox-profile language. Example head of `airportd.sb`:

```scheme
;; Copyright (c) 2012 Apple Inc.  All Rights reserved.
;; WARNING: The sandbox rules in this file currently constitute
;; Apple System Private Interface and are subject to change at any time…

(version 1)
(deny default)                          ; start from total denial
(import "system.sb")                    ; pull in the standard system allow-list
(system-network)                        ; helper macro: allow network syscalls

(allow authorization-right-obtain
    (right-name "system.keychain.modify")
    (right-name "system.keychain.create.loginkc")
    (right-name "com.apple.wifi")
    (right-name "config.modify.com.apple.wifi")
    (right-name "system.preferences"))

(allow distributed-notification-post)
…
```

This is `sandbox-exec(1)`'s rule format — used by `sandboxd` to enforce per-daemon restrictions. The `(deny default)` + targeted allows is the canonical macOS App Sandbox approach.

### `/private/etc/asl/` — depth 2 (14 ASL filter files)

Apple System Log filters. Each file routes a log facility to a specific destination file with rotation policy.

`com.apple.install` example (representative):
```
# install messages get saved only in /var/log/install.log
? [= Facility install] claim only
* file /var/log/install.log format='$((Time)(JZ)) $Host $(Sender)[$(PID)]: $Message' \
       rotate=seq compress file_max=50M all_max=150M size_only
```

This is why `/private/var/log/install.log` is 18 MB — it's capped at 150 MB total across rotations (current + N gzipped). Sibling filters: `com.apple.authd`, `com.apple.cdscheduler`, `com.apple.contacts.ContactsAutocomplete`, `com.apple.coreduetd`, `com.apple.eventmonitor`, `com.apple.iokit.power`, `com.apple.login.guest`, `com.apple.mail`, `com.apple.MessageTracer`, `com.apple.mkb`, `com.apple.mkb.internal`, `com.apple.networking.boringssl`, `com.apple.performance`.

### `/private/var/folders/l9/zn9x070d4xqb1qb5wfzr9tjr0000gn/T/` — `$TMPDIR` depth 2 (138 MB)

Top consumers:

| Entry | Size | What it is |
|---|---|---|
| `AppTranslocation/` | **62 M** | Where macOS quarantines apps run from Downloads (Ghostty's PATH entry lives in here) |
| `tmp-E1F8957C-1F76-49EC-AA11-C37B7455C138` | 27 M | Random tmpdir (likely an installer or downloader artifact) |
| `plpl-62579CAC-3105-4FFF-8245-0421AD25EA22.png` | 13 M | A 13 MB PNG with a UUID name — probably a paste-board screenshot or app export |
| `node-compile-cache/` | 6.6 M | Node.js v18+ on-disk JIT cache (`NODE_COMPILE_CACHE`) |
| `CFNetworkDownload_VOU2gO.tmp` | 5.3 M | CFNetwork download scratch (Foundation HTTP) |
| `pyrefly_bundled_typeshed_98b51a9c3641/` | 5.1 M | pyrefly (Meta's new Python type checker) typeshed bundle |
| `MediaCache/` | 3.4 M | AVFoundation media-loading cache |
| `com.apple.TelephonyUtilities/` | 2.3 M | iPhone/SMS bridge state |
| `v0_contentLoader.db-wal` | 2.0 M | SQLite WAL for some content loader |
| `CFNetworkDownload_RIsnwD.tmp` | 1.1 M | Another CFNetwork download |
| `com.apple.CloudDocs.iCloudDriveFileProvider/` | 972 K | iCloud Drive scratch |
| `com.apple.imagent/` | 852 K | iMessage agent scratch |
| `tmp.4lBlHlUWHa` | 460 K | Random tmp |
| `unleash-repo-schema-v1-codeium-language-server.json` | 456 K | Codeium LSP feature-flag bundle (Unleash schema) |
| `com.apple.imtransferservices.IMTransferAgent/` | 416 K | iMessage attachment transfer agent |

### `/private/var/folders/.../C/` — per-user cache depth 2 (244 MB)

| Entry | Size | What |
|---|---|---|
| `clang/` | **89 M** | Clang module cache (compiler IR/AST cache) |
| `com.apple.Safari.SafeBrowsing` | 21 M | Safari's Google Safe Browsing local database |
| `com.google.Chrome.helper` | 18 M | Chrome helper WebKit cache |
| `com.apple.dock.iconcache` | 15 M | macOS Dock icon thumbnails |
| `com.apple.FontRegistry` | 10 M | Font-registry cache |
| `com.apple.WebKit.GPU` | 9.7 M | WebKit GPU process cache |
| `com.apple.iconservicesagent` | 8.7 M | Generic icon-service cache |
| `com.anthropic.claudefordesktop.helper` | 6.1 M | Claude Desktop app's WebKit cache |
| `com.apple.FeatureStore` (under `/0/`) | (also present here?) | |
| `com.microsoft.edgemac.helper` | 4.7 M | Edge WebKit cache |
| `com.github.Electron.helper` | 4.4 M | GitHub Desktop Electron cache |
| `com.google.antigravity.helper`, `com.google.antigravity-ide.helper` | 4.4 M + 4.0 M | **Google Antigravity IDE** caches |
| `com.openai.codex.helper` | 3.5 M | OpenAI Codex helper cache |
| `com.microsoft.VSCode.helper` | 3.3 M | VS Code Electron cache |
| `com.openai.atlas.web.helper` | 2.9 M | OpenAI Atlas browser helper cache |

**5 Electron/WebKit-based AI/dev apps in the cache** — Claude Desktop, Codex, Atlas, Antigravity (Google), VS Code — plus 2 traditional browsers (Chrome, Edge). The browser landscape is dense here.

### `/private/var/folders/.../0/` — depth 2 (34 MB)

Mostly **sysdiagnose run scratch** — `sysdiagnose.NNN-XxxxXx/` per-PID temporary dirs (9 of them, sized 0.8–2.2 MB each). Plus:
- `Store/` (4.1 M)
- `com.apple.FeatureStore/` (18 M — Apple Intelligence eligibility store)

### `/private/etc/postfix/postfix-files.d/` — empty

Subdir exists but holds no per-package additions to `postfix-files` policy.

## 13. Final size accounting (after depth-5 sweep)

A clean disk-cost summary for the four roots:

```
TOTAL SIZE OF THE FOUR ROOTS:
  /bin           9.4 MB    (sealed, immutable)
  /opt           12   GB   ≈ Homebrew 12 G + pkgx ~0 B
  /usr          794   MB   (sealed except /usr/local 18 M)
  /private      ~10   GB   (≈ etc 1.5 M + tmp 7.6 M + var 8.8 G)
  ─────────
  Combined:    ~23   GB
```

Inside `/private/var` (8.8 GB), the **recoverable disk**:
- **2.3 GB** — orphan browser code-sign clones in `var/folders/.../X/` (immediate reclaim)
- **2.0 GB** — `sleepimage` (hibernation; reclaimable if hibernation is disabled but most users want it)
- **2.6 GB** — `db/diagnostics` (cannot delete safely; rotates itself; only manual `log erase` should be used)

Inside `/opt/homebrew` (12 GB), the **recoverable disk**:
- **107 MB** — orphan `var/log/newrelic-infra/`
- **39 MB** — `var/log/ollama.log` (would clear if LaunchAgent fixed)
- **1.0 GB** — Caskroom (will return on next cask reinstall but currently cached source archives)
- The 6.6 GB Cellar is all in active use (no multi-version drift; no autoremove candidates).

## 14. Depths 6 + 7 — source files read, structure decoded

At depths 6-7 the system stops being directory-shaped and starts being source-shaped. This section reads the load-bearing files at each frontier rather than just enumerating leaves.

### A real brew formula — `/opt/homebrew/Cellar/atuin/18.16.1/.brew/atuin.rb` (depth 5)

The full file (31 lines) — preserved verbatim because it's small and explanatorily rich:

```ruby
class Atuin < Formula
  desc "Improved shell history for zsh, bash, fish and nushell"
  homepage "https://atuin.sh/"
  url "https://github.com/atuinsh/atuin/releases/download/v18.16.1/source.tar.gz"
  sha256 "aec5c91207f080becc4b13593d5b7edc46685e8d4dbfbaef33d31f8058191bc6"
  license "MIT"
  head "https://github.com/atuinsh/atuin.git", branch: "main"

  depends_on "protobuf" => :build
  depends_on "rust" => :build

  def install
    system "cargo", "install", *std_cargo_args(path: "crates/atuin")
    generate_completions_from_executable(bin/"atuin", "gen-completion", "--shell",
                                         shells: [:bash, :zsh, :fish, :pwsh])
  end

  service do
    run [opt_bin/"atuin", "daemon"]
    keep_alive true                       # ← this becomes <key>KeepAlive</key><true/> in the plist
    log_path var/"log/atuin.log"
    error_log_path var/"log/atuin.log"
  end

  test do
    ENV["ATUIN_SESSION"] = "random"
    assert_match "autoload -U add-zsh-hook", shell_output("#{bin}/atuin init zsh")
    assert shell_output("#{bin}/atuin history list").blank?
  end
end
```

**Three structural facts visible:**

- `depends_on "rust" => :build` and `depends_on "protobuf" => :build` are **build-only deps** (`:build`). Brew installs them while compiling atuin, then atuin's binary is statically linked and runs without them. This is why the Cellar contains `rust` and `protobuf` even though atuin's runtime dependency list (in `INSTALL_RECEIPT.json`) is empty.
- `generate_completions_from_executable(...)` invokes `atuin gen-completion --shell <name>` for each of `bash, zsh, fish, pwsh` and writes the output into `share/<shell>/`. This is how completions land in `/opt/homebrew/share/zsh-completions/_atuin` etc.
- **The `service do` block is the canonical source of brew-managed LaunchAgents.** `keep_alive true` becomes the plist's `<key>KeepAlive</key><true/>`, `log_path var/"log/atuin.log"` becomes `<key>StandardOutPath</key>` etc. The plist file at `homebrew.mxcl.atuin.plist` is rendered from this declaration at install time. **`KeepAlive true` is the formula author's choice, not the user's** — to override, the user must `launchctl unload` and remove the plist, or use `brew services stop atuin` and manage atuin manually.

### `INSTALL_RECEIPT.json` — install-time metadata (atuin's, depth 4)

```json
{
  "homebrew_version": "5.1.11-68-ge7b7e19",          ← brew at install time (now 5.1.13-38-gbc4c8a8)
  "built_as_bottle": true,
  "poured_from_bottle": true,                         ← prebuilt arm64 bottle, not source-compiled
  "loaded_from_api": true,                            ← formula came from the JSON API, not a local tap
  "installed_on_request": true,                       ← user-requested leaf (vs transitive)
  "changed_files": [
    "homebrew.atuin.service",                         ← list of LaunchAgent/systemd files materialized
    "homebrew.mxcl.atuin.plist"
  ],
  "time": 1778688057,                                 ← install epoch (April 17, 2026)
  "source_modified_time": 1778629013,
  "compiler": "clang",
  "runtime_dependencies": [],
  "source": {
    "spec": "stable",
    "versions": { "stable": "18.16.1", "head": null, "version_scheme": 0 },
    "tap": "homebrew/core"
  },
  "arch": "arm64",
  "built_on": {
    "os": "Macintosh",
    "os_version": "macOS 26",
    "cpu_family": "dunno",                            ← brew's old CPU-family classifier doesn't know Apple Silicon
    "xcode": "26.4",
    "clt": "26.4.0.0.1774242506",
    "preferred_perl": "5.34"
  }
}
```

**`installed_on_request: true`** is the field `brew leaves` reads. Every `installed_on_request: false` formula is a transitive dep that brew can autoremove if its parents are uninstalled. **`cpu_family: "dunno"`** is brew's literal string for "unrecognized" — Apple Silicon hasn't been categorized into brew's old Intel CPU family taxonomy (`westmere`, `nehalem`, `sandybridge`, etc.). Cosmetic, not load-bearing.

### Git templates and hooks — `/opt/homebrew/Cellar/git/2.54.0/share/git-core/` (depth 5-7)

**`templates/`** seeds every new `git init` repo. Contents (depth 5):

```
templates/
├── description       ← default description for gitweb
├── hooks/            ← 14 hook templates (all .sample, see below)
└── info/             ← empty (info/exclude is created at init)
```

**`templates/hooks/`** (depth 6) — the 14 hook samples shipped with git 2.54:

```
applypatch-msg.sample, commit-msg.sample, fsmonitor-watchman.sample,
post-update.sample, pre-applypatch.sample, pre-commit.sample,
pre-merge-commit.sample, pre-push.sample, pre-rebase.sample,
pre-receive.sample, prepare-commit-msg.sample, push-to-checkout.sample,
sendemail-validate.sample, update.sample
```

All carry the `.sample` suffix — git ignores them unless renamed to drop `.sample`. The default `pre-commit.sample` (depth 7) is a 49-line shell script that:
- Picks a diff base (`HEAD` or empty tree for initial commit)
- Reads `hooks.allownonascii` from git config
- Rejects non-ASCII filenames using `tr` byte ranges
- Calls `git diff-index --check` to reject trailing whitespace

**`contrib/`** (depth 5) — the "officially shipped but unsupported" extras:

```
contrib/
├── buildsystems/             ← cross-build helpers
├── completion/               ← bash + zsh + tcsh completion sources
├── contacts/                 ← `git contacts <file>` to find file authors
├── credential/               ← credential helper source (osxkeychain, libsecret, etc.)
├── diff-highlight/           ← pretty diff post-processor
├── fast-import/              ← fast-import format examples
├── git-jump/                 ← `git jump` (editor jump-to-diff)
├── git-shell-commands/       ← `git-shell` server helpers
├── libgit-rs/                ← Rust bindings (NEW — recent git versions)
├── libgit-sys/               ← Rust raw C bindings
├── long-running-filter/      ← long-running clean/smudge filter examples
├── Makefile, meson.build, README
├── rerere-train.sh           ← train `git rerere` from history
├── stats/                    ← line-count and file-count tools
├── subtree/                  ← `git subtree` source (it's contrib, not core!)
└── vscode/                   ← VS Code git-development integration
```

Notable: **`subtree/` is in contrib**, not core — `git subtree` ships but is technically not officially supported. **`libgit-rs/` + `libgit-sys/`** are new Rust bindings — git is migrating toward Rust as a build-time language.

**`libexec/git-core/mergetools/`** (depth 4 — pinned now) — 24 mergetool definitions:
`araxis`, `bc`, `codecompare`, `deltawalker`, `diffmerge`, `diffuse`, `ecmerge`, `emerge`, `examdiff`, `guiffy`, `gvimdiff`, `kdiff3`, `kompare`, `meld`, `nvimdiff`, `opendiff`, `p4merge`, `smerge`, `tkdiff`, `tortoisemerge`, `vimdiff`, `vscode`, `winmerge`, `xxdiff`.

These are the legal values of `git mergetool --tool=<name>` and `git config merge.tool <name>`. Each file is a shell script defining `cmd`, `merge_cmd`, etc.

**`share/perl5/Git/`** (depth 5):
`I18N.pm`, `IndexInfo.pm`, `LoadCPAN/`, `LoadCPAN.pm`, `Packet.pm`, `SVN/`, `SVN.pm`. The `SVN/` tree is for `git-svn`; `I18N.pm` is git's translation glue.

### Python 3.14 stdlib — what's new in 3.14 visible at depth 5-6

**`/opt/homebrew/Cellar/python@3.14/3.14.5/Frameworks/Python.framework/Versions/3.14/lib/python3.14/`** holds the 200-entry stdlib. Highlights revealing modernity:

- **Cross-platform support modules**: `_aix_support.py`, `_android_support.py`, `_apple_support.py`, `_ios_support.py`, `_osx_support.py`. **iOS and Android are now first-class Python platforms** (PEP 730/738 landed in 3.13).
- **`_pyrepl/`** subdir — Python 3.13+ shipped a new improved interactive REPL written in pure Python (replacing the old C-based `readline`-bound one). Visible at depth 6.
- **`annotationlib.py`** — new in 3.14 (PEP 749, lazy evaluation of annotations).
- **`build-details.json`** — new machine-readable Python build info (PEP 739).
- **`_sysconfig_vars__darwin_darwin.json`** — sysconfig data serialized as JSON instead of only Python.
- `antigravity.py` — the easter-egg module that opens `xkcd.com/353` in your browser (still there).

**`asyncio/`** (depth 6) — 35 files, showing the recent async maturity:

```
asyncio/
├── __init__.py, __main__.py
├── base_events.py, base_futures.py, base_subprocess.py, base_tasks.py
├── events.py, futures.py, tasks.py
├── protocols.py, streams.py, transports.py, trsock.py
├── proactor_events.py            ← Windows IOCP-style event loop
├── selector_events.py            ← Unix select-style event loop
├── unix_events.py, windows_events.py, windows_utils.py
├── sslproto.py
├── runners.py
├── coroutines.py, exceptions.py, constants.py
├── format_helpers.py, log.py, mixins.py
├── locks.py, queues.py, subprocess.py, threads.py
├── graph.py            ← NEW IN 3.14 (asyncio task-graph introspection)
├── staggered.py        ← staggered race / happy-eyeballs (3.12+)
├── taskgroups.py       ← PEP 654 TaskGroup (3.11+)
├── timeouts.py         ← asyncio.timeout context manager (3.11+)
└── tools.py
```

**`lib-dynload/`** (depth 6) — **76 compiled C extension modules** named `<modname>.cpython-314-darwin.so`:

`_asyncio`, `_bisect`, `_blake2`, `_bz2`, `_codecs_cn`, `_codecs_hk`, `_codecs_iso2022`, `_codecs_jp`, `_codecs_kr`, `_codecs_tw` (the CJK codec family), `_csv`, `_ctypes` + `_ctypes_test`, `_curses` + `_curses_panel`, `_dbm`, `_decimal`, `_elementtree`, `_hashlib`, `_heapq`, … and 55 more.

These are the platform-specific C parts of the stdlib — anything that needs to touch the OS through C: `_socket`, `_ssl`, `_sqlite3`, etc. all live here.

### A brew subcommand source — `/opt/homebrew/Library/Homebrew/cmd/cleanup.rb` (depth 4, 72 lines)

The canonical structure every brew subcommand follows:

```ruby
# typed: strict
# frozen_string_literal: true

require "abstract_command"
require "cleanup"                              # the actual implementation

module Homebrew
  module Cmd
    class CleanupCmd < AbstractCommand
      cmd_args do
        days = Homebrew::EnvConfig::ENVS[:HOMEBREW_CLEANUP_MAX_AGE_DAYS]&.dig(:default)
        description <<~EOS
          Remove stale lock files and outdated downloads for all formulae and casks,
          and remove old versions of installed formulae. …
        EOS
        flag   "--prune=", description: "Remove all cache files older than <days>. " \
                                        "If you want to remove everything, use `--prune=all`."
        switch "-n", "--dry-run", …
        switch "-s", "--scrub", …
        switch "--prune-prefix", …
        named_args [:formula, :cask]
      end

      sig { override.void }
      def run
        days = args.prune.presence&.then do |prune|
          case prune
          when /\A\d+\Z/ then prune.to_i
          when "all"      then 0
          else raise UsageError, "`--prune` expects an integer or `all`."
          end
        end
        cleanup = Cleanup.new(*args.named, dry_run: args.dry_run?, scrub: args.s?, days:)
        if args.prune_prefix?
          cleanup.prune_prefix_symlinks_and_directories
          return
        end
        …
      end
    end
  end
end
```

Three things visible:

- **Sorbet types** (`# typed: strict`, `sig { override.void }`) — brew uses static type checking for its Ruby code. Required by `brew style`.
- **The `cmd/<name>.rb` is a thin shell** — it declares args and runs. Heavy logic lives in `Library/Homebrew/<name>.rb` (here `cleanup.rb`).
- **Env-driven defaults**: `HOMEBREW_CLEANUP_MAX_AGE_DAYS` is documented in the description.

### System zsh — `/usr/share/zsh/5.9/` (depth 5-6)

Apple's sealed-volume zsh tree:

```
zsh/5.9/
├── functions/        ← 1203 completion + utility functions
├── help/             ← run-help text for built-ins
└── scripts/          ← installable shell scripts
```

**`functions/`** has **1203 entries** — each a zsh shell function file. The completion-function naming convention (`_<command>`) means most of these are bundled completions for every common Unix tool. Sample alphabetic head: `__arguments`, `_a2ps`, `_a2utils`, `_aap`, `_abcde`, `_absolute_command_paths`, `_ack`, `_acpi`, `_acpitool`, `_acroread`, `_adb`, `_add-zle-hook-widget`, `_add-zsh-hook`, `_alias`, `_aliases`, `_all_labels`, `_all_matches`, `_alsa-utils`, `_alternative`, `_analyseplugin`, `_ansible`, `_ant`, `_antiword`, `_apachectl`, `_apm`, … (1203 total).

**Apple ships an enormous completion library out of the box.** Most users never invoke `compinit` to load them, but they're there.

`/opt/homebrew/share/zsh/help/` mirrors this for Homebrew's zsh build but with content from the upstream zsh distribution (covers built-ins like `alias`, `autoload`, `bg`, `bindkey`, `break`, `builtin`, `bye`, `cap`, `cd`, `chdir`, …).

### `/private/var/db/uuidtext/<bucket>/<file>` — depth 3

Each two-character hex bucket (`00`–`FF`) holds files named with the remaining 30 hex chars of a UUID. Bucket `00/` (sample) has 8 files:

```
00/
├── 000000000000000000000000000000     ← null-UUID symbol file (anonymous code)
├── 2CF171C7E9350D8034B9B068A90C15
├── 3446363185317DA2465AD444C76C0A
├── 37EF956FFC3AE38B2CBD4D8E968F58
├── 408B3129D039218AB64045DA9A7E33
├── 83D36AF7B7391F8C76FAEE30886097
├── 94DA1DC112381AA22B7ADC430A7113
└── C20F4D00A737A9880ECA848075765C
```

Each file is the binary symbol table for one Mach-O binary, keyed by the binary's LC_UUID load-command. `log show` consults these to translate raw instruction-pointer addresses in tracepoints to symbol names. The `00`-bucket alone has 8 files; aggregated across 256 buckets explains the 715 MB total.

### `/private/var/db/SystemPolicyConfiguration/XProtect.bundle/Contents/Resources/` — depth 5 (Apple's malware brain)

```
XProtect.bundle/Contents/
├── Info.plist
└── Resources/
    ├── gk.db                              ← Gatekeeper SQLite policy database
    ├── XProtect.yara                      ← Apple's MAIN MALWARE YARA RULES
    ├── XPScripts.yr                       ← XProtect script-detection rules (YARA)
    ├── XProtect.plist                     ← bundle index
    ├── XProtect.meta.plist                ← metadata
    └── LegacyEntitlementAllowlist.plist   ← apps grandfathered into legacy entitlements
```

**The actual Apple malware detection ruleset is right here**, on every Mac, in YARA format. `XProtect.yara` is Apple's main signature file; `XPScripts.yr` adds script-pattern detection. These are updated independently of macOS itself via the XProtect updater LaunchDaemon — Apple ships new signatures without a full OS update. Anyone can `cat XProtect.yara` to read them (root for some files), and you'll see the rule names corresponding to currently-known malware families.

`/private/var/db/SystemPolicyConfiguration/XProtect.app/Contents/` (depth 5) is a standard macOS app bundle:

```
XProtect.app/Contents/
├── Info.plist, version.plist, PkgInfo
├── MacOS/                          ← main executable
├── Resources/                      ← icons, .strings, etc.
├── Frameworks/                     ← embedded frameworks
├── _CodeSignature/CodeResources    ← code-signing manifest
└── XPCServices/                    ← XPC services for IPC
```

A full Mach-O .app bundle with XPC services for inter-process communication. Launched not by user click but by `xprotect_service` / `XProtectRemediatorService` per Apple's malware-remediation flow.

### `/private/etc/apache2/{extra,original,other,users}/` — depth 3

**`extra/`** (12 modular Apache configs that `httpd.conf` selectively includes):

```
httpd-autoindex.conf, httpd-dav.conf, httpd-default.conf, httpd-info.conf,
httpd-languages.conf, httpd-manual.conf, httpd-mpm.conf,
httpd-multilang-errordoc.conf, httpd-ssl.conf, httpd-userdir.conf,
httpd-vhosts.conf, proxy-html.conf
```

`httpd-userdir.conf` enables the legacy `~/Sites/` per-user web-serving. `httpd-dav.conf` would enable WebDAV. `httpd-mpm.conf` configures the multi-processing module (worker/prefork/event).

**`original/`** holds Apple's pristine unmodified config (just `httpd.conf` + `extra/`) for rollback.

**`other/`** has two stale extensions:
- `mpm.conf` — additional MPM tuning
- **`php7.conf` — a PHP 7 Apache module config**, but **PHP is not installed** (no `php` formula in brew, no system PHP). Another orphan from a previous PHP-on-Apache experiment.

**`users/`** — empty. Per-user-virtualhost include target.

### `/private/etc/postfix/postfix-files` — file-management policy (441 lines)

The `postfix-install` / `post-install` scripts read this file to set permissions on every Postfix-managed file. Format:

```
# Each record describes one file or directory.
# Fields are separated by ":". Specify a null field as "-".
#   name:type:owner:group:permission:flags
#   No group means don't change group ownership.
# File types:
#   d=directory
#   f=regular file
#   h=hard link (*)
#   l=symbolic link (*)
```

441 lines define the canonical permissions for every Postfix daemon, queue, config file, and helper script. Used not at runtime but during install/upgrade to enforce least-privilege.

### Why depth 7 is the natural floor for human-meaningful inspection

At depth 7+ we're inside files: shell-script lines, Ruby methods, YARA rules, JSON objects, tracev3 binary chunks, compiled .so symbol tables. The directory structure has been exhausted — further descent is reading code line-by-line, which is an *editorial* task (pick what to read because of a question), not a *cataloguing* one (enumerate what's here).

The four roots' total directory inventory at this point:

```
Depth         /bin    /opt    /usr    /private    TOTAL
─────────────────────────────────────────────────────────
1               0       2       7         4         13
2              ~40    ~280    ~120       ~70       ~510
3                     ~750   ~1600     ~370      ~2700
4                    ~9000   ~6000   ~12000     ~27000
5                  ~25000  ~12000   ~45000     ~82000
6                  thousands per branch
7                  files, not dirs
```

(Approximations — `/bin` has only file leaves at depth 1, no descent. `/opt/homebrew/Library/Homebrew/`, `/usr/libexec/apache2/`, `/private/var/db/uuidtext/<bucket>/` are the explosion points.)

## 15. Depths 8 + 9 — primary-source content reads + orthogonal dimensions

### Apple's actual malware ruleset — `/private/var/db/SystemPolicyConfiguration/XProtect.bundle/Contents/Resources/XProtect.yara` (depth 6, content depth 8)

**File metrics**: 17,331 lines, **462 rules**. Structure:

```yara
import "hash"                              ← YARA hash module for SHA matching

private rule Macho
{
    meta:
        description = "private rule to match Mach-O binaries"
    condition:
        uint32(0) == 0xfeedface  or         ← 32-bit LE
        uint32(0) == 0xcefaedfe  or         ← 32-bit BE
        uint32(0) == 0xfeedfacf  or         ← 64-bit LE
        uint32(0) == 0xcffaedfe  or         ← 64-bit BE
        uint32(0) == 0xcafebabe  or         ← fat/universal LE
        uint32(0) == 0xbebafeca              ← fat/universal BE
}

private rule PE { … condition: uint16(0) == 0x5a4d and uint32(uint32(0x3C)) == 0x4550 }  ← MZ + PE
private rule Dylib { … }                  ← Mach-O with MH_DYLIB filetype
private rule Shebang { … condition: uint16(0) == 0x2123 }  ← #! shell scripts
private rule _golang_macho { …            ← matches Go-compiled Mach-Os by symbol presence
    strings:
        $gopclntab = "__gopclntab" ascii fullword
        $gosymtab = "__gosymtab" ascii fullword
        $build_magic_info = "\xff Go buildinf:" ascii
        $build_magic_id =  "\xff Go build ID: " ascii
        $symbol_name0 = "__cgo_init" ascii fullword
}
```

The 5 helper "private rules" (Macho, PE, Dylib, Shebang, _golang_macho) define binary-type predicates by checking magic bytes at known offsets. Then 462 detection rules follow, each typically named for a malware family (`MACOS.<Family>.A` style). Anyone with root read can `cat` this file to see exactly which threats Apple currently detects on this Mac.

### XProtect Safari extension blocklist — `XProtect.meta.plist` (depth 7)

```
ExtensionBlacklist:
  Extensions:
    [0] CFBundleIdentifier="com.searchnt.safari"     Developer Identifier="6ERPEMNB65"
    [1] CFBundleIdentifier="com.shelfsick.safari"    Developer Identifier="33HGJH7H8P"
    [2] CFBundleIdentifier="com.searchnt.safari"     Developer Identifier="LUZSN84HYP"
    [3] CFBundleIdentifier="com.searchtrust.safariext" Developer Identifier="9V6HEQPZK3"
    [4] CFBundleIdentifier="com.leperdvil.safari"    Developer Identifier="Y7QR7RXE99"
    [5] CFBundleIdentifier="info.trovi"              Developer Identifier="2GLUU75QJH"
    [6] CFBundleIdentifier="info.searchquick"        Developer Identifier="2GLUU75QJH"
    …
```

These are Safari extensions Apple has identified as adware/hijackers and disabled on every Mac. The Developer Identifier column lets Apple block by team, not just by bundle ID (same team `2GLUU75QJH` ships both `info.trovi` and `info.searchquick`).

### `gk.db` schema — the YARA bundle's sibling SQLite (depth 8)

```sql
CREATE TABLE settings        (name TEXT, value TEXT, PRIMARY KEY (name));
CREATE TABLE blocked_hashes  (hash BLOB, hash_type INTEGER, flags INTEGER,
                              PRIMARY KEY (hash, hash_type));
CREATE TABLE blocked_teams   (team_id TEXT, flags INTEGER, PRIMARY KEY (team_id));
```

Three tables, surprisingly clean:
- **`blocked_hashes`** — SHA blobs of known-bad binaries. Gatekeeper checks every newly-quarantined Mach-O against this before allowing first run.
- **`blocked_teams`** — revoked Developer ID team IDs. If Apple revokes a developer, the team ID lands here and every binary signed by that team is refused execution.
- **`settings`** — kv config for the policy engine.

The fact this DB is **inside the XProtect.bundle Resources**, not in a parent DB, means Apple ships hash/team blocklists as part of the XProtect-update bundle — independently updatable from macOS itself via the XProtectUpdater LaunchDaemon.

### `.LastGKReject` — empty payload (depth 7)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict/>
</plist>
```

Empty `<dict/>`. The file was modified today (May 22 12:16) but the modification was a **clear**, not a new rejection. **No active Gatekeeper rejection is on record.** The mtime alone misled the depth-5 sweep into suspecting an active rejection event; reading the content disproves it.

### Python's cross-platform stack — `_ios_support.py` (depth 7, full read)

The full file uses ctypes + the Objective-C runtime to call into iOS:

```python
import sys
try:
    from ctypes import cdll, c_void_p, c_char_p, util
except ImportError:
    print("ctypes isn't available; iOS system calls will not be available", file=sys.stderr)
    objc = None
else:
    lib = util.find_library("objc")
    if lib is None:
        raise ImportError("ObjC runtime library couldn't be loaded")
    objc = cdll.LoadLibrary(lib)
    objc.objc_getClass.restype = c_void_p
    objc.objc_getClass.argtypes = [c_char_p]
    objc.sel_registerName.restype = c_void_p
    objc.sel_registerName.argtypes = [c_char_p]


def get_platform_ios():
    is_simulator = sys.implementation._multiarch.endswith("simulator")
    if not objc:
        return None
    objc.objc_msgSend.restype = c_void_p
    objc.objc_msgSend.argtypes = [c_void_p, c_void_p]

    # Equivalent of: device = [UIDevice currentDevice]
    UIDevice = objc.objc_getClass(b"UIDevice")
    SEL_currentDevice = objc.sel_registerName(b"currentDevice")
    device = objc.objc_msgSend(UIDevice, SEL_currentDevice)

    # Equivalent of: device.systemVersion / systemName / model
    SEL_systemVersion = objc.sel_registerName(b"systemVersion")
    device_systemVersion = objc.objc_msgSend(device, SEL_systemVersion)
    SEL_systemName = objc.sel_registerName(b"systemName")
    device_systemName = objc.objc_msgSend(device, SEL_systemName)
    SEL_model = objc.sel_registerName(b"model")
    device_model = objc.objc_msgSend(device, SEL_model)

    SEL_UTF8String = objc.sel_registerName(b"UTF8String")
    objc.objc_msgSend.restype = c_char_p
    system = objc.objc_msgSend(device_systemName, SEL_UTF8String).decode()
    release = objc.objc_msgSend(device_systemVersion, SEL_UTF8String).decode()
    model = objc.objc_msgSend(device_model, SEL_UTF8String).decode()

    return system, release, model, is_simulator
```

This is **Python making raw `objc_msgSend` calls** through libobjc — manually building selectors and sending them to `UIDevice`. The simulator/device distinction comes from `sys.implementation._multiarch` (set at compile time by the iOS build). On macOS this code never runs (`platform.system() == "Darwin"` not "iOS"); it's stdlib readiness for when Python is built for iOS targets.

### Brew's `cleanup.rb` — 830 lines (depth 4, content depth 8)

The cmd shell at `cmd/cleanup.rb` (72 lines) delegates to `Library/Homebrew/cleanup.rb` (830 lines). Top reveals the cache-shape catalogue:

```ruby
# typed: strict
# frozen_string_literal: true

require "utils/bottles"
require "utils/output"
require "installed_dependents"
require "formula"
require "cask/cask_loader"

module Homebrew
  class Cleanup
    extend  Utils::Output::Mixin
    include Utils::Output::Mixin

    CLEANUP_DEFAULT_DAYS              = T.let(Homebrew::EnvConfig.cleanup_periodic_full_days.to_i.freeze, Integer)
    GH_ACTIONS_ARTIFACT_CLEANUP_DAYS  = 3
    private_constant :CLEANUP_DEFAULT_DAYS, :GH_ACTIONS_ARTIFACT_CLEANUP_DAYS

    class << self
      sig { params(pathname: Pathname).returns(T::Boolean) }
      def incomplete?(pathname)
        pathname.extname.end_with?(".incomplete")        # partial-download marker
      end

      sig { params(pathname: Pathname).returns(T::Boolean) }
      def nested_cache?(pathname)
        pathname.directory? && %w[
          cargo_cache
          go_cache
          go_mod_cache
          glide_home
          java_cache
          npm_cache
          pip_cache
          gclient_cache
        ].include?(pathname.basename.to_s)
      end
      …
```

`brew cleanup` knows about **eight nested language-tool caches** (Cargo, Go modules, Go workspace, Glide, Java, npm, pip, gclient) and prunes them by their tool-specific rules, not as opaque dirs. This is why `brew cleanup` is safe to run even when formulae have spawned subdir caches.

`T.let(...)` is **Sorbet typed-constant declaration** — brew's whole codebase uses Sorbet for static typing (`# typed: strict` headers; every method has a `sig { ... }` annotation).

### Symbol table of a compiled stdlib extension — `nm -gU` on `_asyncio.cpython-314-darwin.so` (depth 7, content depth 9)

```
0000000000000a28 T _PyInit__asyncio
```

**Exactly one externally-visible symbol**: `_PyInit__asyncio`. That's the Python C-API convention — each extension exposes only its `PyInit_<modname>` entry point at offset `0xa28` in the binary; CPython's import machinery calls it once at module load and the function registers all the classes and functions internally. The rest of the .so is static (file-local). This explains how Python keeps a clean namespace despite 76 compiled extensions.

### The orthogonal dimensions — xattrs, code-signatures, ACLs

**Extended attributes (xattrs)** are a parallel-depth axis that `ls`, `find`, and `du` don't see. macOS uses them to carry quarantine flags, Spotlight metadata, code-signing proofs, App Sandbox container linkage, and more.

```
/opt/homebrew/bin/atuin                                  → (no xattrs)
/opt/homebrew/Caskroom/codex/0.133.0/codex-…-darwin       → com.apple.metadata:kMDItemAlternateNames: ("codex")
                                                            com.apple.quarantine: 0181;6a0fb204;Homebrew Cask;<UUID>
/Applications/Warp.app                                   → com.apple.quarantine: 0181;6a0fb266;Homebrew Cask;<UUID>
```

**Reading the quarantine string:**
- `01` — quarantine flag set
- `81` — type code (download via known agent)
- `6a0fb204` — Unix timestamp in hex (when the file landed)
- `Homebrew Cask` — provenance string (which agent did the download)
- `<UUID>` — opaque identifier for the download event

**Why brew bottles don't carry the flag but casks do:** brew bottles are .tar.gz archives that brew extracts in place — brew controls the unpacking and never sets the xattr. Brew casks download `.app`/`.pkg`/binary files using mac-native APIs that **do** trigger the quarantine flag, and brew chooses to **preserve** it (changing the provenance string from the browser's "Safari"/"Chrome" to `Homebrew Cask`). This is why brew-cask-installed apps don't get re-quarantined by Gatekeeper on first launch — Gatekeeper sees `Homebrew Cask` and treats it as a recognized installer.

**Code signatures embedded in binaries** (`codesign -d --verbose=4`):

For the codex cask binary:

```
Executable=/opt/homebrew/Caskroom/codex/0.133.0/codex-aarch64-apple-darwin
Identifier=codex
Format=Mach-O thin (arm64)
CodeDirectory v=20500 size=378001 flags=0x10000(runtime) hashes=11802+7
                                                    ← 11,802 page hashes (×16 KB page = ~189 MB hashed content)
                                                    ← flags 0x10000 = hardened runtime ENABLED
Hash type=sha256 size=32
CDHash=6a9b65107fd593e5ec0ab1a06bec873f1bf41367
Signature size=9051
Authority=Developer ID Application: OpenAI OpCo, LLC (2DC432GLL2)
Authority=Developer ID Certification Authority
Authority=Apple Root CA
Timestamp=May 21, 2026 at 12:52:20 PM
TeamIdentifier=2DC432GLL2
```

**Three-tier signing chain** (canonical macOS): the binary signature was issued by Apple's *Developer ID* CA chain to **OpenAI OpCo, LLC** with team ID **`2DC432GLL2`**. The Apple timestamping authority countersigned on **May 21, 2026 at 12:52:20** (yesterday). Hardened runtime is on (`flags=0x10000`) — meaning the binary opts into stricter sandbox-like protections (no library loading from untrusted sources, no dyld_insert_libraries, etc.).

For `/bin/zsh` (sealed Apple-signed):

```
Executable=/bin/zsh
Identifier=com.apple.zsh
Format=Mach-O universal (x86_64 arm64e)
                                                    ← arm64e = pointer-authentication ARM variant (Apple Silicon native)
                                                    ← x86_64 included for compat
CodeDirectory v=20400 size=5382 flags=0x0(none) hashes=163+2
Platform identifier=26                              ← macOS 26 / Tahoe
```

Smaller binary (163 page hashes ≈ 2.6 MB), no hardened-runtime flag (it's sealed-volume code, signed directly by Apple's platform key — different trust path). The arm64e architecture confirms this is a true Apple-Silicon-native binary using pointer authentication codes (PAC).

**ACLs (Access Control Lists)** are also orthogonal to standard Unix permissions. `ls -le` shows them. Sample sensitive system files:

```
-r--r-----  1 root  wheel  1709 Apr 30 15:33 /private/etc/sudoers          ← Unix perms only; no ACL
-rw-------  1 root  wheel 10004 Apr 30 15:33 /private/etc/master.passwd    ← Unix perms only; no ACL
```

Both files rely on Unix mode bits (`r--r-----` and `rw-------`), not extended ACLs. No `+` after the mode field (which would indicate an ACL is attached). On this system, ACLs are not used for these critical files — pure Unix mode applies.

### The `pre-push.sample` template — full content (depth 7)

54 lines. Implements a "no WIP commits in pushes" gate:

```sh
#!/bin/sh
# This sample shows how to prevent push of commits where the log message
# starts with "WIP" (work in progress).

remote="$1"
url="$2"

zero=$(git hash-object --stdin </dev/null | tr '[0-9a-f]' '0')

while read local_ref local_oid remote_ref remote_oid
do
    if test "$local_oid" = "$zero"; then
        : # Handle delete (no-op)
    else
        if test "$remote_oid" = "$zero"; then
            range="$local_oid"                    # New branch → examine all commits
        else
            range="$remote_oid..$local_oid"       # Update → examine new commits
        fi

        commit=$(git rev-list -n 1 --grep '^WIP' "$range")
        if test -n "$commit"; then
            echo >&2 "Found WIP commit in $local_ref, not pushing"
            exit 1
        fi
    fi
done
```

The hook receives `<local_ref> <local_oid> <remote_ref> <remote_oid>` lines on stdin (one per branch being pushed) and `<remote_name> <remote_url>` as `$1 $2`. The "all zeroes" oid (`$zero`) is git's sentinel for "doesn't exist" (delete or initial push).

### git's actual runtime dependency tree — INSTALL_RECEIPT.json (depth 4, content depth 9)

```
3 runtime dependencies:
  - pcre2 10.47           (regex engine for grep, log, etc.)
  - libunistring 1.4.2    (Unicode string handling)
  - gettext 1.0           (i18n / message translation)
```

Surprisingly small — git 2.54 at runtime needs only 3 brew formulae. The big stuff (zlib, openssl, curl, expat, perl) is all linked statically into the brew bottle or fulfilled by the system.

### Apple's airportd sandbox profile — full 242 lines (depth 6, content depth 9)

A full read of `/usr/share/sandbox/airportd.sb` reveals deep Apple-internal architecture not visible in any documentation:

**Wi-Fi chip codename "Sunrise"** — the IOKit allow rules name `AppleSunriseHALDevice` (the HAL — Hardware Abstraction Layer) and `AppleSunriseWLAN` (the WLAN driver). This is Apple's internal codename for the Wi-Fi silicon. Similar to past codenames like "Hurricane" (M-series cores), "Sunrise" is the marketing-public's first glimpse at the chip identity.

**Calibration UUIDs** — `(iokit-property "36C28AB5-6566-4C50-9EBD-CBB920F83843:current-network")` writes to a vendor-specific UUID-keyed property. Each UUID identifies a calibration domain (current-network, preferred-networks, preferred-count); `airportd` is allowed to update them but not arbitrary keys.

**BT/Wi-Fi coexistence** — `MWS_BT_TRAFFIC_IMPACT_BCN_OFFLOAD`, `MWS_BT_TRAFFIC_IMPACT_SCAN_OFFLOAD` properties — "MWS" stands for Mobile Wireless Standards. The Wi-Fi chip and Bluetooth chip negotiate airtime, and `airportd` writes the impact-prediction values that drive that negotiation.

**Apple-private XPC services accessed by airportd**:
```
com.apple.private.corewifi.internal-xpc
com.apple.private.corewifi.unrestricted-xpc
com.apple.private.corewifi.user-agent-xpc
com.apple.corewlan-xpc
com.apple.WiFiVelocityAgent
com.apple.wifivelocityd
com.apple.airport.wps
com.apple.airportd
com.apple.wifid
com.apple.networking.captivenetworksupport
com.apple.private.networkd_privileged          (well — "networkd_privileged" without "private." prefix, but adjacent)
com.apple.duetactivityscheduler
com.apple.AppleSEPUserClient                    ← Secure Enclave access!
com.apple.AppleKeyStoreUserClient               ← Keystore access for credential decryption
com.apple.tccd.system                           ← TCC (Transparency, Consent, Control) — privacy gating
com.apple.symptom_diagnostics
com.apple.symptoms.symptomsd.managed_events
```

The Secure Enclave (`AppleSEPUserClient`) + KeyStore (`AppleKeyStoreUserClient`) access is needed to decrypt stored Wi-Fi passwords (which are protected by Secure Enclave-backed keys on Apple Silicon).

**TCC linkage**: `airportd` talks to `tccd.system` — meaning Wi-Fi operations can trigger the privacy-prompt system (e.g., "Allow X to use your current location via Wi-Fi"). This is how Wi-Fi-based location services route through TCC.

**Sandbox boundaries**:
- Allowed file-write paths: `/private/var/db/mds/system/mds.lock` (Spotlight), `/private/var/log/wifi.log`, `/Library/Keychains`, `/private/var/root/Library/Preferences/com.apple.airport.airportd.plist`
- Allowed device files: `/dev/io8log`, `/dev/io8logmt`, `/dev/io8logtemp` (IOKit logging), `/dev/pf` (packet filter), `/dev/bpf*` (Berkeley packet filter)
- Allowed AppleEvent: only to `com.apple.finder` (for "Reveal in Finder" style actions)

### Brew's TLS / cryptographic configs — `/opt/homebrew/etc/openssl@3/` (depth 4-5)

```
openssl@3/
├── openssl.cnf, openssl.cnf.dist    ← user config + distribution default
├── cert.pem                          ← 195 trusted Certificate Authorities
├── ct_log_list.cnf                   ← Certificate Transparency log list
├── ct_log_list.cnf.dist
├── certs/                            ← per-CA loose certs
├── misc/                             ← demo CA-management scripts
└── private/                          ← private keys (empty unless brew has been used as CA)
```

**195 CAs in the system trust bundle.** Sample issuers from the head: Cisco Root CA 2048, SecureTrust Secure Global CA, Network Solutions, VeriSign Class 3 G5, DigiCert TLS ECC P384 Root G5. This is the union of Mozilla's trust list + brew's tweaks — distinct from macOS's own keychain trust store (which the Keychain Access app shows).

**Three separate CA bundles exist on this machine** in brew alone:
1. `/opt/homebrew/etc/openssl@3/cert.pem` — for openssl(1)
2. `/opt/homebrew/etc/ca-certificates/cert.pem` — for `ca-certificates` formula (used by curl, wget, etc.)
3. `/opt/homebrew/etc/gnutls/cert.pem` — for gnutls

Plus the system's keychain trust store. **Four parallel trust stores.** They all derive from Mozilla's NSS trust list but maintained independently and could drift.

`openssl.cnf` opens with the standard OpenSSL config preamble; it sets `openssl_conf = openssl_init` (load providers on startup) and `config_diagnostics = 1` (warn on config errors). The user has not customized it (matches `.dist` file).

**Other formula configs visible**:
- `/opt/homebrew/etc/gnupg/scdaemon.conf` — smartcard daemon config (single file)
- `/opt/homebrew/etc/fish/config.fish` — system-wide fish init (single file)
- `/opt/homebrew/etc/unbound/` — DNS resolver config (2 entries)
- `/opt/homebrew/etc/byobu/` — byobu terminal-multiplexer config (2 entries)

### Why depth 9 is the genuine cataloguing floor

At depth 9 we've descended from:
- **Depth 1-5**: directory structure (where things live, who owns them, how big)
- **Depth 6-7**: file structure (formats, schemas, table-of-contents of source trees)
- **Depth 8-9**: primary content (actual rule grammars, function bodies, signature internals, xattr semantics)

Going further (depth 10+) means:
- Reading individual YARA rules to identify specific malware families (research task, not cataloguing)
- Disassembling Mach-O binaries (research task, requires `otool -tv` / `objdump`)
- Diffing tracev3 entries (research task, requires `log show --file --predicate`)
- Examining stack frames in running processes (research task, requires `sample`/`spindump`)
- Walking the dyld_shared_cache (research task, requires `dsc_extractor.bundle`)

Each is *editorially driven by a question* ("what was rejected today?" "which malware does this rule detect?" "why is this process hot?"), not by *cataloguing intent*. The forensic-context job is done. The detective-work job — if and when a question arises — begins from here.

## 16. Curation grid — every artifact, judged

The enumeration is done. Now the inversion: for each artifact catalogued, apply the four-question grid (NEED · UNIQUE · ORIGIN · OWNER) and assign an action verb. Six action verbs are available:

- **KEEP** — load-bearing and correct as-is
- **ALIGN** — what's on disk diverges from what the docs/memory/CLAUDE.md claim; bring the description into truth
- **PRUNE** — safe to delete; nothing depends on it
- **DEDUPE** — multiple copies of the same logical thing; pick one source
- **UNIFY** — separate things doing the same job; collapse to one authority
- **CONTAIN** — can't (or shouldn't) remove, but accumulates without bound; needs periodic discipline

The grid is organized by action verb so the action plan is readable as a worklist.

### 16.1 ALIGN — docs/memory/constitution diverge from disk

The constitution is hypothesis; disk is fact. These items have **document-says-X, disk-says-Y** mismatches.

| Artifact | Doc claim | Disk reality | Action |
|---|---|---|---|
| `~/.claude/CLAUDE.md` "Python: Anaconda at `/opt/anaconda3/`" | Anaconda is the Python install | `/opt/anaconda3` does not exist; `conda` not on PATH; only `~/.conda/aau_token{,_host}` residue (30 B) | **ALIGN**: edit chezmoi-source template at `dot_config/ai-context/*.md.tmpl`; replace with truth: "Python: 3.14 via Homebrew (`/opt/homebrew/opt/python@3`), plus pipx/uv-managed user tools; system `/usr/bin/python3` is 3.9.6 sealed." |
| `~/CLAUDE.md` four-registry section assumes anaconda existence implicitly | n/a | n/a | **ALIGN**: re-read for any other anaconda dependencies; none expected |
| MEMORY.md still has no entry recording the depth-1 audit's findings | Memory is hypothesis | This report is the new ground truth | **ALIGN**: add memory entry `project_artifact_2026_05_22_four_roots_audit.md` summarizing key findings |
| Rule #9 "no LaunchAgents anywhere" | Hard rule | 3 brew LaunchAgents + 8 vendor LaunchAgents are installed and running | **ALIGN**: either (a) amend Rule #9 to "no LaunchAgents *unless* brew services or vendor auto-installer, audited annually" — or (b) actually purge them. Decision needed; the current state is silent violation. |
| Memory's `project_session_2026_05_22_sysdiagnose_forensic_audit.md` named Jupyter as P0 SEC | Just naming | Confirmed verbatim — depth-7 read of `com.jupyter.server.plist` proved empty-token + wildcard CORS + XSRF-disabled | **ALIGN**: memory entry is accurate; no edit needed |

### 16.2 PRUNE — safe to delete, no dependents

For each: a one-line justification + the exact command. **Nothing here is executed by me** — these are recommendations only.

#### Trivially safe (small footprint, no risk)

| What | Where | Why safe | Command |
|---|---|---|---|
| Anaconda residue | `~/.conda/` (30 B total) | Conda is gone; tokens are stranded | `rm -rf ~/.conda` |
| `~/seed.yaml` | misplaced copy (IRF-OPS-040) | Already tracked; user-trash decision pending | `rm ~/seed.yaml` (or move to trash) |
| 16 broken `/usr/local/bin/python*t*` symlinks | `PythonT.framework` missing | Targets don't exist; cause `which python3t` to lie | `sudo find /usr/local/bin -name 'python*t*' -type l ! -execdir test -e {} \; -delete` |
| `/etc/paths.d/10-pmk-global` | pkgx PATH entry to `/pkg/env/global/bin` (broken on two axes since 2025-02) | Dead PATH entry every shell session | `sudo rm /etc/paths.d/10-pmk-global` |

#### Reclaim significant disk (>50 MB each)

| What | Where | Size | Command |
|---|---|---|---|
| Chrome code-sign clone | `$TMPDIR/X/com.google.Chrome.code_sign_clone` | 1.3 GB | `rm -rf "$TMPDIR/X/com.google.Chrome.code_sign_clone"` |
| OpenAI Atlas code-sign clone | `$TMPDIR/X/com.openai.atlas.web.code_sign_clone` | 956 MB | `rm -rf "$TMPDIR/X/com.openai.atlas.web.code_sign_clone"` |
| Orphan newrelic-infra logs | `/opt/homebrew/var/log/newrelic-infra/` | 107 MB | `rm -rf /opt/homebrew/var/log/newrelic-infra` |
| Ollama log spam | `/opt/homebrew/var/log/ollama.log` | 39 MB | `truncate -s 0 /opt/homebrew/var/log/ollama.log` (after stopping the LaunchAgent — see CONTAIN below) |
| Stale Homebrew Apache `mpm.conf` + `php7.conf` orphan | `/private/etc/apache2/other/` | <100 KB but conceptually | `sudo rm /private/etc/apache2/other/php7.conf` (apache won't run anyway) |

#### Orphan brew configs in `/opt/homebrew/etc/`

Verified at depth 5 that the parent formulae are uninstalled:

| Config | Parent formula | Status | Command |
|---|---|---|---|
| `redis.conf`, `redis-sentinel.conf` | `redis` | not installed | `rm /opt/homebrew/etc/redis.conf /opt/homebrew/etc/redis-sentinel.conf` |
| `php/` dir | `php` | not installed | `rm -rf /opt/homebrew/etc/php` |
| `freetds.conf` | `freetds` | not installed | `rm /opt/homebrew/etc/freetds.conf` |
| `newrelic-infra/` dir | `newrelic-infra` | not installed | `rm -rf /opt/homebrew/etc/newrelic-infra` |
| `pkcs11/`, `pkcs11.conf.example` | `pkcs11-helper` | not installed | `rm -rf /opt/homebrew/etc/pkcs11 /opt/homebrew/etc/pkcs11.conf.example` |
| `openldap/` dir | `openldap` | not installed | `rm -rf /opt/homebrew/etc/openldap` |
| `slsh.rc` | `s-lang` | not installed | `rm /opt/homebrew/etc/slsh.rc` |
| `odbc.ini`, `odbcinst.ini` | `unixodbc` | not installed | `rm /opt/homebrew/etc/odbc.ini /opt/homebrew/etc/odbcinst.ini` |
| `php-fpm.log` + `redis.log` | matching above | not installed | `rm /opt/homebrew/var/log/php-fpm.log /opt/homebrew/var/log/redis.log` |

#### Anaconda receipts in Apple's pkg ledger

| What | Where | Why prune | Command |
|---|---|---|---|
| 5 `io.continuum.pkg.*` receipts | `/private/var/db/receipts/` | Anaconda is gone; Apple thinks it's still installed | `sudo pkgutil --forget io.continuum.pkg.prepare_installation io.continuum.pkg.run_conda_init io.continuum.pkg.run_installation io.continuum.pkg.shortcuts io.continuum.pkg.user_post_install` |

#### LaunchAgents to consider removing

| Agent | Why | Command |
|---|---|---|
| `com.jupyter.server.plist` (P0 SEC) | Empty-token + wildcard CORS = drive-by RCE | `launchctl unload ~/Library/LaunchAgents/com.jupyter.server.plist && rm ~/Library/LaunchAgents/com.jupyter.server.plist && uv tool uninstall jupyter-core jupyterlab` (also removes the tools if you don't use them) |
| `homebrew.mxcl.ollama.plist` (error state) | LaunchAgent is failing to start; generates the 39 MB of log spam | `brew services stop ollama` (and decide: keep as on-demand CLI or uninstall) |

### 16.3 DEDUPE — same logical thing in multiple places, pick one source

| Logical thing | Copies | Which to keep | What to do |
|---|---|---|---|
| **zsh** | `/bin/zsh` (Apple 5.9, login shell) + `/opt/homebrew/bin/zsh` (brew 5.9, unused) | Decision needed | If keeping Apple zsh: `brew uninstall zsh` (frees ~5 MB) unless it's a dep of `zsh-{autocomplete,autosuggestions,completions,syntax-highlighting}`. If switching login: `sudo sh -c "echo /opt/homebrew/bin/zsh >> /etc/shells" && chsh -s /opt/homebrew/bin/zsh` |
| **Python 3.13** | `/opt/homebrew/Cellar/python@3.13` (brew transitive dep) + `/Library/Frameworks/Python.framework/Versions/3.13` (python.org installer) | Decision needed | If only brew matters: uninstall python.org via `sudo /Library/Frameworks/Python.framework/Versions/3.13/Resources/uninstall_python.sh` or `pkgutil --forget org.python.Python.Python*-3.13` + `rm -rf /Library/Frameworks/Python.framework/Versions/3.13 && rm /usr/local/bin/python3.13*` (frees ~70 MB + removes the dangling-symlink risk) |
| **bash** | `/bin/bash` (Apple 3.2.57, GPLv2-frozen) + `/opt/homebrew/bin/bash` (brew 5.3.9) | Keep both | They're not duplicates — Apple's is frozen for license reasons; brew's is current. Scripts that need bash ≥4 syntax must use the brew one. **No action; document the distinction.** |
| **CA trust stores** | `openssl@3/cert.pem` (195 CAs) + `ca-certificates/cert.pem` + `gnutls/cert.pem` + macOS Keychain | Each tool wants its own | **No prune** — these are required-separate-by-design. But UNIFY (next section) could symlink them to one source. |
| **Codex** | brew cask `codex` (185 MB Caskroom binary, in PATH via brew) + native `~/.local/share/claude` for Claude Code | Both serve different agents | Keep both — codex is OpenAI's, claude is Anthropic's |
| **VS Code variants** | `visual-studio-code` (1.121.0 stable) + `visual-studio-code@insiders` (1.122.0-insider) | User decision | If insider is the daily driver: `brew uninstall --cask visual-studio-code` |
| **Node aliases** | `node`, `node.js`, `nodejs`, `node@25`, `node@26` all → `Cellar/node/26.0.0` | All aliases of one install | **No action** — these are brew's intended symlink farm; can't dedupe without confusing dependent formulae |
| **Ruby aliases** | `ruby`, `ruby@3`, `ruby@3.4`, `ruby@4`, `ruby@4.0` all → `Cellar/ruby/4.0.5` | Same | **No action** — same pattern |

### 16.4 UNIFY — separate authorities doing the same job

| Domain | Separate authorities | Unify to | How |
|---|---|---|---|
| **CA trust** | 4 stores: openssl@3, ca-certificates, gnutls, Keychain | Could symlink the three brew bundles to one Mozilla-derived source | brew's `ca-certificates` formula updates first; the others can symlink: `ln -sf /opt/homebrew/etc/ca-certificates/cert.pem /opt/homebrew/etc/openssl@3/cert.pem` and similarly for gnutls. Then `brew reinstall ca-certificates` propagates updates to all three. Risk: openssl and gnutls expect file ownership; symlinks should work but test first. |
| **Plan registries** | `~/.claude/plans/` + per-repo `<repo>/.claude/plans/` + IRF + atoms registry + pipeline queue | The four-registry table in `CLAUDE.md` already names them; nothing to unify mechanically — they serve different scopes | KEEP separate; the existing routing is correct. |
| **CA bundles within macOS Keychain + brew bundle** | System keychain (managed by Apple) vs brew-managed `cert.pem` | Different sources; same purpose | Apple's keychain is updated via Software Update; brew's via `brew reinstall ca-certificates`. **No mechanical unification possible** — different update channels. Document the parallel and trust each within its scope. |
| **LaunchAgent inventory** | brew (3) + vendor (8) + Apple system (many) + user-custom (Jupyter) | No single inventory exists | **UNIFY** by writing a curated `~/Library/LaunchAgents/INVENTORY.md` listing every agent + decision-status. Periodic audit ritual. |
| **PATH composition** | 39 entries from `/etc/paths` + `/etc/paths.d/*` + user zsh init + Claude plugin caches + per-tool prefixes | This many entries makes shadowing unpredictable | **UNIFY**: write a documented PATH-order policy in chezmoi source; remove dead entries (`/pkg/env/global/bin`, ruby `gems/3.4.0/bin`, Ghostty AppTranslocation). Audit which Claude plugin bin paths are actually used. |

### 16.5 CONTAIN — can't remove cleanly, but accumulates

| Artifact | Accumulation pattern | Containment ritual |
|---|---|---|
| `/private/var/db/diagnostics/` (2.6 GB) | Apple grows the unified-log persistent store unbounded; will roll old chunks naturally but slowly | `sudo log erase --all` clears history (drastic); usually leave alone |
| `/private/var/db/uuidtext/` (715 MB) | Grows with every new binary signed; rarely shrinks | Apple-managed; no action |
| `/private/var/folders/.../X/` browser code-sign clones | Browsers leak these when self-updating | Periodically `find $TMPDIR/X -name '*code_sign_clone' -mtime +7 -exec rm -rf {} +` |
| `/private/var/folders/.../C/clang` (89 MB) | Clang module cache grows | `rm -rf $TMPDIR/C/clang` periodically (will rebuild) |
| `/private/var/folders/.../C/com.*.helper/` | Electron-app WebKit caches (Claude, Codex, Atlas, Antigravity, VS Code, etc.) | Each app should self-manage; if not, periodic prune |
| `/opt/homebrew/var/cache/` (6 MB) | Tarball download cache | `brew cleanup --prune=30` removes >30-day tarballs |
| `/opt/homebrew/Caskroom/<cask>/` | Cached installer dirs after install | `brew cleanup` handles |
| Vendor LaunchAgents (Google Updater, Edge Updater, OpenAI Atlas update-helper, etc.) | Each new app installs one without asking | Periodic audit + selective `launchctl disable` |
| `/usr/libexec/apache2/` (115 modules staged, not running) | Apple-shipped, sealed, immutable | No action — accept the ~10 MB shadow |
| `/usr/libexec/postfix/` (43 daemons staged, not running) | Apple-shipped, sealed | No action |
| `/private/var/db/receipts/` (94 files) | Grows with every `.pkg` install | `pkgutil --forget <id>` for confirmed-uninstalled apps; don't touch Apple-iWork ones |
| brew formula install records on disk (.brew/*.rb pinned at install time) | Each `brew upgrade` leaves the old pin | Auto-cleaned by `brew cleanup` |
| `/private/var/log/*.bz2` rotations | wifi.log rotates 11 times | Apple-managed (`newsyslog`) |

### 16.6 KEEP — verified correct as-is

Listed for completeness; no action.

| Domain | Verdict |
|---|---|
| `/bin` 37 sealed shells/utilities | Required by every script using `#!/bin/sh` etc. |
| `/usr/{bin,sbin,libexec,lib,share,standalone}` sealed | Apple-managed, signed, immutable |
| `/etc/paths` ordering | Correct as-is |
| `/etc/paths.d/{10-cryptex,100-rvictl,homebrew}` | Correct — only `10-pmk-global` is dead |
| User's `~/.zshrc` override for HISTFILE (per memory `feedback_histfile_override`) | Correct workaround for Apple `/etc/zshrc` clobber |
| `/opt/homebrew` as ARM brew prefix | Correct — Apple Silicon convention |
| Brew's `service do … keep_alive true` formula declarations | Formula-author choice; users override via `brew services stop` not by deleting plists |
| `homebrew.mxcl.atuin.plist` (live, working) | Atuin needs the daemon for shell-history sync; KEEP |
| `/opt/homebrew/Cellar` 230 formulae, all single-version | Brew has been kept tidy; no orphan deps detected |
| `/opt/homebrew/Library/Homebrew/` (brew's own source) | Standard layout |
| `/private/etc/pam.d/sudo_local.template` | Apple's blessed extension point — leave alone unless adding Touch ID for sudo (then copy template to `sudo_local`) |
| `/private/etc/ssh/{ssh,sshd}_config.d/100-macos.conf` | Apple-shipped SSH defaults |
| `/private/var/db/SystemPolicyConfiguration/{SystemPolicy,ExecPolicy,KextPolicy,Tickets,XProtect.bundle/}` | SIP-protected; root-only; managed by macOS |
| `XProtect.yara` (17,331 lines, 462 rules) | Apple-managed malware signatures; auto-updated |
| `/private/var/vm/sleepimage` (2 GB) | Required if hibernation enabled (`hibernatemode 3 + standby 1`) |
| `~/CLAUDE.md` being local-only | Documented constitutional gap (deliberate, per chezmoi-root-collision; offsite reproducibility via session-transcript registry) |

### 16.7 The grid summarized — by ownership

A complementary view: instead of grouping by action, group by **who owns** the thing — because action options collapse along that axis.

| Owner | Items | Available actions |
|---|---|---|
| **Apple (sealed SIP)** | `/bin/*`, `/usr/{bin,sbin,libexec,lib,share,standalone}/*`, `XProtect.{app,bundle}`, `/private/var/db/SystemPolicyConfiguration/*` | KEEP only — cannot mutate without disabling SIP |
| **Apple (writable `/private/etc/*`, `/private/var/db/*`)** | `pam.d/`, `ssh/`, `paths/`, `paths.d/`, `apache2/`, `postfix/`, `receipts/`, `xpc.launchd/disabled.*.plist`, `.LastGKReject` | KEEP/ALIGN/PRUNE specific orphans (e.g., apache `php7.conf`, anaconda receipts) |
| **Apple (`/private/var/{db,folders,log,vm}`)** | The 3.9 G of db/ + 2.7 G of folders/ + 92 M of log/ | KEEP/CONTAIN — `log erase`, `find … -delete` for confirmed orphan caches |
| **Homebrew ([user]:staff, `/opt/homebrew/*`)** | Cellar/, Caskroom/, etc/, var/, bin/, lib/, share/, Library/ | KEEP active formulae; PRUNE the 8 orphan configs + newrelic logs; DEDUPE brew vs Apple zsh; UNIFY CA bundles |
| **User ([user], `~/Library/LaunchAgents`, `~/.local/share/uv/tools/`, `~/.conda`)** | jupyter plist, vendor agents, uv tools, anaconda residue | Full mutation authority; PRUNE Jupyter + Anaconda; CONTAIN vendor agents |
| **Vendor-installer-owned (app bundles in /Applications and /Library)** | Backblaze, iMazing, Google Keystone, OpenAI Atlas helper, etc. | Per-app: KEEP or uninstall via the app's own uninstaller |
| **Abandoned (root-owned but unmaintained)** | `/opt/pkg/` (pkgx), `/etc/paths.d/10-pmk-global` | PRUNE — no maintainer to consult |

### 16.8 Action priority — first-cut sequence

If executing in order, the safest-first / highest-value-first sequence is:

1. **ALIGN documentation** (no-risk, high clarity gain) — fix CLAUDE.md Anaconda lie via chezmoi source; add this audit as memory entry.
2. **PRUNE trivially safe** (zero-dependency removals):
   - 16 broken `python*t*` symlinks in `/usr/local/bin`
   - `/etc/paths.d/10-pmk-global`
   - `~/.conda/`
3. **PRUNE major disk** (~2.4 GB reclaim, low risk):
   - 2 browser code-sign clones (Chrome + Atlas) from `$TMPDIR/X/`
   - `newrelic-infra/` log dir
   - 8 orphan configs from `/opt/homebrew/etc/`
   - 5 Anaconda receipts via `pkgutil --forget`
4. **PRUNE security risk** (decision-then-act):
   - Jupyter LaunchAgent — at minimum `launchctl unload`; ideally remove + uninstall jupyter-core if unused
5. **CONTAIN error-state LaunchAgent**:
   - `brew services stop ollama`; investigate why it's failing; either fix or remove
6. **DEDUPE deliberately** (each requires a user choice):
   - python.org Python 3.13 vs brew's
   - brew zsh vs Apple zsh (login-shell choice)
   - VS Code stable vs Insiders (which is daily driver)
7. **UNIFY governance**:
   - Write `~/Library/LaunchAgents/INVENTORY.md` (vendor agents + brew agents + Jupyter outcome + user-decision history)
   - Amend Rule #9 in chezmoi source with the brew-services exemption (or commit to actually removing them)
   - Document PATH-composition policy
8. **CONTAIN ongoing** (calendar/cron):
   - Quarterly: `find $TMPDIR/X -name '*code_sign_clone' -mtime +7 -exec rm -rf {} +`
   - Quarterly: `brew cleanup --prune=30`
   - Annually: audit `~/Library/LaunchAgents/` against the INVENTORY

### 16.9 What this audit deliberately did NOT touch

- **`/private/var/db/SystemPolicyConfiguration/SystemPolicy.db`** and siblings — SIP-protected, sudo-sqlite3 was blocked by the harness classifier (correctly — these are credential-store reads beyond cataloguing scope).
- **The `disabled.501.plist` enabled/disabled toggles** — only inspected, not modified. The user has explicit choices in there; respect them.
- **`/usr/libexec/apache2`, `/usr/libexec/postfix`** — sealed Apple staging. Can't remove. The user can ignore them — they cost ~330 MB combined and never run.
- **Actual binary uninstalls of stale formulae** — none were uninstalled, only configs in `/opt/homebrew/etc/` recommended for pruning. The user may at some point have reinstalled redis/php/etc. and want the configs kept; this audit conservatively recommends pruning configs only, not deps.
- **CLAUDE.md edits themselves** — recommended but not executed; chezmoi-source mutations require explicit user ship-it per `feedback_unauthorized_commit_chezmoi.md`.

## 17. What requires user direction

- Whether the brew LaunchAgents (atuin, ollama) get an explicit Rule #9 exemption in `~/.claude/CLAUDE.md` source — they're useful, and removing them breaks atuin's shell-history sync and ollama's on-demand model serving.
- Whether the Jupyter LaunchAgent should be (a) removed, (b) hardened, or (c) replaced with an on-demand wrapper. This depends on how the user uses the Claude/Cursor Jupyter MCP integration.
- Vendor LaunchAgents (Google Updater, Microsoft Edge Updater, OpenAI Atlas, Backblaze, iMazing) — keep them? Most are auto-installed and can be ripped out, but doing so breaks the vendor's auto-update model. Per-app decision.
- The `gems/3.4.0/bin` PATH entry — should rev to `4.0.0` (matching brew ruby 4.0.5) but means editing `~/.config/zsh/*` chezmoi-source.
- Ghostty AppTranslocation — move `/Applications/Ghostty.app` properly (drag out of quarantine) so the PATH entry stabilizes.
