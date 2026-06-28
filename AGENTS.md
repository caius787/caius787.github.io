# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Project Overview

This is a static personal website portfolio hosted on GitHub Pages (caius787.github.io). It contains HTML/CSS/JavaScript pages with interactive games, utilities, and various web applications.

## Local Development

```bash
# Start a local development server
python3 -m http.server 8000
# Then visit http://localhost:8000
```

No build step or package manager is required - this is a purely static site.

## Architecture

- **Static HTML pages**: Each feature/app is a standalone HTML file with inline CSS and JavaScript
- **No shared framework**: Pages are independent and self-contained
- **Command bar navigation**: The main `index.html` has a command bar (/) that routes to hidden pages using a JavaScript command mapping
- **Media assets**: MP3 audio files and PNG images are stored alongside their related HTML files

## Key Patterns

- Most pages use inline `<style>` and `<script>` tags rather than external files
- The `dad/` section uses Bootstrap (via node_modules/bootswatch)
- Pages follow a purple (#9370DB) color scheme with Poppins font
- Interactive elements typically use vanilla JavaScript event listeners

## Hidden Pages (accessed via command bar)

The command bar on the main page supports commands like: `glorious`, `taco`, `workout`, `vr`, `prime`, `rsvp`, `instruments`, `trampoline`, `poweroutage`, `money`. Type `help` or `list` in the command bar to see available commands.
