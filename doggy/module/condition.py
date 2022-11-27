### 8 methods define the 8 behaviors of the puppy.
    '''
    Idle
    30s內偵測到拍背
    '''
    def idle(self, value):
        print('idle')
        self.faceExpression(Neutral)
        self.faceExpression(MIDDLE_RIGHT)
        self.faceExpression(MIDDLE_LEFT)
        self.soundEffect(DOG_SNIFF)        
        #如果在等待時間不超過三十秒
        while self.waitOver(30000) == False:
            #如果被摸到
            if self.isTouched == True:
                self.behavior = self.wandering()
    '''
    wandering
    30s內吃到骨頭
    經過30s沒有吃到骨頭
    '''
    def wandering(self):
        self.faceExpression(PINCHED_LEFT)
        self.faceExpression(PINCHED_RIGHT)
        self.faceExpression(PINCHED_MIDDLE)
        self.soundEffect(DOG_BARK_1)
        while self.waitOver(30000) == False:
            if boneAte(self) == True:
                self.happy(self)
        if boneAte(self) == False:
            self.sad(self)
                
    '''
    sleep
    偵測到拍背
    受到攻擊
    '''
    def asleep(self):
        
        
    
    '''alert
    待機超過30秒
    受到攻擊
    '''
    def alert():
        self.faceExpression(self, ANGRY)
        while self.waitOver(self, ) == False:
            self.soundEffect(self, DOG_GROWL)
    
    '''
    rage
    狂奔超過10秒
    '''
    def rage(self):
        #把速度加上去
        self.robot.settings(straight_speed, straight_acceleration, turn_rate, turn_acceleration)
        self.soundEffect(self, SPEED_UP)
        self.robot.turn(360)
        self.robot.run_target(self)
        self.soundEffect(self, SPEED_IDLE)
        self.robot.turn(360)
        self.soundEffect(self, SPEED_DOWN)
        
        
        
    
    '''
    sad
    待機超過30s
    受到攻擊
    '''
    def sad(self):
        self.soundEffect(self, CRYING)
        self.faceExpression(self, TIRED_LEFT)
        self.soundEffect(self, CRYING)
        self.faceExpression(self, TIRED_Middle)
        self.soundEffect(self, CRYING)
        self.faceExpression(self, TIRED_Right)
        self.soundEffect(self, CRYING)
    
    '''
    happy
    完成動作後: 3s後
    '''
    def happy(self):
        self.soundEffect(self, DOG_BARK_1)
        self.faceExpression(self, WINKING)
        self.soundEffect(self, DOG_BARK_1)
        self.faceExpression(self, NEUTRAL)
        self.soundEffect(self, DOG_BARK_1)
        self.faceExpression(self, CRAZY_1)
        self.soundEffect(self, DOG_BARK_1)
        self.faceExpression(self, CRAZY_2)                        
    

    def go_to_sleep(self):
        """Makes the puppy go to sleep."""
        if self.did_behavior_change:
            print('go_to_sleep')
            self.eyes = self.TIRED_EYES
            self.sit_down()
            self.move_head(self.HEAD_DOWN_ANGLE)
            self.eyes = self.SLEEPING_EYES
            self.ev3.speaker.play_file(SoundFile.SNORING)
        if self.touch_sensor.pressed() and Button.CENTER in self.ev3.buttons.pressed():
            self.count_changed_timer.reset()
            self.behavior = self.wake_up

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
        self