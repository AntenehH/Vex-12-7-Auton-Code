# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       limjedidiah8152                                              #
# 	Created:      11/6/2025, 8:09:52 AM                                        #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

brain = Brain()
controller = Controller()
drive_train_intertial = Inertial(Ports.PORT1)
# define motors
intake_motor = Motor(Ports.PORT2, True) # entrance motor
outtake_motor = Motor(Ports.PORT3) # outtake

left_motor_a = Motor(Ports.PORT4) # left front motor
left_motor_b = Motor(Ports.PORT5) # left back motor
right_motor_a = Motor(Ports.PORT6) # right front motor
right_motor_b = Motor(Ports.PORT7) # right back motor
# define drive train
left_motor_group = MotorGroup(left_motor_a, left_motor_b)
right_motor_group = MotorGroup(right_motor_a, right_motor_b)
drive_train = SmartDrive(left_motor_group, right_motor_group, drive_train_intertial)

PLACEHOLDER = 10
# functions

def intake(sec): # spin intake motor for sec SECONDS
    intake_motor.spin(FORWARD)
    wait(sec, SECONDS)
    intake_motor.stop()

def outtake(sec): # spin intake + outtake motors for sec SECONDS
    intake_motor.spin(FORWARD)
    outtake_motor.spin(FORWARD)
    wait(sec, SECONDS)
    intake_motor.stop()
    outtake_motor.stop()



def pre_autonomous(): # runs before autonomous
    # calibrate inertial
    drive_train_intertial.calibrate()
    while drive_train_intertial.is_calibrating():
        wait(50, MSEC)

pre_autonomous()

def autonomous(): 
    drive_train_intertial.set_heading(0) # reset heading

    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    # place automonous code here
    drive_train.set_drive_velocity(50, PERCENT)
    drive_train.set_turn_velocity(80, PERCENT)
    intake_motor.set_velocity(100, PERCENT) 
    outtake_motor.set_velocity(100, PERCENT)

    # route
    # start intake
    
    drive_train.drive_for(FORWARD, PLACEHOLDER, INCHES) # start forward
    drive_train.turn_for(RIGHT, PLACEHOLDER, DEGREES) # right 
    # stop intake

    drive_train.drive_for(REVERSE, PLACEHOLDER,INCHES) # backwards align with goal
    drive_train.turn_for(RIGHT, PLACEHOLDER, DEGREES) # turn so output faces goal
    drive_train.drive_for(REVERSE, PLACEHOLDER, INCHES) # back into goal
    # start outtake

def user_control():
    brain.screen.clear_screen()
    brain.screen.print("driver control")
    # place driver control in this while loop
    while True:
        turn = controller.axis1.position()
        forward = controller.axis3.position()

        drive_train.drive(DirectionType.FORWARD, forward, VelocityUnits.PERCENT) 
        
        if turn > 0:
            drive_train.turn(RIGHT, turn, VelocityUnits.PERCENT)
            brain.screen.print("turn RIGHT\n")
        elif turn < 0:
            drive_train.turn(LEFT, -turn, VelocityUnits.PERCENT)
            brain.screen.print("turn LEFT\n")

        wait(20, MSEC)
    # add other functions later

# create competition instance
comp = Competition(user_control, autonomous)

# actions to do when the program starts
brain.screen.clear_screen()