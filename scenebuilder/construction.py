import matplotlib.pyplot as plt
# from matplotlib.patches import Marker
from matplotlib.lines import Line2D
from typing import List
from scenebuilder.entities import Obstacle, Drone
import numpy as np
from scenebuilder.patches import ObstaclePatch, DronePatch
from scenebuilder.patches import Marker
# import pyclipper


class PatchManager:
    def __init__(self, ax: plt.Axes):
        self.ax = ax
        self.building_patches:dict[Obstacle, ObstaclePatch]  = {}
        self.drone_patches:dict[Drone, DronePatch] = {}
        # self.temp_drone_starts:list[Line2D] = []
        self.current_building_vertices:list[Line2D] = []
        self.drone_start = None

    def add_building_patch(self, building: Obstacle, **kwargs)->None:
        patch = ObstaclePatch(
            building,
            edgecolor=kwargs.get('edgecolor', (0, 0, 0, 1)),
            facecolor=kwargs.get('facecolor', (0, 0, 1, 0.5)),
            closed=kwargs.get('closed', True),
            linewidth=kwargs.get('linewidth', 2.0),
            picker=kwargs.get('picker', True),
        )
        self.ax.add_patch(patch)
        self.building_patches[building] = patch
    
    def add_building_vertex(self,vertex:tuple)->None:
        point = Marker(vertex, "go").create_marker()
        self.current_building_vertices.append(point)

    def get_building_patch(self,building:Obstacle)->ObstaclePatch:
        '''Obtains the patch for the building passed as argument
        and returns it. If the patch doesn't exist, returns KeyError.
        '''
        return self.building_patches[building]
    
    def get_building_from_patch(self, patch:ObstaclePatch)->Obstacle:
        '''Obtains the building from the patch passed as argument
        '''
        for building, building_patch in self.building_patches.items():
            if building_patch == patch:
                # call the selected building setter to highlight the building
                return building
            
    def make_building(self)->Obstacle:
        '''Create a building from the current vertices'''
        if not len(self.current_building_vertices) >= 3:
            return
        vertices = np.array(
            [point.get_xydata() for point in self.current_building_vertices]
        )
        vertices = vertices.squeeze(axis=1)
        building = Obstacle(vertices)
        self.add_building_patch(building)
        self.clear_building_vertices()
        return building
    
    def make_drone(self)->Drone:
        return Drone(
                ID=f"V{len(self.drones)}", position=None, goal=None
            )


        
    def add_drone_patch(self, drone: Drone, **kwargs)->None:
        # Similar logic for adding drone patches
        drone_patch = DronePatch(drone, self.ax)
        patches = drone_patch.create_patches()
        self.drone_patches[drone] = drone_patch

    def add_temp_drone_start(self, point:list)->None:
        # self.temp_drone_starts.append(point)
        self.drone_start = Marker(
                point, style="ko"
            ).create_marker()

    def remove_temp_drone_start(self)->None:
        if self.drone_start:
            self.drone_start.remove()
            self.drone_start = None
    
    def _remove_markers_from_list(self, lst:List[Line2D])->None:
        for element in lst:
            element.remove()
        lst.clear()

    def redraw_drone(self, drone:Drone)->None:
        self.drone_patches[drone].update()

    def redraw_building(self,building:Obstacle)->None:
        self.building_patches[building].update_visual()
        

    def remove_building_patch(self, building: Obstacle):
        if building in self.building_patches:
            self.building_patches[building].remove()
            del self.building_patches[building]

    def remove_drone_patch(self, drone: Drone)->None:
        '''Remove drone patch from the figure and the patches dictionary
        and remove the patches from the figure
        '''
        self.drone_patches.pop(drone).remove()

    def clear_building_vertices(self):
        self._remove_markers_from_list(self.current_building_vertices)

    def clear_all(self):
        for patch in self.building_patches.values():
            patch.remove()
        for patch in self.drone_patches.values():
            patch.remove()
        self.remove_temp_drone_start()
        self.building_patches.clear()
        self.drone_patches.clear()

