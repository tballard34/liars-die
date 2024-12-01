import random
from typing import Dict, List, Tuple, Optional
from math import comb

MULTIPLIERS: Dict[int, float] = {1: 1.0, 2: 1.2, 3: 1.4, 4: 1.6, 5: 1.8, 6: 2.0}
POWER: float = 3
BIAS_FACTOR_PREVIOUS: float = 1.2
LIAR_CALLOUT_SCALING_FACTOR: float = 0.5


class LiarsDieBot:
    def __init__(self) -> None:
        self.dice: List[int] = []

    def start_game(self, num_dice: int) -> None:
        self.dice = [0] * num_dice
        self.roll_dice()

    def make_move(
        self,
        previous_call: Optional[Tuple[int, int]],
        previous_caller_dice: int,
        total_dice: int,
    ) -> Tuple[str, Tuple[int, int]]:
        if previous_call:
            return self._make_move_after(previous_call, previous_caller_dice, total_dice)
        else:
            return self._make_first_move(total_dice)

    def reveal_dice(self) -> List[int]:
        return self.dice

    def lose_dice(self) -> None:
        if self.dice:
            self.dice.pop()

    def reroll_dice(self) -> None:
        self.roll_dice()

    def roll_dice(self) -> None:
        self.dice = [random.randint(1, 6) for _ in self.dice]

    def _make_first_move(self, total_dice: int) -> Tuple[str, Tuple[int, int]]:
        expected_counts = self._expected_dice_count(total_dice)
        weighted_counts = [expected_counts[i] * MULTIPLIERS[i + 1] for i in range(6)]
        powered_counts = [count**POWER for count in weighted_counts]
        total_powered = sum(powered_counts)
        probabilities = [count / total_powered for count in powered_counts]
        die_face = self._weighted_choice(probabilities)
        die_count = int(expected_counts[die_face - 1])
        die_count = max(1, die_count)
        return ("No Liar", (die_count, die_face))

    def _make_move_after(
        self,
        previous_call: Tuple[int, int],
        previous_caller_dice: int,
        total_dice: int,
    ) -> Tuple[str, Tuple[int, int]]:
        """
        Decide whether to bluff or not based on the previous call and game state.

        Args:
            previous_call (Tuple[int, int]): The previous move as (count, number).
            previous_caller_dice (int): Number of dice the previous caller has.
            total_dice (int): Total number of dice in the game.

        Returns:
            Tuple[str, Tuple[int, int]]: A tuple where the first element is either "No Liar" or "Liar",
                                          and the second element is the new move or the previous call.
        """
        count, number = previous_call
        prob_prev_call_true = self._probability_at_least(count, number, total_dice, previous_caller_dice)
        prob_prev_call_false = 1 - prob_prev_call_true

        possible_moves = self._generate_possible_moves(previous_call, total_dice)

        best_move = None
        best_move_ev = float("-inf")  # Initialize with negative infinity

        for move in possible_moves:
            move_count, move_number = move
            prob_move_true = self._probability_at_least(move_count, move_number, total_dice, previous_caller_dice)
            prob_player_calls_liar = self._probability_player_calls_liar(move, total_dice, previous_caller_dice)

            # Calculate EV: Probability the move is true multiplied by the chance the next player calls it wrong
            ev = prob_move_true * prob_player_calls_liar

            if ev > best_move_ev:
                best_move_ev = ev
                best_move = move

        # Decision based on EV comparison with the previous call's false probability
        if best_move_ev > prob_prev_call_false:
            return ("No Liar", best_move)
        else:
            return ("Liar", previous_call)

    def _expected_dice_count(self, total_dice: int) -> List[float]:
        other_dice = total_dice - len(self.dice)
        expected_counts = [self.dice.count(i) + (other_dice / 6) for i in range(1, 7)]
        return expected_counts

    def _weighted_choice(self, probabilities: List[float]) -> int:
        cumulative = 0.0
        rand = random.random()
        for i, prob in enumerate(probabilities):
            cumulative += prob
            if rand < cumulative:
                return i + 1
        return 6

    def _probability_at_least(self, count: int, number: int, total_dice: int, previous_caller_dice: int) -> float:
        bot_count = self.dice.count(number)
        remaining_dice = total_dice - len(self.dice)

        # Calculate the number of dice not owned by the bot or the caller
        other_dice = remaining_dice - previous_caller_dice
        other_dice = max(0, other_dice)

        # Probability parameters for the caller's dice
        if previous_caller_dice > 0:
            p_number_caller = BIAS_FACTOR_PREVIOUS / 6
            p_other_caller = (1 - (BIAS_FACTOR_PREVIOUS - 1) / previous_caller_dice) / 6
            # Ensure probabilities are valid
            p_other_total = p_other_caller * 5
            if not (0 <= p_number_caller <= 1) or not (0 <= p_other_total <= 1):
                raise ValueError("Invalid bias factor leading to invalid probabilities.")
        else:
            p_number_caller = 0.0
            p_other_caller = 0.0

        # Generate PMF for caller's dice
        if previous_caller_dice > 0:
            caller_pmf = [0.0 for _ in range(previous_caller_dice + 1)]
            for i in range(previous_caller_dice + 1):
                caller_pmf[i] = comb(previous_caller_dice, i) * (p_number_caller**i) * ((1 - p_number_caller) ** (previous_caller_dice - i))
        else:
            caller_pmf = [1.0]

        # Generate PMF for other dice
        if other_dice > 0:
            p_number_other = 1 / 6
            other_dice_pmf = [0.0 for _ in range(other_dice + 1)]
            for j in range(other_dice + 1):
                other_dice_pmf[j] = comb(other_dice, j) * (p_number_other**j) * ((1 - p_number_other) ** (other_dice - j))
        else:
            other_dice_pmf = [1.0]

        # Calculate the needed number of 'number's from caller and other dice
        needed = count - bot_count
        if needed <= 0:
            return 1.0  # Bot already satisfies the bid

        combined_prob = 0.0
        for i, p_i in enumerate(caller_pmf):
            for j, p_j in enumerate(other_dice_pmf):
                if i + j >= needed:
                    combined_prob += p_i * p_j

        return combined_prob

    def _generate_possible_moves(self, previous_call: Tuple[int, int], total_dice: int) -> List[Tuple[int, int]]:
        prev_count, prev_number = previous_call
        possible_moves = []

        possible_moves.append((prev_count + 1, prev_number))

        for new_number in range(prev_number + 1, 7):
            possible_moves.append((prev_count, new_number))
            possible_moves.append((prev_count + 1, new_number))

        return possible_moves

    # TODO: This is a heuristic and should be replaced with a more sophisticated model
    def _probability_player_calls_liar(self, move: Tuple[int, int], total_dice: int, previous_caller_dice: int) -> float:
        """
        Estimate the probability that the next player will call Liar on the bot's move.

        Args:
            move (Tuple[int, int]): The bot's proposed move as (count, number).
            total_dice (int): Total number of dice in the game.
            previous_caller_dice (int): Number of dice the previous caller has.

        Returns:
            float: Probability that the next player calls Liar on the bot's move.
        """
        move_count, move_number = move
        prob_move_true = self._probability_at_least(move_count, move_number, total_dice, previous_caller_dice)

        # Assuming the next player will call Liar if they believe the move is unlikely to be true.
        # We can model this as a function of the inverse of prob_move_true.
        # For simplicity, let's assume the probability of calling Liar increases as prob_move_true decreases.
        # This can be adjusted based on more sophisticated modeling or empirical data.

        # Example heuristic: Next player calls Liar with probability proportional to (1 - prob_move_true)
        prob_call_liar = 1 - prob_move_true

        # To make it less aggressive, we can apply a scaling factor (e.g., 0.5)
        prob_call_liar = min(max(prob_call_liar * LIAR_CALLOUT_SCALING_FACTOR, 0.0), 1.0)

        return prob_call_liar
