# FusionScale

A Fusion 360 add-in that scales the viewport to **real-life 1:1 dimensions** using screen calibration.

Place a ruler against your screen and verify that your design matches its physical size — no printing or exporting required.

## Features

- **One-click 1:1 scale** — instantly zooms the viewport so objects appear at their true physical size on screen
- **Screen calibration** — a guided first-run calibration measures your screen's actual pixel density using a physical ruler
- **Persistent calibration** — calibrate once, the correction factor is saved between sessions
- **Non-destructive** — uses temporary overlay graphics during calibration, never modifies your design

## Installation

### Manual (GitHub)

1. Download or clone this repository
2. Copy the `FusionScale` folder to your Fusion 360 add-ins directory:
   - **Windows:** `%appdata%\Autodesk\Autodesk Fusion 360\API\AddIns\`
   - **macOS:** `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/`
3. In Fusion 360, open **UTILITIES > Add-Ins** (or press `Shift+S`)
4. Find **FusionScale** in the Add-Ins tab and click **Run**
5. Optionally check **Run on Startup** to load it automatically

## Usage

### First run (calibration)

1. Open any design in Fusion 360
2. Click the **1:1 Scale** button in the UTILITIES toolbar (Add-Ins panel)
3. A red **50 mm reference line** appears on screen with a calibration dialog
4. Measure the reference line on your screen with a **physical ruler**
5. Enter the measured length in millimeters and click **OK**
6. Your design reappears at true 1:1 scale

### Subsequent use

Click the **1:1 Scale** button — the viewport instantly scales to 1:1 using your saved calibration.

### Recalibrate

Delete the `config.json` file in the add-in folder and click the button again to redo calibration. Recalibration is needed if you change monitors or screen resolution.

## System requirements

- Autodesk Fusion 360 (latest version recommended)
- Windows or macOS

## How it works

The add-in uses orthographic projection and the `Camera.setExtents()` API to set the viewport's visible area to match the physical screen dimensions. Since operating systems often report inaccurate DPI values, a one-time calibration step measures the true pixel density of your screen by having you compare a known model-space length against a physical ruler.

## Known limitations

- Calibration is stored as a single global value (not per-monitor)
- After applying 1:1 scale, zooming or panning will break the scale — click the button again to restore it
- The reference line is placed at the model origin; designs not centered at the origin will appear off-center at 1:1

## Project structure

```
FusionScale/
  FusionScale.py          # Entry point — registers toolbar button
  FusionScale.manifest    # Add-in manifest
  commands/
    scale_command.py       # Calibration + scale command logic
  lib/
    config.py              # Persistent calibration storage
    camera.py              # Viewport math (pixel density, setExtents)
  resources/               # Toolbar icons (16x16, 32x32)
```

## License

MIT License — see [LICENSE](LICENSE).
