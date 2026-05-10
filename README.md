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

### 🔑 UUID Generator
Generate UUIDs of different versions instantly.

**Keyword:**
```
uuid
```

**Usage:**
| Command | Description |
|---------|-------------|
| `uuid` | Generate UUID v4 |
| `uuid v1` | Generate UUID v1 |
| `uuid v4` | Generate UUID v4 |
| `uuid v5 <domain>` | Generate UUID v5 (default: example.com) |

**Example Output:** `550e8400-e29b-41d4-a716-446655440000`

---

### 🔐 Password Generator
Generate secure random passwords with customizable length.

**Keyword:**
```
pass
```

**Usage:**
| Command | Description |
|---------|-------------|
| `pass` | Generate 3 random passwords (16 characters) |
| `pass 32` | Generate 3 passwords with 32 characters |

**Options:**
- Minimum length: 8 characters
- Maximum length: 64 characters
- Includes: uppercase, lowercase, numbers, special characters

---

### ⚡ Kill Process
Search and kill running processes by name.

**Keyword:**
```
kill
```

**Usage:**
| Command | Description |
|---------|-------------|
| `kill` | List all running processes |
| `kill firefox` | Search and list processes matching "firefox" |

**How to use:** Select a process and press `Enter` to kill it.

---

### 🚪 Kill Port
Kill processes listening on specific ports.

**Keyword:**
```
killport
```

**Usage:**
| Command | Description |
|---------|-------------|
| `killport` | List all open/listening ports |
| `killport 8080` | Filter and show ports matching "8080" |

**How to use:** If no ports match the search, all ports are displayed. Select a port and press `Enter` to kill the process.

---

### 🗑️ Empty Trash
Instantly empty your trash/recycle bin.

**Keyword:**
```
emptytrash
```

**Usage:**
| Command | Description |
|---------|-------------|
| `emptytrash` | Empty the trash immediately |

⚠️ **Warning:** This action cannot be undone!

---

### 🔍 Google Search
Search directly on Google.

**Keyword:**
```
g
```

**Usage:**
| Command | Description |
|---------|-------------|
| `g python tutorial` | Search for "python tutorial" on Google |

---

### 🤖 Google AI Search
Search on Google with AI Mode enabled.

**Keyword:**
```
gai
```

**Usage:**
| Command | Description |
|---------|-------------|
| `gai what is machine learning` | Search with Google AI Mode |

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

## 🚀 Quick Start

After installation, simply type one of the keywords in Ulauncher:

```
uuid          → Generate a UUID
pass 20       → Generate a 20-character password
kill chrome   → Find and kill Chrome processes
killport 3000 → Kill process on port 3000
g your query  → Search Google
```

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
- **Python:** 3.6 or higher
- **System Commands:**
  - `ss` command (for killport feature)
  - `ps` command (for kill feature)
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