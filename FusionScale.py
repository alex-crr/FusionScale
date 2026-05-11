import adsk.core
import adsk.fusion
import traceback
import os

from commands.scale_command import (
    COMMAND_ID,
    COMMAND_NAME,
    COMMAND_TOOLTIP,
    CommandCreatedHandler,
    RECALIBRATE_ID,
    RECALIBRATE_NAME,
    RECALIBRATE_TOOLTIP,
    RecalibrateCreatedHandler,
)

_app = None
_ui = None
_handlers = []

PANEL_ID = "InspectPanel"

_COMMANDS = [
    (COMMAND_ID, COMMAND_NAME, COMMAND_TOOLTIP, CommandCreatedHandler),
    (RECALIBRATE_ID, RECALIBRATE_NAME, RECALIBRATE_TOOLTIP, RecalibrateCreatedHandler),
]


def run(context):
    global _app, _ui
    try:
        _app = adsk.core.Application.get()
        _ui = _app.userInterface

        resource_dir = os.path.join(os.path.dirname(__file__), "resources")

        panel = _ui.allToolbarPanels.itemById(PANEL_ID)

        for cmd_id, cmd_name, cmd_tooltip, handler_class in _COMMANDS:
            cmd_def = _ui.commandDefinitions.itemById(cmd_id)
            if cmd_def:
                cmd_def.deleteMe()

            cmd_def = _ui.commandDefinitions.addButtonDefinition(
                cmd_id, cmd_name, cmd_tooltip, resource_dir
            )

            handler = handler_class()
            cmd_def.commandCreated.add(handler)
            _handlers.append(handler)

            if panel:
                existing = panel.controls.itemById(cmd_id)
                if not existing:
                    panel.controls.addCommand(cmd_def)

    except:
        if _ui:
            _ui.messageBox(traceback.format_exc())


def stop(context):
    global _ui
    try:
        if _ui:
            panel = _ui.allToolbarPanels.itemById(PANEL_ID)
            for cmd_id, _, _, _ in _COMMANDS:
                cmd_def = _ui.commandDefinitions.itemById(cmd_id)
                if cmd_def:
                    cmd_def.deleteMe()
                if panel:
                    ctrl = panel.controls.itemById(cmd_id)
                    if ctrl:
                        ctrl.deleteMe()
    except:
        if _ui:
            _ui.messageBox(traceback.format_exc())
