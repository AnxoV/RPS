import random
from enum import IntEnum


class GameAction(IntEnum):
    Rock = 0
    Paper = 1
    Scissors = 2
    Lizzard = 3
    Spock = 4


class GameResult(IntEnum):
    Victory = 0
    Defeat = 1
    Tie = 2


Victories = {
    GameAction.Rock: GameAction.Paper,
    GameAction.Rock: GameAction.Spock,
    GameAction.Paper: GameAction.Scissors,
    GameAction.Paper: GameAction.Lizzard,
    GameAction.Scissors: GameAction.Rock,
    GameAction.Scissors: GameAction.Spock,
    GameAction.Lizzard: GameAction.Scissors,
    GameAction.Lizzard: GameAction.Rock,
    GameAction.Spock: GameAction.Paper,
    GameAction.Spock: GameAction.Lizzard
}

user_action_history = []

def assess_game(user_action, computer_action):

    game_result = None

    if user_action == computer_action:
        print(f"User and computer picked {user_action.name}. Draw game!")
        game_result = GameResult.Tie

    # You picked Rock
    elif user_action == GameAction.Rock:
        if computer_action == GameAction.Scissors:
            print("Rock smashes scissors. You won!")
            game_result = GameResult.Victory
        else:
            print("Paper covers rock. You lost!")
            game_result = GameResult.Defeat

    # You picked Paper
    elif user_action == GameAction.Paper:
        if computer_action == GameAction.Rock:
            print("Paper covers rock. You won!")
            game_result = GameResult.Victory
        else:
            print("Scissors cuts paper. You lost!")
            game_result = GameResult.Defeat

    # You picked Scissors
    elif user_action == GameAction.Scissors:
        if computer_action == GameAction.Rock:
            print("Rock smashes scissors. You lost!")
            game_result = GameResult.Defeat
        else:
            print("Scissors cuts paper. You won!")
            game_result = GameResult.Victory

    return game_result


def get_computer_action():
    if len(user_action_history) <= 1:
        random_number = random.randint(0, len(GameAction)-1)
        computer_selection = GameAction(random_number)
    else:
        user_action_occurences = {}
        for action in user_action_history:
            if action in user_action_occurences:
                user_action_occurences[action] += 1
            else:
                user_action_occurences[action] = 1
        
        user_action_probability = {}
        for action in user_action_occurences.keys():
            user_action_used = user_action_occurences[action]
            total_actions = len(user_action_history)
            user_action_probability[action] = user_action_used / total_actions

        sorted_user_action_probability = dict(sorted(
            user_action_probability.items(),
            key=lambda item: item[1]
        ))

        predicted_next_user_move = list(sorted_user_action_probability.keys())[0]
        counter_move = Victories[predicted_next_user_move]
        computer_selection = counter_move

    computer_action = GameAction(computer_selection)
    print(f"Computer picked {computer_action.name}.")

    return computer_action


def get_user_action():
    # Scalable to more options (beyond rock, paper and scissors...)
    game_choices = [f"{game_action.name}[{game_action.value}]" for game_action in GameAction]
    game_choices_str = ", ".join(game_choices)
    user_selection = int(input(f"\nPick a choice ({game_choices_str}): "))
    user_action = GameAction(user_selection)

    user_action_history.append(user_action)

    return user_action


def play_another_round():
    another_round = input("\nAnother round? (y/n): ")
    return another_round.lower() == 'y'


def main():

    while True:
        try:
            user_action = get_user_action()
        except ValueError:
            range_str = f"[0, {len(GameAction) - 1}]"
            print(f"Invalid selection. Pick a choice in range {range_str}!")
            continue

        computer_action = get_computer_action()
        assess_game(user_action, computer_action)

        if not play_another_round():
            break


if __name__ == "__main__":
    main()
