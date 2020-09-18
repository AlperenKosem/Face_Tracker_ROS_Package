/*
 * rosserial Servo Control Example
 *
 * This sketch demonstrates the control of hobby R/C servos
 * using ROS and the arduiono
 * 
 * For the full tutorial write up, visit
 * www.ros.org/wiki/rosserial_arduino_demos
 *
 * For more information on the Arduino Servo Library
 * Checkout :
 * http://www.arduino.cc/en/Reference/Servo
 */

 // rosrun rosserial_python serial_node.py /dev/ttyUSB0

#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include <WProgram.h>
#endif

#include <Servo.h> 
#include <ros.h>
#include <std_msgs/Int16.h>

ros::NodeHandle  nh;

Servo servo;

void servo_cb( const std_msgs::Int16& cmd_msg){
  servo.write(cmd_msg.data); //set servo angle, should be from 0-180  
  
}


ros::Subscriber<std_msgs::Int16> sub("/servo_controller", servo_cb);

void setup(){
  

  nh.initNode();
  nh.subscribe(sub);
  
  servo.attach(3); //attach it to pin 3
}


void loop(){
  nh.spinOnce();
  delay(1);
}
