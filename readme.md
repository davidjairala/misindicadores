# Mis Indicadores

Translation: My Indicators.

It provides an almost real time reading of a great number of Mexican Economic Indicators, such as Dollar, Yen, British Pound, Euro equivalencies, Gold, Oil, Silver values, Dow Jones, NASDAQ, S&P 500, Nikkei 225, Consumer Prices Indexes, UDIS, Government Bonds, Unemployment rates, Federal Reserves, and much more.

It obtained these values automatically through a series of crons that were set to run at different but very often intervals, some of which still function, but some may need some updating.

Eventually this system became the basis for a profitable Mexican startup started on 2010 and the system was discountinued in this form, but I thought the code could maybe help someone make a something similar.

See it in action: [http://misindicadores.davemode.com/](http://misindicadores.davemode.com/)

# Sections

The site could prove difficult to understand because it's entirely in spanish (it was a Mexican venture).  So I'll go over the interesting parts and link them here directly.

#### [Dollar equivalency](http://misindicadores.davemode.com/divisas/dolar/)

Obtains the US dollar - Mexican Pesos equivalency from the main banks in Mexico throughout the day, plots the buy, sell and market values, obtains maximums, minimums, predictions, etc.

#### [Euro equivalency](http://misindicadores.davemode.com/divisas/euro/)

Same as the US Dollar equivalency but for the Euro.

#### [British Pound](http://misindicadores.davemode.com/divisas/libra/)

Same as the US Dollar equivalency but for the British Pound.

#### [Metals](http://misindicadores.davemode.com/divisas/metales/)

Market values for aluminum, copper, zinc, etc.

#### [Gold](http://misindicadores.davemode.com/divisas/oro/)

Market buy and sell values for all the gold types in Mexico.

#### [Oil](http://misindicadores.davemode.com/divisas/petroleo/)

Market values for Mexican Oil, Brent and WTI.

#### [Silver](http://misindicadores.davemode.com/divisas/plata/)

Market values for silver types in Mexico.

#### [Yen](http://misindicadores.davemode.com/divisas/yen/)

Same as the US Dollar equivalency but for the Yen.

#### [Currencies comparations](http://misindicadores.davemode.com/divisas/tabla_comparativa/)

A simple chart comparing different types of currencies and their tendencies.

#### [Mexican Stock Market](http://misindicadores.davemode.com/bolsas/bmv/)

Data, charts, tendencies and predictions for all stocks and bonds in the Mexican Stock Market.

It's also possible to obtain more info on a specific stock, for example: [ALFA day](misindicadores.davemode.com/bolsas/bmv/emisora/alfa/), [ALFA week](misindicadores.davemode.com/bolsas/bmv/emisora/alfa/semana/), [ALFA month](misindicadores.davemode.com/bolsas/bmv/emisora/alfa/mes/), [ALFA 3 months](misindicadores.davemode.com/bolsas/bmv/emisora/alfa/3meses/), [ALFA 6 months](misindicadores.davemode.com/bolsas/bmv/emisora/alfa/6meses/).

#### [Dow Jones](http://misindicadores.davemode.com/bolsas/dow/)

Data, charts, tendencies and predictions for the Dow Jones.

#### [NASDAQ](http://misindicadores.davemode.com/bolsas/nasdaq/)

Data, charts, tendencies and predictions for the NASDAQ.

#### [S&P 500](http://misindicadores.davemode.com/bolsas/sp500/)

Data, charts, tendencies and predictions for the S&P 500.

#### [Nikkei 225](http://misindicadores.davemode.com/bolsas/nikkei/)

Data, charts, tendencies and predictions for the Nikkei 225.

#### [Mexican Consumer Price Index](http://misindicadores.davemode.com/inflacion/inpc/)

Data, charts, tendencies and predictions for the Mexican Consumer Price Index.

#### [US Consumer Price Index](http://misindicadores.davemode.com/inflacion/cpi/)

Data, charts, tendencies and predictions for the US Consumer Price Index.

#### [Unemployment](http://misindicadores.davemode.com/desempeno/desempleo/)

Data, charts, tendencies and predictions for unemployment percentages in Mexico.

#### [Federal Reserves](http://misindicadores.davemode.com/desempeno/reservas/)

Data, charts, tendencies and predictions for the Mexican Federal Reserves.

#### [News](http://misindicadores.davemode.com/medios/)

News aggregation and grouping of related articles from several mexican economic news sources.

* *Note: there are more sections to the site, but these ones were the most used ones*

# Requirements

* Python
* Django
* MySQL
* numpy
* scipy
* matplotlib

# Installation

Should be good to go as soon as you create the database, user and password for it and run a quick:

    python manage.py syncdb

Of course, it's pretty useless without the data, which, as I mentioned, could be hard to get through the crons unless updated.  If you wanna see it working with the last used data (minus forums posts, users, etc.), you can visit [misindicadores.davemode.com](http://misindicadores.davemode.com/).