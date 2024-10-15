
# Tank Game

A simple tank game built using Python and Pygame, where the player controls a tank to navigate through obstacles, avoid enemies, and progress through levels. The game increases in difficulty with each level, and includes a congratulatory message upon completing the final level.

## Features
- Move the tank using arrow keys
- Random enemy movement that changes direction upon collision with obstacles
- Level progression with increasing difficulty
- Visual representation of arrow keys for intuitive gameplay

## Folder Structure
```
Tank-Game/
│
├── classes/                  # Directory containing all the classes used in the game
│   ├── playerTank.py             # Player class
│   ├── enemy.py              # Enemy class
│   ├── obstacle.py           # Obstacle class
│   └── boss.py               # Enemy Boss class
│   └── projectile.py         # Projectile class
│
├── constants.py              # File containing all the game constants
├── audio                     # File containing all the game audios
├── images                    # File containing all the game sprites
├── main.py                   # Main game loop and logic
└── README.md                 # Project description and documentation
```

## Prerequisites

Make sure you have Python installed on your system. This game uses the Pygame library, which can be installed using the following command:

```bash
pip install pygame
```

## How to Run the Game

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/pranjolkoirala/HIT-137-Final-Assessment.git
   ```

2. Navigate to the project directory:

   ```bash
   cd HIT-137-Final-Assessment
   ```

3. Run the game:

   ```bash
   python main.py
   ```

## Gameplay Instructions

- **Controls**: Use the arrow keys on your keyboard to move the tank:
  - Up Arrow: Move up
  - Down Arrow: Move down
  - Left Arrow: Move left
  - Right Arrow: Move right

- **Objective**: Avoid enemies and obstacles to complete each level. When you reach Level 3 and complete it, you'll receive a congratulatory message and be asked to play again.

## Future Improvements
- Add different types of enemies with unique behaviors
- Implement power-ups and bonus items
- Enhance graphics and add sound effects
- Include additional levels with varying challenges


## Acknowledgments
- [Pygame](https://www.pygame.org/) for the game development library
- Inspiration from classic tank games
