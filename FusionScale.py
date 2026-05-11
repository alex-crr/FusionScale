import adsk.core
import adsk.fusion
import traceback
import os

from commands.scale_command import (
    COMMAND_ID,
    COMMAND_NAME,
    COMMAND_TOOLTIP,
    CommandCreatedHandler,
)

_app = None
_ui = None
_handlers = []

PANEL_ID = "SolidScriptsAddinsPanel"


def run(context):
    global _app, _ui
    try:
        _app = adsk.core.Application.get()
        _ui = _app.userInterface

        cmd_def = _ui.commandDefinitions.itemById(COMMAND_ID)
        if cmd_def:
            cmd_def.deleteMe()

        resource_dir = os.path.join(os.path.dirname(__file__), "resources")
        cmd_def = _ui.commandDefinitions.addButtonDefinition(
            COMMAND_ID, COMMAND_NAME, COMMAND_TOOLTIP, resource_dir
        )

        on_created = CommandCreatedHandler()
        cmd_def.commandCreated.add(on_created)
        _handlers.append(on_created)

        panel = _ui.allToolbarPanels.itemById(PANEL_ID)
        if panel:
            existing = panel.controls.itemById(COMMAND_ID)
            if not existing:
                panel.controls.addCommand(cmd_def)

    except:
        if _ui:
            _ui.messageBox(traceback.format_exc())


def stop(context):
    global _ui
    try:
        if _ui:
            cmd_def = _ui.commandDefinitions.itemById(COMMAND_ID)
            if cmd_def:
                cmd_def.deleteMe()

            panel = _ui.allToolbarPanels.itemById(PANEL_ID)
            if panel:
                ctrl = panel.controls.itemById(COMMAND_ID)
                if ctrl:
                    ctrl.deleteMe()
    except:
        if _ui:
            _ui.messageBox(traceback.format_exc())
