# CaretPositionNavigation
Navigate prev-next over cursor position history in Sublime Text!

## Installation

### Git

#### Linux
```bash
cd ~/.config/sublime-text-3/Packages/
git clone https://github.com/rohanrhu/CaretPositionNavigation.git CaretPositionNavigation
```

### Windows

```bash
cd "%HOMEPATH%\AppData\Roaming\Sublime Text 3\Packages"
git clone https://github.com/rohanrhu/CaretPositionNavigation.git CaretPositionNavigation
```

## Usage

### Shortcuts
There're two default shortcuts, you can set under `Prefences > Package Settings > CaretPositionNavigation > Keybindings (User)`

- Go Prev: `ctrl+alt+left`
- Go Next: `ctrl+alt+right`

### Menu Commands
There're one menu (ctrl+shift+p) command

- Clear History: `CaretPositionNavigation: Clear History` *(Clear history for current tab)*

### Main Menu Entries
There're two menu entries for navigating prev-next under

- Go Prev: `Goto > Caret Goto Prev`
- Go Next: `Goto > Caret Goto Next`

## Configuration
There're two settings, you can set under `Prefences > Package Settings > CaretPositionNavigation > Settings (User)`

- History Length: `history_length: Integer` *(Default: 50)*
- Threshold: `threshold: Integer` *(Default: 20)*

## License
MIT
