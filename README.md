# AirplaneHudPY

### Create python env ###
python3 -m venv venv
source ./venv/bin/activate

### Project planning ###
1 - wire MMA8452Q with RPi
2 - wire ADXL345 with RPi
4 - wire OLED
3 - Interface accelerometer/ with socketIO to get the attitude of the aircraft on OLED
5 - Build AI module in another python page. It will do image detection and return position of the object detect to the socketio service
6 - Use dotnet project to wire everything together. You will have control over the buttons of the board.
        -joystick up / down to calibrate the horizontal alignement
        -turn on/off oled
        
