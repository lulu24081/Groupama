# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 11:25:17 2022

@author: LArib
"""

import time
import pandas as pd
import requests
import os
import urllib.request
import urllib.parse
import numpy as np
import os
import matplotlib.pyplot as plt
from tqdm import trange

import datetime



  # Proxy connexion 
GAM_PROXY = '165.225.76.40:80'
  # Modify env variables
os.environ['http_proxy'] = GAM_PROXY
os.environ['https_proxy'] = GAM_PROXY
  # afficher le proxy
PROXY_DICT = urllib.request.getproxies()
print(PROXY_DICT)

  # Recovery of data
def recup_data_wheel(date_start,date_end):
      
    
    data = {
        "correlator" : "test",
        "conditions" : [
            ["date", "within", [date_start,date_end]],
            ["tradeType", "=", "Execution"],
            ["moniker", "=", "1931"],
            ["status", "in", ["1", "2", "3", "4"]],
            ["algoStrategy", "in", ["IS"]],
            ["value4_symbol", "in", ["CITI_AW", "EXANE_AW", "JPM_AW", "KEPL_AW", "ML_AW", "MS_AW", "SG_AW"]],
            ],
        "fields" : [
            "pmOrderId",
            "brokerName",
            "side",
            "lastQty", # Traded Shares
            "transactionTime",
            "bm_priceConverted_2_exc", # ask Trade Based Bench Price (EUR)
            "bm_priceConverted_3_exc", # Bid Trade Based Bench Price (EUR)
            "pmAvgPxConverted", # PM Execution Price( avg) 
            "marketCapBucket",  # MArket cap bucket
            "volatilityBucket",   # volatility bucket 
            "trader",   # Trader Name
            "percentCompletePMShares",  # Percentage completed 
            "medianPercentDVBucket",   # % DV
            "venueType",     #venue type 
            "pmOrderQty", # qtt of shares             
            
            
            
        ],
        
        "settings": {
            "timezone" : "Europe/Brussels",
            "currency" : "EUR",
            "regionClassification" : "service",
            "volumeType" : "composite",
            "symbolClassification" : "bloombergMarketSymbol",
            "thaiOverrideType" : "thaiIndicated",
            "defaultBenchmark" : "bm_price_1_alc",
            "defaultBenchmark2" : "bm_price_2_alc",
            "defaultBenchmark3" : "bm_price_6_alc"
        },
        "rows" : 50000
    }
      # API connexion
    resp = requests.post("https://portal.virtu.com/api/rest/1/POST/analytics/getTCATrades", json=data, 
       headers = {
            "authorization" : "GrSuldYDjk6gBWrYf0b4vj+vRAzE1NY7ufqzNYLv6ENNWF3zNavqfm6UX7NzMUK4kq2amwCNLSQcr8o0JoG55PFfjJ2ApeqRfsf1zZAI60pgQS9wE7WvQrlox1OkDoT15l09pwGwiyWLjvsAZPvZTR0sHz80hLTK8jBGx2a99/8wr6imfs0WeSBcu/kM9ZafBGmAV0bQmgO6T3MRWvdYkBjhRGVXEjCAtb2cCcGpXVsl+mKmeEhQmtJgpRTc7P7DTGSjUVDRoTKxN5NAWcYsx4MRlSIRicRqTVlimD9d7PDm7qrechjS2JCAHWV82L1QbtsuarFaS3SBW5efcB5Q2zkuKeHsaMQrM1RGk8bRf7U8cnIgKFk/ytbTxfqoVsjucx5J8w6hrjtZzUznVyQPgHpGQ+BaDc3Vxd3FC4pGQmvtF59tjYQHjdq6Q244ViY9k3aDVjp5smu6FuKyEeHOUUOEP0BY5NZNCH2ePZ6NgADpmk/AkbUGq95ofOheOteUoaLv/iQZB6QfKV8iZchUNV3xW4s++LNWxyc02oCYgtARhGA1ib64k61QSOkHqL77Xk+uVC8M2XBD8DWtQCPkSt9CuL9tfG6HhgYktCnXvojjs4DUT/ksqxly4veJy+4QEB8IyvXfFEeBBTZwWNjWzPMdatr0xs39cAMiC5VU5lpaK276mTCTu/yFMCSzO5K1dK387gdrrZMkm5gTz1Pw/9ezj1Iw0R1HGPvDaqHQnlfD2OaDl3M5dFRQsMRyaBbXvRW/0k5zH58Qj0h2UuNw3H1OuBlQgot3Vuvuomdyr9d+jlXb1ghuIsfiSdZPzGmvK3E00FLbcmMYT941kFVWuPZsWMGD7hVYs191BhJ0o6seH9h59fXuX3s8odQkxkR9hNAO1fg/WRhAxyUboVEIzdMwDiCkUblVM5oMdsoKWo0ZkyP7a+x4vGf1ZxwvlGXOn12cGdv0lNK149IRbHCC6DadSQeCXZ8DGi/TUSNsAF7GkOsuaG64RQ==",
            "user" : "larib-externe@groupama-am.fr",
            "Content-Type" : "application/json"
       })
    
    
    t0 = time.time()
    df = pd.DataFrame()
    df = pd.DataFrame(resp.json()['data']['data'])
    print("temps de traitement: " , time.time()-t0)
      # treatment of the data 
        
    
    #del df['moniker']      
    #del df['assetClass']
    #del df['businessUnit']
    df.columns = ['Broker_ID', 'Broker_Name', 'Side', 'traded_Shares', 'Transaction_Time',
                  'Ask_Bench_Px', 'Bid_Bench_Px', 'Average', 'market_cap', 'volatility', 'Trader_Name', '%complete', '%DV', 'Venue_type', 'Nb_Shares' ]
    df['Val_order'] = ''
    #with open('tab.csv', 'a') as f :
        #df0.to_csv(f,header=False, index=False)
    #date_start =date_start.replace('.', '-')
    #date_end =date_end.replace('.', '-')
       
    #df = df[(df['Transaction_Time'] >= date_start) & (df['Transaction_Time'] <= date_end)]
    df_gb2 = df.groupby(['Broker_ID', 'Broker_Name']).agg({'Transaction_Time' : [np.min, np.max],})
    df_gb2.columns = [ 'Tmin', 'Tmax']
    df_gb2 = df_gb2.reset_index()
    for i in trange(len(df_gb2)): # Use trange from tqdm to display a progress bar
        # Filter DF on current broker ID
        broker_id_df = df.loc[df['Broker_ID'] == df_gb2.iloc[i, 0]]
        # Filter broker DF on Tmin & inject relevant data in grouped_by DF
        broker_id_min = broker_id_df[broker_id_df["Transaction_Time"] == df_gb2.loc[i, "Tmin"]].reset_index()
        df_gb2.loc[i, "AskTmin"] = broker_id_min.loc[0, "Ask_Bench_Px"]
        df_gb2.loc[i, "BidTmin"] = broker_id_min.loc[0, "Bid_Bench_Px"]
        df_gb2.loc[i, "Avg"] = broker_id_min.loc[0, "Average"]
        df_gb2.loc[i, "Side"] = broker_id_min.loc[0, "Side"]
        df_gb2.loc[i, "market_cap"] = broker_id_min.loc[0, "market_cap"]
        df_gb2.loc[i, "volatility"] = broker_id_min.loc[0, "volatility"]
        df_gb2.loc[i, "Trader_Name"] = broker_id_min.loc[0, "Trader_Name"]
        df_gb2.loc[i, "%complete"] = broker_id_min.loc[0, "%complete"]
        df_gb2.loc[i, "%DV"] = broker_id_min.loc[0, "%DV"]
        df_gb2.loc[i, "Venue_type"] = broker_id_min.loc[0, "Venue_type"]
        df_gb2.loc[i, 'Nb_Shares'] = broker_id_min.loc[0, 'Nb_Shares']
        df_gb2.loc[i, 'Val_order'] =  df_gb2.loc[i, 'Nb_Shares']*df_gb2.loc[i, 'Avg']
        
        if df_gb2.loc[i,'Val_order'] <= 50000 :
            df_gb2.loc[i, 'categorie'] = '0-50K'
        elif df_gb2.loc[i,'Val_order'] > 50000 and df_gb2.loc[i,'Val_order']<= 100000 :
            df_gb2.loc[i, 'categorie'] = '50K-100K'
        elif df_gb2.loc[i,'Val_order'] > 100000 and df_gb2.loc[i,'Val_order']<= 2000000 :
            df_gb2.loc[i, 'categorie'] = '100K-200K'
        elif df_gb2.loc[i,'Val_order'] > 200000 and df_gb2.loc[i,'Val_order']<= 500000 :
            df_gb2.loc[i, 'categorie'] = '200K-500K'
        elif df_gb2.loc[i,'Val_order'] > 500000 and df_gb2.loc[i,'Val_order']<= 1000000 : 
            df_gb2.loc[i, 'categorie'] = '500K-1M'
        elif df_gb2.loc[i,'Val_order'] > 1000000 and df_gb2.loc[i,'Val_order']<= 3000000 : 
            df_gb2.loc[i, 'categorie'] = '1M-3M'  
        else :
                df_gb2.loc[i, 'categorie'] = '>3M'
        # Filter broker DF on Tmax & inject relevant data in grouped_by DF
        broker_id_max = broker_id_df[broker_id_df["Transaction_Time"] == df_gb2.loc[i, "Tmax"]].reset_index()
        df_gb2.loc[i, "AskTmax"] = broker_id_max.loc[0, "Ask_Bench_Px"]
        df_gb2.loc[i, "BidTmax"] = broker_id_max.loc[0, "Bid_Bench_Px"]
        
        if df_gb2.loc[i, "Side"] == 'Buy' :
            
            df_gb2.loc[i, "Avg/Entree"] = ((df_gb2.iloc[i]['Avg']/df_gb2.iloc[i]['AskTmin'])-1)*100
            df_gb2.loc[i, "Last/Entree"] = ((df_gb2.iloc[i]['AskTmax']/df_gb2.iloc[i]['AskTmin'])-1)*100
        else :
            df_gb2.loc[i, "Avg/Entree"] = ((df_gb2.iloc[i]['Avg']/df_gb2.iloc[i]['BidTmin'])-1)*100
            df_gb2.loc[i, "Last/Entree"] = ((df_gb2.iloc[i]['BidTmax']/df_gb2.iloc[i]['BidTmin'])-1)*100
        
        df_gb2.loc[i, 'Entree'] = df_gb2.loc[i, 'Val_order']*(1 - df_gb2.loc[i, "Avg/Entree"]/100)
        df_gb2.loc[i, 'cout_avg'] = df_gb2.loc[i, 'Val_order'] - df_gb2.loc[i, 'Entree']
        df_gb2.loc[i, 'cout_last'] = df_gb2.loc[i, 'Entree']* df_gb2.loc[i, "Last/Entree"]/100
    df_gb2.sort_values(by=['Broker_ID'] )  
   
    df1 = pd.read_csv('data/tab_wheel.csv')
    os.remove('data/tab_wheel.csv')
    final_df = pd.concat([df1, df_gb2])
    final_df_removed =final_df.drop_duplicates(subset=['Tmin','Tmax'])
    final_df_removed.sort_values(by=['Tmin'], inplace = True  )
                      
    final_df_removed.to_csv('data/tab_wheel.csv', index = False)
    
    
    return  

def collecte_data_IS(date_start, date_end):
  
    data = {
          "correlator" : "test",
          "conditions" : [
              ["date", "within", [date_start, date_end]],
              ["tradeType", "=", "Execution"],
              ["moniker", "=", "1931"],
              ["status", "in", ["1", "2", "3", "4"]],
              ],
          "fields" : [
              "pmOrderId",
              "brokerName",
              "side",
              "lastQty", # Traded Shares
              "transactionTime",
              "bm_priceConverted_2_exc", # ask Trade Based Bench Price (EUR)
              "bm_priceConverted_3_exc", # Bid Trade Based Bench Price (EUR)
              "pmAvgPxConverted", # PM Execution Price( avg) 
              "marketCapBucket",  # MArket cap bucket
              "volatilityBucket",   # volatility bucket 
              "trader",   # Trader Name
              "brokerOrderReason",   # Broker_reason
              "fundStrategy",     # fund stratégie
              "percentCompletePMShares",  # Percentage completed 
              "medianPercentDVBucket",   # % DV
              "venueType",
              "pmOrderQty", # qtt of shares  
              
              
              
          ],
          
          "settings": {
              "timezone" : "Europe/Brussels",
              "currency" : "EUR",
              "regionClassification" : "service",
              "volumeType" : "composite",
              "symbolClassification" : "bloombergMarketSymbol",
              "thaiOverrideType" : "thaiIndicated",
              "defaultBenchmark" : "bm_price_1_alc",
              "defaultBenchmark2" : "bm_price_2_alc",
              "defaultBenchmark3" : "bm_price_6_alc"
          },
          "rows" : 70000
      }
        # API connexion
    resp = requests.post("https://portal.virtu.com/api/rest/1/POST/analytics/getTCATrades", json=data, 
      headers = {
          "authorization" : "GrSuldYDjk6gBWrYf0b4vj+vRAzE1NY7ufqzNYLv6ENNWF3zNavqfm6UX7NzMUK4kq2amwCNLSQcr8o0JoG55PFfjJ2ApeqRfsf1zZAI60pgQS9wE7WvQrlox1OkDoT15l09pwGwiyWLjvsAZPvZTR0sHz80hLTK8jBGx2a99/8wr6imfs0WeSBcu/kM9ZafBGmAV0bQmgO6T3MRWvdYkBjhRGVXEjCAtb2cCcGpXVsl+mKmeEhQmtJgpRTc7P7DTGSjUVDRoTKxN5NAWcYsx4MRlSIRicRqTVlimD9d7PDm7qrechjS2JCAHWV82L1QbtsuarFaS3SBW5efcB5Q2zkuKeHsaMQrM1RGk8bRf7U8cnIgKFk/ytbTxfqoVsjucx5J8w6hrjtZzUznVyQPgHpGQ+BaDc3Vxd3FC4pGQmvtF59tjYQHjdq6Q244ViY9k3aDVjp5smu6FuKyEeHOUUOEP0BY5NZNCH2ePZ6NgADpmk/AkbUGq95ofOheOteUoaLv/iQZB6QfKV8iZchUNV3xW4s++LNWxyc02oCYgtARhGA1ib64k61QSOkHqL77Xk+uVC8M2XBD8DWtQCPkSt9CuL9tfG6HhgYktCnXvojjs4DUT/ksqxly4veJy+4QEB8IyvXfFEeBBTZwWNjWzPMdatr0xs39cAMiC5VU5lpaK276mTCTu/yFMCSzO5K1dK387gdrrZMkm5gTz1Pw/9ezj1Iw0R1HGPvDaqHQnlfD2OaDl3M5dFRQsMRyaBbXvRW/0k5zH58Qj0h2UuNw3H1OuBlQgot3Vuvuomdyr9d+jlXb1ghuIsfiSdZPzGmvK3E00FLbcmMYT941kFVWuPZsWMGD7hVYs191BhJ0o6seH9h59fXuX3s8odQkxkR9hNAO1fg/WRhAxyUboVEIzdMwDiCkUblVM5oMdsoKWo0ZkyP7a+x4vGf1ZxwvlGXOn12cGdv0lNK149IRbHCC6DadSQeCXZ8DGi/TUSNsAF7GkOsuaG64RQ==",
          "user" : "larib-externe@groupama-am.fr",
          "Content-Type" : "application/json"
    })
     
    t0 = time.time()
    df = pd.DataFrame()
    df = pd.DataFrame(resp.json()['data']['data'])
    print("temps de traitement: " , time.time()-t0)
      # treatment of the data 
    
    del df['moniker']      
    del df['assetClass']
    del df['businessUnit']
    
    df.columns = ['Broker_ID', 'Broker_Name', 'Side', 'traded_Shares', 'Transaction_Time',
                  'Ask_Bench_Px', 'Bid_Bench_Px', 'Average', 'market_cap', 'volatility', 'Trader_Name','Broker_reason', 'fund_strategie', '%complete', '%DV','Venue_type', 'Nb_Shares' ]

    df['Val_order'] = ''
    #with open('tab.csv', 'a') as f :
        #df0.to_csv(f,header=False, index=False)
    #date_start =date_start.replace('.', '-')
    #date_end =date_end.replace('.', '-')
       
    #df = df[(df['Transaction_Time'] >= date_start) & (df['Transaction_Time'] <= date_end)]
    df_gb2 = df.groupby(['Broker_ID', 'Broker_Name']).agg({'Transaction_Time' : [np.min, np.max],})
    df_gb2.columns = [ 'Tmin', 'Tmax']
    df_gb2 = df_gb2.reset_index()
    for i in trange(len(df_gb2)): # Use trange from tqdm to display a progress bar
        # Filter DF on current broker ID
        broker_id_df = df.loc[df['Broker_ID'] == df_gb2.iloc[i, 0]]
        # Filter broker DF on Tmin & inject relevant data in grouped_by DF
        broker_id_min = broker_id_df[broker_id_df["Transaction_Time"] == df_gb2.loc[i, "Tmin"]].reset_index()
        df_gb2.loc[i, "AskTmin"] = broker_id_min.loc[0, "Ask_Bench_Px"]
        df_gb2.loc[i, "BidTmin"] = broker_id_min.loc[0, "Bid_Bench_Px"]
        df_gb2.loc[i, "Avg"] = broker_id_min.loc[0, "Average"]
        df_gb2.loc[i, "Side"] = broker_id_min.loc[0, "Side"]
        df_gb2.loc[i, "market_cap"] = broker_id_min.loc[0, "market_cap"]
        df_gb2.loc[i, "volatility"] = broker_id_min.loc[0, "volatility"]
        df_gb2.loc[i, "Trader_Name"] = broker_id_min.loc[0, "Trader_Name"]
        df_gb2.loc[i, "%complete"] = broker_id_min.loc[0, "%complete"]
        df_gb2.loc[i, "%DV"] = broker_id_min.loc[0, "%DV"]
        df_gb2.loc[i, "Venue_type"] = broker_id_min.loc[0, "Venue_type"]
        df_gb2.loc[i, 'Nb_Shares'] = broker_id_min.loc[0, 'Nb_Shares']
        df_gb2.loc[i, 'Val_order'] =  df_gb2.loc[i, 'Nb_Shares']*df_gb2.loc[i, 'Avg']
        
        if df_gb2.loc[i,'Val_order'] <= 50000 :
            df_gb2.loc[i, 'categorie'] = '0-50K'
        elif df_gb2.loc[i,'Val_order'] > 50000 and df_gb2.loc[i,'Val_order']<= 100000 :
            df_gb2.loc[i, 'categorie'] = '50K-100K'
        elif df_gb2.loc[i,'Val_order'] > 100000 and df_gb2.loc[i,'Val_order']<= 2000000 :
            df_gb2.loc[i, 'categorie'] = '100K-200K'
        elif df_gb2.loc[i,'Val_order'] > 200000 and df_gb2.loc[i,'Val_order']<= 500000 :
            df_gb2.loc[i, 'categorie'] = '200K-500K'
        elif df_gb2.loc[i,'Val_order'] > 500000 and df_gb2.loc[i,'Val_order']<= 1000000 : 
            df_gb2.loc[i, 'categorie'] = '500K-1M'
        elif df_gb2.loc[i,'Val_order'] > 1000000 and df_gb2.loc[i,'Val_order']<= 3000000 : 
            df_gb2.loc[i, 'categorie'] = '1M-3M'  
        else :
            df_gb2.loc[i, 'categorie'] = '>3M'
        # Filter broker DF on Tmax & inject relevant data in grouped_by DF
        broker_id_max = broker_id_df[broker_id_df["Transaction_Time"] == df_gb2.loc[i, "Tmax"]].reset_index()
        df_gb2.loc[i, "AskTmax"] = broker_id_max.loc[0, "Ask_Bench_Px"]
        df_gb2.loc[i, "BidTmax"] = broker_id_max.loc[0, "Bid_Bench_Px"]
        if df_gb2.loc[i, "Side"] == 'Buy' :
            
            df_gb2.loc[i, "Avg/Entree"] = ((df_gb2.iloc[i]['Avg']/df_gb2.iloc[i]['AskTmin'])-1)*100
            df_gb2.loc[i, "Last/Entree"] = ((df_gb2.iloc[i]['AskTmax']/df_gb2.iloc[i]['AskTmin'])-1)*100
        else :
            df_gb2.loc[i, "Avg/Entree"] = ((df_gb2.iloc[i]['Avg']/df_gb2.iloc[i]['BidTmin'])-1)*100
            df_gb2.loc[i, "Last/Entree"] = ((df_gb2.iloc[i]['BidTmax']/df_gb2.iloc[i]['BidTmin'])-1)*100
        df_gb2.loc[i, 'Entree'] = df_gb2.loc[i, 'Val_order']*(1 - df_gb2.loc[i, "Avg/Entree"]/100)
        df_gb2.loc[i, 'cout_avg'] = df_gb2.loc[i, 'Val_order'] - df_gb2.loc[i, 'Entree']
        df_gb2.loc[i, 'cout_last'] = df_gb2.loc[i, 'Entree']* df_gb2.loc[i, "Last/Entree"]/100
    df_gb2.sort_values(by=['Broker_ID'] )  
    #os.remove('tab_traité.csv')     
    
    #df_gb2.to_csv("tab_traité1.csv", index = False )
    df1 = pd.read_csv("data/tab_is.csv")
    os.remove("data/tab_is.csv")
    final_df = pd.concat([df1, df_gb2])
    final_df_removed =final_df.drop_duplicates(subset=['Tmin','Tmax'])
    final_df_removed.sort_values(by=['Tmin'], inplace =True )
                      
    final_df_removed.to_csv("data/tab_is.csv", index = False)
    
    
    return  

df = pd.read_csv("data/tab_is.csv")
df1 = pd.read_csv("data/tab_wheel.csv")
df.sort_values(by = ['Tmin'] )
df1.sort_values(by = ['Tmin'] )
date_today = datetime.datetime.now() 
date_today = date_today.strftime("%Y-%m-%d") 
date_start = pd.to_datetime(df['Tmin'][len(df)-1]) + datetime.timedelta(days=1)
date_start = date_start.strftime("%Y-%m-%d")


#collecte_data_IS(date_start, date_today)
recup_data_wheel(date_start, date_today)



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    