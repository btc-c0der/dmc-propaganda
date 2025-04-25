import turtle
import math
import time

# Set up the screen
screen = turtle.Screen()
screen.title("Spain to Brazil Adventure - Kids Geography Game")
screen.setup(width=800, height=500)
screen.bgpic("") # Will use a clear background

# Create world map
screen.register_shape("worldmap", (
    (-300, 200), (300, 200), (300, -200), (-300, -200)
))
map_bg = turtle.Turtle()
map_bg.shape("worldmap")
map_bg.penup()

# Set the background color to represent oceans
screen.bgcolor("lightblue")

# Create main map turtle
map_drawer = turtle.Turtle()
map_drawer.penup()
map_drawer.hideturtle()
map_drawer.speed(0)  # Fastest speed

# Create text writer
text = turtle.Turtle()
text.penup()
text.hideturtle()
text.color("black")

# Draw continents (simplified)
def draw_continents():
    # Europe (simplified)
    map_drawer.color("lightgreen")
    map_drawer.begin_fill()
    map_drawer.goto(-50, 100)
    map_drawer.goto(0, 100)
    map_drawer.goto(50, 50)
    map_drawer.goto(50, 150)
    map_drawer.goto(-100, 150)
    map_drawer.goto(-100, 50)
    map_drawer.goto(-50, 100)
    map_drawer.end_fill()
    
    # Africa (simplified)
    map_drawer.begin_fill()
    map_drawer.goto(-50, 50)
    map_drawer.goto(50, 50)
    map_drawer.goto(50, -50)
    map_drawer.goto(-50, -50)
    map_drawer.goto(-50, 50)
    map_drawer.end_fill()
    
    # South America (simplified)
    map_drawer.begin_fill()
    map_drawer.goto(-200, -50)
    map_drawer.goto(-150, -50)
    map_drawer.goto(-150, -150)
    map_drawer.goto(-200, -150)
    map_drawer.goto(-200, -50)
    map_drawer.end_fill()

# Create airplane turtle
airplane = turtle.Turtle()
airplane.shape("arrow")
airplane.shapesize(0.5, 1.5)
airplane.color("red")
airplane.penup()

# Coordinates (simplified for turtle graphics)
spain_x, spain_y = -30, 120
brazil_x, brazil_y = -175, -100

# Create location markers
def create_marker(x, y, color):
    marker = turtle.Turtle()
    marker.penup()
    marker.shape("circle")
    marker.color(color)
    marker.shapesize(0.5, 0.5)
    marker.goto(x, y)
    return marker

# Create markers for Spain and Brazil
spain_marker = create_marker(spain_x, spain_y, "red")
brazil_marker = create_marker(brazil_x, brazil_y, "blue")

# Add text labels
def add_label(x, y, label, color="black"):
    text.color(color)
    text.goto(x, y)
    text.write(label, align="center", font=("Arial", 12, "bold"))

# Flight path calculation
def calculate_flight_path(start_x, start_y, end_x, end_y, steps=30):
    path = []
    for i in range(steps + 1):
        t = i / steps
        # Simple arc to simulate curved path
        x = start_x + (end_x - start_x) * t
        y = start_y + (end_y - start_y) * t - math.sin(t * math.pi) * 30
        path.append((x, y))
    return path

# Generate flight path
flight_path = calculate_flight_path(spain_x, spain_y, brazil_x, brazil_y)

# Function to animate airplane along path
def fly_airplane(path, airplane):
    for point in path:
        x, y = point
        # Calculate heading
        if path.index(point) < len(path) - 1:
            next_x, next_y = path[path.index(point) + 1]
            heading = math.degrees(math.atan2(next_y - y, next_x - x))
            airplane.setheading(heading)
        airplane.goto(x, y)
        time.sleep(0.1)  # Animation speed

# Draw dotted line for flight path
def draw_flight_path(path):
    map_drawer.penup()
    map_drawer.goto(path[0])
    map_drawer.pendown()
    map_drawer.color("black")
    
    for i, point in enumerate(path):
        if i % 2 == 0:  # Create dotted effect
            map_drawer.pendown()
        else:
            map_drawer.penup()
        map_drawer.goto(point)
    map_drawer.penup()

# Interactive elements
def start_game():
    screen.clear()
    screen.bgcolor("lightblue")
    
    # Redraw map elements
    draw_continents()
    
    # Add labels
    add_label(spain_x, spain_y + 20, "SPAIN", "darkred")
    add_label(brazil_x, brazil_y + 20, "BRAZIL", "darkblue")
    
    # Create distance quiz
    text.goto(0, 200)
    text.write("How far is it from Spain to Brazil?", align="center", font=("Arial", 14, "bold"))
    
    options = [
        "A) About 5,000 miles",
        "B) About 7,500 miles",
        "C) About 10,000 miles"
    ]
    
    for i, option in enumerate(options):
        text.goto(0, 170 - (i * 25))
        text.write(option, align="center", font=("Arial", 12, "normal"))
    
    # Draw flight path
    draw_flight_path(flight_path)
    
    # Position airplane at start
    airplane.goto(spain_x, spain_y)
    
    # Fly the airplane
    fly_airplane(flight_path, airplane)
    
    # Show answer
    text.goto(0, -170)
    text.color("green")
    text.write("The correct answer is A! Spain to Brazil is about 5,000 miles.", 
              align="center", font=("Arial", 14, "bold"))
    
    # Fun facts
    text.goto(0, -200)
    text.color("purple")
    text.write("Fun fact: A flight from Madrid to Brasília takes about 10 hours!", 
              align="center", font=("Arial", 12, "normal"))

# Create start button
start_button = turtle.Turtle()
start_button.penup()
start_button.shape("square")
start_button.shapesize(2, 6)
start_button.color("green")
start_button.goto(0, -150)

# Add button text
text.goto(0, -150)
text.write("START ADVENTURE", align="center", font=("Arial", 14, "bold"))

# Set up click handler
def button_click(x, y):
    # Check if click is on button
    if -60 < x < 60 and -170 < y < -130:
        start_game()

# Listen for clicks
screen.onclick(button_click)

# Initial setup
draw_continents()
add_label(spain_x, spain_y + 20, "SPAIN", "darkred")
add_label(brazil_x, brazil_y + 20, "BRAZIL", "darkblue")

text.goto(0, 180)
text.color("black")
text.write("Welcome to the Spain-Brazil Adventure!", align="center", font=("Arial", 16, "bold"))
text.goto(0, 150)
text.write("Click the green button to start your journey", align="center", font=("Arial", 12, "normal"))

# Keep window open
turtle.mainloop()