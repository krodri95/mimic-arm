import sys
from tkinter import *
from Renderer import Renderer

# Display dimensions
DWIDTH = 560
DHEIGHT = 360

# Segment length
DLENGTH = 150


def main():
    if not len(sys.argv) == 2:
        print("Wrong arguments. Provide the path to the video.")
        exit()

    master = Tk()
    master.title = 'Planar Robot Manipulator'
    canvasBot = Canvas(master,width = DWIDTH, height = DHEIGHT, background='white')
    canvasBot.pack(side='left')

    canvasImg = Canvas(master,width = DWIDTH, height = DHEIGHT, background='white')
    canvasImg.pack(side='left')
    
    #Draw the axes
    canvasBot.create_line(DWIDTH//2,0,DWIDTH//2,DHEIGHT, fill='black',width=1)
    canvasBot.create_line(0,DHEIGHT//2,DWIDTH,DHEIGHT//2, fill='black',width=1)   
    
    render = Renderer(DLENGTH, canvasBot, canvasImg, sys.argv[1])

    # Create a button to trigger the run
    button = Button(master, text="Start", command=render.run)
    button.pack()

    master.mainloop()
    render.releaseVideo()
    return
    

if __name__=="__main__":
    main()