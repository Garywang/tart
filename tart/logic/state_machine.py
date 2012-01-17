import sys, time
import threading, thread
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
import math

class StateMachine(threading.Thread):
    def __init__(self, robot):
        threading.Thread.__init__(self)
        self.robot = robot
        self.running = False
        
    def run(self):
        self.running = True
        self.robot.ard.waitReady() # wait for arduino first
        
        self.state = self.scan
        while self.running:
            self.state = self.state()
            time.sleep(0)
    
    def stop(self):
        self.running = False
    
    def scan(self):
        if self.robot.map.get_closest_ball(): # sees a ball
            return self.approach
        self.robot.drive.rotate(50)
        return self.scan
    
    def approach(self):
        if self.robot.map.get_closest_ball() is None:
            return self.scan
        x, y = self.robot.map.get_vector_to(self.robot.map.get_closest_ball())
        # this stuff should go in control eventually.
        angle=math.pi/2-atan2(y, x)     #Right is positive, left is negative
        self.robot.drive.forward(rotation=angle*100)
        return self.approach

if __name__ == '__main__':
    sm = StateMachine()
    sm.start()
