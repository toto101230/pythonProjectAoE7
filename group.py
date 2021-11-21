import pygame
import math
from selection import Selection
from settings import TILE_SIZE


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

            if self.selected == []:
                for u in world.unites:
                    if self.is_in_selection(u,A,B,C,D):
                        self.selected.append(u)

        if pygame.mouse.get_pressed()[2]:  # deselection de toutes les unites
            if self.selected != []:
                print(self.selected)
                self.selected.clear()

    def is_in_selection(self, unite, A, B, C, D):
        t1 = self.tri_area(A,C,unite.pos)
        t2 = self.tri_area(C,B,unite.pos)
        t3 = self.tri_area(B,D,unite.pos)
        t4 = self.tri_area(D,A,unite.pos)
        if t1+t2+t3+t4 - self.poly_area(A,C,B) < 0 :
            return True
        return False

    def poly_area(self, A, C, D):
        return 2*self.tri_area(A,C,D)

    def tri_area(self, A, B ,C):
        p = (self.tri_perimeter(A,B,C))/2
        return self.isqrt_dicho_rec(p*(p-self.segment_len(A,B))*(p-self.segment_len(B,C))*(p-self.segment_len(C,A))) #formule de Héron

    def tri_perimeter(self, A, B, C):
        return self.segment_len(A,B) + self.segment_len(B,C) + self.segment_len(C,A)

    def segment_len(self, A, B):
        return self.isqrt_dicho_rec((B[0]-A[0])**2 + (B[1]-A[1])**2)

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
