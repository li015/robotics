#!/usr/bin/env pybricks-micropython

"""
Example LEGO® MINDSTORMS® EV3 Puppy Program
-------------------------------------------

This program requires LEGO® EV3 MicroPython v2.0.
Download: https://education.lego.com/en-us/support/mindstorms-ev3/python-for-ev3

Building instructions can be found at:
https://education.lego.com/en-us/support/mindstorms-ev3/building-instructions#building-core
"""

import urandom

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, TouchSensor, GyroSensor, UltrasonicSensor
from pybricks.parameters import Port, Button, Color, Direction
from pybricks.media.ev3dev import Image, ImageFile, SoundFile
from pybricks.tools import wait, StopWatch
from pybricks.robotics import DriveBase


class Puppy:
    # These constants are used for positioning the legs.
    HALF_UP_ANGLE = 25
    STAND_UP_ANGLE = 65
    STRETCH_ANGLE = 125

    # These constants are for positioning the head.
    HEAD_UP_ANGLE = 0
    HEAD_DOWN_ANGLE = -40

    # These constants are for the eyes.
    NEUTRAL_EYES = Image(ImageFile.NEUTRAL)
    PINCHED_LEFT = Image(ImageFile.PINCHED_LEFT)
    PINCHED_RIGHT = Image(ImageFile.PINCHED_RIGHT)
    TIRED_EYES = Image(ImageFile.TIRED_MIDDLE)
    TIRED_LEFT_EYES = Image(ImageFile.TIRED_LEFT)
    TIRED_RIGHT_EYES = Image(ImageFile.TIRED_RIGHT)
    SLEEPING_EYES = Image(ImageFile.SLEEPING)
    HURT_EYES = Image(ImageFile.HURT)
    ANGRY_EYES = Image(ImageFile.ANGRY)
    HEART_EYES = Image(ImageFile.LOVE)
    SQUINTY_EYES = Image(ImageFile.TEAR)  # the tear is erased later

    def __init__(self):

        self.ev3 = EV3Brick()

        # 檢查 port & functions. 每次都要調整&確認;
        # left.motor = 左前腳, right.motor = 右前腳

        self.left_motor = Motor(Port.D)
        self.right_motor = Motor(Port.C)

        # 因為有給定gear train, motor.run_target(speed,target)的角度這裡直接是輸出所轉過的角度
        self.head_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE,
                                gears=[[1, 24], [12, 36]])

        self.gyro = GyroSensor(Port.S2)
        self.touch_A = TouchSensor(Port.S4)
        self.d_1 = UltrasonicSensor(Port.S1)

        # 初始化車輛基座 ; Initialize the drive base.
        # 有關 DriveBase的使用: https://pybricks.com/ev3-micropython/robotics.html
        # turn/straight 的輸入參數目前為相反值 ; for now, the input value of turn/stright are the opposites.

        self.robot = DriveBase(
            self.left_motor, self.right_motor, wheel_diameter=30, axle_track=105)

        # Initialize the Color Sensor. It is used to detect the colors when
        # feeding the puppy.
        self.color_sensor = ColorSensor(Port.S3)

        # # Initialize the touch sensor. It is used to detect when someone pets
        # # the puppy.
        
        #####世界內計時器
        self.pet_count_timer = StopWatch()
        self.feed_count_timer = StopWatch()
        self.count_changed_timer = StopWatch()
        #####行為內計時器initialize
        #待機超過30s=>gotosleep
        #遊走超過30s=>sad
        #狂奔10s=>gotosleep
        #難過超過30s=>gotosleep
        #警戒超過30s=>idle
        #開心3s=>follow




        # These attributes are initialized later in the reset() method.
        self.pet_target = None
        self.feed_target = None
        self.pet_count = None
        self.feed_count = None

        # These attributes are used by properties.
        self._behavior = None
        self._behavior_changed = None
        self._eyes = None
        self._eyes_changed = None

        # These attributes are used in the eyes update
        self.eyes_timer_1 = StopWatch()
        self.eyes_timer_1_end = 0
        self.eyes_timer_2 = StopWatch()
        self.eyes_timer_2_end = 0
        self.eyes_closed = False

        # These attributes are used by the playful behavior.
        self.playful_timer = StopWatch()
        self.playful_bark_interval = None

        # These attributes are used in the update methods.
        self.prev_petted = None
        self.prev_color = None
        # These attributes are used in gyro (movement detection)
        self.gyro_timer = StopWatch()
        GYRO_MAXRATE = 50
        DISTANCE_NEAR = 50
    
    ''' 以下是動作與偵測部分'''
    # 移動頭部

    def move_head(self, target):
        """Move the head to the target angle.

        Arguments:.
            target (int):
                The target angle in degrees. 0 is the starting position,
                negative values are below this point and positive values
                are above this point.
        """
        self.head_motor.run_target(20, target)
    # 旋轉是內建的driveBase內建的函式
    # straight(distance), turn(angle), settings(straight_speed, straight_acceleration, turn_rate, turn_acceleration)
    # stop(), distance()量測距離
    # 觸摸功能：self.touch_A.pressed() True if the sensor is pressed, False if it is not pressed.
    # 顏色感知功能：self.color()

    #timer: 判斷等待的時間是否超過特定的秒數
    def waitOver(self, value):
        n = StopWatch.time()
        value *= 1000

        while n < value:
            condition = False

        StopWatch.reset()
        return True
    '''以下是事件部分'''

    def boneAte(self):
        if self.color_sensor.color() != None:
            # print(self.color_sensor.color())
            return True
        else:
            return False

    def isTouched(self):
        touched = self.touch_A.pressed()
        return touched

    def faceExpression(self, condition):
        self.eyes = self.condition

    def soundEffect(self, effect):
        ### speaker.set_volume(volumn, which='_all')
        self.ev3.speaker.play_file(SoundFile.effect)

    '''以下是狀態部分'''

    def reset(self):
        # Set initial behavior.
        # self.move_head(20)
        self.behavior = self.idle

    # def idle(self):
    #     """The puppy is idle and waiting for someone to pet it or feed it."""
    #     if self.did_behavior_change:
    #         print('idle')
    #         self.stand_up()
    #     self.update_eyes()
    #     self.update_behavior()
    #     self.update_pet_count()
    #     self.update_feed_count()
    '''
    Idle
    30s內偵測到拍背
    '''

    def idle(self):
        print('idle')
        self.eyes = self.NEUTRAL_EYES
        # self.faceExpression(MIDDLE_RIGHT)
        # self.faceExpression(MIDDLE_LEFT)
        self.ev3.speaker.play_file(SoundFile.DOG_SNIFF)
        # 如果在等待時間不超過三十秒
        print(self.isTouched())
        if self.isTouched() == True:
            self.count_changed_timer.reset()
            self.behavior = self.wandering()
            self.count_changed_timer.reset()
        # while self.waitOver(value) == False:
        if self.count_changed_timer.time() > 30000:
            print('boring~')
    '''
    wandering
    30s內吃到骨頭
    經過30s沒有吃到骨頭
    '''

    def wandering(self):
        print('wandering')
        # if self.count_changed_timer.time() < 30000:

        self.eyes = self.PINCHED_LEFT
        self.eyes = self.PINCHED_RIGHT
        self.ev3.speaker.play_file(SoundFile.DOG_BARK_1)
            # self.faceExpression(PINCHED_LEFT)
            # self.faceExpression(PINCHED_RIGHT)
            # self.faceExpression(PINCHED_MIDDLE)
            # self.soundEffect(DOG_BARK_1)
 
        # 判斷多少時間內吃到???
        if self.boneAte() == True:
            self.count_changed_timer.reset()
            self.behavior = self.happy()
        else:
            # self.count_changed_timer.time() > 30000:
            # self.count_changed_timer.reset()
            self.behavior = self.sad()
    

    def sad(self):
        print('sad')
        sad_timer= StopWatch()
        # self.soundEffect(self, CRYING)
        # self.faceExpression(self, TIRED_LEFT)
        # self.soundEffect(self, CRYING)
        # self.faceExpression(self, TIRED_Middle)
        # self.soundEffect(self, CRYING)
        # self.faceExpression(self, TIRED_Right)
        # self.soundEffect(self, CRYING)
        
        if sad_timer.time() < 30000:
            if self.gyro ==True:
                print('rage')
                self.behavior=self.rage
            
        ###受到攻擊
        elif sad_timer.time() > 30000:
            print('gotosleep')
            self.behavior=self.go_to_sleep
            

   
    def alert():
        print('alert')
        # self.faceExpression(self, ANGRY)
        # while self.waitOver(self, ) == False:
        #     self.soundEffect(self, DOG_GROWL)

        ###如果受到攻擊

        self.behavior=self.rage


    
    '''
    rage
    狂奔超過10秒
    '''

    def rage(self):
        print('rage')
        self.rage_timer= StopWatch()
        # 把速度加上去
        self.robot.settings(
            straight_speed, straight_acceleration, turn_rate, turn_acceleration)
        # self.soundEffect(self, SPEED_UP)
        self.robot.turn(360)
        self.robot.run_target(self)
        # self.soundEffect(self, SPEED_IDLE)
        self.robot.turn(360)
        # self.soundEffect(self, SPEED_DOWN)

        if rage_timer.time()>10000:
            self.behavior=self.go_to_sleep



    '''
    happy
    完成動作後: 3s後
    '''

    def happy(self):
        print('happy')
        # self.soundEffect(self, DOG_BARK_1)
        # self.faceExpression(self, WINKING)
        # self.soundEffect(self, DOG_BARK_1)
        # self.faceExpression(self, NEUTRAL)
        # self.soundEffect(self, DOG_BARK_1)
        # self.faceExpression(self, CRAZY_1)
        # self.soundEffect(self, DOG_BARK_1)
        # self.faceExpression(self, CRAZY_2)

        '''goto 跟隨
        '''
        # 偵測到拍背
        if self.count_changed_timer.time() >30000:
            self.count_changed_timer.reset()
            self.behavior = self.follow

    def follow(self):
        print('follow')
        # 偵測到拍背
        if self.isTouched() == True:
            self.count_changed_timer.reset()
            self.behavior = self.idle

    def go_to_sleep(self):
        """Makes the puppy go to sleep."""
        if self.did_behavior_change:
            print('go_to_sleep')
            self.eyes = self.TIRED_EYES
            # self.sit_down()
            self.move_head(self.HEAD_DOWN_ANGLE)
            self.eyes = self.SLEEPING_EYES
            self.ev3.speaker.play_file(SoundFile.SNORING)
        if self.touch_A.pressed() and Button.CENTER in self.ev3.buttons.pressed():
            self.count_changed_timer.reset()
            self.behavior = self.idle

    def wake_up(self):
        """Makes the puppy wake up."""
        if self.did_behavior_change:
            print('wake_up')
        self.eyes = self.TIRED_EYES
        self.ev3.speaker.play_file(SoundFile.DOG_WHINE)
        self.move_head(self.HEAD_UP_ANGLE)
        self.sit_down()
        self.stretch()
        wait(1000)
        self.stand_up()
        self.behavior = self.idle

    def act_playful(self):
        """Makes the puppy act playful."""
        if self.did_behavior_change:
            print('act_playful')
            self.eyes = self.NEUTRAL_EYES
            self.stand_up()
            self.playful_bark_interval = 0

        if self.update_pet_count():
            # If the puppy was petted, then we are done being playful
            self.behavior = self.idle

        if self.playful_timer.time() > self.playful_bark_interval:
            self.ev3.speaker.play_file(SoundFile.DOG_BARK_2)
            self.playful_timer.reset()
            self.playful_bark_interval = urandom.randint(4, 8) * 1000

    def act_angry(self):
        """Makes the puppy act angry."""
        if self.did_behavior_change:
            print('act_angry')
        self.eyes = self.ANGRY_EYES
        self.ev3.speaker.play_file(SoundFile.DOG_GROWL)
        self.stand_up()
        wait(1500)
        self.ev3.speaker.play_file(SoundFile.DOG_BARK_1)
        self.pet_count -= 1
        print('pet_count:', self.pet_count, 'pet_target:', self.pet_target)
        self.behavior = self.idle

    def act_happy(self):
        if self.did_behavior_change:
            print('act_happy')
        self.eyes = self.HEART_EYES
        # self.move_head(self.?)
        self.sit_down()
        for _ in range(3):
            self.ev3.speaker.play_file(SoundFile.DOG_BARK_1)
            self.hop()
        wait(500)
        
    # Test gyro speed and angle first
    def gyro_test(self):
        print('Gryo rotational speed = ' + self.gyro.speed() + 'deg/s')
        # print( 'n/Gryo rotational angle = ' + self.gyro.angle() + 'deg')
        # From EV3 documentation: If you use the angle() method, 
        # you cannot use the speed() method in the same program. 
        # Doing so would reset the sensor angle to zero every time you read the speed.

    def gyro(self):
        if self.gyro.speed() < GYRO_MAXRATE:
            return False
        else:
            if self.d_1.distance () < DISTANCE_NEAR:
                return True

            else:
                return False
            
###########
#定義
###########

    @property
    def behavior(self):
        """Gets and sets the current behavior."""
        return self._behavior

    @behavior.setter
    def behavior(self, value):
        if self._behavior != value:
            self._behavior = value
            self._behavior_changed = True

    @property
    def did_behavior_change(self):
        """bool: Tests if the behavior changed since the last time this
        property was read.
        """
        if self._behavior_changed:
            self._behavior_changed = False
            return True
        return False
    @property
    def eyes(self):
        """Gets and sets the eyes."""
        return self._eyes

    @eyes.setter
    def eyes(self, value):
        if value != self._eyes:
            self._eyes = value
            self.ev3.screen.load_image(value)

    def update_eyes(self):
        if self.eyes_timer_1.time() > self.eyes_timer_1_end:
            self.eyes_timer_1.reset()
            if self.eyes == self.SLEEPING_EYES:
                self.eyes_timer_1_end = urandom.randint(1, 5) * 1000
                self.eyes = self.TIRED_RIGHT_EYES
            else:
                self.eyes_timer_1_end = 250
                self.eyes = self.SLEEPING_EYES

        if self.eyes_timer_2.time() > self.eyes_timer_2_end:
            self.eyes_timer_2.reset()
            if self.eyes != self.SLEEPING_EYES:
                self.eyes_timer_2_end = urandom.randint(1, 10) * 1000
                if self.eyes != self.TIRED_LEFT_EYES:
                    self.eyes = self.TIRED_LEFT_EYES
                else:
                    self.eyes = self.TIRED_RIGHT_EYES

############
#計時器
############
    def monitor_counts(self):
        #是否30s沒換行為
        if self.count_changed_timer.time() > 30000:
            # If nothing has happened for 30 seconds, go to sleep
            self.count_changed_timer.reset()
            self.behavior = self.idle()


        #待機超過30s=>gotosleep
        #遊走超過30s=>sad
        #狂奔10s=>gotosleep
        #難過超過30s=>gotosleep
    def sad_time_counts(self):
        if self.sad_timer.time()>30000:
            self.sad_timer.reset()
            self.behavior = self.rage()
        #警戒超過30s=>idle
        #開心3s=>follow

    

    def run(self):
        self.reset()
        while True:
            self.monitor_counts()
            self.behavior()
            wait(100)

if __name__ == '__main__':
    puppy = Puppy()
    puppy.run()
