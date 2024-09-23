
import math
class Segment:
    def __init__(self, dx, dy):
        self.corn   = math.atan(dy / dx)
        self.sin    = math.sin(self.corn)
        self.len    = (dx * dx + dy * dy) ** 0.5
        self.dy     = dy

class ConstWay:
    def __init__(self, way_t, search_depth = 30):
        self.g = 9.81
        self.dx = 0.001
        self.eps = 10 ** -6
        self.way_t = way_t
        self.search_depth = search_depth

    def proc_seg(self, v0, seg):
        a = self.g * seg.sin / 2
        b = v0
        c = -seg.len
        d = b * b - 4 * a * c
        if d < 0:
            print('d < 0')
            return -1, -1
        dt = (-b + d ** 0.5) / (2 * a)
        v1 = v0 + self.g * seg.sin * dt
        # print ('proc_seg', v0, seg.dy, dt, v1)
        return dt, v1

    def lbin_search(self, b, e, func, args):
        # print ('bin_search', b, e)
        depth = 0
        while depth < self.search_depth:
            depth += 1
            m = (b + e) / 2
            if func(m, args):
                e = m
            else:
                b = m
        return b

    def check_seg(self, dy, segments):
        # print ('check_seg', dy)
        new_seg = Segment(self.dx, dy)
        t, v0 = self.proc_seg(0, new_seg)
        if t > self.way_t:
                return True
        for seg in reversed(segments):
            dt, v1 = self.proc_seg(v0, seg)
            if dt < 0:
                print ('lbin dt<0')
                return True
            t += dt
            if t > self.way_t:
                # print ('lbin t>way_t')
                return False
            v0 = v1
        return True

    def get_time(self, dy, segments):
        # print ('check_seg', dy)
        new_seg = Segment(self.dx, dy)
        t, v0 = self.proc_seg(0, new_seg) if dy else (0, 0)
        for seg in reversed(segments):
            dt, v1 = self.proc_seg(v0, seg)
            if dt < 0:
                print ('get_time dt<0')
                return 0
            t += dt
            v0 = v1
        return t
    
    def is_rise(self, dy, segments):
        return self.get_time(dy + self.eps / 100, segments) > self.get_time(dy, segments)

    def get_way(self, dx, way_t, segments_max = 10):
        self.dx = dx
        self.way_t = way_t
        h_max = self.g * (self.way_t ** 2) / 2
        segments = []
        dy = self.eps
        dy_max = self.dx
        # print ('h_max', h_max)
        while len(segments) < segments_max:
            dy = self.lbin_search(dy, dy_max, self.check_seg, segments)
            if abs(dy - self.dx) < self.eps:
                break
            segments.append(Segment(self.dx, dy))

        # dy = self.dx
        while len(segments) < segments_max:
            dy_max = self.lbin_search(dy, h_max, self.is_rise, segments)
            # print('dy_max', dy_max)
            if (dy_max  + self.eps > h_max):
                print('h_max reached', dy, h_max, segments[-1].corn / 6.28 * 360, self.dx)
                break
            if (dy  + self.eps > dy_max):
                print('dy_max reached', dy_max, h_max, segments[-1].corn / 6.28 * 360, self.dx)
                break
            dy = self.lbin_search(dy, dy_max, self.check_seg, segments)
            segments.append(Segment(self.dx, dy))
            # print ('add seg', self.dx, dy, len(segments))


        res = [(0, 0)]
        x = 0
        y = 0
        for seg in segments:
            x += self.dx
            y += seg.dy
            res.append((x, y))
        return res

    def sq_solve(self, a, b, c):
        return (-b + (b * b - 4 * a *c)) / (2 * a)


# class Prm:
#     def __init__(self):
#         self.step       = 0.001
#         self.points_cnt = 1000
#         self.travel_time = 2
#         self.accuracy   = 30

def print_res(way, step, travel_time, points_cnt, accuracy):
    print('step, m:', step)
    print('travel_time, s:', travel_time)
    print('points_cnt:', points_cnt)
    print('accuracy:', accuracy)
    print('result:')
    for point in way:
        print(round(point[0], 6), ',', round(point[1], 6), sep='')

def show_res(points, label):
    x = []
    y = []
    for point in points:
        x.append(point[0])
        y.append(point[1])
    import matplotlib.pyplot as plt
    plt.plot(x, y, label=label)
    plt.show()


sol = ConstWay(2, 30)
step = 0.001
points_cnt = 10000
travel_time = 0.5
way = sol.get_way(step, travel_time, points_cnt)

print_res(way, step, travel_time, points_cnt, sol.search_depth)

show_res(way, 'time_'+ str(travel_time))