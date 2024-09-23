#include <Servo.h>

Servo servo1;
Servo servo2;

void setup() {
  Serial.begin(9600);
  
  // Attach the servos to pins 9 and 10
  servo1.attach(10);
  servo2.attach(9);
}

void moveServo(Servo &servo, int angle) {
  // Clamp the angle between 0 and 180 degrees
  angle = constrain(angle, 0, 180);
  servo.write(angle);  // Move the servo to the specified angle
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim();

    if (input.startsWith("a;") && input.indexOf(", b;") != -1) {
      String angle1_str = input.substring(2, input.indexOf(","));
      String angle2_str = input.substring(input.indexOf(", b;") + 4);

      int angle1 = angle1_str.toInt();
      int angle2 = angle2_str.toInt();

      moveServo(servo1, angle1);  // Move servo 1
      moveServo(servo2, angle2);  // Move servo 2

      Serial.print("Moving servos to angles: ");
      Serial.print(angle1);
      Serial.print(" and ");
      Serial.println(angle2);
    }
  }

  delay(20);  // Small delay for stability
}
