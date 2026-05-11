<div align="center">

# uLauncher OmniPack
### A powerful [Ulauncher](https://ulauncher.io/) extension with multiple utilities to boost your productivity.

<br>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge&logo=appveyor)](https://opensource.org/licenses/MIT)
[![Ulauncher](https://img.shields.io/badge/Ulauncher-5.0+-blue.svg?style=for-the-badge&logo=ulauncher&logoColor=white)](https://ulauncher.io/)
[![Python](https://img.shields.io/badge/Python-3.6+-green.svg?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)

<br>

</div>

---

## ✨ Features

### 🧮 Calculator
Evaluate math expressions safely. Supports basic arithmetic, percentages, and common math functions (`sqrt`, `sin`, `cos`, etc.).

**Keywords:**
- `omni calc <expr>`
- `calc <expr>` (direct)
- `= <expr>` (alias)

**Usage:**
| Command | Description |
|---------|-------------|
| `calc 2+2*5` | Evaluate expression (result: 12) |
| `= 5% of 100` | Calculate percentage (result: 5) |
| `= sqrt(16)` | Math function (result: 4) |
| `omni calc 1/2` | Simple division (result: 0.5) |

---

### 🔍 File Search
Search files recursively using glob/grep patterns.

**Keywords:**
- `omni file <pattern>`
- `f <pattern>` (direct)
- `f /some/path <pattern>` (direct with custom path)

**Usage:**
| Command | Description |
|---------|-------------|
| `f config` | Search files with "config" in name |
| `f *.py` | Search python files (glob) |
| `f ~/Downloads *.zip` | Search zip files in Downloads |
| `omni file test` | Search files with "test" in name |

---

### 📺 YouTube Search
Search for videos on YouTube instantly.

**Keywords:**
- `omni yt <query>`
- `yt <query>` (direct)

**Usage:**
| Command | Description |
|---------|-------------|
| `yt lofi hip hop` | Search for music videos |
| `omni yt coding tutorial` | Search for educational content |

---

### 🔑 UUID Generator
Generate UUIDs of different versions instantly.

**Keywords:**
- `omni uuid`
- `uuid` (direct)

**Usage:**
| Command | Description |
|---------|-------------|
| `omni uuid` | List all UUID options |
| `uuid` | Generate UUID v4 (quick) |
| `uuid v1` | Generate UUID v1 |
| `uuid v5 <domain>` | Generate UUID v5 (default: example.com) |

**Example Output:** `550e8400-e29b-41d4-a716-446655440000`

---

**Keywords:**
- `omni pass`
- `pass` (direct)

**Usage:**
| Command | Description |
|---------|-------------|
| `omni pass` | Generate 5 random passwords (16 chars) |
| `pass 32` | Generate passwords with 32 chars |

**Options:**
- Minimum length: 8 characters
- Maximum length: 64 characters
- Includes: uppercase, lowercase, numbers, special characters

---

**Keywords:**
- `omni kill`
- `kill` (direct)

**Usage:**
| Command | Description |
|---------|-------------|
| `omni kill` | List all running processes |
| `kill firefox` | Search processes matching "firefox" |

**How to use:** Select a process and press `Enter` to kill it.

---

**Keywords:**
- `omni port`
- `killport` (direct)

**Usage:**
| Command | Description |
|---------|-------------|
| `omni port` | List all open/listening ports |
| `killport 8080` | Filter ports matching "8080" |

**How to use:** If no ports match the search, all ports are displayed. Select a port and press `Enter` to kill the process.
**Behavior:** 
* `killport`: Lists all active listening ports.
* `killport [port]`: Displays specific matching port info.
* Missing Port: Shows all active ports if the target is inactive.
* Empty State: Displays an error if no ports are open.
---

**Keywords:**
- `omni trash`
- `emptytrash` (direct)

**Usage:**
| Command | Description |
|---------|-------------|
| `omni trash` | Empty trash with confirmation |
| `emptytrash` | Instant access to trash cleanup |

⚠️ **Warning:** This action cannot be undone!

---

**Keywords:**
- `omni g`
- `g` (direct)

**Usage:**
| Command | Description |
|---------|-------------|
| `omni g query` | Search Google for "query" |

---

**Keywords:**
- `omni ai`
- `gai` (direct)

**Usage:**
| Command | Description |
|---------|-------------|
| `omni ai query` | Search with Google AI Mode |

---

## 📥 Installation

1. Open **Ulauncher** settings
2. Go to **EXTENSIONS** tab
3. Click **+ Add extension**
4. Paste the following URL:
   ```
   https://github.com/forhadkhan/ulauncher-omnipack
   ```
5. Click **Add**

### Alternative: Manual Installation

```bash
cd ~/.config/ulauncher/extensions/
git clone https://github.com/forhadkhan/ulauncher-omnipack.git
```

---

### 🚀 Quick Start

OmniPack gives you two ways to interact with your tools:

#### 1. The Unified Command (`omni`)
Type `omni` followed by a space to see a list of all available modules. You can then type the module name and your query.
```
omni uuid          → Generate a UUID
omni pass 20       → Generate a 20-character password
omni kill chrome   → Find and kill Chrome processes
omni port 3000     → Kill process on port 3000
omni g your query  → Search Google
```

#### 2. Direct Keywords
If you prefer speed, you can use the module's keyword directly without the `omni` prefix.
```
uuid          → Quick UUID
pass 16       → Quick password
kill firefox  → Search and kill
g search term → Search Google
```

> 💡 **Tip:** All keywords (including `omni`) are customizable in the extension settings.

---

## ⚙️ Customization

All keywords can be customized in OmniPack configuration. 

**Path:** Ulauncher Settings → EXTENSIONS → OmniPack

| Feature | Default Keyword | Customizable |
|---------|----------------|--------------|
| UUID Generator | `uuid` | 🗹 |
| Password Generator | `pass` | 🗹 |
| Kill Process | `kill` | 🗹 |
| Kill Port | `killport` | 🗹 |
| Empty Trash | `emptytrash` | 🗹 |
| Google Search | `g` | 🗹 |
| Google AI Search | `gai` | 🗹 |

---

## 📋 Requirements

- **Ulauncher:** 5.0 or higher
- **Python:** 3.12 or higher (recommended)
- **System Commands:**
  - `lsof` command (for kill port feature)
  - `ps` command (for kill process feature)
- **Operating System:** Linux (tested on Ubuntu, Fedora, Arch)

---

## 🔧 Troubleshooting

### Kill/Killport not working

**Problem:** Commands don't return results or fail to kill processes.

**Solutions:**
- 🗹 Ensure `ss` and `ps` commands are available on your system
- 🗹 Some processes may require elevated permissions to kill
- 🗹 Try running: `which ss` and `which ps` to verify installation

### Empty Trash not working

**Problem:** Trash doesn't empty or throws an error.

**Solutions:**
- 🗹 Ensure `~/.local/share/Trash` directory exists
- 🗹 Check permissions: `ls -la ~/.local/share/Trash`

### General Issues

- **Extension not appearing:** Restart Ulauncher (`Alt+F2` → type `ulauncher` → Enter)
- **Keywords not working:** Check for keyword conflicts in Ulauncher settings
- **Need help?** [Open an issue](https://github.com/forhadkhan/ulauncher-omnipack/issues)

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

### Ways to Contribute:
- 🐛 Report bugs
- 💡 Suggest new features
- 📝 Improve documentation
- 🔧 Submit pull requests

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 👨‍ Author

**Forhad Khan**  
🌐 Website: [forhadkhan.com](https://forhadkhan.com)  
💻 GitHub: [@forhadkhan](https://github.com/forhadkhan)

---

<div align="center">

**If you find this extension helpful, please ⭐ star the repository!**

[Report Bug](https://github.com/forhadkhan/ulauncher-omnipack/issues) · [Request Feature](https://github.com/forhadkhan/ulauncher-omnipack/issues) · [View Repository](https://github.com/forhadkhan/ulauncher-omnipack)

</div>