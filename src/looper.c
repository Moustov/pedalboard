#include <stdio.h>
#include <stdlib.h>
#include <portaudio.h>
#include <string.h>
#include <wiringPi.h>

#define SAMPLE_RATE 44100
#define FRAMES_PER_BUFFER 256
#define LOOPER_DURATION 5 // Durée d'enregistrement en secondes
#define BUTTON_PIN 0 // Numéro du GPIO pour le bouton (WiringPi)
#define MCP3008_CS_PIN 8 // GPIO pour CS du MCP3008
#define POT_CHANNEL 0 // Canal du potentiomètre

float *buffer;
int bufferSize;
int writeIndex = 0;
int isRecording = 0;

// Prototypes
int readADC(int channel);

// Callback pour le traitement audio
static int audioCallback(const void *inputBuffer, void *outputBuffer,
                         unsigned long framesPerBuffer,
                         const PaStreamCallbackTimeInfo *timeInfo,
                         PaStreamCallbackFlags statusFlags,
                         void *userData) {
    float *in = (float *)inputBuffer;
    float *out = (float *)outputBuffer;
    unsigned long i;

    (void)timeInfo; // Supprimer les avertissements de compilateur
    (void)statusFlags;

    for (i = 0; i < framesPerBuffer; i++) {
        if (isRecording) {
            // Enregistrer dans le buffer
            buffer[writeIndex] = *in++;
            writeIndex = (writeIndex + 1) % bufferSize; // Gérer l'index
        } else {
            // Lire depuis le buffer
            *out++ = buffer[(writeIndex + i) % bufferSize]; // Lecture en boucle
        }
    }
    return paContinue;
}

// inits the GPIO
void setupGPIO() {
    wiringPiSetup(); // Initialiser WiringPi
    pinMode(BUTTON_PIN, INPUT); // Configurer le pin du bouton en entrée
    pullUpDnControl(BUTTON_PIN, PUD_UP); // Activer la résistance pull-up
    pinMode(MCP3008_CS_PIN, OUTPUT);
    digitalWrite(MCP3008_CS_PIN, HIGH); // Désactiver le MCP3008
}

// reads the analog sound signal from the potentiometer to set the output level
int readADC(int channel) {
    unsigned char buff[3];

    digitalWrite(MCP3008_CS_PIN, LOW); // Activer le MCP3008
    buff[0] = 1; // Start bit
    buff[1] = (8 + channel) << 4; // Configurer le canal
    buff[2] = 0; // Dummy byte

    wiringPiSPIDataRW(0, buff, 3); // Envoyer et recevoir des données
    digitalWrite(MCP3008_CS_PIN, HIGH); // Désactiver le MCP3008

    return ((buff[1] & 3) << 8) + buff[2]; // Récupérer la valeur
}

int main() {
    PaError err;

    // Initialiser PortAudio
    err = Pa_Initialize();
    if (err != paNoError) {
        fprintf(stderr, "PortAudio Error: %s\n", Pa_GetErrorText(err));
        return -1;
    }

    bufferSize = SAMPLE_RATE * LOOPER_DURATION; // Taille du buffer
    buffer = (float *)calloc(bufferSize, sizeof(float)); // Allouer le buffer

    PaStream *stream;
    // Ouvrir un flux audio
    err = Pa_OpenDefaultStream(&stream,
                               1, // entrée stéréo
                               1, // sortie stéréo
                               paFloat32, // format
                               SAMPLE_RATE,
                               FRAMES_PER_BUFFER,
                               audioCallback,
                               NULL); // données utilisateur
    if (err != paNoError) {
        fprintf(stderr, "PortAudio Error: %s\n", Pa_GetErrorText(err));
        return -1;
    }

    // Initialiser le GPIO
    setupGPIO();

    // Démarrer le flux
    err = Pa_StartStream(stream);
    if (err != paNoError) {
        fprintf(stderr, "PortAudio Error: %s\n", Pa_GetErrorText(err));
        return -1;
    }

    printf("Appuyez sur le bouton pour démarrer l'enregistrement.\n");

    while (1) {
        // Lire la valeur du potentiomètre
        int potValue = readADC(POT_CHANNEL);
        float potLevel = potValue / 1023.0; // Normaliser entre 0 et 1
        printf("Niveau du potentiomètre : %.2f\n", potLevel);

        // Vérifier si le bouton est pressé
        if (digitalRead(BUTTON_PIN) == LOW) { // Si le bouton est pressé
            if (!isRecording) {
                isRecording = 1; // Commencer l'enregistrement
                printf("Enregistrement en cours...\n");
            } else {
                isRecording = 0; // Arrêter l'enregistrement
                printf("Enregistrement arrêté. Lecture en boucle...\n");
            }
            // Attendre que le bouton soit relâché
            while (digitalRead(BUTTON_PIN) == LOW);
            delay(200); // Délai pour éviter le rebond
        }
        delay(100); // Délai pour éviter une lecture trop rapide
    }

    // Arrêter et fermer le flux
    err = Pa_StopStream(stream);
    if (err != paNoError) {
        fprintf(stderr, "PortAudio Error: %s\n", Pa_GetErrorText(err));
    }

    err = Pa_CloseStream(stream);
    if (err != paNoError) {
        fprintf(stderr, "PortAudio Error: %s\n", Pa_GetErrorText(err));
    }

    // Libérer la mémoire et terminer PortAudio
    free(buffer);
    Pa_Terminate();
    return 0;
}