import pygame
from selection import Selection
from settings import TILE_SIZE


class Group:
    def __init__(self):
        self.selected = []


    def update(self, selection, world, camera):
        if selection.rec_coord is not None:
            grid_rec_pos = (world.mouse_to_grid(selection.rec_coord[0], selection.rec_coord[1], camera.scroll)[0],
                            world.mouse_to_grid(selection.rec_coord[0], selection.rec_coord[1], camera.scroll)[1],
                            world.mouse_to_grid(selection.rec_coord[2], selection.rec_coord[3], camera.scroll)[0],
                            world.mouse_to_grid(selection.rec_coord[2], selection.rec_coord[3], camera.scroll)[1])
            if self.selected == []:
                for u in world.unites:
                        if grid_rec_pos[0] < u.pos[0] < grid_rec_pos[2] and grid_rec_pos[1] < u.pos[1] < grid_rec_pos[3]:
                                self.selected.append(u)


        if pygame.mouse.get_pressed()[2]:  # deselection de toutes les unites
            if self.selected != []:
                print(self.selected)
                self.selected.clear()

