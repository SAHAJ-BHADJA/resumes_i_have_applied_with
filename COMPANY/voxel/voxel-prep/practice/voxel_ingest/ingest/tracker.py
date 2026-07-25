"""Track objects across frames by matching new detections to existing tracks.

The idea: when a new frame's detections come in, match each one to the most
plausible existing track (same label, boxes overlap enough). Unmatched
detections become new tracks. Tracks that go unseen for too long are dropped.
"""

from typing import Dict, List

from .geometry import iou
from .models import Detection, Track


class Tracker:
    def __init__(self, iou_threshold: float = 0.3, max_age_frames: int = 30):
        self.iou_threshold = iou_threshold
        self.max_age_frames = max_age_frames
        self._tracks: Dict[int, Track] = {}
        self._next_id = 1

    def _new_track(self, detection: Detection) -> Track:
        track = Track(
            track_id=self._next_id,
            label=detection.label,
            last_box=detection.box,
            last_seen_frame=detection.frame.frame_number,
            history=[detection.box],
        )
        detection.track_id = self._next_id
        self._tracks[self._next_id] = track
        self._next_id += 1
        return track

    def update(self, detections: List[Detection]) -> List[Track]:
        """Match detections to tracks, create/age tracks, return active ones."""
        if not detections:
            return list(self._tracks.values())

        current_frame = detections[0].frame.frame_number
        matched_track_ids = set()

        for detection in detections:
            best_track = None
            best_iou = self.iou_threshold

            for track in self._tracks.values():
                if track.label != detection.label:
                    continue
                score = iou(track.last_box, detection.box)
                if score >= best_iou:
                    best_iou = score
                    best_track = track

            if best_track is not None:
                best_track.last_box = detection.box
                best_track.last_seen_frame = current_frame
                best_track.hit_count += 1
                best_track.history.append(detection.box)
                detection.track_id = best_track.track_id
                matched_track_ids.add(best_track.track_id)
            else:
                new = self._new_track(detection)
                matched_track_ids.add(new.track_id)

        # age out stale tracks
        stale = [
            tid
            for tid, track in self._tracks.items()
            if current_frame - track.last_seen_frame > self.max_age_frames
        ]
        for tid in stale:
            del self._tracks[tid]

        return list(self._tracks.values())
