from tkinter import *
from tkinter.ttk import *
from tkinter import Canvas as TkCanvas

from Core.Collisions.CollisionDetector import CollisionObject, ObjectsCollide
from Core.Geometry.Intersections import IntersectSegments
from Core.BasicDefs import vector
from Core.Geometry.Utils import GetOrientedEdges, GetEdgeNormals
from GUI.drawing_state import DrawingState
from GUI.polygon_storage import PolygonStorage, PolygonObject

OOBB_COLOR = 'LightYellow4'


class Canvas(TkCanvas):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw, width=1200, height=800, bg='white')
        self.pack(fill='both', expand=True)


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
        self.all_ids = set()
        self.colliding_ids = set()
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
            self.active_line = self.canvas.create_line((event.x, event.y), (event.x, event.y), dash=(7, 3))

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
            try:
                self.add_polygon()
            except (ValueError, IndexError):
                return
            self.cleanup_lines()
            self.drawing_state += 1

    def add_polygon(self):
        vertices = self.polygon_coords + [self.polygon_coords[0]]
        polygon = PolygonObject([vector(v) for v in vertices])
        OOBBs = polygon.OOBBs()

        polygon_id = self.canvas.create_polygon(vertices, tags="token",
                                                fill=DrawingState.drawing_color(self.drawing_state),
                                                outline=DrawingState.drawing_color(self.drawing_state))

        polygon.canvas_id = polygon_id
        for oobb_level in OOBBs:
            line_id = self.canvas.create_line(oobb_level.OOBB(), fill=OOBB_COLOR, width=2)
            oobb_level.canvas_id = line_id
            polygon.oobb_canvas_ids[line_id] = oobb_level

        self.polygons.add(polygon)

    def cleanup_lines(self):
        self.canvas.delete(*self.lines_ids)
        self.canvas.delete(self.active_line)
        self.active_line = None
        self.intersects = False
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

        self.polygons.get(self._drag_data["item"].canvas_id).move(delta_x, delta_y)
        self.canvas.move(self._drag_data["item"].canvas_id, delta_x, delta_y)
        for i in self._drag_data["item"].oobb_canvas_ids:
            self.canvas.move(i, delta_x, delta_y)

        for i in self.polygons.get(self._drag_data["item"].canvas_id).all_canvas_ids():
            self.canvas.tag_raise(i)

        self.check_collisions()

        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def check_collisions(self):
        self.colliding_ids = set()

        polygon1, polygon2 = self.polygons.get(0, by_order=True), self.polygons.get(1, by_order=True)
        root1, root2 = polygon1.oobb_hierarchy.root, polygon2.oobb_hierarchy.root

        self.collides(root1, root2)

        for i in self.all_ids:
            self.set_collision_object(i, False)
        for i in self.colliding_ids:
            self.set_collision_object(i, True)


    def collides(self, level1, level2):
        if level1 is None or level2 is None:
            return False

        children_collisions = []
        for ch in level1.children:
            if ch is not None:
                if self.check_collides(ch.oobb, level2.oobb):
                    self.colliding_ids.add(ch.canvas_id)
                    self.colliding_ids.add(level2.canvas_id)

        for ch in level2.children:
            if ch is not None:
                if self.check_collides(ch.oobb, level1.oobb):
                    self.colliding_ids.add(ch.canvas_id)
                    self.colliding_ids.add(level1.canvas_id)

        for ch1 in level1.children:
            for ch2 in level2.children:
                children_collisions.append(self.collides(ch1, ch2))

        result = True in children_collisions or self.check_collides(level1.oobb, level2.oobb)

        self.all_ids.add(level1.canvas_id)
        self.all_ids.add(level2.canvas_id)
        if result:
            self.colliding_ids.add(level1.canvas_id)
            self.colliding_ids.add(level2.canvas_id)

        return result

    def check_collides(self, oobb1, oobb2):
        colEA = GetOrientedEdges(oobb1)
        colEB = GetOrientedEdges(oobb2)
        normalsA = GetEdgeNormals(colEA)
        normalsB = GetEdgeNormals(colEB)

        colObjA = CollisionObject(oobb1, normalsA)
        colObjB = CollisionObject(oobb2, normalsB)

        return ObjectsCollide(colObjA, colObjB)

    def set_collision_object(self, canvas_id, collides=True):
        if collides:
            self.canvas.itemconfigure(canvas_id, fill='red', width=4)
        else:
            self.canvas.itemconfigure(canvas_id, fill=OOBB_COLOR, width=2)


if __name__ == '__main__':
    root = Tk()
    app = Application(master=root)
    app.mainloop()
