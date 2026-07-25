from ingest import FrameBatcher

from .conftest import make_frame


def test_flushes_when_full():
    batches = []
    b = FrameBatcher(sink=batches.append, max_batch_size=3, buffer=[])
    # add more than enough to force at least one flush
    for i in range(6):
        b.add(make_frame(frame_number=i, timestamp=float(i) * 0.01))
    assert len(batches) >= 1
    assert all(len(batch) <= 3 for batch in batches), [len(x) for x in batches]


def test_flush_empties_the_buffer():
    batches = []
    b = FrameBatcher(sink=batches.append, max_batch_size=2, buffer=[])
    b.add(make_frame(frame_number=0, timestamp=0.0))
    b.add(make_frame(frame_number=1, timestamp=0.01))
    b.flush()
    b.add(make_frame(frame_number=2, timestamp=0.02))
    # after the auto-flush at size 2, then manual flush, buffer should hold 1
    assert len(b.buffer) == 1


def test_flushes_on_age():
    batches = []
    b = FrameBatcher(sink=batches.append, max_batch_size=100, max_wait_seconds=0.5, buffer=[])
    b.add(make_frame(frame_number=0, timestamp=0.0))
    b.add(make_frame(frame_number=1, timestamp=0.6))   # 0.6s > 0.5s wait
    assert len(batches) == 1


# ---------------------------------------------------------------- B2 lives here

def test_two_batchers_do_not_share_a_buffer():
    """Each FrameBatcher must have its own buffer.

    Construct two batchers WITHOUT passing buffer= explicitly. Add a frame to
    the first. The second must still be empty. If they share, one camera's
    frames leak into another camera's batch.
    """
    first = FrameBatcher(sink=lambda batch: None, max_batch_size=10)
    second = FrameBatcher(sink=lambda batch: None, max_batch_size=10)

    first.add(make_frame(frame_number=0, timestamp=0.0))

    assert len(first.buffer) == 1
    assert len(second.buffer) == 0


# ---------------------------------------------------------------- B3 lives here

def test_batch_size_is_exactly_max_not_one_over():
    """max_batch_size=4 should flush AT 4 frames, producing batches of 4 — not
    batches of 5."""
    batches = []
    b = FrameBatcher(sink=batches.append, max_batch_size=4, buffer=[])
    for i in range(8):
        b.add(make_frame(frame_number=i, timestamp=float(i) * 0.001))
    assert all(len(batch) == 4 for batch in batches), [len(x) for x in batches]
    assert len(batches) == 2
