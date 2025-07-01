# Bouncing DVD Logo

This is a Python application that displays a classic DVD logo bouncing around your screen. The logo changes color randomly whenever it hits the edges of the screen, and the application window itself is transparent, allowing the logo to float seamlessly over your desktop.

Note: this has not been tested on MacOS.

## Features

* **Bouncing Animation:** The DVD logo moves continuously across the screen.
* **Random Color Change:** Upon hitting any screen edge, the logo's color changes to a random one from a predefined set of PNG images.
* **Transparent Background:** The application window is frameless and transparent, giving the illusion of the logo floating directly on your desktop.
* **Multi-Monitor Support:** You can specify which monitor the logo should appear on.
* **Customizable Size and Speed:** Easily adjust the logo's size and animation speed.

## Setup and Installation

1.  **Clone the Repository:**
    If you've uploaded this to GitHub, clone it:
    ```bash
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
    cd YOUR_REPO_NAME
    ```
    Otherwise, ensure all project files (`dvd_logo_pyqt.py`, `pngconverter.py`, `DVD_logo.svg`, and the `generated_pngs` folder if it exists) are in the same directory.

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv .venv
    ```

3.  **Activate the Virtual Environment:**
    * **Windows:**
        ```bash
        .venv\Scripts\activate
        ```
    * **macOS/Linux:**
        ```bash
        source .venv/bin/activate
        ```

4.  **Install Dependencies:**
    ```bash
    pip install PyQt5 Pillow
    ```
    (Pillow is for `pngconverter.py` if you use it, PyQt5 is for the main app).

5.  **Generate PNGs:**
    This project uses pre-generated PNG images of the DVD logo in different colors. If you don't have the `generated_pngs` folder or want to regenerate them:
    * Ensure you have [Inkscape](https://inkscape.org/) installed and its executable path is correctly set in `pngconverter.py` (`INKSCAPE_CMD`).
    * Run the converter script:
        ```bash
        python pngconverter.py
        ```
    This will create the `generated_pngs` directory containing `dvd_red.png`, `dvd_blue.png`, etc.

## How to Run

1.  **Activate your virtual environment** (if not already active).
2.  Run the main application:
    ```bash
    python dvd_logo_pyqt.py
    ```

### Running on a Specific Monitor

If you have multiple monitors, you can specify which one to display the logo on by providing its index as a command-line argument:

* To display on the **primary monitor** (default):
    ```bash
    python dvd_logo_pyqt.py
    ```
* To display on the **second monitor** (index `1`):
    ```bash
    python dvd_logo_pyqt.py 1
    ```
* And so on for other monitors (indices `2`, `3`, etc.). The script will print the number of detected screens.

## Customization

You can easily adjust the logo's size and speed by modifying the configuration variables at the top of `dvd_logo_pyqt.py`:

* **`TARGET_LOGO_WIDTH` & `TARGET_LOGO_HEIGHT`**: Change these values to make the logo larger or smaller.
* **`INITIAL_DX` & `INITIAL_DY`**: Increase these values to make the logo move faster horizontally and vertically.
* **`ANIMATION_INTERVAL_MS`**: Decrease this value (in milliseconds) to make the overall animation faster (e.g., `5` for very fast).

Enjoy your bouncing DVD logo!
