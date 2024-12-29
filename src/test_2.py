import pygame, sys, gif_pygame

win = pygame.display.set_mode((512, 512))
example_gif = gif_pygame.load("../test.gif")  # Loads a .gif file
#example_png = gif_pygame.load("example.png")  # Loads a .png file,
# the module supports non-animated files, but it is not recommended

s1 = pygame.Surface((66, 66))
s2 = pygame.Surface((66, 66))
s3 = pygame.Surface((66, 66))
s1.fill((255, 0, 0))
s2.fill((0, 255, 0))
s3.fill((0, 0, 255))

example_surfs = gif_pygame.GIFPygame([(s1, 1), (s2, 1), (s3, 1)])

clock = pygame.time.Clock()

while True:
    clock.tick(60)
    win.fill((0, 0, 0))

    # There are 2 ways of rendering the animated img file, the first method is doing "gif.render(surface, (x, y))", the other method is doing "surface.blit(gif.blit_ready(), (x, y))". THE ".blit_ready()" FUNCTION MUST BE CALLED WHEN DOING THE SECOND METHOD
    example_gif.render(win, (128 - example_gif.get_width() * 0.5, 256 - example_gif.get_height() * 0.5))
    #example_png.render(win, (256 - example_png.get_width() * 0.5, 256 - example_png.get_height() * 0.5))
    win.blit(example_surfs.blit_ready(),
             (384 - example_surfs.get_width() * 0.5, 256 - example_surfs.get_height() * 0.5))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit();
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if example_gif.paused:  # Check whether `example_gif` is paused or not
                    example_gif.unpause()  # unpauses `example_gif` if it was paused
                else:
                    example_gif.pause()  # pauses `example_gif` if it was unpaused

                #if example_png.paused:  # Check whether `example_png` is paused or not, since this is a non-animated image, it will not be affected
                #    example_png.unpause()  # unpauses `example_png` if it was paused, since this is a non-animated image, it will not be affected
                #else:
                #    example_png.pause()  # pauses `example_png` if it was unpaused, since this is a non-animated image, it will not be affected

                if example_surfs.paused:  # Check whether `example_surfs` is paused or not
                    example_surfs.unpause()  # unpauses `example_surfs` if it was paused
                else:
                    example_surfs.pause()  # pauses `example_surfs` if it was unpaused

    pygame.display.flip()






"""
print("--------")
print(self.current_epoch)
print(map)
print(self.maps[map].name)
print(self.maps[map].epoch)
print(self.maps[map].name == self.maps[self.current_map].name, "test current map")
print(self.maps[map].epoch == self.current_epoch, "test époque")
print("--------")
"""
