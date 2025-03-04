# Personal Website Portfolio

A dynamic personal website hosted on GitHub Pages featuring various interactive web applications, games, and utilities.

## Project Structure

### Main Applications
- **Minigames**: Collection of browser-based games
  - Rock Paper Scissors (rps.html)
  - Tic Tac Toe (tic.html)

- **Countdown Timers**: Multiple countdown applications
  - 6 different countdown implementations

- **Tesla Quiz**: Interactive quiz about Tesla vehicles
  - Features multiple Tesla models and images
  - Includes Cybertruck, Model 3, Model X, and Roadster content

- **Minecraft Tools**
  - All Blocks in MC viewer
  - MC Passenger system

- **Instruments Section**
  - Instrument inventory tracker
  - Wishlist management

### Interactive Features
- Sound integration (ding.mp3, dirtman.mp3)
- RSVP system
- Typing game
- Random number generator
- Workout tracker
- Thai to USA converter

### Additional Content
- Prime section with multiple pages
- Dad's section with custom styling (Bootstrap integration)
- Various interactive buttons and features

## Technologies
- HTML/CSS
- JavaScript
- Bootstrap (in dad/ section)
- Custom media assets (images, sounds)

## Setup
This is a static website that can be served directly from GitHub Pages. No additional setup required.

### Local Development
To run the website locally:
1. Navigate to the project directory
2. Start a local server:
   ```bash
   python3 -m http.server 8000
   ```
3. Open http://localhost:8000 in your browser

## Usage
- Live site: Visit caius787.github.io
- Local development: http://localhost:8000

## File Structure
```
.
├── index.html                 # Main entry point
├── minigames/                 # Games section
│   ├── rps.html              # Rock Paper Scissors
│   └── tic.html              # Tic Tac Toe
├── countdowns/               # Countdown applications
│   ├── countdown1.html
│   ├── countdown2.html
│   ├── countdown3.html
│   ├── countdown4.html
│   ├── countdown5.html
│   └── countdown6.html
├── teslaquiz/               # Tesla quiz with images
├── instruments/             # Instrument tracking
│   ├── instruhave.html
│   └── instruwant.html
├── mcpassenger/            # Minecraft-related tools
├── prime/                  # Prime section
├── rsvp/                   # RSVP system
└── dad/                    # Dad's section with Bootstrap
