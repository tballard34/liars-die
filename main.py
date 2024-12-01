import sys
from liars_die import LiarsDieBot


def print_menu():
    print("\n--- Liar's Die Bot Menu ---")
    print("1. Start Game")
    print("2. Make Move")
    print("3. Remove Die")
    print("4. Reveal Dice")
    print("5. Reroll Dice")
    print("6. Exit")


def main():
    bot = LiarsDieBot()
    game_started = False

    while True:
        print_menu()
        choice = input("Select an option (1-6): ").strip()

        if choice == "1":
            try:
                num_dice = int(input("\nEnter number of dice for each player: ").strip())
                bot.start_game(num_dice)
                game_started = True
                print(f"Game started with {num_dice} dice per player.")
            except ValueError:
                print("Invalid number of dice.")

        elif choice == "2":
            if not game_started:
                print("Start the game first.")
                continue
            prev_call = input("\nEnter previous call as count,number (or leave blank if first move): ").strip()
            if prev_call:
                try:
                    count, number = map(int, prev_call.split(","))
                    previous_call = (count, number)
                except ValueError:
                    print("Invalid input format.")
                    continue

                try:
                    previous_caller_dice = int(input("Enter number of dice the previous caller has: ").strip())
                except ValueError:
                    print("Invalid number of dice for the previous caller.")
                    continue

                try:
                    total_dice = int(input("Enter total number of dice in the game: ").strip())
                    move = bot.make_move(previous_call, previous_caller_dice, total_dice)
                    print(f"Bot decision: {move[0]}")
                    print(f"Bot move: Count = {move[1][0]}, Number = {move[1][1]}")
                except ValueError as e:
                    print(f"Error: {e}")
            else:
                # No previous call; first move
                previous_call = None
                try:
                    total_dice = int(input("Enter total number of dice in the game: ").strip())
                    move = bot.make_move(previous_call, 0, total_dice)
                    print(f"Bot decision: {move[0]}")
                    print(f"Bot move: Count = {move[1][0]}, Number = {move[1][1]}")
                except ValueError as e:
                    print(f"Error: {e}")

        elif choice == "3":
            if not game_started:
                print("Start the game first.")
                continue
            bot.lose_dice()
            print("\nA die has been removed from the bot.")
            print(f"Bot now has {len(bot.dice)} dice remaining.")
            if len(bot.dice) == 0:
                print("Bot has no dice remaining. Game over.")
                sys.exit(0)

        elif choice == "4":
            if not game_started:
                print("Start the game first.")
                continue
            dice = bot.reveal_dice()
            print(f"\nBot's dice: {dice}")

        elif choice == "5":
            if not game_started:
                print("Start the game first.")
                continue
            bot.reroll_dice()
            print("\nThe bot's dice have been rerolled.")

        elif choice == "6":
            print("\nExiting the game.")
            sys.exit(0)

        else:
            print("Invalid option. Please select a number between 1 and 6.")


if __name__ == "__main__":
    main()
