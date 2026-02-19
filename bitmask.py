class Bitmask:
    def __init__(self, initial_value: int = 0):
        self.value: int = initial_value

    def get_bit(self, bit: int):
        return (self.value >> bit) & 1

    def set_bit(self, bit: int):
        self.value |= 1 << bit

    def reset_bit(self, bit: int):
        self.value &= ~(1 << bit)

    def set_bit_value(self, bit: int, value: bool):
        if value:
            self.set_bit(bit)
        else:
            self.reset_bit(bit)

    def get_set_bits(self):
        value = self.value
        position = 0
        result: list[int] = []
        while value:
            if value & 1:
                result.append(position)
            position += 1
            value >>= 1

        return result

    def get_subset_masks(self):
        value = self.value
        result: list[int] = []
        while value:
            result.append(value)
            value = self.value & (value - 1)

        return result

    def __or__(self, other: Bitmask) -> Bitmask:
        result: Bitmask = Bitmask(self.value | other.value)
        return result

    def __and__(self, other: Bitmask) -> Bitmask:
        result: Bitmask = Bitmask(self.value & other.value)
        return result

    def __invert__(self) -> Bitmask:
        result: Bitmask = Bitmask(~self.value)
        return result

    def __lshift__(self, shift_value: int) -> Bitmask:
        result: Bitmask = Bitmask(self.value << shift_value)
        return result

    def __rshift__(self, shift_value: int) -> Bitmask:
        result: Bitmask = Bitmask(self.value >> shift_value)
        return result

    def __ior__(self, other: Bitmask) -> Bitmask:
        self.value |= other.value
        return self

    def __iand__(self, other: Bitmask) -> Bitmask:
        self.value &= other.value
        return self

    def __ilshift__(self, shift_value: int) -> Bitmask:
        self.value <<= shift_value
        return self

    def __irshift__(self, shift_value: int) -> Bitmask:
        self.value >>= shift_value
        return self
