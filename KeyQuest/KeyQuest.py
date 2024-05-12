import random
import copy
from tkinter import *


class DDR(Tk):
    def __init__(self):
        super().__init__()
        #self.resizable(width=0,height=0)

        #Sets difficulty of the game, default is "easy"
        self.difficulty = "easy" 
        
        #Creates dictionary of 3 difficulties and their settings
        self.difficulty_settings = {"easy":[2,1],"medium":[3,2],"hard":[8,1]} 
        '''The rate at which arrows created in each difficulty scales linearly with 
        time and changes based on the difficulty selected. 
        Let the value of a difficulty mode be [a,b]. This means that (a-b) arrows 
        will be created every second at the start of the game. This rate will 
        linearly scale with time to (a) arrows per second at the end of the game.
        '''
        #Import icon for the game
        self.window_icon=PhotoImage(file="window_icon.png")
        self.iconphoto(False,self.window_icon)
        
        # Empty string for player name
        self.player_name="" 
    
    
    #Starts the game window with input options for user name and difficulty    
    def arena(self):
        #Sets name of game
        self.title("Key Quest")

        #Sets size of game window
        self.geometry("1366x1080") 
        
        #Gets user input as player name
        self.player_name=self.entry.get()
        print(self.player_name)

        #Set background imagets game window background
        self.background_image=PhotoImage(file="background.png")

        #Set ts arrow spawn background
        self.column_image = PhotoImage(file="column.png")
        
        #Creates label to display background image
        background_label = Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        #Default game variables
        self.total_score = 0
        self.game_duration = 30
        self.arrow_interval=1000
        
        #Create dictionary to set arrow appearance 
        self.arrow_images = {
            "Up": PhotoImage(file="up.png"),
            "Down": PhotoImage(file="down.png"),
            "Left": PhotoImage(file="left.png"),
            "Right": PhotoImage(file="right.png"),
        }

        #Create label score display
        self.shown_score = Label(self, text="Score:{}".format(self.total_score))
        self.shown_score.pack(pady=10)

        #Create label timer display
        self.timer_label = Label(self, text="Time: {}".format(self.game_duration))
        self.timer_label.pack(pady=10)

        #Create frame for arrow spawn areas
        self.top_frame = Frame(self)
        self.top_frame.pack()
        
        #Create spwan area for Left arrow column
        self.area1 = Canvas(self.top_frame, width=150, height=600, bg="#FFFFFF")
        self.area1.create_image(0, 0, anchor="nw", image=self.column_image)
        self.area1.pack(side='left', padx=0, pady=0)
        
        #Create spwan area for Down arrow column
        self.area2 = Canvas(self.top_frame, width=150, height=600, bg="#FFFFFF")
        self.area2.create_image(0, 0, anchor="nw", image=self.column_image)
        self.area2.pack(side='left', padx=0, pady=0)

        #Create spwan area for Up arrow column
        self.area3 = Canvas(self.top_frame, width=150, height=600, bg="#FFFFFF")
        self.area3.create_image(0, 0, anchor="nw", image=self.column_image)
        self.area3.pack(side='left', padx=0, pady=0)

        #Create spwan area for Right arrow column
        self.area4 = Canvas(self.top_frame, width=150, height=600, bg="#FFFFFF")
        self.area4.create_image(0, 0, anchor="nw", image=self.column_image)
        self.area4.pack(side='left', padx=0, pady=0)
        
        #Creates dictionary to set spawn area column for specific arrow type
        self.arrow_area = {"Left": self.area1, "Down": self.area2, "Up": self.area3, "Right": self.area4}

        #Create empty list for arrow
        self.arrow = []
        
        #Set arrow spwan speed
        self.arrow_speed = 15

        #Starts gameplay
        self.start_game()
        self.mainloop()

    ##Randomly creates arrow in the 4 columns and changes gameplay accordingly with difficulty, ends game when timer hits 0 
    def spawn_arrow(self):
        #if timer is above 0, continue spwawning arrows
        if self.game_duration > 0:

            #Create list of the 4 arrow types
            arrow_types = ["Up", "Down", "Left", "Right"]

            #Randomly select one of the arrow types
            arrow_choice = random.choice(arrow_types)

            #Specify the area of randomly selected arrow to spawn at
            arrow_spawn_area = self.arrow_area[arrow_choice]

            # Create image of spawned arrow
            arrow = arrow_spawn_area.create_image(75, 0, image=self.arrow_images[arrow_choice], anchor="center", tags=arrow_types)

            #
            self.arrow.append({"id": arrow, "type": arrow_choice, "spawn_area": arrow_spawn_area})

            #Modify arrow spawning intervally accordingly to setting selected and time remaining
            self.arrow_interval=int(1000/(self.difficulty_settings[self.difficulty][0]-self.difficulty_settings[self.difficulty][1]*(self.game_duration/45)))
            self.after(self.arrow_interval, self.spawn_arrow)
            self.game_duration -= self.arrow_interval/1000
            self.timer_label.config(text="Time: {:.0f}".format(abs(self.game_duration)))
        
        #When timer is not above 0, stops spawning arrows and shows game over screen
        else:
            self.game_over()

    #Gameover Screen 
    def game_over(self):
        # Clean up game elements
        for arrow in self.arrow:
            arrow["spawn_area"].delete(arrow["id"])
        self.arrow = []

        # Display game-over message
        game_over_label = Label(self, text="Game Over", font=("Helvetica", 36), fg="red")
        game_over_label.pack()

        # Optionally, display final score or other relevant information
        final_score_label = Label(self, text="Final Score: {}".format(self.total_score), font=("Helvetica", 24))
        final_score_label.pack()
        self.update_highscores()
        button1 = Button(self, text='Back to Menu', width=25, command=self.gotoIntro)
        button1.pack()
        button1.place(x=20, y=20)

    #Resets game screen
    def gotoIntro(self):
        #Destroys current window
        self.destroy()

        #Recreates game object
        game = DDR()

        #Display intro screen
        game.IntroPage()
        
    def move_arrows(self):
        arrows_to_remove = []

        for arrow in copy.copy(self.arrow):
            arrow_id = arrow["id"]
            arrow_spawn_area = arrow["spawn_area"]

            arrow_spawn_area.move(arrow_id, 0, self.arrow_speed)
            
            #Check if arrow has gone past play area
            if arrow_spawn_area.coords(arrow_id)[1] > 600: 
                arrow_spawn_area.delete(arrow_id)
                arrows_to_remove.append(arrow)

        for arrow in arrows_to_remove:
            self.arrow.remove(arrow) #remove arrow
            self.total_score -= 1 #deduct point 
            self.update_score() #update scoreboard

        if self.game_duration>0:
            self.after(30, self.move_arrows) 

    def update_score(self):
        self.shown_score.config(text="Score: {}".format(self.total_score)) #update scoreboard

    def input(self, event):
        input_key = event.keysym
        for arrow in copy.copy(self.arrow): #iterate through existing arrows
            arrow_id = arrow["id"]
            arrow_type = arrow["type"]
            arrow_spawn_area = arrow["spawn_area"]
            arrow_coord = arrow_spawn_area.coords(arrow["id"])

            if 500 < arrow_coord[1] < 600: #check if arrow is in scoring zone
                if arrow_type == input_key: #check if appropriate key is pressed
                    arrow_spawn_area.delete(arrow_id) #remove arrow
                    self.arrow.remove(arrow)
                    self.total_score += 1 #add score
                    self.update_score() #update scoreboard

    def start_game(self):
        self.bind("<Up>", self.input) #set keybinds
        self.bind("<Down>", self.input) 
        self.bind("<Left>", self.input) 
        self.bind("<Right>", self.input) 
        self.spawn_arrow()
        self.move_arrows()

    def which_button(self,button_press): 
        self.difficulty = button_press #set game difficulty
        self.label1.configure(text="You have selected: "+button_press+" difficulty") #display chosen difficulty
        
    def IntroPage(self): #main menu
        self.title("Introduction") #window title
        self.geometry("600x500") #window size

        self.label1 = Label(text="Key Quest", font=("Helvetica", 24)) #welcome text
        self.label1.pack()
        label = Label(text="Name") #username entry label
        label.pack()
        self.entry = Entry() #username entry widget
        self.entry.pack()
        self.entry.insert(END, "Your name") #default username
        button1 = Button(self, text='Start', width=25, command=self.arena) #start button
        button1.pack()
        easy = Button(self, text='Easy', width=25, command=lambda m="easy": self.which_button(m)) #difficulty selection button
        easy.pack()
        medium = Button(self, text='Medium', width=25, command=lambda m="medium": self.which_button(m)) #difficulty selection button
        medium.pack()
        hard = Button(self, text='Hard', width=25, command=lambda m="hard": self.which_button(m)) #difficulty selection button
        hard.pack()
        displayHighscore = Button(self, text='Display High Score', width=25, command=self.gotoHighScore) #display highscore button
        displayHighscore.pack()
        self.mainloop()
        
    def gotoHighScore(self):
        self.destroy()
        game = DDR()
        game.displayHighScore()
        
    def displayHighScore(self):
        self.title("DisplayScore")
        self.geometry("1000x10000")
        f = open('highscores.txt','r')
        lst=f.read().split("\n")
        score = []
        for i in lst:
            if i != "":
                score.append(i.split("@@@"))
        label = Label( self, text = "SCORE TABLE", font=("Helvetica", 30))
        label.pack()
        for i in range(len(score)):
            label = Label( self, text = score[i], relief=RAISED, font=("Helvetica", 10))
            label.pack()
        button1 = Button(self, text='Back to Menu', width=25, command=self.gotoIntro)
        button1.pack()
        self.mainloop()

    def update_highscores(self): #add and sort new score in highscore file
        f=open('highscores.txt','r') #opens the highscore file
        lst=f.read() #reads the contents of the highscore file
        f.close() #closes the highscore file
        newlst=[] #initialises new list to store data from the highscore file
        for x in lst.split("\n"): #splits the content in the highscore 
            if x=="": #ignores empty lines
                continue
            y=x.split("@@@") #splits each line into parameters based on our data storage format
            newlst.append([int(y[1]),y[0],y[2]]) #adds data to new list
        newlst.append([self.total_score,self.player_name,self.difficulty]) #adds new score
        newlst=sorted(newlst,reverse=True) #sorts the scores in descending order
        f=open('highscores.txt','w') #opens the highscore file
        for x in newlst: #updates highscore file with new score
            f.write(x[1]+"@@@"+str(x[0])+"@@@"+x[2]+"\n")
        f.close() #closes the highscore file

    



if __name__ == "__main__":
    game = DDR()
    game.IntroPage()
    
