import rclpy
import math
import time
from rclpy.node import Node
from gpiozero import PWMLED
from geometry_msgs.msg import Twist

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

        self.vector = [0, 0]
        self.sinus = 0.0
        self.cosinus = 0.0
        self.lin_x = 0.0
        self.ang_z = 0.0
        self.ulozeny_cas = 0

        self.subscription = self.create_subscription(Twist, 'cmd_vel', self.callback, 10)
        self.subscription      

        self.timer = self.create_timer(0.1, self.movement)

    def movement(self):      

        if(time.time() - self.ulozeny_cas > 0.2):
            self.lin_x = 0.0
            self.lin_y = 0.0 
            self.ang_z = 0.0
            self.vector[1] = 0
            self.vector[0] = 0



        self.vector[1] = self.lin_y         
        self.vector[0] = self.lin_x

        self.cosinus = (math.cos(self.vector[1] - (math.pi/2)) - math.sin(self.vector[1] - (math.pi/2))) / 2 if self.vector[0] or self.vector[1] != 0 else 0
        self.sinus = (math.cos(self.vector[1] - (math.pi/2)) + math.sin(self.vector[1] - (math.pi/2))) / 2  if self.vector[0] or self.vector[1] != 0 else 0


        if(self.sinus == 0.0 and self.cosinus == 0.0):
            self.M_lp.run(0.5*self.ang_z)
            self.M_lz.run(0.5*self.ang_z)
            self.M_pp.run((-0.5)*self.ang_z)
            self.M_pz.run((-0.5)*self.ang_z)
        else:

            self.M_lp.run(self.sinus) #self.sinus
            self.M_pz.run(self.sinus) #self.sinus
            self.M_lz.run(self.cosinus) #self.cosinus
            self.M_pp.run(self.cosinus) #self.cosinus



        self.get_logger().info(f"aktualni pohyb: sin={self.sinus}, cos={self.cosinus}")


    def callback(self, msg):
        self.lin_x = msg.linear.x
        self.lin_y = msg.linear.y
        self.ang_z = msg.angular.z
        #self.get_logger().info(f"Přijato Twist: lin.x={self.lin_x}, ang.z={self.lin_y}")
        self.ulozeny_cas = time.time()




def main(args=None):
    rclpy.init(args=args)
    action = Move()
    rclpy.spin(action)
    action.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()