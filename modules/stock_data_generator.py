import logging
from random import random


class StockData:
    def __init__(self, ticker: str):
        self._ticker = ticker
        self._stock_value = 0
        self._epoch = 0

    @staticmethod
    def _generate_movement():
        movement = -1 if random() < 0.5 else 1
        return movement

    def _stock_data_gen(self):
        while True:
            movement = self._generate_movement()
            stock_value = self._stock_value + movement if self._stock_value + movement >= 0 else 0
            yield stock_value

    async def generate_point(self):
        self._stock_value = next(self._stock_data_gen())
        logging.info(f"VALUE_GENERATED for ticker {self._ticker}, value: {self._stock_value}")
        return self._stock_value
