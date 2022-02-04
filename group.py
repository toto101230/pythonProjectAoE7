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

            if not self.selected and self.poly_area(A, B, C) >= 2:
                for u in world.unites:
                    if self.is_in_selection(u, A, B, C, D) and (u.joueur.name == "joueur 1"):
                        self.selected.append(u)
                        world.examined_unites_tile.append(u)

        if pygame.mouse.get_pressed(3)[2] or pygame.mouse.get_pressed(3)[0]:  # deselection de toutes les unites
            if self.selected:
                self.selected.clear()

    def is_in_selection(self, unite, A, B, C, D):
        t1 = self.tri_area(A, C, unite.pos)
        t2 = self.tri_area(C, B, unite.pos)
        t3 = self.tri_area(B, D, unite.pos)
        t4 = self.tri_area(D, A, unite.pos)
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
        if (p * (p - a) * (p - b) * (p - c)) > 0:
            return math.floor(math.sqrt(p * (p - a) * (p - b) * (p - c)))  # formule de Héron
        return math.floor(math.sqrt(p * (p - a) * (p - b) * (p - c)+0.0000001))

    def segment_len(self, A, B):
        return math.sqrt((B[0] - A[0]) ** 2 + (B[1] - A[1]) ** 2)

    def isqrt_dicho_rec(self, n):
        low = 0
        high = n

        def borne(bas, haut):
            if haut - bas > 1:
                middle = (bas + haut) // 2
                if middle * middle > n:
                    return borne(bas, middle)
                else:
                    return borne(middle, haut)
            return haut if haut * haut <= n else bas

        return borne(low, high)
