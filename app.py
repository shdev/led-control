from flask import Flask, request, jsonify, send_from_directory
from threading import Thread, Event
import signal
import sys
import logging
import shared_state
from led_control import set_color, clear_strip, color_wipe, pulse_from_center, theater_chase, rainbow_cycle, config


app = Flask(__name__)

# Global thread controller
current_thread = None
stop_event = Event()


current_animation = "CLEAR"

def stop_current_animation():
    global current_thread
    if current_thread and current_thread.is_alive():
        logging.info("Stopping current animation")
        shared_state.stop_animation = True
        current_thread.join()
        shared_state.stop_animation = False
        logging.info("Current animation stopped")

def run_animation(name, animation_func, *args):
    global current_thread
    stop_current_animation()
    logging.info(f"Starting new animation: {animation_func.__name__}")
    current_thread = Thread(target=animation_func, args=args)
    current_animation = name
    current_thread.start()

@app.route('/set_color', methods=['POST'])
def set_color_route():
    data = request.json
    color = data.get('color', [255, 255, 255])
    logging.info(f"Setting color to: {color}")
    run_animation("SET_COLOR", set_color, tuple(color))
    return jsonify({'status': 'success'})

@app.route('/clear', methods=['POST'])
def clear_route():
    logging.info("Clearing LED strip")
    run_animation("CLEAR", color_wipe, tuple([0, 0, 0]), 100)
    return jsonify({'status': 'success'})

@app.route('/color_wipe', methods=['POST'])
def color_wipe_route():
    data = request.json
    color = data.get('color', [0, 0, 0])
    wait_ms = int(data.get('wait_ms', 50))  # Convert to integer
    logging.info(f"Starting color_wipe with color: {color} and wait_ms: {wait_ms}")
    run_animation("COLOR_WIPE", color_wipe, tuple(color), wait_ms)
    return jsonify({'status': 'success'})

@app.route('/theater_chase', methods=['POST'])
def theater_chase_route():
    data = request.json
    color = data.get('color', [255, 255, 255])
    wait_ms = int(data.get('wait_ms', 50))  # Convert to integer
    iterations = int(data.get('iterations', 10))  # Convert to integer
    logging.info(f"Starting theater_chase with color: {color}, wait_ms: {wait_ms}, iterations: {iterations}")
    run_animation("THEATER_CHASE", theater_chase, tuple(color), wait_ms, iterations)
    return jsonify({'status': 'success'})

@app.route('/rainbow_cycle', methods=['POST'])
def rainbow_cycle_route():
    data = request.json
    wait_ms = int(data.get('wait_ms', 20))  # Convert to integer
    iterations = int(data.get('iterations', 5))  # Convert to integer
    logging.info(f"Starting rainbow_cycle with wait_ms: {wait_ms}, iterations: {iterations}")
    run_animation("RAINBOW_CYCLE", rainbow_cycle, wait_ms, iterations)
    return jsonify({'status': 'success'})

@app.route('/pulse_from_center', methods=['POST'])
def pulse_from_center_route():
    data = request.json
    color = data.get('color', [0, 0, 0])
    wait_ms = int(data.get('wait_ms', 50))  # Convert to integer
    iterations = int(data.get('iterations', 10))  # Convert to integer
    logging.info(f"Starting pulse_from_center with color: {color}, wait_ms: {wait_ms}, iterations: {iterations}")
    run_animation("PULSE_FROM_CENTER", pulse_from_center, tuple(color), wait_ms, iterations)
    return jsonify({'status': 'success'})

@app.route('/current_animation', methods=['GET'])
def current_animation_route():
    return jsonify({'name': current_animation})


@app.route('/')
def serve_index():
    return send_from_directory('content', 'index.html')

@app.route('/<path:filename>', methods=['GET'])
def serve_static(filename):
    try:
        return send_from_directory('content', filename)
    except Exception as e:
        logging.error(f"Error serving file {filename}: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 404

def handle_exit(sig, frame):
    logging.info("Received exit signal")
    stop_current_animation()
    clear_strip()
    logging.info("LED strip cleared, exiting now")
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)

if __name__ == '__main__':
    host = config.get('HOST', '0.0.0.0')
    port = config.get('PORT', 5000)
    logging.info(f"Starting server on {host}:{port}")
    app.run(host=host, port=port, threaded=True)