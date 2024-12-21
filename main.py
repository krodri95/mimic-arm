"""
main.py

Usage:
    python main.py <video_path>

    Example:
        python main.py path/to/video.mp4

Constants:
    - DWIDTH: Width of the display canvas.
    - DHEIGHT: Height of the display canvas.
    - DLENGTH: Segment length for the robot manipulator.

"""

import sys
from tkinter import * # pylint: disable=unused-wildcard-import
from renderer import Renderer

# Display dimensions
DWIDTH = 560
DHEIGHT = 360

# Segment length
DLENGTH = 150


def main():
    """
    Visualise a planar robot manipulator and process a video file.

    This function initializes a GUI using Tkinter with two canvases: one for 
    visualising the robot manipulator and the other for displaying video frames. 
    It also sets up a button to trigger the rendering process.

    Args:
        None

    Returns:
        None

    Note:
        The program expects a single command-line argument: the path to the video file.
        If the argument is missing or incorrect, the function will exit with an error message.
    """

    if not len(sys.argv) == 2:
        print("Wrong arguments. Provide the path to the video.")
        sys.exit(1)

    master = Tk()
    master.title = "Planar Robot Manipulator"
    canvas_bot = Canvas(master, width=DWIDTH, height=DHEIGHT, background="white")
    canvas_bot.pack(side="left")

    canvas_img = Canvas(master, width=DWIDTH, height=DHEIGHT, background="white")
    canvas_img.pack(side="left")

    # Draw the axes
    canvas_bot.create_line(DWIDTH // 2, 0, DWIDTH // 2, DHEIGHT, fill="black", width=1)
    canvas_bot.create_line(0, DHEIGHT // 2, DWIDTH, DHEIGHT // 2, fill="black", width=1)

    render = Renderer(DLENGTH, canvas_bot, canvas_img, sys.argv[1])

    # Create a button to trigger the run
    button = Button(master, text="Start", command=render.run)
    button.pack()

    master.mainloop()
    render.release_video()


if __name__ == "__main__":
    main()
