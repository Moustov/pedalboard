# Variables
CC = /c/w64devkit/bin/cc.exe
CFLAGS = -I/c/tmp/fftw-3.3.10/api -mwindows
LDFLAGS = -L/c/tmp/fftw-3.3.10/.libs -lfftw3 -lwinmm -lgdi32
SRC = fft.c
OBJ = $(SRC:.c=.o)
TARGET = fft_display.exe

# Règle par défaut pour construire l'exécutable
all: $(TARGET)

# Règle pour lier l'exécutable
$(TARGET): $(OBJ)
	$(CC) -o $@ $^ $(LDFLAGS)

# Règle pour compiler les fichiers source en objets
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Règle pour nettoyer les fichiers générés
clean:
	rm -f $(OBJ) $(TARGET)

# Règle pour afficher un message d'aide
help:
	@echo "Utilisation : make [cible]"
	@echo "Cibles disponibles :"
	@echo "  all       - Compile l'application"
	@echo "  clean     - Supprime les fichiers objets et l'exécutable"
	@echo "  help      - Affiche ce message d'aide"