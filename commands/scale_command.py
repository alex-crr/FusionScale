import adsk.core
import adsk.fusion
import traceback
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from lib import config, camera

_handlers = []
_cg_group = None
_hidden_occurrences = []
_hidden_bodies = []
_saved_camera = None

COMMAND_ID = "FusionScale_ScaleView"
COMMAND_NAME = "1:1 Scale"
COMMAND_TOOLTIP = "Scale viewport to real-life 1:1 dimensions.\nFirst use requires calibration."


class CommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def notify(self, args: adsk.core.CommandCreatedEventArgs):
        try:
            app = adsk.core.Application.get()
            cmd = args.command
            cfg = config.load()

            if config.is_calibrated():
                viewport = app.activeViewport
                camera.apply_1to1_scale(viewport, cfg["px_per_cm"])
                cmd.isAutoExecute = True
                return

            design = adsk.fusion.Design.cast(app.activeProduct)
            if not design:
                app.userInterface.messageBox("Please open or create a design first.")
                return

            _show_calibration_view(app, design, cfg)
            self._setup_calibration_inputs(cmd, cfg)

        except:
            app = adsk.core.Application.get()
            app.userInterface.messageBox(traceback.format_exc())

    def _setup_calibration_inputs(self, cmd, cfg):
        inputs = cmd.commandInputs
        ref_len_mm = cfg["reference_length_mm"]
        ref_len_cm = ref_len_mm / 10.0

        inputs.addTextBoxCommandInput(
            "instructions",
            "",
            f"A {ref_len_mm:.0f} mm reference line is displayed.\n"
            "Measure it on your screen with a physical ruler,\n"
            "then enter the measured length below.",
            4,
            True,
        )
        inputs.addStringValueInput(
            "measured_length",
            "Measured length (mm)",
            str(ref_len_mm),
        )

        on_execute = CalibrateExecuteHandler()
        cmd.execute.add(on_execute)
        _handlers.append(on_execute)

        on_destroy = CommandDestroyHandler()
        cmd.destroy.add(on_destroy)
        _handlers.append(on_destroy)


class CalibrateExecuteHandler(adsk.core.CommandEventHandler):
    def notify(self, args: adsk.core.CommandEventArgs):
        try:
            app = adsk.core.Application.get()
            inputs = args.command.commandInputs

            measured_input = adsk.core.StringValueCommandInput.cast(
                inputs.itemById("measured_length")
            )
            measured_mm = float(measured_input.value)

            cfg = config.load()
            viewport = app.activeViewport
            cfg["px_per_cm"] = camera.compute_px_per_cm(
                viewport.width, cfg["reference_length_mm"], measured_mm
            )
            config.save(cfg)

            _restore_view(app)

            camera.apply_1to1_scale(viewport, cfg["px_per_cm"])

        except:
            app = adsk.core.Application.get()
            app.userInterface.messageBox(traceback.format_exc())


class CommandDestroyHandler(adsk.core.CommandEventHandler):
    def notify(self, args: adsk.core.CommandEventArgs):
        try:
            app = adsk.core.Application.get()
            _restore_view(app)
        except:
            pass


def _show_calibration_view(app, design, cfg):
    global _cg_group, _hidden_occurrences, _hidden_bodies, _saved_camera

    root = design.rootComponent
    viewport = app.activeViewport

    _saved_camera = viewport.camera

    _hidden_occurrences = []
    for i in range(root.allOccurrences.count):
        occ = root.allOccurrences.item(i)
        if occ.isLightBulbOn:
            occ.isLightBulbOn = False
            _hidden_occurrences.append(occ)

    _hidden_bodies = []
    for i in range(root.bRepBodies.count):
        body = root.bRepBodies.item(i)
        if body.isLightBulbOn:
            body.isLightBulbOn = False
            _hidden_bodies.append(body)

    ref_len_cm = cfg["reference_length_mm"] / 10.0
    half = ref_len_cm / 2.0

    _cg_group = root.customGraphicsGroups.add()

    coords = adsk.fusion.CustomGraphicsCoordinates.create(
        [-half, 0, 0, half, 0, 0]
    )
    line = _cg_group.addLines(coords, [], False, [])
    red = adsk.fusion.CustomGraphicsSolidColorEffect.create(
        adsk.core.Color.create(220, 40, 40, 255)
    )
    line.color = red
    line.weight = 5.0

    tick = 0.4
    tick_coords = adsk.fusion.CustomGraphicsCoordinates.create(
        [-half, -tick, 0, -half, tick, 0, half, -tick, 0, half, tick, 0]
    )
    ticks = _cg_group.addLines(tick_coords, [], False, [])
    ticks.color = red
    ticks.weight = 4.0

    transform = adsk.core.Matrix3D.create()
    transform.translation = adsk.core.Vector3D.create(-1.2, -1.2, 0)
    text = _cg_group.addText(
        f"{cfg['reference_length_mm']:.0f} mm", "Arial", 0.5, transform
    )
    text.color = red

    cam = viewport.camera
    cam.cameraType = adsk.core.CameraTypes.OrthographicCameraType
    cam.isSmoothTransition = False
    cam.eye = adsk.core.Point3D.create(0, 0, 100)
    cam.target = adsk.core.Point3D.create(0, 0, 0)
    cam.upVector = adsk.core.Vector3D.create(0, 1, 0)
    cam.setExtents(15.0, 10.0)
    viewport.camera = cam
    viewport.refresh()


def _restore_view(app):
    global _cg_group, _hidden_occurrences, _hidden_bodies, _saved_camera

    design = adsk.fusion.Design.cast(app.activeProduct)
    if not design:
        return
    root = design.rootComponent

    if _cg_group:
        try:
            _cg_group.deleteMe()
        except:
            pass
        _cg_group = None

    for occ in _hidden_occurrences:
        try:
            occ.isLightBulbOn = True
        except:
            pass
    _hidden_occurrences = []

    for body in _hidden_bodies:
        try:
            body.isLightBulbOn = True
        except:
            pass
    _hidden_bodies = []

    if _saved_camera:
        try:
            viewport = app.activeViewport
            _saved_camera.isSmoothTransition = False
            viewport.camera = _saved_camera
        except:
            pass
        _saved_camera = None

    app.activeViewport.refresh()
