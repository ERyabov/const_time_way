
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

    def get_way(self, dx, way_t, segments_max = 10):
        self.dx = dx
        self.way_t = way_t
        h_max = self.g * (self.way_t ** 2) / 2
        segments = []
        dy = self.eps
        # print ('h_max', h_max)
        while len(segments) < segments_max:
            dy = self.lbin_search(dy, self.dx, self.check_seg, segments)
            # print ('add seg', self.dx, dy)
            if dy + self.eps > h_max:
                break
            segments.append(Segment(self.dx, dy))

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


sol = ConstWay(2)
step = 0.001
points_cnt = 1000
travel_time = 2
way = sol.get_way(step, travel_time, points_cnt)
print('step, m:', sol.dx)
print('travel_time, s:', travel_time)
print('points_cnt:', points_cnt)
print('result:')
for point in way:
    print(round(point[0], 6), round(point[1], 6))

# dy = 0.00001
# for i in range(100):
#     dt, v1 = sol.proc_seg(0, Segment(sol.dx, dy))
#     print(dt, dy, v1)
#     dy *= 1.1