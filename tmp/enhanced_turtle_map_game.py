import turtle
import math
import time
import random

# Set up the screen
screen = turtle.Screen()
screen.title("Spain to Brazil Explorer - Interactive Kids Geography Game")
screen.setup(width=800, height=600)
screen.bgcolor("lightblue")

# Create main game class to better organize the application
class GeographyGame:
    def __init__(self):
        # Game state
        self.score = 0
        self.current_level = 0
        self.game_active = False
        
        # Create turtles
        self.setup_turtles()
        
        # Define locations
        self.spain_pos = (-150, 100)
        self.brazil_pos = (150, -100)
        
        # Cultural facts for quiz
        self.facts = [
            {"question": "What language is spoken in Brazil?", 
             "options": ["Spanish", "Portuguese", "Italian"], 
             "answer": 1},
            {"question": "What is the capital of Spain?", 
             "options": ["Barcelona", "Madrid", "Valencia"], 
             "answer": 1},
            {"question": "What river flows through Brazil's rainforest?", 
             "options": ["Amazon", "Nile", "Mississippi"], 
             "answer": 0},
            {"question": "Which famous dance is from Spain?", 
             "options": ["Tango", "Samba", "Flamenco"], 
             "answer": 2},
            {"question": "What famous football player is from Brazil?", 
             "options": ["Messi", "Pelé", "Ronaldo"], 
             "answer": 1},
        ]
        
        # Draw initial welcome screen
        self.draw_welcome_screen()

    def setup_turtles(self):
        # Map drawer
        self.map_drawer = turtle.Turtle()
        self.map_drawer.hideturtle()
        self.map_drawer.penup()
        self.map_drawer.speed(0)
        
        # Text writer
        self.writer = turtle.Turtle()
        self.writer.hideturtle()
        self.writer.penup()
        self.writer.speed(0)
        
        # Airplane
        self.airplane = turtle.Turtle()
        self.airplane.shape("arrow")
        self.airplane.color("red")
        self.airplane.shapesize(0.7, 1.5)
        self.airplane.penup()
        
        # Create button turtles
        self.buttons = []
        
    def draw_continent(self, points, color="lightgreen"):
        self.map_drawer.penup()
        self.map_drawer.color(color)
        self.map_drawer.begin_fill()
        for point in points:
            self.map_drawer.goto(point)
        self.map_drawer.end_fill()
        
    def draw_world_map(self):
        # Clear previous drawings
        self.map_drawer.clear()
        
        # Draw Europe (simplified)
        europe_points = [
            (-200, 80), (-160, 100), (-120, 120), 
            (-80, 120), (-40, 100), (-40, 60), 
            (-60, 40), (-100, 30), (-150, 50), (-180, 70), (-200, 80)
        ]
        self.draw_continent(europe_points)
        
        # Draw Africa (simplified)
        africa_points = [
            (-100, 30), (-60, 40), (-40, 20), (-20, -40),
            (-40, -80), (-80, -100), (-120, -80), 
            (-140, -40), (-140, 0), (-100, 30)
        ]
        self.draw_continent(africa_points, "tan")
        
        # Draw South America (simplified)
        south_america_points = [
            (80, -20), (100, -40), (120, -80), 
            (120, -120), (100, -160), (60, -180),
            (20, -160), (20, -120), (40, -80),
            (60, -40), (80, -20)
        ]
        self.draw_continent(south_america_points, "lightgreen")
        
        # Draw ocean (equator line)
        self.map_drawer.penup()
        self.map_drawer.color("blue")
        self.map_drawer.goto(-350, 0)
        self.map_drawer.pendown()
        self.map_drawer.goto(350, 0)
        self.map_drawer.penup()
        
        # Mark Spain and Brazil
        self.mark_location(self.spain_pos[0], self.spain_pos[1], "red", "SPAIN")
        self.mark_location(self.brazil_pos[0], self.brazil_pos[1], "green", "BRAZIL")
    
    def mark_location(self, x, y, color, name):
        self.map_drawer.penup()
        self.map_drawer.goto(x, y)
        self.map_drawer.dot(10, color)
        self.map_drawer.goto(x, y - 15)
        self.map_drawer.color("black")
        self.map_drawer.write(name, align="center", font=("Arial", 10, "bold"))
    
    def create_button(self, x, y, width, height, color, text):
        button = turtle.Turtle()
        button.hideturtle()
        button.penup()
        button.shape("square")
        button.shapesize(height/20, width/20)  # Turtle square is 20x20
        button.color(color)
        button.goto(x, y)
        button.showturtle()
        
        self.writer.penup()
        self.writer.goto(x, y - 5)
        self.writer.color("black")
        self.writer.write(text, align="center", font=("Arial", 12, "bold"))
        
        self.buttons.append({
            "turtle": button,
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "text": text
        })
        return button
    
    def animate_flight(self):
        # Calculate flight path (with a nice arc)
        start_x, start_y = self.spain_pos
        end_x, end_y = self.brazil_pos
        
        steps = 40
        path = []
        
        # Create an arcing path
        for i in range(steps + 1):
            t = i / steps
            x = start_x + (end_x - start_x) * t
            y = start_y + (end_y - start_y) * t
            # Add an arc to simulate Earth's curvature
            arc_height = 40 * math.sin(math.pi * t)
            y += arc_height
            path.append((x, y))
        
        # Dotted line for path
        self.map_drawer.penup()
        self.map_drawer.goto(start_x, start_y)
        for i, (x, y) in enumerate(path):
            if i % 2 == 0:
                self.map_drawer.pendown()
            else:
                self.map_drawer.penup()
            self.map_drawer.goto(x, y)
        
        # Animate airplane
        self.airplane.goto(start_x, start_y)
        self.airplane.showturtle()
        
        for i, (x, y) in enumerate(path):
            self.airplane.goto(x, y)
            
            # Calculate heading for the airplane
            if i < len(path) - 1:
                next_x, next_y = path[i+1]
                dx, dy = next_x - x, next_y - y
                heading = math.degrees(math.atan2(dy, dx))
                self.airplane.setheading(heading)
            
            time.sleep(0.05)
    
    def draw_welcome_screen(self):
        self.writer.clear()
        
        # Draw title
        self.writer.goto(0, 200)
        self.writer.color("navy")
        self.writer.write("Spain to Brazil Explorer", align="center", 
                         font=("Arial", 24, "bold"))
        
        # Draw subtitle
        self.writer.goto(0, 160)
        self.writer.color("black")
        self.writer.write("An Educational Geography Adventure for Kids!", 
                         align="center", font=("Arial", 16, "normal"))
        
        # Draw instruction
        self.writer.goto(0, 100)
        self.writer.write("Learn about countries, distances, and cultures", 
                         align="center", font=("Arial", 14, "normal"))
        
        # Create start button
        self.create_button(0, 0, 150, 40, "green", "Start Adventure")
        
        # Credits
        self.writer.goto(0, -250)
        self.writer.color("gray")
        self.writer.write("Created for DMC Propaganda - Educational Division", 
                         align="center", font=("Arial", 10, "italic"))
    
    def start_game(self):
        self.score = 0
        self.current_level = 0
        self.game_active = True
        self.clear_buttons()
        self.start_level()
    
    def start_level(self):
        if self.current_level == 0:
            self.map_introduction()
        elif self.current_level <= len(self.facts):
            self.show_quiz_question()
        else:
            self.show_final_score()
    
    def map_introduction(self):
        self.writer.clear()
        self.draw_world_map()
        
        # Introduction text
        self.writer.goto(0, 250)
        self.writer.color("navy")
        self.writer.write("Let's explore the journey from Spain to Brazil!", 
                         align="center", font=("Arial", 18, "bold"))
        
        self.writer.goto(0, 220)
        self.writer.write("Watch the airplane fly between the two countries.", 
                         align="center", font=("Arial", 14, "normal"))
        
        # Interesting fact
        self.writer.goto(0, -220)
        self.writer.color("black")
        self.writer.write("Did you know? A flight from Spain to Brazil crosses the Atlantic Ocean!", 
                         align="center", font=("Arial", 12, "italic"))
        
        # Create continue button
        self.create_button(0, -250, 150, 40, "orange", "Fly Now!")
    
    def animate_and_continue(self):
        self.clear_buttons()
        self.animate_flight()
        
        # After animation
        self.writer.goto(0, -220)
        self.writer.color("green")
        self.writer.write("Great job! The flight took about 10 hours!", 
                         align="center", font=("Arial", 14, "bold"))
        
        # Create continue button
        self.create_button(0, -250, 150, 40, "blue", "Continue to Quiz")
    
    def show_quiz_question(self):
        self.writer.clear()
        
        # Get current question
        fact = self.facts[self.current_level - 1]
        
        # Show question
        self.writer.goto(0, 200)
        self.writer.color("navy")
        self.writer.write(f"Question {self.current_level}: {fact['question']}", 
                         align="center", font=("Arial", 18, "bold"))
        
        # Show options
        y_pos = 120
        for i, option in enumerate(fact['options']):
            # Create button for each option
            btn = self.create_button(0, y_pos, 300, 40, "lightblue", f"{i+1}. {option}")
            y_pos -= 60
    
    def check_answer(self, selected_index):
        fact = self.facts[self.current_level - 1]
        correct_index = fact['answer']
        
        self.writer.clear()
        self.clear_buttons()
        
        # Show result
        self.writer.goto(0, 150)
        
        if selected_index == correct_index:
            self.score += 10
            self.writer.color("green")
            self.writer.write("Correct! Well done!", align="center", font=("Arial", 20, "bold"))
        else:
            self.writer.color("red")
            self.writer.write("Not quite right!", align="center", font=("Arial", 20, "bold"))
            
            # Show correct answer
            self.writer.goto(0, 100)
            self.writer.color("black")
            self.writer.write(f"The correct answer was: {fact['options'][correct_index]}", 
                             align="center", font=("Arial", 16, "normal"))
        
        # Show current score
        self.writer.goto(0, 50)
        self.writer.color("blue")
        self.writer.write(f"Current Score: {self.score}", align="center", font=("Arial", 16, "normal"))
        
        # Create continue button
        self.create_button(0, -50, 150, 40, "purple", "Continue")
    
    def continue_game(self):
        self.current_level += 1
        self.start_level()
    
    def show_final_score(self):
        self.writer.clear()
        self.clear_buttons()
        
        # Final score and message
        self.writer.goto(0, 100)
        self.writer.color("navy")
        self.writer.write("Congratulations! You've completed the adventure!", 
                         align="center", font=("Arial", 20, "bold"))
        
        self.writer.goto(0, 50)
        self.writer.color("black")
        self.writer.write(f"Your final score: {self.score} / {len(self.facts) * 10}", 
                         align="center", font=("Arial", 16, "normal"))
        
        # Educational summary
        self.writer.goto(0, 0)
        self.writer.write("You've learned about Spain and Brazil:", 
                         align="center", font=("Arial", 14, "normal"))
        
        y_pos = -40
        points = [
            "- The geography and distance between countries",
            "- Cultural facts about both nations",
            "- Language differences and similarities",
            "- The journey across the Atlantic Ocean"
        ]
        
        for point in points:
            self.writer.goto(-150, y_pos)
            self.writer.write(point, align="left", font=("Arial", 12, "normal"))
            y_pos -= 30
        
        # Create restart button
        self.create_button(0, -200, 150, 40, "green", "Play Again")
    
    def clear_buttons(self):
        # Hide all buttons
        for button_data in self.buttons:
            button_data["turtle"].hideturtle()
        self.buttons = []
    
    def handle_click(self, x, y):
        if not self.game_active:
            # Check if we clicked the start button
            for button in self.buttons:
                btn_x, btn_y = button["x"], button["y"]
                width, height = button["width"], button["height"]
                
                if (btn_x - width/2 < x < btn_x + width/2 and 
                    btn_y - height/2 < y < btn_y + height/2):
                    self.game_active = True
                    self.start_game()
                    return
        else:
            # Game is active, check which button was clicked
            for i, button in enumerate(self.buttons):
                btn_x, btn_y = button["x"], button["y"]
                width, height = button["width"], button["height"]
                
                if (btn_x - width/2 < x < btn_x + width/2 and 
                    btn_y - height/2 < y < btn_y + height/2):
                    
                    if self.current_level == 0:
                        # Map intro screen, start animation
                        self.animate_and_continue()
                        return
                    
                    if button["text"] == "Continue to Quiz":
                        self.current_level = 1
                        self.start_level()
                        return
                    
                    if button["text"] == "Continue":
                        self.continue_game()
                        return
                    
                    if button["text"] == "Play Again":
                        self.game_active = False
                        self.draw_welcome_screen()
                        return
                    
                    if self.current_level > 0 and self.current_level <= len(self.facts):
                        # This is an answer option
                        if button["text"].startswith("1. "):
                            self.check_answer(0)
                        elif button["text"].startswith("2. "):
                            self.check_answer(1)
                        elif button["text"].startswith("3. "):
                            self.check_answer(2)
                        return

# Create game and register click handler
game = GeographyGame()
screen.onclick(game.handle_click)

# Keep window open
turtle.mainloop()