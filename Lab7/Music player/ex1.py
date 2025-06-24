import pygame

pygame.init()

screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption('Pygame Music Player')

image = pygame.image.load("player.png")
image = pygame.transform.scale(image, (400, 200))

music_list = ['song1.mp3', 'song2.mp3', 'song3.mp3', 'song4.mp3', 'song5.mp3', 'song6.mp3']

SONG_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(SONG_END)

current_song_index = 0
paused = False

def play_song():
    pygame.mixer.music.load(music_list[current_song_index])
    pygame.mixer.music.play()
    print(f"Now playing: {music_list[current_song_index]}")

play_song()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        
        if event.type == SONG_END:
            current_song_index += 1
            if current_song_index >= len(music_list):
                current_song_index = 0
            play_song()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                current_song_index += 1
                if current_song_index >= len(music_list):
                    current_song_index = 0
                play_song()
            
            if event.key == pygame.K_LEFT:
               current_song_index -= 1
               if current_song_index < 0:
                    current_song_index = len(music_list) - 1
               play_song()
            
            if event.key == pygame.K_SPACE:
               if paused:
                    pygame.mixer.music.unpause()  
                    paused = False
                    print("Resumed")
               else:
                    pygame.mixer.music.pause()  
                    paused = True
                    print("Paused")

            if event.key == pygame.K_s:
                pygame.mixer.music.stop()
                print("Music stopped")

    screen.fill((255, 255, 255))
    screen.blit(image, (0, 0))
    pygame.display.flip()