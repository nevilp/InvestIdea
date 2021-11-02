

import requests
from django.shortcuts import render

# Create your views here.
from lxml import html
from .models import IntrisicData



def index(request):
    return render(request, 'index.html')


def getData(request):
    answer='Nifty200M30'
    if request.method == 'GET' and 'category' in request.GET:
     answer = request.GET['category']
    FundName = '//tr//td[2]//a'
    intrisicValue = '//tr/td[6]'
    marketPrice = '//tr//td[7]'

    BaseURL = getScrapUrl(answer)
    page = requests.get(BaseURL)
    tree = html.fromstring(page.content)
    fundNamesElements = tree.xpath(FundName)
    intrinsicValuesElements = tree.xpath(intrisicValue)
    marketPricesElements = tree.xpath(marketPrice)
    IntrisicData.objects.all().delete()
    for i in range(len(fundNamesElements)):
        intrisicData = IntrisicData()
        intrisicData.tickerName = fundNamesElements[i].text_content()
        intrisicValuefloat =  float(intrinsicValuesElements[i].text_content().replace(',',''))
        intrisicData.intrinsicValue = intrisicValuefloat
        marketValuefloat =float(marketPricesElements[i].text_content().replace(',',''))
        intrisicData.marketValue = marketValuefloat
        intrisicData.PercentageIncreament= (intrisicValuefloat-marketValuefloat)*100/ ((intrisicValuefloat + marketValuefloat) / 2)
        intrisicData.save()
    return render(request, 'DataPoint.html', {'data': IntrisicData.objects.all().order_by('-PercentageIncreament')})

def getScrapUrl(category):
        switcher = {
            'Nifty50': 'http://www.attainix.com/ICTrackerSummary.aspx?indexcode=NIFTY',
            'NiftyNext50': 'https://www.attainix.com/ICTrackerSummary.aspx?indexcode=CNXLVL',
            'Nifty200M30': 'https://www.attainix.com/ICTrackerSummary.aspx?indexcode=NF2Q30',
            'Momentum':'https://www.attainix.com/ICTrackerSummary.aspx?indexcode=NFTM30',
            'Nifty100': 'http://www.attainix.com/ICTrackerSummary.aspx?indexcode=CNX100',
            'strongBuy':'https://www.attainix.com/ICTrackerSummary.aspx?actioncode=1.IN',
            'midcapnifty':'https://www.attainix.com/ICTrackerSummary.aspx?indexcode=CNXMID'
        }
        return switcher.get(category, 'https://www.attainix.com/ICTrackerSummary.aspx?indexcode=NF2Q30')