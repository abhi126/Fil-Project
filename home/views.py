from django.shortcuts import render
import requests

# CHARTS
import shrimpy
import plotly.graph_objects as go
from plotly.offline import plot
import json
import yfinance as yf
import datetime as dt
from django.shortcuts import render
from plotly.offline import plot
from plotly.graph_objs import Scatter

from .model_prediction import cryptoprediction

# insert your public and secret keys here
public_key = '3c12e05edc95c31267c9ff3d0a033c8a9a4c3f2490486075d68724f19f9b32be'
secret_key = 'a7c56a7d23b9d78329b15106c743c9d0a5d33ad65d07771d31c4cffeb8d0d8beb9d4cea3225352ca62a1a897f6f4173aabea8494e8c1143cfd037a0d23659e5f'

# create the client
client = shrimpy.ShrimpyApiClient(public_key, secret_key)


def plot_chart(sym):
    # get the candles
    candles = client.get_candles(
        'binance',  # exchange
        sym,      # base_trading_symbol
        'USDC',      # quote_trading_symbol
        '15m'       # interval
    )

    # create lists to hold our different data elements
    dates = []
    open_data = []
    high_data = []
    low_data = []
    close_data = []

    # convert from the Shrimpy candlesticks to the plotly graph objects format
    for candle in candles:
        dates.append(candle['time'])
        open_data.append(candle['open'])
        high_data.append(candle['high'])
        low_data.append(candle['low'])
        close_data.append(candle['close'])

    # construct the figure
    fig = go.Figure(data=[go.Candlestick(x=dates,
                        open=open_data, high=high_data,
                        low=low_data, close=close_data)])
    fig.update_layout(height = 600,width = 1100)

    # display our graph
    # fig.show()
    # print(fig)
    plt_div = plot(fig, output_type='div')
    return plt_div

# Create your views here.

def top_bar():

    url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=10&page=1&sparkline=false'
    data = requests.get(url).json()
    barlist=[]
    for item in data:
        sym = item['symbol'].upper()
        curr_p = float(item['current_price'])
        c_chng = item['price_change_24h']
        if c_chng < 0:
            c_chng = "tf-ion-arrow-down-b down-status"
        else:
            c_chng = "tf-arrow-dropup up-status"

         
        barlist.append({'sym': sym,'class':c_chng,'curr_p':curr_p }) 

    context = {'top_bar': barlist}
    return context
def get_news():
	# Grab Crypto Price Data
        price_request = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH,XRP,BCH,EOS,LTC,XLM,ADA,USDT,MIOTA,TRX&tsyms=USD")
        price = json.loads(price_request.content)
        # Grab Crypto News
        api_request = requests.get("https://min-api.cryptocompare.com/data/v2/news/?lang=EN")
        api = json.loads(api_request.content)
        return api;


def cal_con(request):
    url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=EUR&order=market_cap_desc&per_page=15&page=1&sparkline=false'
    data = requests.get(url).json()



    url2 ='http://api.exchangeratesapi.io/latest?access_key=eb70758538d0f60d66ccf9abe7f9054f'
    
    data2= requests.get(url2).json()
    rates = data2['rates']
    context = {'data':data}
    d = top_bar()   
    context.update(d)        
   

    if request.method == 'POST':
        value1 = float(request.POST['value']) 
        curr1 = request.POST['curr1']
        curr2 = request.POST['curr2']
        

        for item in data:
            if item['symbol'] == curr1:
                price = float(item['current_price'])
                if curr2 == 'EUR':
                    Result = "{:,}".format(round(value1*price,2))
                else:
                    Result = "{:,}".format(round(value1*price*rates[curr2],2) )                 
        
        k= {'Result': str('= ' + str(Result)),'value':value1,'curr1':curr1.upper(),'curr2': curr2}
        
        
        context.update(k)
        return render(request, 'cal_con.html', context)

    
    else:
        return render(request, 'cal_con.html', context)


def about(request):
    d = top_bar()  
    return render(request, 'about.html', d)


def faq(request):
    d = top_bar()  
    return render(request, 'faq.html', d)

def blog(request):
    d = top_bar()  
    p=get_news();
    d['api']=p;
    return render(request, 'blog.html',d)

def guide(request):
    d = top_bar()  
    return render(request, 'guide.html',d)


def home(request):
    d = top_bar()
    url3 = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=10&page=1&sparkline=false'
    data3 = requests.get(url3).json()
    # return HttpResponse(data)

    context = {'data': data3}
    context.update(d)
    
    
   
    
    for i in data3:
        i['plot'] = plot_chart(i['symbol'].upper())
        i['current_price'] = "{:,}".format(float(i['current_price']))
        i['market_cap'] = "{:,}".format(float(i['market_cap']))
    
        
    return render(request, 'home.html', context)

def prediction_data(request,name):
    d=top_bar()
    ac,pr,date_list,pre,r2,mae=cryptoprediction(name);
    date_list=json.dumps(date_list[0:len(ac)])
    d['r2_score']=r2;
    d["mae"]=mae
    d["ac"]=ac
    d["pr"]=pr
    d["data_list"]=date_list
    d["pre"]=pre
    d["name"]=name
    end=dt.datetime.now();
    d['predicted_date']=end+dt.timedelta(days=5)
    return render(request,'prediction.html',d)

def compare_crypto(request):
    d1={"Bitcoin":"BTC-USD","Ethereum":"ETH-USD",'Binance Coin':"BNB-USD",'Tether':"USDT-USD",'Cardano':"ADA-USD",'XRP':"XRP-USD",'Solana':"SOL1-USD",'Polkadot':"DOT1-USD",'Dogecoin':"DOGE-USD",'USD Coin':"USDC-USD"}
    if request.method=="POST":
        list1=request.POST.getlist('cryptos')
        t_per=request.POST['t_period']
        all_data={}
        end=dt.datetime.now();
        cryptos_list1=""
        if(t_per=="1"):
            start=end-dt.timedelta(days=365)
        elif(t_per=="2"):
            start=end-dt.timedelta(days=30)
        elif(t_per=="3"):
            start=end-dt.timedelta(days=365*5)
        colours=['red','blue','green','black']
        fig = go.Figure()
        try:
            for i in range(0,len(list1)):
                cryptos_list1+=list1[i]+" "
                data1 = yf.download(d1[list1[i]],start=start, end=end)
                data = data1.reset_index()
                all_data[list1[i]]=list(data['Close'])
                l1=list(data['Date'])
                scatter = go.Scatter(x=l1, y=list(data['Close']),
                        mode='lines', name=list1[i],
                        opacity=0.8, marker_color=colours[(i+1)%4])
                fig.add_trace(scatter)
        except:
            d=top_bar()
            d["cryptos_list"]=list(d1)
            return render(request,'compare_crypto.html',d)
        fig.update_layout(title=cryptos_list1+"Price Comparison",
                   xaxis_title='Time',
                   yaxis_title='Price(in USD)')
        plot_div = plot(fig, output_type='div')
        d=top_bar()
        d["cryptos_list1"]=cryptos_list1+"Price Comparison"
        d["cryptos_list"]=list(d1)
        d['data']=all_data
        d['plot_div']= plot_div
        return render(request,'compare_crypto.html',d)
    else:
        d=top_bar()
        d["cryptos_list"]=list(d1)
        return render(request,'compare_crypto.html',d)

