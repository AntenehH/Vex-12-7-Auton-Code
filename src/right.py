#consts
PLACEHOLDER = 5
DEGREESPLACEHOLDER = 50

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

#variables
e_brake_is_up = False
descorer_is_up = False
match_loader_is_up = False

# intializations
brain = Brain()
controller = Controller()
drive_train_intertial = Inertial(Ports.PORT19) # intertial sensor

# pneumatics
e_brake = DigitalOut(brain.three_wire_port.h) # e brake wheel
descorer = DigitalOut(brain.three_wire_port.f) 
match_loader = DigitalOut(brain.three_wire_port.g)

#distance sensors
# distance_a = Distance(Ports.PORT10) # distance sensor top
# distance_b = Distance(Ports.PORT11) # distance sensor bottom

# define motors
intake_motor_entrance = Motor(Ports.PORT2, True) # entrance intake
intake_motor_top = Motor(Ports.PORT4, True) # top intake
outtake_motor = Motor(Ports.PORT6) # top outtake

#drive train motors
left_motor_a = Motor(Ports.PORT20, True) # left front motor
left_motor_b = Motor(Ports.PORT10, True) # left back motor
right_motor_a = Motor(Ports.PORT11) # right front motor
right_motor_b = Motor(Ports.PORT1) # right back motor

# define drive train
left_motor_group = MotorGroup(left_motor_a, left_motor_b)
right_motor_group = MotorGroup(right_motor_a, right_motor_b)
drive_train = SmartDrive(left_motor_group, right_motor_group, drive_train_intertial, 250, 300, 100, MM, 6)

# functions

def entrance(): # only start entrance motor
    intake_motor_entrance.spin(FORWARD)

def entrance_stop(): # stop entrance motor
    intake_motor_entrance.stop()

def entrance_intake_for_seconds(sec):
    entrance()
    wait(sec, SECONDS)
    entrance_stop()

def intake(): # start intake
    intake_motor_entrance.spin(FORWARD)
    while not distance_a.is_object_detected() and not distance_b.is_object_detected(): # while no blocks in top chamber spin the top motor
        intake_motor_top.spin(FORWARD)

def intake_stop(): # stop intake
    intake_motor_entrance.stop()
    intake_motor_top.stop()

def intake_for_seconds(sec): # spin intake motor for sec SECONDS
    intake()
    wait(sec, SECONDS)
    intake_stop()

def outtake(): # start outtake
    intake()
    outtake_motor.spin(FORWARD)

def outtake_stop(): # stop outtake
    intake_stop()
    outtake_motor.stop()

def outtake_for_seconds(sec): # outtake for sec SECONDS
    outtake()
    wait(sec, SECONDS)
    outtake_stop()

def e_brake_down():
    global e_brake_is_up

    e_brake.set(True)
    e_brake_is_up = False

def e_brake_up():
    global e_brake_is_up

    e_brake.set(False)
    e_brake_is_up = True

def e_brake_toggle(): # for manual, map e brake to one button toggle
    global e_brake_is_up

    if e_brake_is_up:
        e_brake_down()
    else:
        e_brake_up()

def match_loader_up():
    global match_loader_is_up

    match_loader.set(True)
    match_loader_is_up = True

def match_loader_down():
    global match_loader_is_up

    match_loader.set(False)
    match_loader_is_up = True

def match_loader_toggle(): # for manual, map match loader to one button toggle
    global match_loader_is_up

    if match_loader_is_up:
        match_loader_down()
    else:
        match_loader_up()

def descorer_up():
    global descorer_is_up

    descorer.set(True)
    descorer_is_up = True
def descorer_down():
    global descorer_is_up

    descorer.set(False)
    descorer_is_up = False

def descorer_toggle():
    global descorer_is_up

    if descorer_is_up:
        descorer_down()
    else:
        descorer_up()

# movement functions

def f(inch):
    drive_train.drive_for(FORWARD, inch, INCHES)

def b(inch):
    drive_train.drive_for(REVERSE, inch, INCHES)

def r(deg):
    drive_train.turn_for(RIGHT, deg, DEGREES)

def l(deg):
    drive_train.turn_for(LEFT, deg, DEGREES)

# main functions

def pre_autonomous(): # runs before autonomous
    e_brake_up()
    match_loader_up()
    descorer_down()
    
    # calibrate inertial
    drive_train_intertial.calibrate()
    while drive_train_intertial.is_calibrating():
        wait(50, MSEC)

def autonomous():
    drive_train_intertial.set_heading(37.5) # update heading

    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    # place automonous code here
    drive_train.set_drive_velocity(20, PERCENT)
    drive_train.set_turn_velocity(20, PERCENT)
    outtake_motor.set_velocity(100, PERCENT)

    # route
    intake() # start intaking
    f(10) # start forward
    r(90)# right 
    intake_stop() # stop intaking
    b(10) # backwards align with goal
    l(45) # turn so output faces goal
    b(10) # back into goal
    outtake() # outtake into goal
    # if time + to column vvv

    user_control() # remove at comp

def user_control():
    # open buttons:
    # L2, Up, Down, Right, X, Y

    brain.screen.clear_screen()
    brain.screen.print("driver control")

    # button functions
    controller.buttonLeft.pressed(e_brake_toggle)
    controller.buttonA.pressed(descorer_toggle)
    controller.buttonB.pressed(match_loader_toggle)

    # intake/outtake motors
    controller.buttonR2.pressed(entrance) # run only entrance motor
    controller.buttonR2.released(entrance_stop)

    controller.buttonR1.pressed(intake) # run both intake motors
    controller.buttonR1.released(intake_stop)

    controller.buttonL1.pressed(outtake) # run all motors
    controller.buttonL1.released(outtake_stop)

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

pre_autonomous()
autonomous()

# create competition instance
# comp = Competition(user_control, autonomous)

# actions to do when the program starts
brain.screen.clear_screen()