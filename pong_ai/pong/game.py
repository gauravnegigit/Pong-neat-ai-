from .paddle import Paddle 
from .ball import Ball 
import pygame 
pygame.init()

class GameInfo :
    def __init__(self , left_hits , right_hits , left_score , right_score) -> None:
        self.left_hits = left_hits
        self.right_hits = right_hits
        self.left_score = left_score
        self.right_score = right_score 
    

class Game :
    """
    Thi class is used to initialize and instance and call the .loop() method to run the game .
    """

    SCORE_FONT = pygame.font.SysFont("comicsans", 50)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0 , 0 , 255)
    GREEN = (0 , 255 , 0)
    RED = (255, 0, 0)

    def __init__(self , window , window_width , window_height) -> None:
        self.window_width = window_width
        self.window_height = window_height 

        # creating the main component objects of teh game 
        self.left_paddle = Paddle(10 , self.window_height//2 - Paddle.HEIGHT //2)
        self.right_paddle = Paddle(self.window_width - 10 - Paddle.WIDTH , self.window_height // 2- Paddle.HEIGHT//2)
        self.ball = Ball(self.window_width // 2 , self.window_height//2)
    
        self.left_score = 0
        self.right_score = 0
        self.left_hits = 0
        self.right_hits = 0
        self.window = window
    
    def _draw_score(self):
        left_score_text = self.SCORE_FONT.render(
            f"{self.left_score}", 1, self.WHITE)
        right_score_text = self.SCORE_FONT.render(
            f"{self.right_score}", 1, self.WHITE)
        self.window.blit(left_score_text, (self.window_width //
                                           4 - left_score_text.get_width()//2, 20))
        self.window.blit(right_score_text, (self.window_width * (3/4) -
                                            right_score_text.get_width()//2, 20))

    # these below functions are made private because they are not called outside the class  

    def _draw_divider(self):
        for i in range(0 , self.window_height , self.window_height//20):
            if i % 2 == 1 :
                continue 

            pygame.draw.rect(self.window , self.BLACK, (self.window_width//2 - 5 , i , 10 , self.window_height // 20 - 10))

    def _draw_hits(self):
        hits_text = self.SCORE_FONT.render(
            f"{self.left_hits + self.right_hits}", 1, self.RED)
        self.window.blit(hits_text, (self.window_width // 2 - hits_text.get_width()//2, 10))
    
    def _handle_collision(self):
        ball = self.ball 
        left_paddle = self.left_paddle
        right_paddle = self.right_paddle 

        if ball.y + ball.RADIUS >= self.window_height :
            ball.y_vel *= -1 
        
        elif ball.y - ball.RADIUS <= 0 :
            ball.y_vel *= - 1
        
        #middle_y = 0 

        collide = False 

        if ball.x_vel < 0 :
            if (ball.y >= left_paddle.y and ball.y <= left_paddle.y + Paddle.HEIGHT) and (ball.x - ball.RADIUS <= left_paddle.x + Paddle.WIDTH) :
                
                middle_y = left_paddle.y + Paddle.HEIGHT / 2
                self.left_hits += 1

                collide = True 
        
        else :
            if (ball.y >= right_paddle.y and ball.y <= right_paddle.y + Paddle.HEIGHT) and (ball.x + ball.RADIUS >= right_paddle.x) :
                middle_y = right_paddle.y + Paddle.HEIGHT / 2
                self.right_hits += 1

                collide = True 
        
        if collide : 
            ball.x_vel *= -1 
            dy = middle_y - ball.y 
            reduction_factor = (Paddle.HEIGHT / 2) / ball.MAX_VEL 
            y_vel = dy / reduction_factor
            ball.y_vel = -1 * y_vel 
    
    def draw(self , draw_score = True , draw_hits = True) :
        self.window.fill(self.GREEN)
        self._draw_divider()

        if draw_score :
            self._draw_score()
        else :
            self._draw_hits()
        
        for paddle in [self.left_paddle , self.right_paddle]:
            paddle.draw(self.window , self.BLUE)
        
        self.ball.draw(self.window)
    
    def move_paddle(self , left  , up = True ):
        """
        moves the eft and irght paddle
        """

        if left:
            if up and self.left_paddle.y - Paddle.VEL < 0:
                return False
            if not up and self.left_paddle.y + Paddle.HEIGHT > self.window_height:
                return False
            self.left_paddle.move(up)
        else:
            if up and self.right_paddle.y - Paddle.VEL < 0:
                return False
            if not up and self.right_paddle.y + Paddle.HEIGHT > self.window_height:
                return False
            self.right_paddle.move(up)

        return True

    def loop(self):
        """
        this method helps to provide updated game_info to the test_ai method in main.py file 
        """

        self.ball.move()
        self._handle_collision()

        if self.ball.x < 0:
            self.ball.reset()
            self.right_score += 1
        elif self.ball.x > self.window_width:
            self.ball.reset()
            self.left_score += 1

        game_info = GameInfo(
            self.left_hits, self.right_hits, self.left_score, self.right_score)

        return game_info


    def reset(self):
        """
        this method resets the whoel game
        """
        self.ball.reset()
        self.left_paddle.reset()
        self.right_paddle.reset()
        self.left_score = 0
        self.right_score = 0
        self.left_hits = 0
        self.right_hits = 0