#include <stdio.h>
#include <wiringPi.h>

void scanButton (int button)
{
  int once;
  if (digitalRead (button) == HIGH)
        once = 0;
  while (digitalRead (button) == LOW)   // Low is pushed
    if (once ==0) {
        printf("Button: %d\n", button);
        switch(button)
        {
            case 1:
            system ("sh /home/pi/psd/resetwifi.sh");
            break;
            case 2:
            system ("sudo python /home/pi/psd/wifi.py");
            break;
            case 3:
            system ("sudo python /home/pi/psd/scanner.py");
            break;
        }
        once = 1;
    }
}

int main (void)
{
  int i ;
  wiringPiSetup () ;

  for (i = 1 ; i < 4 ; ++i)  {
    pinMode         (i, INPUT) ;
    pullUpDnControl (i, PUD_UP) ;
    printf ("pin set: %d\n", i) ;
  }
  for (;;)  {
    for (i = 1 ; i < 4 ; ++i)
      scanButton (i) ;
    delay (1) ;
  }
}
