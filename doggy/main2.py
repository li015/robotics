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
import threading
import time

def threading_example():
  # 子執行緒的工作函數
    def job():
        for i in range(5):
            print("Child thread:", i)
            time.sleep(1)

    # 建立一個子執行緒
    t = threading.Thread(target = job)

    # 執行該子執行緒
    t.start()

    # 主執行緒繼續執行自己的工作
    for i in range(3):
        print("Main thread:", i)
        time.sleep(1)

    # 等待 t 這個子執行緒結束
    # t.join()

    print("Done.")

class Puppy:

    '''get image file'''
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
    MIDDLE_RIGHT = Image(ImageFile.MIDDLE_RIGHT)
    MIDDLE_LEFT = Image(ImageFile.MIDDLE_LEFT)

    def __init__(self):

        self.ev3 = EV3Brick()

        # 檢查 port & functions. 每次都要調整&確認;
        # left.motor = 左前腳, right.motor = 右前腳
        self.left_motor = Motor(Port.D)
        self.right_motor = Motor(Port.C)
        self.gyro = GyroSensor(Port.S2)
        self.touch_A = TouchSensor(Port.S4)
        self.d_1 = UltrasonicSensor(Port.S1)
        self.color_sensor = ColorSensor(Port.S3)
        # 因為有給定gear train, motor.run_target(speed,target)的角度這裡直接是輸出所轉過的角度
        self.head_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE,
                                gears=[[1, 24], [12, 36]])
        

        # 初始化車輛基座 ; Initialize the drive base.
        # 有關 DriveBase的使用: https://pybricks.com/ev3-micropython/robotics.html
        # turn/straight 的輸入參數目前為相反值 ; for now, the input value of turn/stright are the opposites.
        self.robot = DriveBase(
            self.left_motor, self.right_motor, wheel_diameter=30, axle_track=105)

        '''Stopwatch timer'''
        self.pet_count_timer = StopWatch()
        self.feed_count_timer = StopWatch()
        self.count_changed_timer = StopWatch()

        self.idle_timer = StopWatch()#待機超過30s=>gotosleep
        self.rage_timer = StopWatch() #狂奔10s=>gotosleep
        self.sad_timer = StopWatch() #難過超過30s=>gotosleep
        self.alert_timer = StopWatch() #警戒超過30s=>idle
        self.happy_timer = StopWatch() #開心3s=>follow
        self.ateyet_timer = StopWatch() #遊走30內沒吃到=>sad
        self.sleep_timer = StopWatch() #測試用

        # These attributes are initialized later in the reset() method.
        # self.pet_target = None
        # self.feed_target = None
        # self.pet_count = None
        # self.feed_count = None

        '''@property'''
        # These attributes are used by properties.
        self._behavior = None
        self._behavior_changed = None
        self._eyes = None
        self._eyes_changed = None

        '''用了眼睛會隨機眨比較生動'''
        # These attributes are used in the eyes update
        self.eyes_timer_1 = StopWatch()
        self.eyes_timer_1_end = 0
        self.eyes_timer_2 = StopWatch()
        self.eyes_timer_2_end = 0
        self.eyes_closed = False

        # These attributes are used by the playful behavior.
        # self.playful_timer = StopWatch()
        # self.playful_bark_interval = None

        # These attributes are used in the update methods.
        # self.prev_petted = None
        # self.prev_color = None

        '''gyro'''
        # These attributes are used in gyro (movement detection)
        self.gyro_timer = StopWatch()
        self.GYRO_MAXRATE = 50
        self.DISTANCE_NEAR = 50
    

    
    
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

    ''' movement'''

    # 移動頭部（卡住時要用）
    def move_head(self, target):
        """Move the head to the target angle.

        Arguments:.
            target (int):
                The target angle in degrees. 0 is the starting position,
                negative values are below this point and positive values
                are above this point.
        """
        self.head_motor.run_target(20, target)

    # the next 4 methods define actions that are used to make some parts of
    # the behaviors below.
    def sit_down(self):
        """Makes the puppy sit down."""
        self.left_leg_motor.run(-50)
        self.right_leg_motor.run(-50)
        wait(1000)
        self.left_leg_motor.stop()
        self.right_leg_motor.stop()
        wait(100)

    def stand_up(self):
        """Makes the puppy stand up."""
        self.left_leg_motor.run_target(100, self.HALF_UP_ANGLE, wait=False)
        self.right_leg_motor.run_target(100, self.HALF_UP_ANGLE)
        while not self.left_leg_motor.control.done():
            wait(100)

        self.left_leg_motor.run_target(50, self.STAND_UP_ANGLE, wait=False)
        self.right_leg_motor.run_target(50, self.STAND_UP_ANGLE)
        while not self.left_leg_motor.control.done():
            wait(100)

        wait(500)

    def stretch(self):
        """Makes the puppy stretch its legs backwards."""
        self.stand_up()

        self.left_leg_motor.run_target(100, self.STRETCH_ANGLE, wait=False)
        self.right_leg_motor.run_target(100, self.STRETCH_ANGLE)
        while not self.left_leg_motor.control.done():
            wait(100)

        self.ev3.speaker.play_file(SoundFile.DOG_WHINE)

        self.left_leg_motor.run_target(100, self.STAND_UP_ANGLE, wait=False)
        self.right_leg_motor.run_target(100, self.STAND_UP_ANGLE)
        while not self.left_leg_motor.control.done():
            wait(100)

    def hop(self):
        """Makes the puppy hop."""
        self.left_leg_motor.run(500)
        self.right_leg_motor.run(500)
        wait(275)
        self.left_leg_motor.hold()
        self.right_leg_motor.hold()
        wait(275)
        self.left_leg_motor.run(-50)
        self.right_leg_motor.run(-50)
        wait(275)
        self.left_leg_motor.stop()
        self.right_leg_motor.stop()

    # 狂奔不知道要不要寫
    # def runnn(self):
        # 旋轉是內建的driveBase內建的函式
        # straight(distance), turn(angle), settings(straight_speed, straight_acceleration, turn_rate, turn_acceleration)
        # stop(), distance()量測距離


    ''' sensor '''
    def gyro_test(self):
        print('Gryo rotational speed = ' + str(self.gyro.speed()) + 'deg/s')
        # print( 'n/Gryo rotational angle = ' + self.gyro.angle() + 'deg')
        # From EV3 documentation: If you use the angle() method, 
        # you cannot use the speed() method in the same program. 
        # Doing so would reset the sensor angle to zero every time you read the speed.

    def gyro1(self):
        if self.gyro.speed() < self.GYRO_MAXRATE:
            return False
        else:
            if self.d_1.distance () < self.DISTANCE_NEAR:
                return True

            else:
                return False
            
    # gyro2 continually assess gyro & ultrasonic sensor every 100ms
    def gyro2(self):    
        self.gyro_timer.reset()

        yield self._behavior #current behavior
        
        while True:

            if self.gyro.speed() < 50:
                return False
            else:
                if self.d_1.distance() < 50:
                    yield True
            # Beep and then restore the previous behavior from before the
            # ultrasonic sensor detected a movement.
            self.gyro.timer.reset()
            self.ev3.speaker.beep(1000, -1)
            while self.gyro_timer.time()<100:
                yield self._behavior
            self.ev3.speaker.beep(0,-1)

        # This adds a small delay since we don't need to read these sensors
        # continuously. Reading once every 100 milliseconds is fast enough.
            self.gyro_timer.reset()
            while self.gyro_timer.time() < 100:
                yield

    #check color sensor 顏色感知功能：self.color()
    def isboneAte(self):
        if self.color_sensor.color() != None:
            # print(self.color_sensor.color())
            return True
        else:
            return False

    #check touch sensor 觸摸功能：self.touch_A.pressed() True if the sensor is pressed, False if it is not pressed.
    def isTouched(self):
        touched = self.touch_A.pressed()
        return touched

    #check ultrasonic sensor
    #def istooclose(self):


    '''behavior changer 判斷是否要換行為'''

    #check when idle (wandering/ go to sleep)
    def idle_tree(self):
        if self.idle_timer.time() > 0:
            self.idle_timer.reset()
        while self.idle_timer.time() < 30000:
            
            if self.isTouched() == True:
                print(self.isTouched())
                self.behavior = self.wandering
                break
        else:
            print("over30s")
            self.behavior = self.go_to_sleep

    #check when wandering (happy/sad)
    def wandering_tree(self):
        if self.ateyet_timer.time() > 0:
            self.ateyet_timer.reset()
        while self.ateyet_timer.time() <10000:
            if self.isboneAte() == True:
                print(self.isboneAte())
                self.behavior = self.happy
                break
        else:
            print("10s no food!")
            self.behavior = self.sad
    
    #check when  sad (rage/ go to sleep)
    def sad_tree(self):
        if self.sad_timer.time() > 0:
            self.sad_timer.reset()
        while self.sad_timer.time() <10000 :

            if self.gyro.speed() >30:
                self.gyro_test()
                self.behavior = self.rage
                break

        else:
            self.behavior=self.go_to_sleep
    
    #check when rage (go to sleep)
    def rage_tree(self):
        if self.rage_timer.time() > 0:
            self.rage_timer.reset()
        while self.rage_timer.time() <10000 :
            if self.rage_timer.time() <10000:
                continue
        else:
            self.behavior=self.go_to_sleep
    
    #check when happy ( follow )
    def happy_tree(self):
        if self.happy_timer.time() > 0:
            self.happy_timer.reset()
        while self.happy_timer.time() <3000 :
            if self.happy_timer.time() <3000:
                continue
        else:
            self.behavior=self.follow


    #check when alert (rage/ idle )
    def alert_tree(self):
        if self.alert_timer.time() > 0:
            self.alert_timer.reset()
        while self.alert_timer.time() <10000 :

            if self.gyro.speed() >30:
                self.gyro_test()
                self.behavior = self.rage
                break
            # else:
            #     continue
            break
        else:
            self.behavior=self.go_to_sleep

    #check when follow
    def follow_tree(self):
        if self.isTouched() == True:
            self.behavior = self.idle

    #check when sleep
    def go_to_sleep_tree(self):
        if self.sleep_timer.time()>0:
            self.sleep_timer.reset()
        while self.sleep_timer.time()< 30000:
            ###目前用拍背判斷，還沒有測距
            if self.isTouched() == True:
                print(self.isTouched())
                self.behavior = self.alert
                break
        else:
            #睡著到起來遊走中間可能要有行為
            self.behavior = self.wandering


    '''behavior'''

    # Start in a reset state
    def reset(self):
        # must be called when puppy is sitting down.
        # self.move_head(20)
        # self.left_leg_motor.reset_angle(0)
        # self.right_leg_motor.reset_angle(0)
        self.behavior = self.idle


    #Idle
    def idle(self):
        if self.did_behavior_change:
            print('idle')
    
        ##聲音表情
        def idle_expression():
            for i in range(5):
                print("idle thread:", i)
                self.update_eyes()
                # self.eyes = self.MIDDLE_RIGHT #這樣寫不會換表情
                # self.eyes = self.SLEEPING_EYES
                self.ev3.speaker.play_file(SoundFile.DOG_SNIFF)
                time.sleep(1)
        t = threading.Thread(target = idle_expression)
        t.start()
        # 事件 #如果在等待時間不超過三十秒
        self.idle_tree()

  
    #wandering
    def wandering(self):
        if self.did_behavior_change:
            print('wandering')

        ##聲音表情
        self.eyes = self.PINCHED_LEFT
        self.eyes = self.PINCHED_RIGHT
        self.ev3.speaker.play_file(SoundFile.DOG_BARK_1)
            # self.faceExpression(PINCHED_LEFT)
            # self.faceExpression(PINCHED_RIGHT)
            # self.faceExpression(PINCHED_MIDDLE)
            # self.soundEffect(DOG_BARK_1)

        # 事件
        self.wandering_tree()
    
    #sad
    def sad(self):
        if self.did_behavior_change:
            print('sad')
        
        ##聲音表情
        # self.soundEffect(self, CRYING)
        # self.faceExpression(self, TIRED_LEFT)
        # self.soundEffect(self, CRYING)
        # self.faceExpression(self, TIRED_Middle)
        # self.soundEffect(self, CRYING)
        # self.faceExpression(self, TIRED_Right)
        # self.soundEffect(self, CRYING)
        
        # 事件
        self.sad_tree()
            

    #alert
    def alert(self):
        if self.did_behavior_change:
            print('alert')

        ##聲音表情
        # self.faceExpression(self, ANGRY)
        # while self.waitOver(self, ) == False:
        #     self.soundEffect(self, DOG_GROWL)

        ##事件
        self.alert_tree()
    
   
    #rage
    def rage(self):
        if self.did_behavior_change:
            print('rage')
        ##聲音表情

        ##動作
        # 把速度加上去
        # self.robot.settings(
        #     straight_speed, straight_acceleration, turn_rate, turn_acceleration)
        # # self.soundEffect(self, SPEED_UP)
        # self.robot.turn(360)
        # self.robot.run_target(self)
        # # self.soundEffect(self, SPEED_IDLE)
        # self.robot.turn(360)
        # # self.soundEffect(self, SPEED_DOWN)

        ##事件
        self.rage_tree()



    #happy
    def happy(self):
        if self.did_behavior_change:
            print('happy')

        ###聲音表情
        # self.soundEffect(self, DOG_BARK_1)
        # self.faceExpression(self, WINKING)
        # self.soundEffect(self, DOG_BARK_1)
        # self.faceExpression(self, NEUTRAL)
        # self.soundEffect(self, DOG_BARK_1)
        # self.faceExpression(self, CRAZY_1)
        # self.soundEffect(self, DOG_BARK_1)
        # self.faceExpression(self, CRAZY_2)

        ###事件
        self.happy_tree()

    #follow
    def follow(self):
        if self.did_behavior_change:
            print('follow')
        
        ###聲音表情

        ###動作
        '''
        要用到電腦視覺
        '''

        ###事件
        self.follow_tree()
        
    #go to sleep
    def go_to_sleep(self):
        if self.did_behavior_change:
            print('go_to_sleep')

        ###聲音表情
        # self.eyes = self.TIRED_EYES
        # self.sit_down()
        # self.move_head(self.HEAD_DOWN_ANGLE)
        # self.eyes = self.SLEEPING_EYES
        # self.ev3.speaker.play_file(SoundFile.SNORING)
    
        ###事件
        self.go_to_sleep_tree()

    '''unuse behavior that may be useful? in the future '''
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

    '''
    定義
    '''        
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


    '''God View 判斷一些全局的行為變化'''
    #是否30s沒換行為
    def monitor_counts(self):
        if self.count_changed_timer.time() > 30000:
            # If nothing has happened for 30 seconds, go to sleep
            self.count_changed_timer.reset()
            self.behavior = self.idle()

    #判斷等待的時間是否超過特定的秒數
    def waitOver(self, value):
        n = StopWatch.time()
        value *= 1000

        while n < value:
            condition = False

        StopWatch.reset()
        return True

    '''程式執行'''
    def run(self):
        self.reset()
        while True:
            # self.monitor_counts()
            self.behavior()
            wait(100)

if __name__ == '__main__':
    threading_example()
    puppy = Puppy()
    puppy.run()
    