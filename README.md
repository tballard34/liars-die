# liars-die

An implementation of the game "Liar's Die" in Python

## Table of Contents

- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
  - [Starting the Game](#starting-the-game)
  - [Making a Move](#making-a-move)
  - [Killing a Die](#killing-a-die)
  - [Rerolling Dice](#rerolling-dice)
- [Strategy Overview](#strategy-overview)
  - [Case 1: Bot is the First Guesser](#case-1-bot-is-the-first-guesser)
  - [Case 2: Bot Receives a Previous Call](#case-2-bot-receives-a-previous-call)
  - [Example Scenario](#example-scenario)

## Installation and Setup

To set up the **liars-die** project, follow these steps:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/tballard34/liars-die.git
   cd liars-die
   ```

2. **Create a Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

## Usage

To run the Liar's Die game, execute the following command in your terminal:

```bash
python main.py
```

## Strategy Overview

### Case 1: Bot is the First Guesser

- The bot makes a smart guess based on the number of dice in the game.

### Case 2: Bot Receives a Previous Call

- The bot checks how likely it is that the last guess was wrong, and calculates the percentage chance it will lose a die if it were to call the last player a liar.
- The bot also figures out its best next move and checks how likely it is to be wrong.
- It then considers the chance that the next player will call it a liar.
- It then multiplies the chance its next best move is wrong by the chance the next player will call it a liar to find the expected percentage chance it will lose a die making the best next move.

### Example Scenario

1. **Situation**: The bot is playing with 3 other players, each having 5 dice. The current call is "three 4s".
2. **Bot's Dice**: The bot has the following dice: [2, 4, 4, 5, 6].
3. **Bot's Analysis**:
   - **Likelihood of Current Call Being Wrong**: The bot calculates the probability that there are at least three 4s among all dice. For example, it estimates a 60% chance that the current call is incorrect.
   - **Best Next Move**: The bot considers calling "four 4s" based on its own dice and the probability distribution of the remaining dice. It calculates a 30% chance that there are at least four 4s.
   - **Called a Liar Estimation**: The bot evaluates the risk of being called a liar if it makes the next move and the likelihood of losing a die. It estimates a 80% chance of being called a liar.
4. **Decision**: Based on the analysis, the bot decides whether to call the previous player a liar or make a new call. 

   - **Calling Liar**: If the bot calls the previous player a liar, it has a 60% chance of losing a die.
   - **Making a New Call**: If the bot makes a new call, it calculates the probability of losing a die as follows:
     - The chance of its next best move being correct is 30%, so the chance of it being wrong is 70%.
     - The chance of being called a liar is 80%.
     - Therefore, the probability of losing a die by making a new call is \(70\% \times 80\% = 56\%\).

   Given these calculations, the bot might decide to make a new call since the probability of losing a die is slightly lower than calling Liar(56% vs. 60%).

---
