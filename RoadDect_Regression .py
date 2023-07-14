# Hello World Example
#
# Welcome to the OpenMV IDE! Click on the green run arrow button below to run the script!

import time, image,sensor,math,pyb,ustruct

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.GRAYSCALE) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QQQVGA)   # Set frame size to QVGA (320x240)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
uart = pyb.UART(3, 115200, timeout_char = 1000)     #定义串口3变量

clock = time.clock()                # Create a clock object to track the FPS.
thresholds = (0, 50)

#roi_c = (144,10,32,44)
#roi_l = (66,10,32,42)
#roi_r = (230,10,32,46)

while(True):
    img = sensor.snapshot()
    clock.tick()                    # Update the FPS clock.
    Find_Flag=0
    buchang = 0

    line = img.get_regression([(0,50)], robust = True)
    if (line):
        rho_err = abs(line.rho())-img.width()/2
        if line.theta()>90:
            theta_err = line.theta()-180
        else:
            theta_err = line.theta()
        img.draw_line(line.line(), color = 127)
        print(rho_err,line.magnitude(),rho_err)



    print("路口类型",Find_Flag)    #0，1是直行，2是左转，3是右转，4是T路口
    print("补偿",buchang)         #1是右补偿，2是左补偿
    if (Find_Flag <= 1):
        FH = bytearray([0x2C,0x12,buchang,0,1,3,0x5B])
        uart.write(FH)
    else:
        FH = bytearray([0x2C,0x12,buchang,0,1,3,0x5B])
        uart.write(FH)
    print(clock.fps())
