import time
           
from Motor import *            
PWM=Motor()          
def test_Motor(): 
    try:
        PWM.setMotorModel(1000,1000,1000,1000)       #Forward
        print ("The car is moving forward")
        time.sleep(1)
        PWM.setMotorModel(-1000,-1000,-1000,-1000)   #Back
        print ("The car is going backwards")
        time.sleep(1)
        PWM.setMotorModel(-1500,-1500,2000,2000)       #Left 
        print ("The car is turning left")
        time.sleep(1)
        PWM.setMotorModel(2000,2000,-1500,-1500)       #Right 
        print ("The car is turning right")  
        time.sleep(1)
        PWM.setMotorModel(0,0,0,0)                   #Stop
        print ("\nEnd of program")
    except KeyboardInterrupt:
        PWM.setMotorModel(0,0,0,0)
        print ("\nEnd of program")
           
# Main program logic follows:
if __name__ == '__main__':

    print ('Program is starting ... ')
    import sys
    if len(sys.argv)<2:
        print ("Parameter error: Please assign the device")
        exit()
    if sys.argv[1] == 'Motor':
        test_Motor()              
        
        
        
        
