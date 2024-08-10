import time
import board
import neopixel
import json
import logging
import shared_state

# Load configuration from config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Configure logging
logging.basicConfig(level=config.get('LOG_LEVEL', logging.INFO), format='%(asctime)s - %(levelname)s - %(message)s')


LED_COUNT = config.get('LED_COUNT', 56)
LED_PIN = getattr(board, config.get('LED_PIN', 'D18'))
LED_BRIGHTNESS = 255

# Create NeoPixel object with appropriate configuration.
pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness=LED_BRIGHTNESS, auto_write=False)

def set_color(color):
    shared_state.stop_animation = False
    logging.debug(f"Setting color to: {color}")
    pixels.fill(color)
    pixels.show()

def clear_strip():
    shared_state.stop_animation = False
    logging.debug("Clearing LED strip")
    pixels.fill((0, 0, 0))
    pixels.show()

def color_wipe(color, wait_ms=50):
    shared_state.stop_animation = False
    wait_ms = int(wait_ms)  # Convert wait_ms to an integer
    logging.debug(f"Starting color_wipe with color: {color} and wait_ms: {wait_ms}")
    for i in range(LED_COUNT):
        if shared_state.stop_animation:
            logging.debug("Stopping color_wipe")
            break
        pixels[i] = color
        pixels.show()
        time.sleep(wait_ms / 1000.0)
    logging.debug("Finished color_wipe")

def theater_chase(color, wait_ms=50, iterations=10):
    shared_state.stop_animation = False
    wait_ms = int(wait_ms)  # Convert wait_ms to an integer
    iterations = int(iterations)  # Convert iterations to an integer
    logging.debug(f"Starting theater_chase with color: {color}, wait_ms: {wait_ms}, iterations: {iterations}")
    iteration_count = 0
    while iterations == -1 or iteration_count < iterations:
        if shared_state.stop_animation:
            logging.debug("Stopping theater_chase")
            break
        for q in range(3):
            for i in range(0, LED_COUNT, 3):
                if i + q < LED_COUNT:
                    if shared_state.stop_animation:
                        logging.debug("Stopping theater_chase")
                        break
                    pixels[i+q] = color
            pixels.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, LED_COUNT, 3):
                if i + q < LED_COUNT:
                    if shared_state.stop_animation:
                        logging.debug("Stopping theater_chase")
                        break
                    pixels[i+q] = (0, 0, 0)
        iteration_count += 1
    logging.debug("Finished theater_chase")

def scaled_color(color, intensity):
    return tuple(int(c * (intensity / 255)) for c in color)

def pulse_from_center(color, wait_ms=50, iterations=10):
    shared_state.stop_animation = False
    wait_ms = int(wait_ms)  # Convert to integer
    iterations = int(iterations)  # Convert to integer
    logging.debug(f"Starting pulse_from_center with color: {color}, wait_ms: {wait_ms}, iterations: {iterations}")

    middle = LED_COUNT // 2
    iteration_count = 0
    while iterations == -1 or iteration_count < iterations:
        if shared_state.stop_animation:
            logging.debug("Stopping pulse_from_center")
            break

        # Fade in
        for intensity in range(0, 256, 5):  # Increase intensity
            if shared_state.stop_animation:
                logging.debug("Stopping pulse_from_center during fade in")
                break
            scaled_color = tuple(int(c * (intensity / 255)) for c in color)
            for offset in range(middle + 1):
                if middle + offset < LED_COUNT:
                    pixels[middle + offset] = scaled_color
                if middle - offset >= 0:
                    pixels[middle - offset] = scaled_color
            pixels.show()
            time.sleep(wait_ms / 1000.0)

        # Fade out
        for intensity in range(255, -1, -5):  # Decrease intensity
            if shared_state.stop_animation:
                logging.debug("Stopping pulse_from_center during fade out")
                break
            scaled_color = tuple(int(c * (intensity / 255)) for c in color)
            for offset in range(middle + 1):
                if middle + offset < LED_COUNT:
                    pixels[middle + offset] = scaled_color
                if middle - offset >= 0:
                    pixels[middle - offset] = scaled_color
            pixels.show()
            time.sleep(wait_ms / 1000.0)

        iteration_count += 1
    logging.debug("Finished pulse_from_center")

def rainbow_cycle(wait_ms=20, iterations=5):
    shared_state.stop_animation = False
    wait_ms = int(wait_ms)  # Convert wait_ms to an integer
    iterations = int(iterations)  # Convert iterations to an integer
    logging.debug(f"Starting rainbow_cycle with wait_ms: {wait_ms}, iterations: {iterations}")
    iteration_count = 0
    while iterations == -1 or iteration_count < iterations:
        if shared_state.stop_animation:
            logging.debug("Stopping rainbow_cycle")
            break
        for j in range(256):
            if shared_state.stop_animation:
                logging.debug("Stopping rainbow_cycle")
                break
            for i in range(LED_COUNT):
                pixel_index = (i * 256 // LED_COUNT) + j
                pixels[i] = wheel(pixel_index & 255)
            pixels.show()
            time.sleep(wait_ms / 1000.0)
        iteration_count += 1
    logging.debug("Finished rainbow_cycle")

def wheel(pos):
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)