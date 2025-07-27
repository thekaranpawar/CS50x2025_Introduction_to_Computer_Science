def luhn_checksum(card_number):
    total = 0
    # Reverse the number to make indexing easier
    reversed_digits = card_number[::-1]

    for i, digit in enumerate(reversed_digits):
        n = int(digit)
        # Double every second digit (i starts at 0)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9 
        total += n

    return total % 10 == 0


def get_card_type(card_number):
    length = len(card_number)

    if length == 15 and (card_number.startswith("34") or card_number.startswith("37")):
        return "AMEX"
    elif length == 16 and card_number[:2] in ["51", "52", "53", "54", "55"]:
        return "MASTERCARD"
    elif (length == 13 or length == 16) and card_number.startswith("4"):
        return "VISA"
    else:
        return "INVALID"


def main():
    card_number = input("Number: ").strip()

    # Validate using Luhn’s Algorithm
    if luhn_checksum(card_number):
        print(get_card_type(card_number))
    else:
        print("INVALID")


if __name__ == "__main__":
    main()


