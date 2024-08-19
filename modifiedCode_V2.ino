int prescaler = 256; // set this to match whatever prescaler value you set in CS registers below

// intialize values for the PWM duty cycle
float pwmDC1 = 75;  // Set duty cycle for Valve 1
float pwmDC2 = 50;  // Set duty cycle for Valve 2
float pwmDC3 = 25;  // Set duty cycle for Valve 3

float pwmFreq = 50; // Frequency for PWM

void updatePWM() {
    // Set PWM frequency by adjusting ICR
    ICR3 = F_CPU / (prescaler * pwmFreq * 2);
    ICR4 = F_CPU / (prescaler * pwmFreq * 2);
}

void sequenceTiming(){
    unsigned long interval = 1000; // Time in milliseconds for each valve to be open

    // Open Valve 1
    OCR3A = (ICR3) * (pwmDC1 * 0.01);  // Set duty cycle to open Valve 1
    delay(interval);

    // Open Valve 2
    OCR4A = (ICR4) * (pwmDC2 * 0.01);  // Set duty cycle to open Valve 2
    delay(interval);

    // Open Valve 3
    OCR4B = (ICR4) * (pwmDC3 * 0.01);  // Set duty cycle to open Valve 3
    delay(interval);

    // Turn off all valves
    OCR3A = 0;  // Close Valve 1
    OCR4A = 0;  // Close Valve 2
    OCR4B = 0;  // Close Valve 3

    // Optionally, add a delay here if you want a pause between sequences
    delay(interval);        // Delay before the next cycle begins
}

void setup() {
    Serial.begin(9600);
    pinMode(5, OUTPUT);
    pinMode(6, OUTPUT);
    pinMode(7, OUTPUT);

    // Clear and configure Timer registers for PWM
    int eightOnes = 255;  
    TCCR3A &= ~eightOnes;
    TCCR3B &= ~eightOnes;
    TCCR4A &= ~eightOnes;
    TCCR4B &= ~eightOnes;

    TCCR3A = _BV(COM3A1);
    TCCR3B = _BV(WGM33) | _BV(CS32);
    TCCR4A = _BV(COM4A1) | _BV(COM4B1);
    TCCR4B = _BV(WGM43) | _BV(CS42);

    updatePWM(); // Set initial PWM configurations
}

void loop() {
    sequenceTiming();  // Execute valve sequencing
}
