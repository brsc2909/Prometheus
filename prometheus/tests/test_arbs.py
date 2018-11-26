import unittest
import database as db
from arbs import arbs
from decimal import Decimal
import matplotlib.pyplot as plt
from pylab import figure, show, legend, ylabel

FEES = {'MAKER': Decimal(0.0000150), 'TAKER': Decimal(0.00030)}
order_book = db.get_order_book()
arb = arbs.Arbs(order_book, FEES)


class TestArbs(unittest.TestCase):

    def test_calc_purchase(self):

        print(arb.trade_price('USDT', 'TRX'))

        self.assertEqual(0, 0)

    def test_pentarb(self):
        start = 1000
        symbols = ['TRX', 'BNB', 'ETH', 'BTC']
        splits = []
        profit = arb.multiarb(
            spend=start,
            base='USDT',
            symbols=symbols,
            profit=(start-6)
        )
        profit.sort(key=lambda p: p[1])
        profits = []
        for i in profit:
            profits.append(i[1])
            trade_path = i[0]
            len_of_path = len(trade_path)
            split = arb.pct_split('USDT', i[0][0])

            for pos in range(0, len_of_path-1):
                split += arb.pct_split(trade_path[pos], trade_path[pos+1])
            split += arb.pct_split(trade_path[-1], 'USDT')

            splits.append(split*100)
        #
        # plt.plot(range(len(profits)), splits, color='g')
        # plt.plot(range(len(profits)), profits, color='orange')
        # plt.xlabel('profits/split')
        # plt.ylabel('iteration')
        # plt.title('arbs')
        # plt.show()

        # create the general figure
        fig1 = figure()

        # and the first axes using subplot populated with data
        ax1 = fig1.add_subplot(111)
        line1 = ax1.plot(splits, 'o-')
        ylabel("Split")

        # now, the second axes that shares the x-axis with the ax1
        ax2 = fig1.add_subplot(111, sharex=ax1, frameon=False)
        line2 = ax2.plot(profits, 'xr-')
        ax2.yaxis.tick_right()
        ax2.yaxis.set_label_position("right")
        ylabel("Profits")

        # for the legend, remember that we used two different axes so, we need
        # to build the legend manually
        legend((line1, line2), ("S", "P"))
        show()

        self.assertGreater(start, 0)
