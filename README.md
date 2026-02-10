# 🐹 Whack-a-Mole

A classic Whack-a-Mole arcade game built with Python and Pygame. Moles pop up on a 3×3 grid and you have **90 seconds** to whack as many as you can!

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.0%2B-green?logo=pygame)
![License](https://img.shields.io/badge/Licence-MIT-yellow)


## Features

- **90-second timed gameplay** — countdown timer turns red in the final 15 seconds
- **Live score tracking** — your score updates instantly with every successful whack
- **Sound effects** — satisfying audio feedback on hits and misses
- **Instructions screen** — clear guidance before the game begins
- **Game-over screen** — displays your final score with a rating and the option to play again or quit
- **Pause / Resume** — press "P" at any time to pause the action
- **Visual polish** — styled grid with holes, and moles drawn with eyes and a nose

## Screenshots

> *Add your own screenshots here after cloning the project.*

## Getting Started

### Prerequisites

- **Python 3.8** or later
- **Pygame 2.0** or later

### Installation

1. **Clone the repository**

   git clone https://github.com/macbuildssys/whack-a-mole.git
   cd whack-a-mole

2. **Install Pygame**

   pip install pygame

3. **Run the game**

   python whackAmole.py

## How to Play

1. Launch the game — you will see the **instructions screen**.
2. Press **S** to start.
3. Moles appear one at a time on the 3×3 grid. **Click on a mole** to whack it and score a point.
4. Each mole only stays for about one second, so be quick!
5. The game lasts **90 seconds**. Your score and remaining time are displayed throughout.
6. When time runs out, you will see your **final score** along with a rating.
7. Press **R** to play again or **Q** to quit.

### Controls

| Key / Action | Description            |
|--------------|------------------------|
| **S**        | Start the game         |
| **Click**    | Whack a mole           |
| **P**        | Pause / Resume         |
| **R**        | Play again (game over) |
| **Q**        | Quit (game over)       |


## Sound Files

The repository includes `hit.wav` and `miss.wav`. If you would prefer to use your own sound effects, simply drop `hit.mp3` (or `hit.wav`) and `miss.mp3` (or `miss.wav`) into the project directory; the game checks for `.mp3` first and falls back to `.wav`.


## Licence

This project is licensed under the **MIT Licence**. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Built with [Pygame](https://www.pygame.org/)
- Inspired by the classic arcade game