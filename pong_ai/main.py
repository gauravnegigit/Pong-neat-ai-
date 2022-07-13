from pong import Game 
import pygame  
import os 
import time 
import neat 
import pickle 


class PongGame :
    def __init__(self , window , width , height) -> None:
        self.game = Game(window , width , height)
        self.ball = self.game.ball
        self.left_paddle = self.game.left_paddle 
        self.right_paddle = self.game.right_paddle 
    
    def test_ai(self , net):
        """
        test the ait against a human player by passign a NEAT neural network
        """

        clock = pygame.time.Clock()
        run = True 
        while run :
            clock.tick(FPS)
            game_info = self.game.loop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT :
                    run = False 
                    break 
            
            output = net.activate((self.right_paddle.y , abs(self.right_paddle.x - self.ball.x) , self.ball.y))
            decision = output.index(max(output))

            if decision == 1:  # AI moves up
                self.game.move_paddle(left=False, up=True)
            elif decision == 2:  # AI moves down
                self.game.move_paddle(left=False, up=False)

            keys = pygame.key.get_pressed()

            if keys[pygame.K_w]:
                self.game.move_paddle( True , up = True )
            elif keys[pygame.K_s] :
                self.game.move_paddle( True , up = False)

            self.game.draw(draw_score = True)
            pygame.display.update()
    
    def train_ai(self , genome1 , genome2 , config , draw = True):
        """
        this method is used to train the AI by passign two NEAT neural networks and the NEAT config
        object . These AI's will play against each other to determine their fitness .
        """

        run = True 
        start_time = time.time()

        net1 = neat.nn.FeedForwardNetwork.create(genome1 , config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2 , config)
        
        self.genome1 , self.genome2 = genome1 , genome2

        max_hits = 50 

        while run :
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    quit()
            

            output1 = net1.activate((self.left_paddle.y ,  self.ball.y , abs(self.left_paddle.x - self.ball.x)))
            decision1 = output1.index(max(output1))
            

            if decision1 == 0 :
                pass 
            elif decision1 == 1:
                self.game.move_paddle(left = True , up= True)
            else :
                self.game.move_paddle(left = True , up = False)

            output2 = net2.activate((self.right_paddle.y  , self.ball.y , abs(self.right_paddle.x - self.ball.x)))
            decision2 = output2.index(max(output2))
        
            if decision2 == 0 :
                pass 
            elif decision2 == 1 :
                self.game.move_paddle(left = False , up = True)
            else :
                self.game.move_paddle(left = False , up = False)



            game_info = self.game.loop()

            '''self.move_ai_paddles(net1 , net2)'''

            if draw :
                self.game.draw(draw_score = False , draw_hits = True )
            
            pygame.display.update()

            duration = time.time() - start_time 

            if game_info.left_score == 1 or game_info.right_score == 1 or game_info.left_hits >= max_hits :
                self.calculate_fitness(genome1 , genome2 , game_info , duration)
                break 
            

        return False 
    
    def calculate_fitness(self , genome1 , genome2 , game_info , duration):
        genome1.fitness += game_info.left_hits 
        genome2.fitness += game_info.right_hits  
    
    def move_ai_paddles(self , net1 , net2):
        """
        this ethod will be used to determine where to move the left and the right paddle based on the two neural networks that control them
        """

        players = []

    def run(self ):
        clock = pygame.time.Clock()
        run = True 

        while run :
            clock.tick(FPS)
            game_info  = self.game.loop()

            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    run = False 
                    break 
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] :
                self.game.move_paddle(left = True , up = True )
            elif keys[pygame.K_s]:
                self.game.move_paddle(left = True , up = False)

            if keys[pygame.K_UP]:
                self.game.move_paddle( False , up = True )
            elif keys[pygame.K_DOWN] :
                self.game.move_paddle(False , up = False)

            self.game.draw(draw_score = False)
            pygame.display.update()

def eval_genomes(genomes , config):
    window = pygame.display.set_mode((WIDTH , HEIGHT))

    for i , (genome_id1 , genome1) in enumerate(genomes) :
        if i == len(genomes) - 1 :
            break 

        genome1.fitness = 0
        for genome_id2 , genome2 in genomes[i + 1 :]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness 
            game = PongGame(window , WIDTH , HEIGHT)
            game.train_ai(genome1 , genome2 , config)

def run_neat(config):
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes , 50)
    with open('ai.pickle' , "wb") as f :
        pickle.dump(winner , f)

def test_ai(config):
    with open("best.pickle" , "rb") as f :
        winner = pickle.load(f)
    
    
    game = PongGame(WIN , HEIGHT , HEIGHT)
    game.test_ai(winner)

if __name__ == "__main__":
    # main screen constants 
    WIDTH , HEIGHT = 1000 , 600 
    FPS = 60 
    WIN = pygame.display.set_mode((WIDTH , HEIGHT))
    '''pygame.display.set_caption("Pong game")
    
    pong = PongGame(WIN , WIDTH , HEIGHT)
    pong.run()'''

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir , "config.txt")

    config = neat.Config(neat.DefaultGenome , neat.DefaultReproduction , neat.DefaultSpeciesSet , neat.DefaultStagnation , config_path)

    #run_neat(config)
    test_ai(config)