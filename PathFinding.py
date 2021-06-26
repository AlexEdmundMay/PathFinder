# -*- coding: utf-8 -*-
"""
Created on Sat May 29 21:06:04 2021

Path Finding

Author: Alex May
"""
import numpy as np
import tkinter as tk

grid_dim = 15       #Dimensions of Grid (15x15)

#Coordinates of start and end points
start_x=start_y=0
end_x=end_y=grid_dim-1


class Button():
    """
    Class to store the tk.Button object with its x and y grid positions
    """
    def __init__(self, x_pos,y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
                
        
class Gui():
    """
    Graphical User Interface Class:
        -Sets up board
        -Allows users to choose wall positions
        -Runs Path Finding Code when 
    """
    def __init__(self, window):
        #Setup Window
        self.window = window
        self.window.title("Path Finding")
        self.window.minsize(width=1500, height=850)
        
        self.has_run=False     #Path Finding Code has not yet been run
        
        #Run Setup
        self.setup()
        
    def setup(self):
        """
        Adds Widgets to GUI
        """
        frame = tk.Frame(self.window).grid()     #Gets window's frame
        
        self.is_wall = np.full((grid_dim,grid_dim),False)    #No walls placed yet
        
        #Create Done Button for when user is finished placing walls
        self.done_button = tk.Button(frame,text='Done',bg="green",height=2,width=7,
                                padx=0,pady=0,command=self.done_pressed)
        self.done_button.grid(row = 15, column = 0,columnspan=15,sticky = tk.W+tk.E)
        
        #Setup coordinate grid of buttons so user can place walls
        self.button_grid_array = []    #array to store Button objects
        for i in range(grid_dim):
            temp_array = []     #array storing row of buttons
            for j in range(grid_dim):
                #Create Button
                button_obj = Button(i,j)
                grid_button = tk.Button(frame,command=lambda x=i, y=j: self.grid_button_pressed(x,y),
                                        bg="grey",height=2,width=7,padx=0,pady=0)
                button_obj.button = grid_button
                grid_button.grid(row = i, column = j)

                temp_array.append(button_obj)    #add Button to row
                
                #make start and end points uneditable
                if (i==start_x and j==start_y) or (i==end_x and j==end_y):
                    grid_button['bg']="black"
                    grid_button['state']="disabled"
            self.button_grid_array.append(temp_array)    #add row to button array
    
    def grid_button_pressed(self,x,y):
        #If no wall, place a wall
        if self.button_grid_array[x][y].button['bg']=='grey':
            self.button_grid_array[x][y].button['bg']='red'
            self.is_wall[y,x]=True
        else:           #If wall, delete wall
            self.button_grid_array[x][y].button['bg']='grey'
            self.is_wall[y,x]=False
            
    def done_pressed(self):
        """
        Runs When Done Button is Pressed
        """
        self.done_button['text']="Processing..."
        
        #If path finding hasn't been run, run it
        if self.has_run == False:
            path_finding(self)
            self.has_run = True
            self.done_button['text']="Reset"
        else:       #Reset the grid
            self.reset()
            self.has_run = False
            self.done_button['text']="Done"
    
    def reset(self):
        """
        Resets the Grid
        """
        self.is_wall = np.full((grid_dim,grid_dim),False)    #No walls placed yet
        for i in range(grid_dim):
            for j in range(grid_dim):
                self.button_grid_array[j][i].button['text']=""
                if (i==start_x and j==start_y) or (i==end_x and j==end_y):
                        self.button_grid_array[j][i].button['bg']="black"
                        self.button_grid_array[j][i].button['state']="disabled"
                else:
                    self.button_grid_array[j][i].button['bg']="grey"
                    self.button_grid_array[j][i].button['state']="normal"


def path_finding(gui):
    """
    Function containing the Path Finding Algorithm:
    """
    #Set start and end coordinates
    start_coords = np.array([start_x,start_y])
    end_coords= np.array([end_x,end_y])
    
    #set of vectors to transform a coord to the 8 coords surrounding it
    surrounding_coords = np.array([[-1,1],[0,1],[1,1]
                                   ,[1,0],[1,-1],[0,-1]
                                   ,[-1,-1],[-1,0]])
    
    path = np.array([start_coords,])    #array to store the path
    
    current_coords = start_coords       #Set current coord to the start coord
    
    #loops until code has reached the end (Unless 'break' occurs)
    while current_coords[0] != end_coords[0] or current_coords[1] != end_coords[1]:
        #shortest distance of adjacent coords to end coord
        shortest_dist = np.inf
        shortest_coords = current_coords
        
        #loop around each coord touching the current coord
        for i in range(len(surrounding_coords)):
            
            new_coords = current_coords + surrounding_coords[i]
            
            #Check new coord is on the grid
            if min(new_coords)>=0 and max(new_coords)<=grid_dim-1:
                #Check new coord is not a wall
                if gui.is_wall[new_coords[0]][new_coords[1]] != True:
                    
                    #check new coord is not touching a previous path coord
                    allowed = True
                    for p in path[0:len(path)-1]:
                        if p[0]-1<=new_coords[0]<=p[0]+1 and p[1]-1<=new_coords[1]<=p[1]+1:
                            allowed=False    #not allowed
                            break   #break out of for loop if touching
                            
                    #new Coord is valid        
                    if allowed:
                        #find distance to end from new coord
                        coord_dif = end_coords-new_coords
                        dist = min(coord_dif)+max(coord_dif)-min(coord_dif)
                        
                        #if distance is new shortest distance, update values
                        if dist<shortest_dist:
                            shortest_dist=dist
                            shortest_coords=new_coords
                            
        if shortest_dist == np.inf:    #no valid positions
            #set current postion to a wall (i.e. do not go here)
            gui.is_wall[current_coords[0]][current_coords[1]]=True
            
            #Reset colour, text and editability to default
            x=current_coords[0]
            y=current_coords[1]
            if not((x==start_x and y==start_y) or (x==end_x and y==end_y)):
                gui.button_grid_array[current_coords[1]][current_coords[0]].button['bg']='grey'
                gui.button_grid_array[current_coords[1]][current_coords[0]].button['state']="normal"
                gui.button_grid_array[current_coords[1]][current_coords[0]].button['text']=""
            
            #delete current position from path
            path = np.delete(path,-1,axis=0)
            if len(path) == 0:
                break   #if no posible paths, stop path searching
            
            #Update with previous value (current path no longer available)
            current_coords = path[-1]
            
        else:       #At least on position was valid
            #Add current coord to path
            path = np.vstack((path,shortest_coords))
            
            #Update Current coord
            current_coords = shortest_coords
            x=current_coords[0]
            y=current_coords[1]
            
            #Set grid point colour, text and editability
            if not((x==start_x and y==start_y) or (x==end_x and y==end_y)):
                gui.button_grid_array[current_coords[1]][current_coords[0]].button['bg']='yellow'
                gui.button_grid_array[current_coords[1]][current_coords[0]].button['state']="disabled"
                gui.button_grid_array[current_coords[1]][current_coords[0]].button['text']=str(len(path)-1)

        
def main():
    
    #Initialise  and Set-Up Graphical User Interface
    window = tk.Tk()    
    gui = Gui(window) 
    
    #window bring to front
    window.attributes("-topmost", True)  
            
    #runs GUI's main loop
    gui.window.mainloop()
    
    #After Mainloop, try destroying the window
    try:
        gui.window.destroy()
    except Exception:    #Window already closed
        pass
    
if __name__ == "__main__":
    main()      #run main

        