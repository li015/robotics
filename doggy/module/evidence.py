 '''以下是事件部分'''
    def isBoneAte(self):
        if self.ateyet_timer.time() > 0:
            ateyet_timer.reset()
        while self.ateyet_timer.time() <30000:
            if self.color() != None:
                self.behavior = self.happy
            else:
                continue
        else:
            self.behavior = self.sad()
    
    def sad_tree(self):
        if self.sad_timer.time() > 0:
            sad_timer.reset()
        while self.sad_timer.time() <30000 
            if self.gyro ==True:
                self.behavior = self.rage()
            else:
                continue
        else:
            self.behavior=self.go_to_sleep

    def boneAte(self):
        if self.color() != None:
            return True
        else:
            return False
    
    def isTouched(self):
        return self.touch_A.pressed()
    
    def faceExpression(self, condition):
        self.eyes = self.condition
    
    def soundEffect(self, effect):
        self.ev3.speaker.play_file(SoundFile.effect)