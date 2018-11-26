from itertools import permutations, combinations
from decimal import Decimal


class Arbs(object):

    def __init__(self, tickers, fees):
        self.pairs = tickers
        self.taker_fee_pct = (1-fees['TAKER'])

    def pct_split(self, symbol1, symbol2):
        pair = symbol1 + symbol2
        reverse = symbol2 + symbol1

        if pair in self.pairs:
            return (self.pairs[pair][1] - self.pairs[pair][0])/self.pairs[pair][1]
        else:
            return (self.pairs[reverse][1] - self.pairs[reverse][0])/self.pairs[reverse][1]

    def trade_price(self, from_sym, to_sym):
        pair = from_sym + to_sym
        reverse = to_sym + from_sym

        if pair in self.pairs:
            return self.pairs[pair][0]
        else:
            return 1 / self.pairs[reverse][1]

    def arb5(self, spend, base, symbols):
        calc = self.trade_price

        return (Decimal(spend) * calc(base, symbols[0]))*self.taker_fee_pct * \
            calc(symbols[0], symbols[1])*self.taker_fee_pct * \
            calc(symbols[1], symbols[2])*self.taker_fee_pct * \
            calc(symbols[2], symbols[3])*self.taker_fee_pct * \
            calc(symbols[3], base)*self.taker_fee_pct

    def arb4(self, spend, base, symbols):
        calc = self.trade_price
        return (Decimal(spend) * calc(base, symbols[0]))*self.taker_fee_pct * \
            calc(symbols[0], symbols[1])*self.taker_fee_pct * \
            calc(symbols[1], symbols[2])*self.taker_fee_pct * \
            calc(symbols[2], base)*self.taker_fee_pct

    def arb3(self, spend, base, symbols):

        calc = self.trade_price

        return (Decimal(spend) * calc(base, symbols[0]))*self.taker_fee_pct * \
            calc(symbols[0], symbols[1])*self.taker_fee_pct * \
            calc(symbols[1], base)*self.taker_fee_pct

    def multiarb(self, spend, base, symbols, profit):
        profitable = []
        arbs = [self.arb3, self.arb4, self.arb5]
        calc = self.trade_price
        init_spend = spend / calc('USDT', base)

        for i in range(2, len(symbols)+1):
            combs = combinations(symbols, i)
            for comb in list(combs):
                for perm in permutations(comb):

                    output = arbs[i-2](init_spend, base, perm)
                    if output >= profit:
                        profitable.append((perm, output))

        return profitable
