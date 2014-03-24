from pyalgotrade import strategy
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.technical import ma


class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, smaPeriod, main_out = []):
        strategy.BacktestingStrategy.__init__(self, feed, 1000)
        self.main_out = main_out
        self.__position = None
        self.__instrument = instrument
        # We'll use adjusted close values instead of regular close values.
        self.getBroker().setUseAdjustedValues(True)
        self.__sma = ma.SMA(feed[instrument].getAdjCloseDataSeries(), smaPeriod)
    def onStart(self):
        self.main_out = []
        self.main_out.append("Initial portfolio value: $%.2f" % self.getBroker().getEquity())

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        self.main_out.append("%s: BUY at $%.2f" % (execInfo.getDateTime(), execInfo.getPrice()))

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        self.main_out.append("%s: SELL at $%.2f" % (execInfo.getDateTime(), execInfo.getPrice()))
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exit()

    def onBars(self, bars):
        # Wait for enough bars to be available to calculate a SMA.
        if self.__sma[-1] is None:
            return

        bar = bars[self.__instrument]
        # If a position was not opened, check if we should enter a long position.
        if self.__position == None:
            if bar.getAdjClose() > self.__sma[-1]:
                # Enter a buy market order for 10 shares. The order is good till canceled.
                self.__position = self.enterLong(self.__instrument, 10, True)
        # Check if we have to exit the position.
        elif bar.getAdjClose() < self.__sma[-1]:
             self.__position.exit()

    def onFinish(self, bars):
        self.main_out.append( "Final portfolio value: $%.2f" % self.getBroker().getEquity())


def run_strategy(smaPeriod, company, file_path):
    # Load the yahoo feed from the CSV file
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV(company, file_path)
    # Evaluate the strategy with the feed.
    myStrategy = MyStrategy(feed, company, smaPeriod)
    myStrategy.run()
    output = myStrategy.main_out
    print len(output)
    return output



