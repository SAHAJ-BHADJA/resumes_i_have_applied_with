from ingest import BBox, Tracker

from .conftest import make_detection


def test_first_detection_creates_a_track():
    tracker = Tracker()
    tracks = tracker.update([make_detection(box=BBox(0, 0, 100, 100))])
    assert len(tracks) == 1
    assert tracks[0].hit_count == 1


def test_same_object_next_frame_keeps_the_same_track():
    tracker = Tracker(iou_threshold=0.3)
    tracker.update([make_detection(frame_number=0, box=BBox(0, 0, 100, 100))])
    tracks = tracker.update(
        [make_detection(frame_number=1, box=BBox(5, 5, 105, 105))]  # moved slightly
    )
    assert len(tracks) == 1
    assert tracks[0].hit_count == 2


def test_different_label_does_not_match():
    tracker = Tracker(iou_threshold=0.3)
    tracker.update([make_detection(label="forklift", box=BBox(0, 0, 100, 100))])
    tracks = tracker.update(
        [make_detection(label="person", frame_number=1, box=BBox(0, 0, 100, 100))]
    )
    assert len(tracks) == 2   # same location, but different object class


def test_stale_track_is_aged_out():
    tracker = Tracker(iou_threshold=0.3, max_age_frames=5)
    tracker.update([make_detection(frame_number=0, box=BBox(0, 0, 100, 100))])
    # a detection 10 frames later, somewhere else
    tracks = tracker.update(
        [make_detection(frame_number=10, box=BBox(500, 500, 600, 600))]
    )
    assert len(tracks) == 1   # the old one aged out, only the new remains


# ---------------------------------------------------------------- B4 lives here

def test_each_detection_claims_a_distinct_track():
    """Two forklifts in frame N, two forklifts in frame N+1. We must end with
    exactly two tracks — each new detection matched to a DIFFERENT existing
    track.

    The bug: if matching doesn't remove a track once it's claimed, two
    detections in the same frame can both match the same track, and one real
    object silently disappears.
    """
    tracker = Tracker(iou_threshold=0.3)

    # frame 0: two well-separated forklifts
    tracker.update([
        make_detection(label="forklift", frame_number=0, box=BBox(0, 0, 100, 100)),
        make_detection(label="forklift", frame_number=0, box=BBox(400, 400, 500, 500)),
    ])
    assert len(tracker._tracks) == 2

    # frame 1: both moved slightly. Each should re-match its OWN track.
    tracks = tracker.update([
        make_detection(label="forklift", frame_number=1, box=BBox(5, 5, 105, 105)),
        make_detection(label="forklift", frame_number=1, box=BBox(405, 405, 505, 505)),
    ])

    assert len(tracks) == 2, f"expected 2 tracks, got {len(tracks)}"
    assert all(t.hit_count == 2 for t in tracks), [t.hit_count for t in tracks]
