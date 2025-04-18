#include <windows.h>
#include <mmsystem.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <fftw3.h>

#define N 2048 // Taille de la FFT
#define SAMPLE_RATE 44100 // Fréquence d'échantillonnage

LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam);
void capture_audio(short *buffer, int num_samples);
void draw_fft(HDC hdc, fftw_complex *out);

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    const char CLASS_NAME[] = "FFTWindowClass";

    WNDCLASS wc = {0};
    wc.lpfnWndProc = WindowProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = CLASS_NAME;

    RegisterClass(&wc);

    HWND hwnd = CreateWindowEx(
        0, CLASS_NAME, "FFT Display",
        WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT, 1024, 600,
        NULL, NULL, hInstance, NULL
    );

    ShowWindow(hwnd, nCmdShow);
    UpdateWindow(hwnd);

    // Boucle principale
    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return 0;
}

LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    static short *buffer = NULL;
    static fftw_complex *out = NULL;
    static fftw_plan p;
    static UINT_PTR timerId = 0;

    switch (uMsg) {
        case WM_CREATE:
            buffer = (short *)malloc(N * sizeof(short));
            out = (fftw_complex *)fftw_malloc(sizeof(fftw_complex) * (N / 2 + 1));
            p = fftw_plan_dft_r2c_1d(N, (double *)buffer, out, FFTW_ESTIMATE);
            timerId = SetTimer(hwnd, 1, 500, NULL); // Timer pour mise à jour toutes les 500 ms
            break;

        case WM_TIMER:
            capture_audio(buffer, N);
            fftw_execute(p);
            InvalidateRect(hwnd, NULL, TRUE); // Redessiner la fenêtre
            break;

        case WM_PAINT: {
            PAINTSTRUCT ps;
            HDC hdc = BeginPaint(hwnd, &ps);
            draw_fft(hdc, out);
            EndPaint(hwnd, &ps);
            break;
        }

        case WM_DESTROY:
            KillTimer(hwnd, timerId);
            fftw_destroy_plan(p);
            fftw_free(out);
            free(buffer);
            PostQuitMessage(0);
            break;

        case WM_SIZE: {
            InvalidateRect(hwnd, NULL, TRUE); // Redessiner lors du redimensionnement
            break;
        }

        default:
            return DefWindowProc(hwnd, uMsg, wParam, lParam);
    }

    return 0;
}

void capture_audio(short *buffer, int num_samples) {
    static HWAVEIN hWaveIn = NULL;
    static WAVEHDR waveHeader = {0};
    static int initialized = 0;

    if (!initialized) {
        WAVEFORMATEX wfx;
        wfx.wFormatTag = WAVE_FORMAT_PCM;
        wfx.nChannels = 1; // Mono
        wfx.nSamplesPerSec = SAMPLE_RATE; // Fréquence d'échantillonnage
        wfx.wBitsPerSample = 16; // 16 bits par échantillon
        wfx.nBlockAlign = wfx.nChannels * wfx.wBitsPerSample / 8;
        wfx.nAvgBytesPerSec = wfx.nSamplesPerSec * wfx.nBlockAlign;

        waveInOpen(&hWaveIn, WAVE_MAPPER, &wfx, 0, 0, CALLBACK_NULL);
        initialized = 1;
    }

    waveHeader.lpData = (LPSTR)buffer;
    waveHeader.dwBufferLength = num_samples * sizeof(short);
    waveHeader.dwFlags = 0;

    waveInPrepareHeader(hWaveIn, &waveHeader, sizeof(WAVEHDR));
    waveInAddBuffer(hWaveIn, &waveHeader, sizeof(WAVEHDR));

    waveInStart(hWaveIn);
    waveInStop(hWaveIn);
    waveInUnprepareHeader(hWaveIn, &waveHeader, sizeof(WAVEHDR));
}

void draw_fft(HDC hdc, fftw_complex *out) {
    double max_amplitude = 0;

    // Calculer la magnitude et trouver la magnitude maximale
    for (int i = 0; i < N / 2; i++) {
        double amplitude = sqrt(out[i][0] * out[i][0] + out[i][1] * out[i][1]);
        if (amplitude > max_amplitude) {
            max_amplitude = amplitude;
        }
    }

    // Dessiner les axes en rouge
    HPEN redPen = CreatePen(PS_SOLID, 2, RGB(255, 0, 0));
    SelectObject(hdc, redPen);

    // Dessiner les axes
    MoveToEx(hdc, 0, 600, NULL); // Axe X
    LineTo(hdc, 1024, 600);
    MoveToEx(hdc, 0, 0, NULL); // Axe Y
    LineTo(hdc, 0, 600);

    // Dessiner les graduations et les étiquettes sur l'axe X
    for (int i = 0; i <= 20; i++) { // 20 graduations pour 20 kHz
        int x = (1024 * i) / 20; // Position des graduations
        double frequency = (double)i * (SAMPLE_RATE / N);
        char label[20];
        sprintf(label, "%.1f", frequency);
        TextOut(hdc, x, 610, label, strlen(label));
    }

    // Dessiner la courbe
    for (int i = 0; i < N / 2; i++) {
        double amplitude = sqrt(out[i][0] * out[i][0] + out[i][1] * out[i][1]);
        int x = (1024 * i) / (N / 2); // Échelle pour l'axe X
        int height = (int)(amplitude / (max_amplitude + 1e-10) * 300); // Ajout d'un petit epsilon
        MoveToEx(hdc, x, 600, NULL);
        LineTo(hdc, x, 600 - height);
    }

    // Libérer le stylo rouge
    DeleteObject(redPen);
}