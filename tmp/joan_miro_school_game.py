import turtle
import math
import time
import random

# Set up the screen
screen = turtle.Screen()
screen.title("Escola Joan Miró - Barcelona Explorer")
screen.setup(width=800, height=600)
screen.bgcolor("lightblue")

# Create main game class to better organize the application
class JoanMiroSchoolGame:
    def __init__(self):
        # Game state
        self.score = 0
        self.current_level = 0
        self.game_active = False
        
        # Create turtles
        self.setup_turtles()
        
        # Define locations
        self.barcelona_pos = (-50, 100)
        self.school_pos = (-40, 90)  # Joan Miró School location
        self.park_guell_pos = (-70, 110)
        self.sagrada_familia_pos = (-30, 120)
        self.camp_nou_pos = (-90, 80)
        
        # Cultural facts for quiz
        self.facts = [
            {"question": "Who was Joan Miró?", 
             "options": ["A famous painter", "A famous football player", "A famous chef"], 
             "answer": 0},
            {"question": "Which famous building in Barcelona was designed by Antoni Gaudí?", 
             "options": ["Torre Agbar", "Sagrada Família", "Casa Batlló"], 
             "answer": 1},
            {"question": "What language is spoken in Barcelona besides Spanish?", 
             "options": ["Portuguese", "French", "Catalan"], 
             "answer": 2},
            {"question": "Which famous Barcelona football player won multiple Ballon d'Or awards?", 
             "options": ["Messi", "Xavi", "Iniesta"], 
             "answer": 0},
            {"question": "What is the famous street in Barcelona with many shops and restaurants?", 
             "options": ["La Rambla", "Passeig de Gràcia", "Avinguda Diagonal"], 
             "answer": 0},
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
        
        # Explorer character - replace airplane with a student character
        self.explorer = turtle.Turtle()
        self.explorer.shape("circle")
        self.explorer.color("red")
        self.explorer.shapesize(0.7, 0.7)
        self.explorer.penup()
        
        # Create button turtles
        self.buttons = []
        
    def draw_map_element(self, points, color="lightgreen"):
        self.map_drawer.penup()
        self.map_drawer.color(color)
        self.map_drawer.begin_fill()
        for point in points:
            self.map_drawer.goto(point)
        self.map_drawer.end_fill()
        
    def draw_barcelona_map(self):
        # Clear previous drawings
        self.map_drawer.clear()
        
        # Draw simplified Barcelona coastline
        self.map_drawer.penup()
        self.map_drawer.color("tan")  # Beach color
        self.map_drawer.begin_fill()
        coast_points = [
            (-150, -150), (150, -150), (150, -120), 
            (100, -110), (50, -100), (0, -100), 
            (-50, -110), (-100, -120), (-150, -130), (-150, -150)
        ]
        for point in coast_points:
            self.map_drawer.goto(point)
        self.map_drawer.end_fill()
        
        # Draw sea
        self.map_drawer.penup()
        self.map_drawer.color("blue")
        self.map_drawer.begin_fill()
        sea_points = [
            (-150, -150), (-150, -200), (150, -200), (150, -150)
        ]
        for point in sea_points:
            self.map_drawer.goto(point)
        self.map_drawer.end_fill()
        
        # Draw Barcelona city area
        self.map_drawer.penup()
        self.map_drawer.color("lightgray")  # City color
        self.map_drawer.begin_fill()
        city_points = [
            (-100, -120), (-50, -110), (0, -100), (50, -100), 
            (100, -110), (120, -50), (100, 0), (50, 50), 
            (0, 70), (-50, 50), (-100, 0), (-120, -50), (-100, -120)
        ]
        for point in city_points:
            self.map_drawer.goto(point)
        self.map_drawer.end_fill()
        
        # Draw main roads
        self.map_drawer.penup()
        self.map_drawer.color("gray")
        self.map_drawer.pensize(3)
        
        # Diagonal Avenue
        self.map_drawer.goto(-120, -50)
        self.map_drawer.pendown()
        self.map_drawer.goto(120, -50)
        self.map_drawer.penup()
        
        # La Rambla
        self.map_drawer.goto(0, -100)
        self.map_drawer.pendown()
        self.map_drawer.goto(0, 70)
        self.map_drawer.penup()
        
        # Passeig de Gracia
        self.map_drawer.goto(50, -100)
        self.map_drawer.pendown()
        self.map_drawer.goto(50, 50)
        self.map_drawer.penup()
        
        # Reset pen size
        self.map_drawer.pensize(1)
        
        # Mark key locations
        self.mark_location(self.school_pos[0], self.school_pos[1], "red", "Escola Joan Miró")
        self.mark_location(self.park_guell_pos[0], self.park_guell_pos[1], "green", "Park Güell")
        self.mark_location(self.sagrada_familia_pos[0], self.sagrada_familia_pos[1], "orange", "Sagrada Família")
        self.mark_location(self.camp_nou_pos[0], self.camp_nou_pos[1], "blue", "Camp Nou")
    
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
    
    def animate_exploration(self, path):
        # Animate explorer character
        self.explorer.goto(path[0])
        self.explorer.showturtle()
        
        for i, (x, y) in enumerate(path):
            self.explorer.goto(x, y)
            
            # Calculate heading for the explorer
            if i < len(path) - 1:
                next_x, next_y = path[i+1]
                dx, dy = next_x - x, next_y - y
                heading = math.degrees(math.atan2(dy, dx))
                self.explorer.setheading(heading)
            
            time.sleep(0.05)
    
    def draw_welcome_screen(self):
        self.writer.clear()
        
        # Draw title
        self.writer.goto(0, 200)
        self.writer.color("navy")
        self.writer.write("Escola Joan Miró - Barcelona Explorer", align="center", 
                         font=("Arial", 24, "bold"))
        
        # Draw subtitle
        self.writer.goto(0, 160)
        self.writer.color("black")
        self.writer.write("¡Una aventura educativa por Barcelona!", 
                         align="center", font=("Arial", 16, "normal"))
        
        # Draw instruction
        self.writer.goto(0, 100)
        self.writer.write("Aprende sobre Barcelona, Joan Miró y la cultura catalana", 
                         align="center", font=("Arial", 14, "normal"))
        
        # Create start button
        self.create_button(0, 0, 150, 40, "green", "Iniciar Aventura")
        
        # Credits
        self.writer.goto(0, -250)
        self.writer.color("gray")
        self.writer.write("Creado para Escola Joan Miró - Barcelona", 
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
        self.draw_barcelona_map()
        
        # Introduction text
        self.writer.goto(0, 250)
        self.writer.color("navy")
        self.writer.write("¡Vamos a explorar Barcelona!", 
                         align="center", font=("Arial", 18, "bold"))
        
        self.writer.goto(0, 220)
        self.writer.write("Mira cómo nuestro explorador visita los lugares más famosos.", 
                         align="center", font=("Arial", 14, "normal"))
        
        # Interesting fact about Joan Miró
        self.writer.goto(0, -220)
        self.writer.color("black")
        self.writer.write("¿Sabías que? Joan Miró fue un famoso pintor surrealista nacido en Barcelona.", 
                         align="center", font=("Arial", 12, "italic"))
        
        # Create continue button
        self.create_button(0, -250, 150, 40, "orange", "¡Explorar!")
    
    def animate_and_continue(self):
        self.clear_buttons()
        
        # Create path from school to various landmarks
        path = []
        path.extend(self._create_path(self.school_pos, self.park_guell_pos))
        path.extend(self._create_path(self.park_guell_pos, self.sagrada_familia_pos))
        path.extend(self._create_path(self.sagrada_familia_pos, self.camp_nou_pos))
        path.extend(self._create_path(self.camp_nou_pos, self.school_pos))
        
        self.animate_exploration(path)
        
        # After animation
        self.writer.goto(0, -220)
        self.writer.color("green")
        self.writer.write("¡Genial! Has visitado los lugares más emblemáticos de Barcelona.", 
                         align="center", font=("Arial", 14, "bold"))
        
        # Create continue button
        self.create_button(0, -250, 150, 40, "blue", "Continuar al Quiz")
    
    def _create_path(self, start, end, steps=15):
        start_x, start_y = start
        end_x, end_y = end
        path = []
        
        for i in range(steps + 1):
            t = i / steps
            x = start_x + (end_x - start_x) * t
            y = start_y + (end_y - start_y) * t
            path.append((x, y))
        
        return path
    
    def show_quiz_question(self):
        self.writer.clear()
        
        # Get current question
        fact = self.facts[self.current_level - 1]
        
        # Show question
        self.writer.goto(0, 200)
        self.writer.color("navy")
        self.writer.write(f"Pregunta {self.current_level}: {fact['question']}", 
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
            self.writer.write("¡Correcto! ¡Muy bien!", align="center", font=("Arial", 20, "bold"))
        else:
            self.writer.color("red")
            self.writer.write("¡No es correcto!", align="center", font=("Arial", 20, "bold"))
            
            # Show correct answer
            self.writer.goto(0, 100)
            self.writer.color("black")
            self.writer.write(f"La respuesta correcta era: {fact['options'][correct_index]}", 
                             align="center", font=("Arial", 16, "normal"))
        
        # Show current score
        self.writer.goto(0, 50)
        self.writer.color("blue")
        self.writer.write(f"Puntuación actual: {self.score}", align="center", font=("Arial", 16, "normal"))
        
        # Create continue button
        self.create_button(0, -50, 150, 40, "purple", "Continuar")
    
    def continue_game(self):
        self.current_level += 1
        self.start_level()
    
    def show_final_score(self):
        self.writer.clear()
        self.clear_buttons()
        
        # Final score and message
        self.writer.goto(0, 100)
        self.writer.color("navy")
        self.writer.write("¡Felicidades! ¡Has completado la aventura!", 
                         align="center", font=("Arial", 20, "bold"))
        
        self.writer.goto(0, 50)
        self.writer.color("black")
        self.writer.write(f"Tu puntuación final: {self.score} / {len(self.facts) * 10}", 
                         align="center", font=("Arial", 16, "normal"))
        
        # Educational summary
        self.writer.goto(0, 0)
        self.writer.write("Has aprendido sobre Barcelona y la Escola Joan Miró:", 
                         align="center", font=("Arial", 14, "normal"))
        
        y_pos = -40
        points = [
            "- La geografía de Barcelona",
            "- Datos sobre Joan Miró",
            "- Lugares emblemáticos de la ciudad",
            "- La cultura catalana"
        ]
        
        for point in points:
            self.writer.goto(-150, y_pos)
            self.writer.write(point, align="left", font=("Arial", 12, "normal"))
            y_pos -= 30
        
        # Create restart button
        self.create_button(0, -200, 150, 40, "green", "Jugar de nuevo")
    
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
                    
                    if button["text"] == "Continuar al Quiz":
                        self.current_level = 1
                        self.start_level()
                        return
                    
                    if button["text"] == "Continuar":
                        self.continue_game()
                        return
                    
                    if button["text"] == "Jugar de nuevo":
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
game = JoanMiroSchoolGame()
screen.onclick(game.handle_click)

# Keep window open
turtle.mainloop()