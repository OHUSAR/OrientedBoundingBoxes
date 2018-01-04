from tkinter import *
from tkinter.ttk import *
from tkinter import Canvas as TkCanvas

from Core.BoundingBox.OrientedBoundingBox import GetOrientedBBox
from Core.ConvexHull.ConvexHull import GetConvexHull
from Core.Geometry.Intersections import IntersectSegments
from Core.Geometry.Utils import GetOrientedEdges
from Core.BasicDefs import vector

OOBB_COLOR = 'LightYellow4'

class DrawingState:
    FIRST = 1
    SECOND = 2
    DONE = 3

    @staticmethod
    def drawing_color(state):
        return {1: 'salmon3', 2: 'chartreuse2'}[state]


class Canvas(TkCanvas):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw, width=1200, height=800, bg='white')
        self.pack(fill='both', expand=True)

class PolygonStorage:
    def __init__(self):
        self.polygons = {}
        self.ordered = []

    def add(self, polygon):
        self.polygons[polygon.canvas_id] = polygon
        self.ordered.append(polygon)

    def get(self, i, by_order=False):
        if by_order:
            return self.ordered[i]
        return self.polygons[i]

class PolygonObject:
    def __init__(self, vertices, canvas_id):
        self.vertices = vertices
        self.canvas_id = canvas_id
        self.oobb_canvas_id = None
        self._oobb = None

    def OOBB(self):
        if self._oobb is None:
            self.compute_bb()
        return self.round_oobb(self._oobb + [self._oobb[0]])

    def move(self, x, y):
        for vector in self.vertices:
            vector[0], vector[1] = vector[0] - x, vector[1] - y
        self.compute_bb()

    def compute_bb(self):
        vertices = [vector(v) for v in self.vertices]
        ch = GetConvexHull(vertices)
        edges = GetOrientedEdges(ch)
        self._oobb = GetOrientedBBox(ch, edges)

    def round_oobb(self, oobb):
        rounded_oobb = []
        for v in oobb:
            rounded_oobb.append([round(x) for x in v])
        return rounded_oobb


class Application(Frame):

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.canvas = Canvas()
        self.polygons = PolygonStorage()

        self.drawing_state = DrawingState.FIRST
        self.intersects = False
        self.active_line = None
        self.lines_ids = []
        self.polygon_coords = []
        self._drag_data = {"x": 0, "y": 0, "item": None}

        self.bind_events()
        self.pack()

    def bind_events(self):
        self.canvas.bind("<ButtonPress-1>", self.draw_line)
        self.canvas.bind("<ButtonPress-3>", self.end_polygon)
        self.canvas.bind("<Motion>", self.move_line)
        self.canvas.tag_bind("token", "<ButtonPress-1>", self.on_token_press)
        self.canvas.tag_bind("token", "<ButtonRelease-1>", self.on_token_release)
        self.canvas.tag_bind("token", "<B1-Motion>", self.on_token_motion)

    def draw_line(self, event):
        if self.drawing_state == DrawingState.DONE or self.intersects:
            return

        if self.active_line:
            self.polygon_coords.append((event.x, event.y))
            line_id = self.canvas.create_line(self.polygon_coords[-2], self.polygon_coords[-1])
            self.lines_ids.append(line_id)
        else:
            self.polygon_coords.append((event.x, event.y))
            self.active_line = self.canvas.create_line((event.x, event.y), (event.x, event.y))

    def move_line(self, event):
        if self.active_line:
            self.canvas.coords(self.active_line, *self.polygon_coords[-1], event.x, event.y)

            if len(self.polygon_coords) > 1:
                self.validate_new_line(event.x, event.y)
                self.set_active_line_color()

    def end_polygon(self, event):
        if self.active_line is None or len(self.polygon_coords) < 3:
            return

        X1, Y1 = self.polygon_coords[-1]
        X2, Y2 = self.polygon_coords[0]
        if self.valid_line(X1, Y1, X2, Y2, skip_first=True):
            self.add_polygon()
            self.cleanup_lines()
            self.drawing_state += 1

    def add_polygon(self):
        vertices = self.polygon_coords + [self.polygon_coords[0]]
        polygon_id = self.canvas.create_polygon(
            vertices,
            tags="token",
            fill=DrawingState.drawing_color(self.drawing_state),
            outline=DrawingState.drawing_color(self.drawing_state),
        )

        polygon = PolygonObject(vertices, polygon_id)
        polygon.oobb_canvas_id = self.canvas.create_line(polygon.OOBB(), width=3, fill=OOBB_COLOR)
        self.polygons.add(polygon)

    def cleanup_lines(self):
        self.canvas.delete(*self.lines_ids)
        self.canvas.delete(self.active_line)
        self.active_line = None
        self.polygon_coords = []

    def valid_line(self, X1, Y1, X2, Y2, skip_first=False):
        start_i = 0
        if skip_first:
            start_i += 1
        previous = self.polygon_coords[start_i]
        for point in self.polygon_coords[start_i+1:-1]:
            X3, Y3, X4, Y4 = previous[0], previous[1], point[0], point[1]
            if IntersectSegments([X1, Y1, X2, Y2], [X3, Y3, X4, Y4]):
                return False
            previous = point
        return True

    def validate_new_line(self, X, Y):
        X1, Y1, X2, Y2 = self.polygon_coords[-1][0], self.polygon_coords[-1][1], X, Y
        self.intersects = not self.valid_line(X1, Y1, X2, Y2)

    def set_active_line_color(self):
        if self.intersects:
            self.canvas.itemconfigure(self.active_line, fill='red')
        else:
            self.canvas.itemconfigure(self.active_line, fill='black')

    def on_token_press(self, event):
        if self.drawing_state != DrawingState.DONE:
            return

        item_id = self.canvas.find_closest(event.x, event.y)[0]
        self._drag_data["item"] = self.polygons.get(item_id)
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def on_token_release(self, event):
        if self.drawing_state != DrawingState.DONE:
            return

        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

    def on_token_motion(self, event):
        if self.drawing_state != DrawingState.DONE:
            return

        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]

        self.canvas.move(self._drag_data["item"].canvas_id, delta_x, delta_y)
        self.canvas.move(self._drag_data["item"].oobb_canvas_id, delta_x, delta_y)

        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

if __name__ == '__main__':
    root = Tk()
    app = Application(master=root)
    app.mainloop()
