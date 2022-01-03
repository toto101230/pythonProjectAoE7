import pygame
import math


class Group:
    def __init__(self):
        self.selected = []

    def update(self, selection, world, camera):
        if selection.rec_coord is not None:

            # var

            # topleft
            A = (world.mouse_to_grid(selection.rec_coord[0], selection.rec_coord[1], camera.scroll))

            # bottomright
            B = (world.mouse_to_grid(selection.rec_coord[2], selection.rec_coord[3], camera.scroll))

            # topright
            C = (world.mouse_to_grid(selection.rec_coord[2], selection.rec_coord[1], camera.scroll))

            # bottomleft
            D = (world.mouse_to_grid(selection.rec_coord[0], selection.rec_coord[3], camera.scroll))

            # print(A,B,C,D)
            # print(self.poly_area(A,B,C))
            if not self.selected and self.poly_area(A, B, C) >= 2:
                for u in world.unites:
                    if self.is_in_selection(u, A, B, C, D):
                        self.selected.append(u)
                        world.examined_unites_tile.append(u.pos)
                # if len(self.selected):
                    # print(str(len(self.selected)) + " unite(s) selected")

        if pygame.mouse.get_pressed()[2]:  # deselection de toutes les unites
            if self.selected:
                # print(self.selected)
                # for u in self.selected:
                    # print(u.pos)
                self.selected.clear()

    def is_in_selection(self, unite, A, B, C, D):
        t1 = self.tri_area(A, C, unite.pos)
        t2 = self.tri_area(C, B, unite.pos)
        t3 = self.tri_area(B, D, unite.pos)
        t4 = self.tri_area(D, A, unite.pos)
        # print(self.poly_area(A,B,C))
        # print("t down")
        # print(t1+t2+t3+t4)
        if t1 + t2 + t3 + t4 - self.poly_area(A, B, C) <= 2:
            return True
        return False

    def poly_area(self, A, B, C):
        return math.floor(2 * self.tri_area(A, B, C))  # ceil ou floor

    def tri_area(self, A, B, C):
        a = self.segment_len(A, B)
        b = self.segment_len(B, C)
        c = self.segment_len(C, A)
        p = (a + b + c) / 2
        return math.floor(math.sqrt(p * (p - a) * (p - b) * (p - c)))  # formule de Héron

    def tri_perimeter(self, A, B, C):  # not used
        return self.segment_len(A, B) + self.segment_len(B, C) + self.segment_len(C, A)

    def segment_len(self, A, B):
        return math.sqrt((B[0] - A[0]) ** 2 + (B[1] - A[1]) ** 2)

    ####---------------------------------------------------------------------------------

    def isqrt_dicho_rec(self, n):
        low = 0
        high = n

        def borne(low, high):
            if high - low > 1:
                middle = (low + high) // 2
                if middle * middle > n:
                    return borne(low, middle)
                else:
                    return borne(middle, high)
            # print(low,high)
            return high if high * high <= n else low

        return borne(low, high)
