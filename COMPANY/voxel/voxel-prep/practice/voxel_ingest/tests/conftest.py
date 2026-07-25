import pytest

from ingest import BBox, Detection, Frame


def make_frame(camera_id="cam-1", frame_number=0, timestamp=0.0, width=1920, height=1080):
    return Frame(
        camera_id=camera_id,
        frame_number=frame_number,
        timestamp=timestamp,
        width=width,
        height=height,
    )


def make_detection(
    label="forklift",
    confidence=0.9,
    box=None,
    camera_id="cam-1",
    frame_number=0,
    timestamp=0.0,
):
    if box is None:
        box = BBox(0, 0, 100, 100)
    return Detection(
        frame=make_frame(camera_id, frame_number, timestamp),
        label=label,
        confidence=confidence,
        box=box,
    )


@pytest.fixture
def frame_factory():
    return make_frame


@pytest.fixture
def detection_factory():
    return make_detection
