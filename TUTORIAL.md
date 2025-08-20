### User Guide: MicroGreenMicroWave Control Software

This guide explains how to use the new features for controlling the 16x16 NeoPixel matrix, including the pre-made animations and the simulation mode for development.

---

#### **1. Using the Pre-made LED Animations**

The new control software includes a library of pre-made animations to easily create dynamic lighting effects on your 16x16 NeoPixel matrix. These animations are provided by the `adafruit-circuitpython-led-animation` library.

**How to access and use the animations:**

1.  **Navigate to the NeoPixel Control Tab:** In the main application window, you will see a series of tabs. Click on the tab labeled **"NeoPixel Control"**.

2.  **Select an Animation:** In this tab, you will find a dropdown menu. Click on it to see a list of available animations, such as:
    *   `Solid`
    *   `Blink`
    *   `ColorCycle`
    *   `Chase`
    *   `Comet`
    *   `Pulse`
    *   `Rainbow`
    *   `Sparkle`

3.  **Run the Animation:** After selecting your desired animation from the dropdown, click the **"Run Animation"** button. The selected animation will start playing on the LED matrix.

**Note:** When an animation is running, the manual pixel editor grid will not update in real-time with the animation. To create a custom static pattern again, you can simply start clicking on the pixels on the grid, which will stop the animation.

---

#### **2. Understanding the Simulation Mode**

To allow for development and testing without needing the physical Raspberry Pi and LED matrix connected, the software includes a **simulation mode**.

**What it is:**
When simulation mode is active, the software does not try to send commands to the hardware. Instead, it prints messages to the console (the terminal where you run the application) describing what it *would* have done.

**How it works:**

*   **Enabled by Default:** Currently, simulation mode is **enabled by default** to prevent errors when running in an environment like Gitpod or on a standard computer.
*   **Console Output:** When you interact with the NeoPixel controls (e.g., clicking a pixel, running an animation), you will see messages printed in your terminal, like:
    ```
    SIM: Setting pixel (5, 10) to (255, 0, 0)
    SIM: Running animation 'Rainbow'
    ```
*   **Visual Feedback:** The GUI is still fully interactive. The 16x16 grid of buttons will change color as you click on them, and you can still save and load your patterns. The simulation only affects the final output to the hardware.

---

#### **3. For Developers: Disabling Simulation Mode**

If you are running this software on a Raspberry Pi with the 16x16 NeoPixel matrix correctly wired, you can disable simulation mode to control the actual hardware.

**How to disable simulation mode:**

1.  Open the file: `_python/Main.py`
2.  Find the following line in the `__init__` method of the `MainWindow` class (around line 467):
    ```python
    self.neopixel_control = NeoPixelControl(simulation=True)
    ```
3.  Change `simulation=True` to `simulation=False`:
    ```python
    self.neopixel_control = NeoPixelControl(simulation=False)
    ```
4.  Save the file and run the application. The software will now attempt to send commands to the NeoPixel matrix via the GPIO pins.
