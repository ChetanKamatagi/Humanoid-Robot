#include <ros.h>
#include <ros/time.h>
#include <geometry_msgs/Vector3Stamped.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

float z;
uint16_t BNO055_SAMPLERATE_DELAY_MS = 100;

// Check I2C device address and correct line below (by default address is 0x29 or 0x28)
//                                   id, address
Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x28, &Wire);
ros::NodeHandle  nh; 

#define leftEncoderPinA 18
#define leftEncoderPinB 19 

#define rightEncoderPinA 2
#define rightEncoderPinB 3

volatile long encoder0Pos = 0;
volatile long encoder1Pos = 0;

geometry_msgs::Vector3Stamped motors_ticks_msg;

ros::Publisher motors_tick_pub("motors_ticks", &motors_ticks_msg);

void setup() {
  encoder0Pos = 0;
  encoder1Pos = 0;
  Serial.begin(115200);
  nh.initNode();    
  nh.getHardware()->setBaud(115200);
  nh.advertise(motors_tick_pub);
  bno.begin();
  attachInterrupt(digitalPinToInterrupt(leftEncoderPinA), change_left_a, CHANGE);
  attachInterrupt(digitalPinToInterrupt(leftEncoderPinB), change_left_b, CHANGE);
  attachInterrupt(digitalPinToInterrupt(rightEncoderPinA), change_right_a, CHANGE);
  attachInterrupt(digitalPinToInterrupt(rightEncoderPinB), change_right_b, CHANGE);
}

void loop() {
  
  
  
  motors_ticks_msg.vector.x = encoder0Pos;
  
  motors_ticks_msg.vector.y = -1*encoder1Pos;
  Serial.println(encoder0Pos);
  Serial.println(encoder1Pos);
  sensors_event_t orientationData;
  bno.getEvent(&orientationData, Adafruit_BNO055::VECTOR_EULER);
  z=printEvent(&orientationData);
  motors_ticks_msg.vector.z = z;
  motors_tick_pub.publish(&motors_ticks_msg);
  nh.spinOnce();
  delay(20);
}

//**************IMU*****************//
float printEvent(sensors_event_t* event) {
  double z = -1000000; //dumb values, easy to spot problem
  if (event->type == SENSOR_TYPE_ORIENTATION) {

    z = event->orientation.x;
  }
return z;
}





// ************** encoders interrupts **************

// ************** encoder 1 *********************


void change_left_a(){  

  // look for a low-to-high on channel A
  if (digitalRead(leftEncoderPinA) == HIGH) { 
    // check channel B to see which way encoder is turning
    if (digitalRead(leftEncoderPinB) == LOW) {  
      encoder0Pos = encoder0Pos + 1;         // CW
    } 
    else {
      encoder0Pos = encoder0Pos - 1;         // CCW
    }
  }
  else   // must be a high-to-low edge on channel A                                       
  { 
    // check channel B to see which way encoder is turning  
    if (digitalRead(leftEncoderPinB) == HIGH) {   
      encoder0Pos = encoder0Pos + 1;          // CW
    }
    else {
      encoder0Pos = encoder0Pos - 1;          // CCW
    }
  }
 
}

void change_left_b(){  

  // look for a low-to-high on channel B
  if (digitalRead(leftEncoderPinB) == HIGH) {   
   // check channel A to see which way encoder is turning
    if (digitalRead(leftEncoderPinA) == HIGH) {  
      encoder0Pos = encoder0Pos + 1;         // CW
    } 
    else {
      encoder0Pos = encoder0Pos - 1;         // CCW
    }
  }
  // Look for a high-to-low on channel B
  else { 
    // check channel B to see which way encoder is turning  
    if (digitalRead(leftEncoderPinA) == LOW) {   
      encoder0Pos = encoder0Pos + 1;          // CW
    } 
    else {
      encoder0Pos = encoder0Pos - 1;          // CCW
    }
  }
  

}

// ************** encoder 2 *********************

void change_right_a(){  

  // look for a low-to-high on channel A
  if (digitalRead(rightEncoderPinA) == HIGH) { 
    // check channel B to see which way encoder is turning
    if (digitalRead(rightEncoderPinB) == LOW) {  
      encoder1Pos = encoder1Pos - 1;         // CW
    } 
    else {
      encoder1Pos = encoder1Pos + 1;         // CCW
    }
  }
  else   // must be a high-to-low edge on channel A                                       
  { 
    // check channel B to see which way encoder is turning  
    if (digitalRead(rightEncoderPinB) == HIGH) {   
      encoder1Pos = encoder1Pos - 1;          // CW
    } 
    else {
      encoder1Pos = encoder1Pos + 1;          // CCW
    }
  }
 
}

void change_right_b(){  

  // look for a low-to-high on channel B
  if (digitalRead(rightEncoderPinB) == HIGH) {   
   // check channel A to see which way encoder is turning
    if (digitalRead(rightEncoderPinA) == HIGH) {  
      encoder1Pos = encoder1Pos - 1;         // CW
    } 
    else {
      encoder1Pos = encoder1Pos + 1;         // CCW
    }
  }
  // Look for a high-to-low on channel B
  else { 
    // check channel B to see which way encoder is turning  
    if (digitalRead(rightEncoderPinA) == LOW) {   
      encoder1Pos = encoder1Pos - 1;          // CW
    } 
    else {
      encoder1Pos = encoder1Pos + 1;          // CCW
    }
  }
  

}
