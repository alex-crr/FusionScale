import adsk.core

# Width of the calibration view extents in cm — must match scale_command.py
CALIBRATION_EXTENTS_WIDTH = 15.0


def compute_px_per_cm(
    viewport_width_px: int,
    reference_length_mm: float,
    measured_mm: float,
) -> float:
    """Compute real screen pixels-per-cm from calibration data.

    During calibration the viewport shows CALIBRATION_EXTENTS_WIDTH cm of model space.
    The reference line (reference_length_mm) spans a known number of pixels at that zoom,
    and the user measured it as measured_mm on screen with a ruler.
    """
    ref_line_cm = reference_length_mm / 10.0
    line_pixels = ref_line_cm * (viewport_width_px / CALIBRATION_EXTENTS_WIDTH)
    measured_cm = measured_mm / 10.0
    return line_pixels / measured_cm


def apply_1to1_scale(viewport: adsk.core.Viewport, px_per_cm: float):
    """Set the camera so that geometry appears at 1:1 on the physical screen."""
    visible_width_cm = viewport.width / px_per_cm
    visible_height_cm = viewport.height / px_per_cm

    cam = viewport.camera
    cam.cameraType = adsk.core.CameraTypes.OrthographicCameraType
    cam.isSmoothTransition = False
    cam.setExtents(visible_width_cm, visible_height_cm)
    viewport.camera = cam
    viewport.refresh()
