# Garbage Collector
# import the necessary packages
import os
import requests
import json
import pigpio
import RPi.GPIO as GPIO
import time
from gpiozero import Button, DistanceSensor
from picamera import PiCamera
from time import sleep
from signal import pause
from PIL import Image
from subparser import Garbage_parser

in1 = 21
in2 = 20
in3 = 24
in4 = 23

# careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move
step_sleep = 0.002

step_count = 4096  # 5.625*(1/64) per step, 4096 steps is 360°

direction = False  # True for clockwise, False for counter-clockwise
# defining stepper motor sequence (found in documentation http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
step_sequence = [
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
]

horizontal_servo_pinout = 13
# vertical_servo_pinout = 17
IR_Pinout = 12

ZERO_DEGREE_POSITION = 500
NINETY_DEGREE_POSITION = 1500
FULL_RANGE_POSITION = 2500
motor_pins = [in1, in2, in3, in4]
camera = PiCamera()
pi = pigpio.pi()
button = Button(2)
# ultrasonic_sensor = DistanceSensor(23,24)
pi.set_mode(horizontal_servo_pinout, pigpio.OUTPUT)
pi.set_PWM_frequency(horizontal_servo_pinout, 50)

foldername = "./images"
# start the camera
camera.rotation = 180
image_number = 0

# horizontal_servo = AngularServo(13,min_pulse_width=0.0006,max_pulse_width=0.0023)
# rotational_servo = Servo(17)

for files in os.listdir("./images"):
        os.remove(os.path.join("images",files))

def _upload_image(payload):
    data = payload
    with open(data, "rb") as filedata:
        filedata = filedata.read()
        response = requests.post(
            "http://3.88.108.90/analyze", files=dict(file=filedata)
        )
        if response.status_code != 200:  # pragma: no cover
            print(f"failed status code {response.status_code}: {response.content}")
    return json.loads(response.content.decode("utf-8"))


def stop_camera():
    camera.stop_preview()
    # exit the program
    exit()

def _ultrasonic_distance():
    # set Trigger to HIGH
    _set_gpios("ultra")
    GPIO_TRIGGER = 17
    GPIO_ECHO = 26
    # set Trigger after 0.01ms to LOW
    sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
def _set_gpios(sensor):
    if sensor == "ultra":
        GPIO.setmode(GPIO.BCM)
            #set GPIO Pins
        GPIO_TRIGGER = 17
        GPIO_ECHO = 26
        #set GPIO direction (IN / OUT)
        GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(GPIO_ECHO, GPIO.IN)
    elif sensor == "stepper":
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(in1, GPIO.OUT)
        GPIO.setup(in2, GPIO.OUT)
        GPIO.setup(in3, GPIO.OUT)
        GPIO.setup(in4, GPIO.OUT)
        
    
def cleanup():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    # GPIO.cleanup()

def stepper_motor_rotation(direction,steps):
    _set_gpios("stepper")
    motor_step_counter = 0
    for i in range(steps):
        print(i)
        for pin in range(0, len(motor_pins)):
            GPIO.output(motor_pins[pin], step_sequence[motor_step_counter][pin])
        if direction == True:
            motor_step_counter = (motor_step_counter - 1) % 8
        elif direction == False:
            motor_step_counter = (motor_step_counter + 1) % 8
        else:  # defensive programming
            print("uh oh... direction should *always* be either True or False")
            cleanup()
            exit(1)
        sleep(step_sleep)
    cleanup()

def _infra_sensor():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IR_Pinout, GPIO.IN)

def _pour():
    pi.set_servo_pulsewidth(horizontal_servo_pinout, FULL_RANGE_POSITION)
    sleep(1)
    pi.set_servo_pulsewidth(horizontal_servo_pinout, ZERO_DEGREE_POSITION)
def _motor_rotation(results):
    result = results["result"]
    print(f"Item Is a: {result}")

    if result == "paper":
        if GPIO.input(IR_Pinout):
            return print("Paper bin is full")
        _pour()
        
    elif result == "plastic":
        stepper_motor_rotation(False,820)
        _pour()
        stepper_motor_rotation(True,820)
    elif result == "glass":
        stepper_motor_rotation(False,1639)
        _pour()
        stepper_motor_rotation(True,1639)
    elif result == "metal":
        stepper_motor_rotation(False,2458)
        _pour()
        stepper_motor_rotation(True,2458)
    else:
        print("Unknown Results")


# take photo when motion is detected
def motion_detected():
    if len(os.listdir("images")) > 1:
        take_photo()


def take_photo():
    global image_number
    image_number += 1
    os.makedirs("images", exist_ok=True)
    image_name = os.path.join(foldername, "image_%s.jpg" % image_number)
    camera.capture(image_name)
    im = Image.open(image_name)
    im.resize((160, 300), Image.ANTIALIAS)
    im.save(image_name)
    print("A photo has been taken")
    results = _upload_image(image_name)
    _motor_rotation(results)
    # _motor_rotation(image_name)

if __name__ == "__main__":
    garbage_parser = Garbage_parser().parser
    args = garbage_parser.parse_args()
    _infra_sensor() 
    if args.button == False:
        try:
            while True:
                dist = _ultrasonic_distance()
                print ("Object detected at %.1f centimeters" % dist)
                if int(dist) <= 50:
                    take_photo
                sleep(3)
                
            # Reset by pressing CTRL + C
        except KeyboardInterrupt:
            print("Measurement stopped by User")
            GPIO.cleanup()


    button.when_pressed = take_photo
    pause()