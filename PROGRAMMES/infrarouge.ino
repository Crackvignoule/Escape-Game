/*
   ROBERT NICOLAS, PAVY KILLIAN, FOURNIER JEREMY
*/

/*
   Ce programme allume une LED branché sur la PIN 11 quand le recepteur infrarouge est actif.
*/

#include <IRremote.h>

int broche_reception = 11; // broche 11 utilisée
IRrecv reception_ir(broche_reception); // crée une instance
decode_results decode_ir; // stockage données reçues

void setup()
{
  Serial.begin(9600);
  pinMode(3, OUTPUT);
  reception_ir.enableIRIn(); // démarre la réception
}
void loop()
{
  if (reception_ir.decode(&decode_ir))
  {
    digitalWrite(3, HIGH);
    Serial.println(decode_ir.value, HEX);
    reception_ir.resume(); // reçoit le prochain code
    delay(250);
    digitalWrite(3, LOW);
  }

}
