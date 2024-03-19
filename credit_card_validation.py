def validate(card):
    # Must start with a 4,5 or 6 .
    if card[0] != '4' and card[0] != '5' and card[0] != '6':
        return False

    # Must contain exactly 16 digits.
    if len(card.replace("-", "")) != 16:
        return False

    # Must only consist of digits (0-9).
    for i in range(len(card)):
        if card[i] == '-':
            continue
        if not card[i].isdigit():
            return False

    # May have digits in groups of 4, separated by one hyphen "-".
    group = 0
    for i in range(len(card)):
        if card[i] == '-' and group != 4:
            return False
        elif card[i] == '-' and group == 4:
            group = 0
        else:
            group += 1

    # Must NOT use any other separator like ' ' , '_', etc.
    if " " in card or "_" in card:
        return False

    # Must NOT have 4 or more consecutive repeated digits.
    repeat = 1
    card_num_no_hyphen = card.replace("-", "")
    for i in range(len(card_num_no_hyphen) - 1):
        if card_num_no_hyphen[i] != card_num_no_hyphen[i + 1]:
            repeat = 1
        else:
            repeat += 1
        if repeat == 4:
            return False

    return True


# Read form Input
input_count = input()
for count in range(int(input_count)):
    card = input()
    if validate(card):
        print("Valid")
    else:
        print("Invalid")