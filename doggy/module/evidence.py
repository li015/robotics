 '''以下是事件部分'''
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