
''' 以下是動作與偵測部分'''
    #移動頭部
    def move_head(self, target):
        """Move the head to the target angle.

        Arguments:
            target (int):
                The target angle in degrees. 0 is the starting position,
                negative values are below this point and positive values
                are above this point.
        """
        self.head_motor.run_target(20, target)
    #旋轉是內建的driveBase內建的函式
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