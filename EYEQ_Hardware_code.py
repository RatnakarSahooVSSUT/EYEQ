# -- coding: utf-8 --
"""
EYQ merged script (threaded & camera-stable) with Push Button for IOP
- Ultrasonic IOP (HC-SR04) with quadratic calibration [NO LED/BUZZER for IOP]
- Blink detection (Picamera2 + Haar cascades)
- Blue-light level (TCS34725) with original LED + BUZZER patterns
- OLED SH1106 dashboard
- Push button on GPIO26: IOP is only measured on button press,
  held for 20 seconds or until next press, then resets to 0/--

Raspberry Pi 4B libs:
  pip install picamera2 luma.oled pillow opencv-python adafruit-circuitpython-tcs34725 RPi.GPIO
  sudo apt install -y python3-opencv
"""

import sys, io, time, threading
import cv2
import board, busio
import RPi.GPIO as GPIO
from datetime import datetime, timedelta

# =============== OLED ===============
from luma.core.interface.serial import i2c as luma_i2c
from luma.oled.device import sh1106
from PIL import Image, ImageDraw, ImageFont

# =============== Camera ===============
from picamera2 import Picamera2

# =============== Blue-light sensor ===============
import adafruit_tcs34725

# ---------- Robust Unicode stdout ----------
try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace", newline="\n")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace", newline="\n")
    else:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", newline="\n")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace", newline="\n")
except Exception:
    pass

# ================= GPIO =================
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

LED_PIN = 17
BUZZER_PIN = 27  # Active LOW
BUTTON_PIN = 26  # Push button for IOP trigger

GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.output(LED_PIN, False)
GPIO.output(BUZZER_PIN, True)  # OFF

# ---- HC-SR04 pins ----
TRIG = 23
ECHO = 24
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# ---- IOP LEDs ----
LED_IOP1 = 20  # "one LED" for Low
LED_IOP2 = 21  # second LED; both on for High
GPIO.setup(LED_IOP1, GPIO.OUT)
GPIO.setup(LED_IOP2, GPIO.OUT)
GPIO.output(LED_IOP1, False)
GPIO.output(LED_IOP2, False)

# ================= OLED Setup =================
serial = luma_i2c(port=1, address=0x3C)
oled = sh1106(serial)
oled_font = ImageFont.load_default()
LINE_H = 10

def oled_message(lines):
    """Display multiple short lines on SH1106."""
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)
    y = 0
    for line in lines[:6]:
        draw.text((0, y), line, font=oled_font, fill=255)
        y += LINE_H
    oled.display(image)

oled_message(["Booting...", "Camera warming"])

# ================= Camera Setup =================
picam2 = Picamera2()
picam2.preview_configuration.main.size = (320, 240)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()

# ================= Haar Cascades =================
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

# ================= Blue Light Sensor =================
i2c_bus = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_tcs34725.TCS34725(i2c_bus)
sensor.integration_time = 100
sensor.gain = 4

# ================= IOP Calibration =================
def distance_to_iop(distance_cm: float) -> float:
    a, b, c = 0.212, -6.54, 55.8
    iop = a * (distance_cm ** 2) + b * distance_cm + c
    return round(iop, 2)

def measure_distance(timeout: float = 0.02):
    GPIO.output(TRIG, False)
    time.sleep(0.000005)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    t0 = time.time()
    pulse_start = None
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        if pulse_start - t0 > timeout:
            return None

    t1 = time.time()
    pulse_end = None
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        if pulse_end - t1 > timeout:
            return None
    pulse_duration = (pulse_end or t1) - (pulse_start or t0)
    distance_cm = pulse_duration * 17150.0
    return round(distance_cm, 2)

def read_iop(samples: int = 5, delay: float = 0.06):
    vals = []
    for _ in range(samples):
        d = measure_distance()
        if d is not None:
            vals.append(d)
        time.sleep(delay)

    if not vals:
        return None, None, "No Echo"

    avg_cm = sum(vals) / len(vals)
    iop_val = distance_to_iop(avg_cm)

    if iop_val > 20:
        status = "High IOP"
    elif iop_val < 9:
        status = "Low IOP"
    else:
        status = "Normal IOP"

    return round(avg_cm, 2), iop_val, status

# ================= Shared State =================
blink_count = 0
eye_closed = False

iop_value = None
iop_status = "--"
iop_avg_cm = None
iop_last_time = 0  # last time button pressed/reading taken

blue_lux = 0.0
blue_level = "Safe"

start_time = time.time()
stop_event = threading.Event()
state_lock = threading.Lock()

# ================= Original Alert Logic (unchanged) =================
def alert(level: str):
    if level == "Safe":
        GPIO.output(LED_PIN, False)
        GPIO.output(BUZZER_PIN, True)
    elif level == "Moderate":
        for _ in range(3):
            GPIO.output(LED_PIN, True)
            GPIO.output(BUZZER_PIN, False)
            time.sleep(0.3)
            GPIO.output(LED_PIN, False)
            GPIO.output(BUZZER_PIN, True)
            time.sleep(0.3)
    elif level == "High":
        for _ in range(5):
            GPIO.output(LED_PIN, True)
            GPIO.output(BUZZER_PIN, False)
            time.sleep(0.3)
            GPIO.output(LED_PIN, False)
            GPIO.output(BUZZER_PIN, True)
            time.sleep(0.3)
    elif level == "Danger":
        for _ in range(10):
            GPIO.output(LED_PIN, True)
            GPIO.output(BUZZER_PIN, False)
            time.sleep(0.2)
            GPIO.output(LED_PIN, False)
            GPIO.output(BUZZER_PIN, True)
            time.sleep(0.2)

# ================= Worker Threads =================
def blue_light_worker():
    global blue_lux, blue_level
    while not stop_event.is_set():
        try:
            r, g, b, c = sensor.color_raw
            if c == 0:
                c = 1
            lux = 0.136 * r + 1.0 * g + 0.444 * b
            blx = (b / c) * lux * 2.5

            if blx < 400:
                lvl = "Safe"
            elif blx < 450:
                lvl = "Moderate"
            elif blx < 500:
                lvl = "High"
            else:
                lvl = "Danger"

            with state_lock:
                blue_lux = blx
                blue_level = lvl

            alert(lvl)
            time.sleep(0.1)

        except Exception as e:
            print(f"[BlueLight] Error: {e}")
            time.sleep(0.2)
def iop_worker():
    """IOP measured only when button pressed, held 20s max."""
    global iop_value, iop_status, iop_avg_cm, iop_last_time
    while not stop_event.is_set():
        now = time.time()
        if GPIO.input(BUTTON_PIN) == GPIO.HIGH:
            avg_cm, iop_val, stat = read_iop(samples=5, delay=0.06)
            with state_lock:
                iop_avg_cm = avg_cm
                iop_value = iop_val
                iop_status = stat
                iop_last_time = now
            if iop_val is not None:
                print(f"[IOP] Button Press: {avg_cm:.2f} cm | {iop_val:.2f} mmHg ({stat})")
                # --- IOP LED logic (GPIO20/21) ---
                if stat == "High IOP":
                    GPIO.output(LED_IOP1, True)
                    GPIO.output(LED_IOP2, True)
                elif stat == "Low IOP":
                    GPIO.output(LED_IOP1, True)
                    GPIO.output(LED_IOP2, False)
                else:  # Normal IOP
                    GPIO.output(LED_IOP1, False)
                    GPIO.output(LED_IOP2, False)
            else:
                print("[IOP] Button Press: No valid echo")

        # Reset to zero if >20s without new press
        if iop_last_time and (now - iop_last_time > 20):
            with state_lock:
                iop_value = None
                iop_status = "--"
                iop_avg_cm = None
                iop_last_time = 0
            print("[IOP] Timeout: reset to --")

        time.sleep(0.05)

def oled_worker():
    while not stop_event.is_set():
        with state_lock:
            iop_str = f"IOP: {iop_value:.2f} mmHg" if iop_value is not None else "IOP: --"
            status_str = f"Status: {iop_status}"
            blx = blue_lux
            lvl = blue_level
            blinks = blink_count

        current_time = datetime.now().strftime("%H:%M:%S")
        elapsed = str(timedelta(seconds=int(time.time() - start_time)))

        lines = [
            f"Time:   {current_time}",
            f"Screen: {elapsed}",
            f"Blinks: {blinks}",
            f"Blue: {blx:.1f} ({lvl})",
            iop_str,
            status_str,
        ]
        try:
            oled_message(lines)
        except Exception as e:
            print(f"[OLED] Error: {e}")
        time.sleep(0.5)

# Start background threads
threads = [
    threading.Thread(target=blue_light_worker, daemon=True),
    threading.Thread(target=iop_worker, daemon=True),
    threading.Thread(target=oled_worker, daemon=True),
]
for t in threads:
    t.start()

# ================= MAIN LOOP (Camera only) =================
try:
    while True:
        frame = picam2.capture_array()
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            face_gray = gray[y:y + h, x:x + w]
            face_color = frame[y:y + h, x:x + w]

            eyes = eye_cascade.detectMultiScale(face_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(face_color, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 1)

            if len(eyes) == 0 and not eye_closed:
                eye_closed = True
            elif len(eyes) > 0 and eye_closed:
                with state_lock:
                    blink_count += 1
                eye_closed = False

        cv2.imshow("EYQ - Blink Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        time.sleep(0.01)

except KeyboardInterrupt:
    pass
finally:
    stop_event.set()
    try:
        picam2.stop()
    except Exception:
        pass
    cv2.destroyAllWindows()
    GPIO.output(LED_PIN, False)
    GPIO.output(BUZZER_PIN, True)
    GPIO.output(LED_IOP1, False)
    GPIO.output(LED_IOP2, False)
    try:
        oled_message(["Shutting down", "Bye!"])
    except Exception:
        pass
    GPIO.cleanup()