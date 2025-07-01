import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QPixmap, QImage

# Configuration for PNG files (generated_pngs folder)
OUTPUT_FOLDER = "generated_pngs"

color_files = {
    "red": f"{OUTPUT_FOLDER}/dvd_red.png",
    "green": f"{OUTPUT_FOLDER}/dvd_green.png",
    "blue": f"{OUTPUT_FOLDER}/dvd_blue.png",
    "yellow": f"{OUTPUT_FOLDER}/dvd_yellow.png",
    "cyan": f"{OUTPUT_FOLDER}/dvd_cyan.png",
    "white": f"{OUTPUT_FOLDER}/dvd_white.png",
    "orange": f"{OUTPUT_FOLDER}/dvd_orange.png",
    "salmonpink": f"{OUTPUT_FOLDER}/dvd_salmonpink.png",
    "wistful": f"{OUTPUT_FOLDER}/dvd_wistful.png",
    "darkred": f"{OUTPUT_FOLDER}/dvd_darkred.png",
    "springgreen": f"{OUTPUT_FOLDER}/dvd_springgreen.png",
    "purple": f"{OUTPUT_FOLDER}/dvd_purple.png",
}

# Configuration for size and speed of the logo. Adjust these values.
TARGET_LOGO_WIDTH = 400
TARGET_LOGO_HEIGHT = 200
INITIAL_DX = 3
INITIAL_DY = 3
ANIMATION_INTERVAL_MS = 10


# A PyQt5 application that displays a bouncing DVD logo image with a transparent background.
# The logo image changes (to a different color version) when it hits the edges of the window.
class DVDLogoApp(QWidget):
    def __init__(self, screen_index=0): # Added screen_index parameter, default to 0 (primary) but you will have to run python main.py (0 or 1) for which monitor
        super().__init__()
        self.setWindowTitle("DVD Logo Bouncing")

        # Set window flags for a frameless, transparent window that stays on top
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Load all colored pixmaps and scale them to the TARGET_LOGO_WIDTH/HEIGHT
        self.pixmaps = []
        for color_name in color_files:
            file_path = color_files[color_name]
            try:
                pixmap = QPixmap(file_path)
                if pixmap.isNull():
                    print(f"Warning: Could not load image from {file_path}. Is the path correct and file accessible?")
                    # Fallback to a placeholder if image fails to load
                    placeholder_pixmap = QPixmap(TARGET_LOGO_WIDTH, TARGET_LOGO_HEIGHT)
                    placeholder_pixmap.fill(QColor(100, 100, 100, 150)) # Semi-transparent grey
                    painter = QPainter(placeholder_pixmap)
                    painter.setPen(QPen(QColor(255, 255, 255)))
                    font = QFont("Arial", 12, QFont.Bold) # Smaller font for placeholder
                    painter.setFont(font)
                    painter.drawText(placeholder_pixmap.rect(), Qt.AlignCenter, "NO IMG")
                    painter.end()
                    self.pixmaps.append(placeholder_pixmap)
                else:
                    # Scale the loaded pixmap to the desired target size
                    scaled_pixmap = pixmap.scaled(TARGET_LOGO_WIDTH, TARGET_LOGO_HEIGHT,
                                                  Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.pixmaps.append(scaled_pixmap)
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
                # Fallback to a placeholder if an exception occurs during loading
                placeholder_pixmap = QPixmap(TARGET_LOGO_WIDTH, TARGET_LOGO_HEIGHT)
                placeholder_pixmap.fill(QColor(100, 100, 100, 150))
                painter = QPainter(placeholder_pixmap)
                painter.setPen(QPen(QColor(255, 255, 255)))
                font = QFont("Arial", 12, QFont.Bold)
                painter.setFont(font)
                painter.drawText(placeholder_pixmap.rect(), Qt.AlignCenter, "NO IMG")
                painter.end()
                self.pixmaps.append(placeholder_pixmap)

        if not self.pixmaps:
            print("Error: No images loaded. Exiting.")
            sys.exit(1)

        # Use the target dimensions for logo width and height
        self.logo_width = TARGET_LOGO_WIDTH
        self.logo_height = TARGET_LOGO_HEIGHT

        # Set the initial window size to match the logo size
        self.setGeometry(100, 100, self.logo_width, self.logo_height)

        # Monitor Selection Logic
        desktop = QApplication.desktop()
        num_screens = desktop.screenCount()

        if not (0 <= screen_index < num_screens):
            print(f"Warning: Screen index {screen_index} is out of bounds. Using primary screen (0).")
            screen_index = 0

        self.screen_rect = desktop.screenGeometry(screen_index)
        print(f"Displaying on screen {screen_index}: {self.screen_rect.width()}x{self.screen_rect.height()} at ({self.screen_rect.x()}, {self.screen_rect.y()})")


        # Initialize the position of the logo randomly within the selected screen's dimensions
        self.logo_x = random.randint(0, self.screen_rect.width() - self.logo_width)
        self.logo_y = random.randint(0, self.screen_rect.height() - self.logo_height)

        # Define the velocity (speed and direction) of the logo using new config
        self.logo_dx = INITIAL_DX
        self.logo_dy = INITIAL_DY

        self.current_pixmap_index = 0
        self.current_pixmap = self.pixmaps[self.current_pixmap_index]

        # Set up a QTimer to trigger the animation using new config
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(ANIMATION_INTERVAL_MS)

        # Move the window to the initial random position on the selected screen
        # Add the screen's top-left coordinates to the logo's random position
        self.move(self.screen_rect.x() + self.logo_x, self.screen_rect.y() + self.logo_y)

    def paintEvent(self, event):
        """
        This method is called whenever the widget needs to be recoloured.
        It handles drawing the current DVD logo image.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw the current pixmap at (0,0) relative to the window's top-left corner
        # The window itself is moving, so the image is always at (0,0) within the window.
        painter.drawPixmap(0, 0, self.current_pixmap)

    def animate(self):
        """
        Updates the position of the DVD logo window and handles collisions with screen edges.
        Changes the logo image upon collision.
        """
        # Use the dimensions of the selected screen for collision detection
        screen_width = self.screen_rect.width()
        screen_height = self.screen_rect.height()

        # Update logo position relative to the selected screen's top-left corner
        self.logo_x += self.logo_dx
        self.logo_y += self.logo_dy

        bounced = False
        # Collision detection with horizontal edges (left/right) of the selected screen
        if self.logo_x + self.logo_width > screen_width or self.logo_x < 0:
            self.logo_dx = -self.logo_dx
            bounced = True

        # Collision detection with vertical edges (top/bottom) of the selected screen
        if self.logo_y + self.logo_height > screen_height or self.logo_y < 0:
            self.logo_dy = -self.logo_dy
            bounced = True

        if bounced:
            self.change_logo_image()

        # Ensure the logo stays strictly within bounds, correcting any overshoot
        if self.logo_x + self.logo_width > screen_width:
            self.logo_x = screen_width - self.logo_width
        if self.logo_x < 0:
            self.logo_x = 0
        if self.logo_y + self.logo_height > screen_height:
            self.logo_y = screen_height - self.logo_height
        if self.logo_y < 0:
            self.logo_y = 0

        # Move the entire window to the new position, offset by the selected screen's top-left coordinates
        self.move(self.screen_rect.x() + self.logo_x, self.screen_rect.y() + self.logo_y)
        # Request a repaint of the widget to show the logo (though image doesn't change unless bounced)
        self.update()

    def change_logo_image(self):
        """
        Cycles to the next logo image in the predefined list, but randomly.
        Ensures the new color is different from the current one.
        """
        # Get the total number of available pixmaps (colors)
        num_pixmaps = len(self.pixmaps)
        if num_pixmaps <= 1: # If there's only one or no pixmaps, no change is possible
            return

        # Generate a new random index
        new_index = random.randrange(num_pixmaps)

        # Keep generating a new index until it's different from the current one
        while new_index == self.current_pixmap_index:
            new_index = random.randrange(num_pixmaps)

        # Update to the new random index
        self.current_pixmap_index = new_index
        self.current_pixmap = self.pixmaps[self.current_pixmap_index]
        self.update() # Request repaint to show the new image

# Standard boilerplate for running a PyQt5 application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    screen_to_display = 0 # Default to primary screen (index 0)

    if len(sys.argv) > 1:
        try:
            screen_to_display = int(sys.argv[1])
        except ValueError:
            print(f"Invalid screen index provided: '{sys.argv[1]}'. Using default screen (0).")
            print("Usage: python your_script_name.py [screen_index]")
            print("  screen_index: Optional. An integer representing the monitor to display on (e.g., 0 for primary, 1 for secondary).")
    else:
        print("No screen index provided. Using primary screen (0).")
        print("To specify a screen, run: python your_script_name.py [screen_index]")
        print("  Example: python your_script_name.py 1 (to display on the second monitor)")
        print(f"Currently detected screens: {QApplication.desktop().screenCount()}")


    ex = DVDLogoApp(screen_index=screen_to_display) # Pass the selected screen index to the app
    ex.show()
    sys.exit(app.exec_())