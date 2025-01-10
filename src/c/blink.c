#include <pigpio.h>
#include <stdio.h>
#define LED_PIN 17  // Numéro de broche GPIO


int main(void) {
    // Initialisation de pigpio
    if (gpioInitialise() < 0) {
        printf("Erreur d'initialisation de pigpio\n");
        return 1;
    }

    // Définir le mode de la broche en sortie
    gpioSetMode(LED_PIN, PI_OUTPUT);
    while (1) {
        // Allumer la LED
        gpioWrite(LED_PIN, 1);
        gpioDelay(500000);  // Attendre 500 ms

        // Éteindre la LED
        gpioWrite(LED_PIN, 0);
        gpioDelay(500000);  // Attendre 500 ms
    }

    // Terminer pigpio
    gpioTerminate();
    return 0;
}