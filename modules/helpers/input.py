def confirm_input(question):
    response = ''
    options = {"y", "n"}
    while response.lower() not in options:
        response = input(f'{question} (y/n): ')
    return response == "y"


def select_action_input():
    actions = ['fold', 'call', 'raise']
    response = ''
    while response not in actions:
        response = input(
            f'> Enter a action ({str(actions)}): ')
    return response


def select_cards_input(player, table):
    for number_str in ['first', 'second']:
        card = input(f'Enter {number_str} card: ')
        table.deal_card(player, rank=card[0], suit=card[1])
