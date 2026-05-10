# uLauncher OmniPack

A powerful Ulauncher extension with multiple utilities to boost your productivity.

## Features

### UUID Generator
Generate UUIDs of different versions instantly.

**Keyword:** `uuid`

**Usage:**
- `uuid` - Generate UUID v4
- `uuid v1` - Generate UUID v1
- `uuid v4` - Generate UUID v4
- `uuid v5 <domain>` - Generate UUID v5 (default: example.com)

### Password Generator
Generate secure random passwords with customizable length.

**Keyword:** `pass`

**Usage:**
- `pass` - Generate 3 random passwords (16 characters)
- `pass 32` - Generate 3 passwords with 32 characters (min: 8, max: 64)

### Kill Process
Search and kill running processes by name.

**Keyword:** `kill`

**Usage:**
- `kill` - List all running processes
- `kill firefox` - Search and list processes matching "firefox"

Select a process and press Enter to kill it.

### Kill Port
Kill processes listening on specific ports.

**Keyword:** `killport`

**Usage:**
- `killport` - List all open/listening ports
- `killport 8080` - Filter and show ports matching "8080"

If no ports match the search, all ports are displayed. Select a port and press Enter to kill the process.

### Empty Trash
Instantly empty your trash/recycle bin.

**Keyword:** `emptytrash`

**Usage:**
- `emptytrash` - Empty the trash immediately

### Google Search
Search directly on Google.

**Keyword:** `g`

**Usage:**
- `g python tutorial` - Search for "python tutorial" on Google

### Google AI Search
Search on Google with AI Mode enabled.

**Keyword:** `gai`

**Usage:**
- `gai what is machine learning` - Search with Google AI Mode

## Installation

1. Open Ulauncher preferences
2. Go to Extensions tab
3. Click "Add extension"
4. Paste: `https://github.com/forhadkhan/ulauncher-omnipack`
5. Click Add

## Customization

All keywords can be customized in Ulauncher preferences:
- UUID Generator keyword (default: `uuid`)
- Password Generator keyword (default: `pass`)
- Kill Process keyword (default: `kill`)
- Kill Port keyword (default: `killport`)
- Empty Trash keyword (default: `emptytrash`)
- Google Search keyword (default: `g`)
- Google AI Search keyword (default: `gai`)

## Requirements

- Ulauncher 5.0+
- Python 3.6+
- `ss` command (for killport feature)
- `ps` command (for kill feature)

## Troubleshooting

**Kill/Killport not working:**
- Ensure `ss` and `ps` commands are available on your system
- Some processes may require elevated permissions to kill

**Empty Trash not working:**
- Ensure `~/.local/share/Trash` directory exists

## License

MIT License

## Author

Forhad Khan
