from yahoo_fin import news
 
p=news.get_yf_rss("BTC-USD")
for i in p:
    print(i)
