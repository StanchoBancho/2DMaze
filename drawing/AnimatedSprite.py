import pygame


class AnimatedSprite(pygame.sprite.Sprite):
    #currently this len(left_images) == len(right_images) should be true
    def __init__(self, left_images, right_images, fps=15):
        pygame.sprite.Sprite.__init__(self)
        self.left_images = left_images
        self.right_images = right_images
        self.is_direction_left = False
        self.is_moving = False
        # Track the time we started, and the time between updates.
        # Then we can figure out when we have to switch the image.
        self._start = pygame.time.get_ticks()
        self._delay = 1000 / fps
        self._last_update = 0
        self._frame = 0
        # Call update to set our first image.
        self.update(pygame.time.get_ticks())

    def update(self, t):
        # Note that this doesn't work if it's been more that self._delay
        # time between calls to update(); we only update the image once
        # then, but it really should be updated twice.
        if t - self._last_update > self._delay:
            if not self.is_moving:
                if self.is_direction_left:
                    self.image = self.left_images[0]
                else:
                    self.image = self.right_images[0]
            else:
                self._frame += 1
                if self._frame >= len(self.left_images):
                    self._frame = 0
                if self.is_direction_left:
                    self.image = self.left_images[self._frame]
                else:
                    self.image = self.right_images[self._frame]
            self._last_update = t
