# AJAZZ AK820 Pro Web Configurator

Local/browser-based configurator for the AJAZZ AK820 Pro keyboard.

Live page:

https://caius787.github.io/ajazz-ak820-config/

## Features

- Connect to the keyboard with WebHID in Chrome or another Chromium browser.
- Upload animated GIFs to the 128 x 128 TFT screen.
- Upload still PNG, JPEG, or WebP images using the same framed upload path as GIFs.
- Sync the keyboard screen clock to the computer's current time.
- Change key RGB lighting mode, color, rainbow mode, brightness, speed, and direction.
- Set the keyboard/display sleep timer.

## Requirements

- AJAZZ AK820 Pro connected by USB-C.
- Keyboard mode switch set to wired USB.
- Chrome, Edge, Brave, Opera, or another Chromium browser with WebHID support.
- HTTPS or localhost. GitHub Pages works because it is served over HTTPS.

Safari and Firefox do not support WebHID. Bluetooth and 2.4 GHz dongle mode do not expose the needed vendor HID interfaces.

## Notes

This is unofficial and not affiliated with AJAZZ or Epomaker. Use at your own risk.

The TFT/GIF upload path is based on Beattrey's AK820 Pro Web Configurator, with the still-image upload changed to use the framed GIF-style path that worked on tested hardware. The lighting and sleep controls are based on MemerGamer's AK820 Pro unofficial WebHID driver.

## Credits

- https://github.com/Beattrey/ajazz-ak820-config
- https://github.com/MemerGamer/AjazzAk820ProUnofficialWebdriver
- https://github.com/gohv/EPOMAKER-Ajazz-AK820-Pro
- https://github.com/TaxMachine/ajazz-keyboard-software-linux
- https://github.com/fpb/ajazz-ak820-pro
