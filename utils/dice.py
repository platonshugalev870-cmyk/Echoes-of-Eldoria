import random

class Dice:
    @staticmethod
    def roll(dice_str):
        if 'd' not in dice_str:
            return int(dice_str)
        count, sides = map(int, dice_str.split('d'))
        result = 0
        for _ in range(count):
            result += random.randint(1, sides)
        return result
    
    @staticmethod
    def d20():
        return random.randint(1, 20)
    
    @staticmethod
    def d100():
        return random.randint(1, 100)
    
    @staticmethod
    def chance(percent):
        return Dice.d100() <= percent
    
    @staticmethod
    def roll_multiple(dice_list):
        results = []
        for dice in dice_list:
            results.append(Dice.roll(dice))
        return results
    
    @staticmethod
    def advantage_roll():
        return max(random.randint(1, 20), random.randint(1, 20))
    
    @staticmethod
    def disadvantage_roll():
        return min(random.randint(1, 20), random.randint(1, 20))