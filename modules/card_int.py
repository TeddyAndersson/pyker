
class CardInt(int):
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

    def __new__(cls, card_str,  *args, **kwargs):
        card_int = cls.card_string_to_binary_integer(card_str)
        return super(CardInt, cls).__new__(cls, card_int)

    def __init__(self, card_int):
        self.suit_unicode = self.get_suit_unicode()
        self.suit_character = self.get_suit_character()
        self.rank_character = self.get_rank_character()

    def __str__(self):
        return f'[ {self.rank_character} {self.suit_unicode} ]'

    def __repr__(self):
        return f'CardInt("{self.rank_character}{self.suit_character}")'

    def get_rank_int(self):
        return (self >> 8) & 0xF

    def get_suit_int(self):
        return (self >> 12) & 0xF

    def get_bitrank_int(self):
        return (self >> 16) & 0x1FFF

    def get_prime(self):
        return self & 0x3F

    def get_rank_character(self):
        rank_int = self.get_rank_int()
        return CardInt.STR_RANKS[rank_int]

    def get_suit_character(self):
        suit_int = self.get_suit_int()
        return CardInt.INT_SUIT_TO_CHAR_SUIT[suit_int]

    def get_suit_unicode(self):
        suit_int = self.get_suit_int()
        return CardInt.UNICODE_SUITS[suit_int]

    @classmethod
    def card_string_to_binary_integer(cls, card_str):
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

        rank_str = card_str[0]
        suit_str = card_str[1]
        rank_int = cls.get_rank_int_from_char(rank_str)
        suit_int = cls.get_suit_int_from_char(suit_str)
        rank_prime_number = cls.PRIME_NUMBERS[rank_int]

        bitrank_bit_int = cls.get_bitrank_bit_int(rank_int)
        suit_bit_int = cls.get_suit_bit_int(suit_int)
        rank_bit_int = cls.get_rank_bit_int(rank_int)

        card_int = int(bitrank_bit_int | suit_bit_int |
                       rank_bit_int | rank_prime_number)
        return card_int

    @classmethod
    def get_suit_int_from_char(cls, suit_char):
        return cls.CHAR_SUIT_TO_INT_SUIT[suit_char]

    @classmethod
    def get_rank_int_from_char(cls, rank_char):
        return cls.CHAR_RANK_TO_INT_RANK[rank_char]

    @classmethod
    def get_bitrank_bit_int(cls, rank_int):
        """
        Get the bitrank (b) bit integer representation.
        +---------+---------+--------+--------+
        |xxx(bbbbb|bbbbbbbb)|cdhsrrrr|xxpppppp|
        +---------+---------+--------+--------+
        b = bit turned on depending on rank of card
        """
        return 1 << rank_int << 16

    @classmethod
    def get_suit_bit_int(cls, suit_int):
        """
        Get the suit (chds) bit integer representation.
        +--------+--------+----------+--------+
        |xxxbbbbb|bbbbbbbb|(cdhs)rrrr|xxpppppp|
        +--------+--------+----------+--------+
        r = bit turned on depending on rank of card
        """
        return suit_int << 12

    @classmethod
    def get_rank_bit_int(cls, rank_int):
        """
        Get the rank (r) bit integer representation.
        +--------+--------+----------+--------+
        |xxxbbbbb|bbbbbbbb|cdhs(rrrr)|xxpppppp|
        +--------+--------+----------+--------+
        r = bit turned on depending on rank of card
        """
        return rank_int << 8

    @classmethod
    def prime_product_from_hand(cls, card_ints):
        rankbits = (card_ints[0] | card_ints[1] |
                    card_ints[2] | card_ints[3] | card_ints[4]) >> 16
        product = 1
        for card_int in card_ints:
            product *= cls.get_prime(card_int)
        return product

    @classmethod
    def prime_product_from_rankbits(cls, rankbits):
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
        for rank_int in cls.INT_RANKS:
            if rankbits & (1 << rank_int):
                product *= cls.PRIME_NUMBERS[rank_int]
        return product
