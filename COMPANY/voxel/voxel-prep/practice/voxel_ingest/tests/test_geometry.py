from ingest import BBox, intersection_area, iou


def test_identical_boxes_have_iou_one():
    box = BBox(0, 0, 100, 100)
    assert iou(box, box) == 1.0


def test_half_overlap():
    a = BBox(0, 0, 100, 100)      # area 10000
    b = BBox(50, 0, 150, 100)     # area 10000, overlap 5000
    # intersection 5000, union 15000 → 1/3
    assert abs(iou(a, b) - (1 / 3)) < 1e-9


def test_touching_boxes_do_not_overlap():
    a = BBox(0, 0, 100, 100)
    b = BBox(100, 0, 200, 100)    # shares an edge, zero area overlap
    assert iou(a, b) == 0.0


# ---------------------------------------------------------------- B1 lives here

def test_disjoint_boxes_have_zero_iou():
    """Two boxes that are nowhere near each other must score 0.

    This is THE bug that silently ruins a tracker: if disjoint boxes report a
    positive IoU, every object gets matched to every other object and identities
    scramble. Trace the intersection math by hand for these two.
    """
    a = BBox(0, 0, 100, 100)
    b = BBox(110, 110, 210, 210)   # 10px gap in both axes, no overlap at all
    assert iou(a, b) == 0.0


def test_intersection_of_disjoint_is_zero_not_positive():
    a = BBox(0, 0, 10, 10)
    b = BBox(20, 20, 30, 30)       # clear gap, zero real overlap
    assert intersection_area(a, b) == 0.0
