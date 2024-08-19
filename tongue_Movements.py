import time
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

# Setup the I2C bus and PCA9685
i2c_bus = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c_bus)
pca.frequency = 50

# Initialize the servos on the specified channels
base_Top = servo.Servo(pca.channels[7], min_pulse=500, max_pulse=2500)
base_Bottom = servo.Servo(pca.channels[3], min_pulse=500, max_pulse=2500)
tip_Top = servo.Servo(pca.channels[0], min_pulse=500, max_pulse=2500)
tip_Bottom = servo.Servo(pca.channels[8], min_pulse=500, max_pulse=2500)

def tongue_BaseUp(main_angle):
    """Move base_Top upwards and adjust base_Bottom to maintain tension."""
    if 90 <= main_angle <= 150:  # Validate angle for base_Top
        base_Top.angle = main_angle
        # Calculate a reduced movement for base_Bottom to maintain tension
        tension_angle = 90 + (main_angle - 90) * 0.3  # Adjust the multiplier as needed
        base_Bottom.angle = tension_angle
        print(f"base_Top moved to {main_angle} degrees.")
        print(f"base_Bottom adjusted to {tension_angle} degrees to maintain tension.")
    else:
        print("Invalid angle for base_Top. Please enter a value between 90 and 150 degrees.")
    time.sleep(1)  # Pause to observe the servo positions

def tongue_BaseDown(main_angle):
    """Move base_Bottom downwards and adjust base_Top to maintain tension."""
    if 30 <= main_angle <= 90:  # Validate angle for base_Bottom
        base_Bottom.angle = main_angle
        # Calculate a reduced movement for base_Top to maintain tension
        tension_angle = 90 + (main_angle - 90) * 0.3  # Adjust the multiplier as needed
        base_Top.angle = tension_angle
        print(f"base_Bottom moved to {main_angle} degrees.")
        print(f"base_Top adjusted to {tension_angle} degrees to maintain tension.")
    else:
        print("Invalid angle for base_Bottom. Please enter a value between 30 and 90 degrees.")
    time.sleep(1)

def tongue_TipUp(main_angle):
    """Move tip_Top upwards and adjust tip_Bottom to maintain tension."""
    if 0 <= main_angle <= 90:  # Validate angle for tip_Top
        tip_Top.angle = main_angle
        # Calculate a reduced movement for tip_Bottom to maintain tension
        tension_angle = 90 + (90 - main_angle) * 0.5  # Adjust the multiplier as needed
        tip_Bottom.angle = tension_angle
        print(f"tip_Top moved to {main_angle} degrees.")
        print(f"tip_Bottom adjusted to {tension_angle} degrees to maintain tension.")
    else:
        print("Invalid angle for tip_Top. Please enter a value between 0 and 90 degrees.")
    time.sleep(1)

def tongue_TipDown(main_angle):
    """Move tip_Bottom downwards and adjust tip_Top to maintain minimal tension."""
    if 90 <= main_angle <= 180:  # Validate angle for tip_Bottom
        tip_Bottom.angle = main_angle
        # Calculate minimal movement for tip_Top to maintain tension
        tension_angle = 180 - (main_angle - 90) * 0.5  # Adjust the multiplier as needed
        tip_Top.angle = tension_angle
        print(f"tip_Bottom moved to {main_angle} degrees.")
        print(f"tip_Top adjusted to {tension_angle} degrees to maintain minimal tension.")
    else:
        print("Invalid angle for tip_Bottom. Please enter a value between 90 and 180 degrees.")
    time.sleep(1)


def returnToNeutral():
    """Reset all servos to their neutral position."""
    base_Top.angle = 90
    base_Bottom.angle = 90
    tip_Top.angle = 90
    tip_Bottom.angle = 90
    print("All servos returned to neutral position.")
    time.sleep(1)

def choose_tip_movement():
    """Prompt for tip movements after base movements."""
    tip_action = input("Choose 'tip up', 'tip down', or 'skip' to finish: ")
    if tip_action.lower() == 'tip up':
        tip_angle = int(input("Enter the angle for tip_Top (0-90): "))
        tongue_TipUp(tip_angle)
    elif tip_action.lower() == 'tip down':
        tip_angle = int(input("Enter the angle for tip_Bottom (90-180): "))
        tongue_TipDown(tip_angle)
    elif tip_action.lower() == 'skip':
        print("Skipping tip adjustment.")

try:
    while True:
        # Get input from the user for base movement
        base_action = input("Enter 'base up', 'base down', 'neutral', or 'exit': ")
        if base_action.lower() == 'exit':
            print("Exiting program.")
            break
        elif base_action.lower() == 'base up':
            base_angle = int(input("Enter the angle for base_Top (90-150): "))
            tongue_BaseUp(base_angle)
            choose_tip_movement()
        elif base_action.lower() == 'base down':
            base_angle = int(input("Enter the angle for base_Bottom (30-90): "))
            tongue_BaseDown(base_angle)
            choose_tip_movement()
        elif base_action.lower() == 'neutral':
            returnToNeutral()
        else:
            print("Please enter 'base up', 'base down', 'neutral', or 'exit'.")

finally:
    # Ensure the PCA9685 is properly shut down
    pca.deinit()
    print("Test complete and PCA9685 shutdown.")
