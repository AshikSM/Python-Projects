import tkinter as tk
from PIL import ImageTk, Image, ImageSequence
import pygame
import sys

# Initialize pygame mixer
try:
    pygame.mixer.init()
except Exception as e:
    print(f"Pygame mixer initialization failed: {e}", file=sys.stderr)

# Define the eye size aspect dictionary
eyesizeaspect = {
    'sleeping': [i / 10 for i in range(0, 21)],     # 0.0 to 2.0
    'tired': [i / 10 for i in range(21, 31)],       # 2.1 to 3.0
    'fully awake': [i / 10 for i in range(31, 51)]  # 3.1 to 5.0
}

# Function to start the main application
def start_main_app():
    # Create the main window
    root = tk.Tk()
    root.title('Eye Size Aspect Checker')

    # Load the images
    try:
        images = {
            'sleeping': ImageTk.PhotoImage(Image.open("sleeping.png")),
            'tired': ImageTk.PhotoImage(Image.open("tired.png"))
            # Note: 'fully awake' will use a GIF instead of an image
        }
        print("Images loaded successfully.", file=sys.stderr)
    except Exception as e:
        print(f"Error loading images: {e}", file=sys.stderr)
        images = {}

    # Load the 'fully awake' GIF
    try:
        awake_gif_frames = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("awake.gif"))]
        print("awake.gif loaded successfully.", file=sys.stderr)
    except Exception as e:
        print(f"Error loading awake.gif: {e}", file=sys.stderr)
        awake_gif_frames = []

    # Load the invalid GIF
    try:
        invalid_gif_frames = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("invalid.gif"))]
        print("invalid.gif loaded successfully.", file=sys.stderr)
    except Exception as e:
        print(f"Error loading invalid.gif: {e}", file=sys.stderr)
        invalid_gif_frames = []

    # Load the click sound
    try:
        click_sound = pygame.mixer.Sound("click.mp3")
        print("click.mp3 loaded successfully.", file=sys.stderr)
    except Exception as e:
        print(f"Error loading click.mp3: {e}", file=sys.stderr)
        click_sound = None

    # Variables to manage GIF playback
    gif_playing = False
    gif_after_id = None  # Store the after() callback ID

    # Function to play click sound
    def play_click_sound():
        if click_sound:
            click_sound.play()
        else:
            print("Click sound not available.", file=sys.stderr)

    # Function to check the eye size aspect
    def check_eye_size():
        nonlocal gif_playing, gif_after_id
        play_click_sound()

        # Cancel any ongoing GIF playback
        if gif_after_id is not None:
            root.after_cancel(gif_after_id)
            gif_after_id = None
        gif_playing = False

        try:
            size = float(entry.get())
            for state, sizes in eyesizeaspect.items():
                if size in sizes:
                    result_label.config(text=f'The state is: {state}')

                    if state == 'fully awake':
                        if awake_gif_frames:
                            gif_playing = True
                            display_gif(awake_gif_frames)
                        else:
                            print("awake.gif frames not available.", file=sys.stderr)
                            image_label.config(image='')
                            image_label.image = None
                    elif state in images:
                        image_label.config(image=images[state])
                        image_label.image = images[state]
                    else:
                        print(f"No image for state '{state}'", file=sys.stderr)
                        image_label.config(image='')
                        image_label.image = None
                    return
            result_label.config(text='Invalid number')
            if invalid_gif_frames:
                gif_playing = True
                display_gif(invalid_gif_frames)
            else:
                image_label.config(image='')
                image_label.image = None
        except ValueError:
            result_label.config(text='Invalid input. Please enter a number.')
            if invalid_gif_frames:
                gif_playing = True
                display_gif(invalid_gif_frames)
            else:
                image_label.config(image='')
                image_label.image = None

    # Function to display GIF
    def display_gif(frames, index=0):
        nonlocal gif_playing, gif_after_id
        if gif_playing and frames:
            frame = frames[index]
            image_label.config(image=frame)
            image_label.image = frame
            gif_after_id = root.after(100, display_gif, frames, (index + 1) % len(frames))
        else:
            image_label.config(image='')
            image_label.image = None

    # Create and place widgets
    label = tk.Label(root, text='Enter eye size:')
    label.pack()

    entry = tk.Entry(root)
    entry.pack()

    button = tk.Button(root, text='Check', command=check_eye_size)
    button.pack()

    result_label = tk.Label(root, text='')
    result_label.pack()

    image_label = tk.Label(root)
    image_label.pack()

    # Bind the Enter key to the check_eye_size function
    root.bind('<Return>', lambda event: check_eye_size())

    # Set focus to the entry widget
    entry.focus()

    # Run the application
    root.mainloop()

# Function to show splash screen
def show_splash_screen():
    splash = tk.Tk()
    splash.title("Splash Screen")

    # Remove window decorations
    splash.overrideredirect(True)

    # Load the splash GIF
    try:
        splash_gif_frames = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("splash.gif"))]
        print("splash.gif loaded successfully.", file=sys.stderr)
    except Exception as e:
        print(f"Error loading splash.gif: {e}", file=sys.stderr)
        splash_gif_frames = []

    if not splash_gif_frames:
        print("No splash GIF frames available.", file=sys.stderr)
        splash.destroy()
        start_main_app()
        return

    # Create a label to display the GIF
    splash_label = tk.Label(splash)
    splash_label.pack()

    # Position the splash screen at the top left of the screen
    splash.geometry('+0+0')

    # Function to play the splash GIF once
    def play_splash(index=0):
        if index < len(splash_gif_frames):
            frame = splash_gif_frames[index]
            splash_label.config(image=frame)
            splash_label.image = frame
            splash.after(100, play_splash, index + 1)
        else:
            fade_out()

    # Function to fade out the splash screen
    def fade_out():
        alpha = splash.attributes('-alpha')
        if alpha > 0:
            alpha -= 0.05
            splash.attributes('-alpha', alpha)
            splash.after(50, fade_out)
        else:
            splash.destroy()
            start_main_app()

    # Set initial opacity and start playing the splash GIF
    splash.attributes('-alpha', 1.0)
    play_splash()

    # Run the splash screen
    splash.mainloop()

# Start the splash screen
show_splash_screen()
