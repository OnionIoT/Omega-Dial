// analog pin for reading the potentiometer value
int potPin = A0;

// resistance value
int potValue = 0;

// delay between sensor reads for stability
int readDelay = 100;

// code to be run once at the start of the program
void setup() 
{
  // initializing serial communication for sending potentiometer value to the Omega
  Serial.begin(9600);
}

// read the potentiometer output as an angle between 0 and 179 and send the end result to the Omega
void readPotValue()
{
  potValue = analogRead(potPin);
  Serial.println(potValue);
  // delay between reads for stability
  delay(readDelay);
}

// continuously read the potentiometer and set the Angle  
void loop() 
{
  readPotValue();
}
