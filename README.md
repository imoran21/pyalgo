pyalgo
======


This app uses pyalgotrade backtesting strategy.

The sample backtesting strategy I used takes 3 inputs

1) year
2) stock symbol
3) SMA (sample moving average)

When the form gets submitted, 

The stock symbol and year are used to grab bar data from yahoo feeds as a csv file.

The data is then read in from the csv file and the csv file is deleted.

Now the data is run through the strategy and added to the feed.  (Since this is just a POC, I clear out the feed every time the post is submitted)


