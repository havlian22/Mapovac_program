import rclpy
import math
import time
from rclpy.node import Node
from gpiozero import PWMLED

PP1 = 27
PP2 = 17
LP1 = 25 #lp
LP2 = 16 #lp
PZ1 = 26
PZ2 = 22
LZ1 = 5 #5
LZ2 = 6 #6

Max_speed = 2


class Motor:
    def __init__(self, IN1, IN2):
        self.dir = PWMLED(IN1)
        self.dir2 = PWMLED(IN2)
        self.x = 0

    def run(self, vel):
        if (vel >= 0):
            self.dir.value = 0 
            self.dir2.value = vel
        else:
            self.dir.value = vel*(-1)
            self.dir2.value = 0


class Move(Node):
    def __init__(self):
        super().__init__("move_node")
        self.M_lz = Motor(LZ1, LZ2)
        self.M_pz = Motor(PZ1, PZ2) 
        self.M_lp = Motor(LP1, LP2) 
        self.M_pp = Motor(PP1, PP2)       

    def movement(self, linear, angular):
        
        self.vector = [linear, angular]
        self.vector[0] = (self.vector[0]/ abs(linear))
        self.vector[1] = self.vector[1] - (math.pi / 4)

        self.cosinus = abs(linear)*(math.sqrt(self.vector[0] - pow(math.sin(self.vector[1]), 2)))
        self.sinus = abs(linear)*(math.sqrt(self.vector[0] - pow(math.cos(self.vector[1]), 2)))

        self.M_lp.run(self.cosinus) #self.sinus
        self.M_pz.run(self.cosinus) #self.sinus
        self.M_lz.run(self.sinus) #self.cosinus
        self.M_pp.run(self.sinus) #self.cosinus




def main(args=None):
    rclpy.init(args=args)
    action = Move()
    action.movement(1, ((math.pi) / 2))
    time.sleep(50)
    action.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()