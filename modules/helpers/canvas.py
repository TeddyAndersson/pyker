
def create_rectangle_with_rounded_corners(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    """
    x1 and y1 represent the top left corner point of a rectangle
    x2 and y2 represent the bottom right corner point of a rectangle
    """
    points = (x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius, x2, y2-radius, x2,
              y2, x2-radius, y2, x2-radius, y2, x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius, x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1)
    return canvas.create_polygon(points, **kwargs, smooth=True)
