from ingest import CameraState, HealthMonitor


def test_unknown_camera_is_offline():
    monitor = HealthMonitor()
    assert monitor.state_of("cam-x", now=100.0) == CameraState.OFFLINE


def test_recent_frame_means_online():
    monitor = HealthMonitor(offline_after_seconds=10.0)
    monitor.record_frame("cam-1", timestamp=100.0)
    assert monitor.state_of("cam-1", now=105.0) == CameraState.ONLINE


def test_gap_means_offline():
    monitor = HealthMonitor(offline_after_seconds=10.0)
    monitor.record_frame("cam-1", timestamp=100.0)
    assert monitor.state_of("cam-1", now=120.0) == CameraState.OFFLINE


def test_offline_cameras_lists_only_the_silent_ones():
    monitor = HealthMonitor(offline_after_seconds=10.0)
    monitor.record_frame("cam-1", timestamp=100.0)   # recent
    monitor.record_frame("cam-2", timestamp=50.0)    # old
    offline = monitor.offline_cameras(now=105.0)
    assert offline == ["cam-2"]
