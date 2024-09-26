class Settings:
    ### A class to store all settings for Alien Invasion. """

    def __init__(self):
        """Initialize game settings"""
        # Screen Settings
        self.image = None
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)

        # Ship settings
        self.ship_speed = 20

        # Bullet settings
        self.ship_bullet_speed = 2.0
        self.ship_bullet_width = 5
        self.ship_bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Meteors settings
        self.meteor_speed = 2
        self.meteor_max = 2

        # Alien settings
        self.alien_points = 30
        self.alien_speed = 1.0
        self.bullet_max = 6
        self.alien_bullet_speed = 2.0
        self.alien_bullet_width = 5
        self.alien_bullet_height = 15
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1
        self.ship_limit = 3

        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game"""
        self.ship_speed = 1.5
        self.ship_bullet_speed = 3.0
        self.alien_speed = 1.0

        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings and alien point values"""
        self.ship_speed *= self.speedup_scale
        self.ship_bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)

    def update_fire_rate(self):
        self.bullets_allowed += 2

    def update_ship_speed(self):
        self.ship_speed =+ 3

    def update_bullet_speed(self):
        self.ship_bullet_speed += 2

    def update_bullet_type(self):
        pass


