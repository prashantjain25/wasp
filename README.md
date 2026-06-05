# wasp - Lightweight LLM CLI for Legacy Systems

**wasp** is a minimal, single-file CLI for running local LLMs on low-resource and legacy hardware. No npm, no node_modules, no heavy frameworks - just Python and a terminal.

```bash
wasp "what is the capital of France?"
>>> tell me more
```

## Philosophy

**Local models first.** wasp is built for models you run yourself. Ollama, LlamaFile, vLLM on your hardware, in your datacenter. No data leaves your network. Cloud providers are an extension path, not the default.

**One file, zero friction.** The entire CLI is a single Python file you can copy to any machine and run. Move it with `scp`, keep it in your dotfiles, run it from a USB stick.

**Designed for legacy systems.** wasp targets Celerons, old Xeons, ARM SBCs, and headless servers where every megabyte counts. It uses threaded I/O, not async frameworks. It polls, not pushes. It works where modern toolchains do not.

**No external runtime dependencies.** Python standard library only. No pip install (except smolagens for agentic mode). No npm, no Docker, no containers.

## Quick Start

```bash
# Clone and run
git clone https://github.com/your-org/wasp ~/wasp
export PATH="$HOME/wasp:$PATH"

# One-shot query
wasp "explain kubernetes in 3 words"

# Interactive REPL
wasp
>>> what is the meaning of life?
>>> /exit

# Pipe mode
cat server.log | wasp "summarize the errors"

# List configured backends
wasp --list
```

## Installation

**Requirements:** Python 3.9+, a local LLM backend (Ollama, LlamaFile, etc.)

```bash
# Copy the single file anywhere
cp wasp ~/wasp/
export PATH="$HOME/wasp:$PATH"

# Or symlink for easy updates
ln -s ~/wasp/wasp ~/.local/bin/wasp
```

### Backend Setup

**Ollama (recommended for legacy hardware):**
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen2.5:1.5b
ollama serve
```

**LlamaFile (no installation, single binary):**
```bash
# Download a llamafile binary and model
curl -sL -o ~/.local/bin/llamafile https://github.com/Mozilla-Ocho/llamafile/releases/download/0.8.13/llamafile-0.8.13
chmod +x ~/.local/bin/llamafile
```

## Configuration

Providers are defined in `~/.llm_config.json`:

```json
{
  "providers": {
    "ollama": {
      "type": "ollama",
      "base_url": "http://localhost:11434",
      "models": [
        { "id": "qwen2.5:1.5b", "name": "Qwen 2.5 1.5B" },
        { "id": "qwen2.5:0.5b", "name": "Qwen 2.5 0.5B" }
      ],
      "options": { "num_ctx": 2048, "temperature": 0.3 },
      "start_cmd": "sudo systemctl start ollama",
      "stop_cmd": "sudo systemctl stop ollama",
      "needs_sudo": true
    },
    "llamafile": {
      "type": "openai",
      "base_url": "http://localhost:8081",
      "models": [
        { "id": "qwen2.5-3b-instruct-q4_k_m", "name": "Qwen 2.5 3B" }
      ],
      "start_cmd": "nohup ~/.local/bin/llamafile --server ... &",
      "stop_cmd": "pkill -f llamafile"
    }
  }
}
```

### Sudo Authentication

Start/stop commands use `sudo` directly when `needs_sudo: true`. The OS sudo cache handles authentication - enter your password once, and sudo reuses it for 5 minutes (configurable via `/etc/sudoers` `timestamp_timeout`).

No credentials are stored by wasp. Sudo authentication is delegated to the OS.

## Commands

### Interactive REPL
| Action | Description |
|--------|-------------|
| `wasp "query"` | One-shot response, then enter REPL |
| `wasp` | Open REPL for multi-turn conversation |
| `type any message` | Send to active model |
| Ctrl+C | Interrupt current response |
| `/exit` or `/quit` | Exit |

### Backend Management
| Command | Description |
|---------|-------------|
| `/start` | Pick backend → pick model. Auto-starts if stopped. |
| `/stop` | Pick backend → confirm stop. All models stop. |
| `/model` | Pick backend → pick model to switch. |

### Agent Mode
| Command | Description |
|---------|-------------|
| `/settings` | Toggle agentic mode ON/OFF, internet ON/OFF |
| `/agent` | Dashboard: status, tool whitelist |

### Web Search
| Command | Description |
|---------|-------------|
| `/search <q>` | Web search via MCP. Results inline. |

### Session
| Command | Description |
|---------|-------------|
| `/new` | Clear conversation context |
| `/help` | Display this guide |

### Command-Line Flags
| Flag | Description |
|------|-------------|
| `--list` | Show configured providers and models |
| `-b <name>` | Select backend on startup |
| `-m <model>` | Override model on startup |

## Architecture

```
User input (>>> prompt)
  │
  ├── /search → cmd_search() → MCP client
  ├── /start /stop /model /settings /agent
  │       → pick() arrow-key menu → ProviderAdapter
  ├── /help /new /exit → REPL handlers
  └── normal message
          ├── Agentic OFF → ProviderAdapter.chat()
          └── Agentic ON  → smolagens.CodeAgent
                              ├── bash()
                              ├── write_file()
                              ├── read_file()
                              ├── edit_file()
                              ├── web_search() (if internet ON)
                              └── web_read()   (if internet ON)
```

### Design Patterns

- **Facade** - `main()` / `LlmCli` wires everything through a single entry point
- **Adapter** - `ProviderAdapter` ABC with `OllamaAdapter` and `OpenAiAdapter`
- **Proxy** - `LoggingProxy` wraps adapters for future cloud auth/rate-limiting
- **Arrow-key menu** - `menu.pick()` for all terminal selections

### File Map

| File | Purpose |
|------|---------|
| `wasp` | Main CLI (~792 lines, single file) |
| `menu.py` | Arrow-key picker (34 lines) |
| `providers_cloud.py` | Extension stub for future cloud LLM adapters |
| `~/.llm_config.json` | Provider configuration |
| `~/.llm_state.json` | Active backend/model persistence |

## Agent Mode

Agentic mode gives the LLM tools to execute code, read/write files, and search the web.

Toggle via `/settings`:
```
  Settings:
  1. Agentic mode: OFF/ON
  2. Internet search: OFF/ON
  3. Return
```

When agentic ON, every chat message is dispatched to `smolagens.CodeAgent` with:
- `bash(command)` - whitelist-checked shell execution
- `write_file(path, content)` - path-restricted file writes
- `read_file(path, start, end)` - file reads
- `edit_file(path, old, new)` - text replacement
- `web_search(query)` - DuckDuckGo (requires Internet ON)
- `web_read(url)` - URL fetch (requires Internet ON)

Works best with **7B+ models**. Smaller models (1.5B–3B) may struggle with the tool-calling protocol.

## Extending for Cloud Providers

The architecture includes extensibility for future cloud LLM providers (OpenAI, Claude, etc.). See `providers_cloud.py` for the pattern:

1. Create a new `ProviderAdapter` subclass with cloud-specific auth
2. Register it in the `ADAPTER_TYPES` dict in `wasp`
3. Add provider config in `~/.llm_config.json`

The `LoggingProxy` provides the extension point for cross-cutting concerns: auth header injection, rate limiting, retry logic.

## Security

- **No credential storage.** Sudo authentication is delegated to the OS sudo cache. wasp never writes passwords to disk.
- **Sudo authentication** is delegated to the OS sudo cache (`timestamp_timeout`).
- **Agent tools are whitelist-restricted.** Only configured commands from `~/.llm_config.json` `agent.bash_whitelist` are allowed.
- **Dangerous patterns blocked.** `rm -rf /`, `dd if=`, and similar are rejected before execution.
- **Path protection.** Agent file tools cannot write to `/etc`, `/sys`, `/proc`, `/bin`, `/sbin`, `/dev`.

## Debugging

All activity is logged to `~/wasp/wasp.log`:
```
[11:49:37.943] START ollama
[11:49:41.642] START ollama OK
[11:51:27.000] CHAT ollama@qwen2.5:1.5b
[11:51:27.723] RESP (42 chars) Hello! How can I help?
```

```bash
tail -50 ~/wasp/wasp.log | grep "DIED\|TIMEOUT\|FAILED"
```

## Performance on Legacy Hardware

Tested on Celeron J4005 (2 cores, no AVX):
- **1.5B models:** ~3 tok/s - usable for chat
- **0.5B models:** ~10 tok/s - fast for simple queries
- **3B+ models:** CPU-bound, recommend GPU or larger host

Tips:
- Use `OLLAMA_FLASH_ATTENTION=1` for faster inference on low RAM
- Set `num_ctx: 2048` to reduce memory pressure
- Consider `OLLAMA_KEEP_ALIVE=5m` to keep models loaded

## License

MIT
