class Card:
    """
    Static class that handles cards. We represent cards as 32-bit integers, so
    there is no object instantiation - they are just ints. Most of the bits are
    used, and have a specific meaning.

    """

    STR_RANKS = '23456789TJQKA'
    STR_SUITS = 'SHDC'
    INT_RANKS = range(13)
    PRIME_NUMBERS = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]

    CHAR_RANK_TO_INT_RANK = dict(zip(list(STR_RANKS), INT_RANKS))
    CHAR_SUIT_TO_INT_SUIT = {
        'S': 1,  # spades
        'H': 2,  # hearts
        'D': 4,  # diamonds
        'C': 8,  # clubs
    }

    INT_SUIT_TO_CHAR_SUIT = 'xshxdxxxc'

    UNICODE_SUITS = {
        1: u"\u2660",  # spades
        2: u"\u2665",  # hearts
        4: u"\u2666",  # diamonds
        8: u"\u2663"  # clubs
    }

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.int = self._calculate_binary_integer()

    def __str__(self):
        rank_int = self.get_rank_int_from_char()
        suit_int = self.get_suit_int_from_char()
        unicode_suit = Card.UNICODE_SUITS[suit_int]
        str_rank = Card.STR_RANKS[rank_int]
        return f'[ {str_rank} {unicode_suit} ]'

    def __repr__(self):
        return f'Card(rank={self.rank}, suit={self.suit})'

    def _calculate_binary_integer(self):
        """
        Converts Card string to binary integer representation of card, inspired by:

        http://suffe.cool/poker/evaluator.html

              bitrank     suit rank   prime
        +--------+--------+--------+--------+
        |xxxbbbbb|bbbbbbbb|cdhsrrrr|xxpppppp|
        +--------+--------+--------+--------+
        1) p = prime number of rank (deuce=2,trey=3,four=5,...,ace=41)
        2) r = rank of card (deuce=0,trey=1,four=2,five=3,...,ace=12)
        3) cdhs = suit of card (bit turned on based on suit of card)
        4) b = bit turned on depending on rank of card
        5) x = unused
        """

        rank_int = self.get_rank_int_from_char()
        suit_int = self.get_suit_int_from_char()
        rank_prime_number = Card.PRIME_NUMBERS[rank_int]

        bitrank_bit_int = self.get_bitrank_bit_int(rank_int)
        suit_bit_int = self.get_suit_bit_int(suit_int)
        rank_bit_int = self.get_rank_bit_int(rank_int)

        return bitrank_bit_int | suit_bit_int | rank_bit_int | rank_prime_number

    def get_suit_int_from_char(self):
        return Card.CHAR_SUIT_TO_INT_SUIT[self.suit]

    def get_rank_int_from_char(self):
        return Card.CHAR_RANK_TO_INT_RANK[self.rank]

    def get_bitrank_bit_int(self, rank_int):
        """
        Get the bitrank (b) bit integer representation.
        +---------+---------+--------+--------+
        |xxx(bbbbb|bbbbbbbb)|cdhsrrrr|xxpppppp|
        +---------+---------+--------+--------+
        b = bit turned on depending on rank of card
        """
        return 1 << rank_int << 16

    def get_suit_bit_int(self, suit_int):
        """
        Get the suit (chds) bit integer representation.
        +--------+--------+----------+--------+
        |xxxbbbbb|bbbbbbbb|(cdhs)rrrr|xxpppppp|
        +--------+--------+----------+--------+
        r = bit turned on depending on rank of card
        """
        return suit_int << 12

    def get_rank_bit_int(self, rank_int):
        """
        Get the rank (r) bit integer representation.
        +--------+--------+----------+--------+
        |xxxbbbbb|bbbbbbbb|cdhs(rrrr)|xxpppppp|
        +--------+--------+----------+--------+
        r = bit turned on depending on rank of card
        """
        return rank_int << 8

    @staticmethod
    def int_to_str(card_int):
        rank_int = Card.get_rank_int(card_int)
        suit_int = Card.get_suit_int(card_int)
        return Card.STR_RANKS[rank_int] + Card.INT_SUIT_TO_CHAR_SUIT[suit_int]

    @staticmethod
    def get_rank_int(card_int):
        return(card_int >> 8) & 0xF

    @staticmethod
    def get_suit_int(card_int):
        return (card_int >> 12) & 0xF

    @staticmethod
    def get_bitrank_int(card):
        return (card.int >> 16) & 0x1FFF

    @staticmethod
    def get_prime(card_int):
        return card_int & 0x3F

    @staticmethod
    def cards_to_card_ints(cards):
        return [card.int for card in cards]

    @staticmethod
    def prime_product_from_hand(card_ints):
        rankbits = (card_ints[0] | card_ints[1] |
                    card_ints[2] | card_ints[3] | card_ints[4]) >> 16
        product = 1
        for card_int in card_ints:
            product *= Card.get_prime(card_int)
        return product

    @staticmethod
    def prime_product_from_rankbits(rankbits):
        """
        Returns the prime product using the bitrank (b)
        bits of the hand. Each 1 in the sequence is converted
        to the correct prime and multiplied in.
        Params:
            rankbits = a single 32-bit (only 13-bits set) integer representing
                    the ranks of 5 _different_ ranked cards
                    (5 of 13 bits are set)
        Primarily used for evaulating flushes and straights,
        two occasions where we know the ranks are *ALL* different.
        Assumes that the input is in form (set bits):
                              rankbits
                        +--------+--------+
                        |xxxbbbbb|bbbbbbbb|
                        +--------+--------+
        """
        product = 1
        for i in Card.INT_RANKS:
            if rankbits & (1 << i):
                product *= Card.PRIME_NUMBERS[i]
        return product

    @staticmethod
    def int_to_pretty_string(card_int):
        """
        Prints a single card
        """

        suit_int = Card.get_suit_int(card_int)
        rank_int = Card.get_rank_int(card_int)

        suit = Card.UNICODE_SUITS[suit_int]
        rank = Card.STR_RANKS[rank_int]

        return " [ " + rank + " " + suit + " ] "

    @staticmethod
    def print_pretty_card(card_int):
        print(Card.int_to_pretty_string(card_int))

    @staticmethod
    def print_pretty_cards(card_ints):
        output = ""
        for i in range(len(card_ints)):
            card = card_ints[i]
            if i != len(card_ints) - 1:
                output += f'{Card.int_to_pretty_string(card)}, '
            else:
                output += Card.int_to_pretty_string(card)
        print(output)

    @staticmethod
    def cards_to_str(cards):
        return ", ".join([str(card) for card in cards])
