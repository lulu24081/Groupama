# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 10:39:19 2022

@author: LArib
"""



from dash import  html, dcc
import datetime
import pandas as pd
import numpy as np 
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash
import plotly.express as px
import plotly.graph_objects as go




 # --Initialisation of the app--

app = dash.Dash(__name__, suppress_callback_exceptions = True, external_stylesheets = [dbc.themes.BOOTSTRAP])
app.title = 'Dashboard'
server = app.server

 # ---Traitement data--
categorie = ['0-50K', '50K-100K', '100K-200K', '200K-500K', '500K-1M', '1M-3M', '>3M']
df_wheel = pd.read_csv("data/tab_wheel.csv")

df_wheel['Tmin'] = pd.to_datetime(df_wheel['Tmin'])
df_wheel['Tmax'] = pd.to_datetime(df_wheel['Tmax'])
df_wheel = df_wheel[df_wheel["%complete"] == 100.0]
df_wheel.sort_values(by=['Broker_ID'] )
Liste_traders_wheel = df_wheel['Trader_Name'].unique()
Liste_brokers_wheel = df_wheel['Broker_Name'].unique()
Liste_brokers_banalisée_wheel = []
for i in range(len(Liste_brokers_wheel)) :
    Liste_brokers_banalisée_wheel.append("Broker " f'{i+1}')
    
df_is = pd.read_csv("data/tab_is.csv")
df_is = df_is[df_is['Broker_Name']!= 'BMO']
df_is = df_is[df_is['Broker_Name'] != 'SGALGO_UL']
df_is['Tmin'] = pd.to_datetime(df_is['Tmin'])
df_is['Tmax'] = pd.to_datetime(df_is['Tmax'])
df_is = df_is[df_is['%complete'] == 100.0]
df_is.sort_values(by = ['Broker_ID'] )
Liste_traders_is = df_is['Trader_Name'].unique()
Liste_brokers_is = df_is['Broker_Name'].unique()
Liste_brokers_banalisée_is = []


    
for i in range(len(Liste_brokers_is)) :
    Liste_brokers_banalisée_is.append("Broker " f'{i+1}')
    
 # --Options for the gam's vue --
options_brok_gam_wheel = [{'label' : 'Tous les brokers', 'value' : 'Tous les brokers'}]
for i in range(len(Liste_brokers_wheel)):
    options_brok_gam_wheel.append({'label' : Liste_brokers_wheel[i], 'value' : Liste_brokers_wheel[i]})

 # --Options for the Broker's vue --   
options_brok_wheel = []
for i in range(len(Liste_brokers_wheel)):
    options_brok_wheel.append({'label' : Liste_brokers_wheel[i], 'value' : Liste_brokers_wheel[i]})

 # --Options for the trader's vue --
options_trader_wheel = [{'label' : 'Tous les traders', 'value' : 'Tous les traders'}]
for i in range(len(Liste_traders_wheel)):
    options_trader_wheel.append({'label' : Liste_traders_wheel[i], 'value' : Liste_traders_wheel[i]}) 
    
 # --Options for the gam's vue --
options_brok_gam_is = [{'label' : 'Tous les brokers', 'value' : 'Tous les brokers'}]
for i in range(len(Liste_brokers_is)):
    options_brok_gam_is.append({'label' : Liste_brokers_is[i], 'value' : Liste_brokers_is[i]})

 # --Options for the Broker's vue --   
options_brok_is = []
for i in range(len(Liste_brokers_is)):
    options_brok_is.append({'label' : Liste_brokers_is[i], 'value' : Liste_brokers_is[i]})

 # --Options for the trader's vue --
options_trader_is = [{'label' : 'Tous les traders', 'value' : 'Tous les traders'}]
for i in range(len(Liste_traders_is)):
    options_trader_is.append({'label' : Liste_traders_is[i], 'value' : Liste_traders_is[i]}) 
    
Venue_type = df_is['Venue_type'].unique()

options_venue_is = [{'label' : 'Tous les types', 'value' : 'Tous les types'}]
for i in range(len(Venue_type)) :
    options_venue_is.append({'label' : Venue_type[i], 'value' : Venue_type[i]})
 # --- Style---

colors = {
    'background' : '#111111',
    'text': '#7FDBFF'
}


Text_header = {
    'textAlign' : 'center',
    'position' : 'fixed',
    'color' : '#ffffff',
    'margin-top' : '50px',
    'text-decoration' : 'underline',
    
    
        }
    
header_style = {
    
    'top' : 0,
    'right' : 0,
    'padding-top' : 63,
    'padding-bottom' : 63,
    'backgroundColor' : '#007b7c',
    'text-decoration' : 'underline',
    'border-style' : 'inset',
    'textAlign' : 'center',
    'color' : "white",
    'font-size' : '155px',
    }


date_today = datetime.datetime.now() 
date_today = date_today.strftime("%Y-%m-%d")
cards = html.Div(
    [
         dbc.Row(
                [   dbc.Col([
                        dbc.Row(
                                    dcc.DatePickerRange(children = 'Select a date range: ',
                                        id = 'calendar',
                                        
                                            
                                            display_format = 'Y-M-D',
                                            start_date_placeholder_text = 'Y-M-D',
                                            end_date_placeholder_text = 'Y-M-D',
                                            min_date_allowed = df_is['Tmin'].min(),
                                            max_date_allowed = df_is['Tmin'].max(),
                                            start_date = '2022-05-02',
                                            end_date = date_today,
                                            style = {'textAlign' : 'center',
                                                     "border-radius": "30px",
                                                     'margin-top' : '60px',
                                                     'margin-left' : '40px',
                                                     'margin-bottom' : '15px',
                                                     'color' : 'white',
                                                     'background-color': '#e2dfdf',
                                                     'width' : '400px',
                                                      }
                                    )),
                        
                                ]),
                    
                    dbc.Col(
                       [
                        dbc.Row(
                             dcc.Dropdown(
                                        id = 'dropdown_data',
                                        options = [
                                            {'label' : 'Wheel', 'value' : 'Wheel'},
                                            {'label' : 'Algo_IS', 'value' : 'Algo_IS'}
                                            
                                            ],
                                        placeholder = "Select data",
                                        value = ['Wheel'],
                                        style = {'textAlign' : 'center', "border-radius" : "30px",
                                                 'margin-top' :'15px',
                                                 'margin-left' : '40px',
                                                 'margin-bottom' : '15px',
                                                 'background-color': '#e2dfdf',
                                                 'color' : 'black',
                                                 'width' : '80%',
                                                 'align-items': 'center',
                                                 'justify-content': 'center',
                                                 
                                                 }
                                        )
                             ),
                        dbc.Row(
                            
                                    dcc.Dropdown(
                                        id = 'dropdown_venue',
                                        options = options_venue_is,
                                        placeholder = "Select venue",
                                        value = ['Tous les types'],
                                        style = {'textAlign' : 'center', "border-radius": "30px",
                                                 'margin-left' : '40px',
                                                 'margin-bottom' : '15px',
                                                 'background-color' : '#e2dfdf',
                                                 'color' : '#3c4d5a',
                                                 'width' : '80%',}
                                                )   
                                ),
                               ]
                       ),
                    dbc.Col([
                        dbc.Row(
                            
                                    dcc.Dropdown(
                                        id = 'dropdown_vue',
                                        options = [
                                            {'label' : 'Vue gam', 'value' : 'Vue gam'},
                                            {'label' : 'Vue Broker', 'value' : 'Vue broker'},
                                            {'label' : 'Vue Trader', 'value' : 'Vue Trader'}
                                            ],
                                        placeholder = "Select vu",
                                        value = [ 'Vue gam'],
                                        style = {'textAlign' : 'center', "border-radius" : "30px",
                                                 'margin-top' :'15px',
                                                 'margin-left' : '40px',
                                                 'margin-bottom' : '15px',
                                                 'background-color': '#e2dfdf',
                                                 'color' : '#3c4d5a',
                                                 'width' : '80%',
                                                 
                                                 }
                                        )
                                    ),
                       dbc.Row(
                                     dcc.Dropdown(
                                        id = 'dropdown_brokers',
                                        options = [],
                                        placeholder = "Select précision",
                                        value = ['Tous les brokers'],
                                        style = {'textAlign' : 'center',
                                                 "border-radius": "30px",
                                                 'margin-left' : '40px',
                                                 'background-color': '#e2dfdf',
                                                 'margin-bottom' : '15px',
                                                 'color' : '#3c4d5a',
                                                 'width' : '80%',}
                                        )),
                                  ]),  
                       dbc.Col([
                           dbc.Row(
                       
                                    html.Button(id = 'submit-button-state',
                                                    children = 'Submit',
                                                      
                                                     style = {'textAlign' : 'center', "border-radius" : "30px",
                                                      'margin-left' : '90px',
                                                      'margin-top' : '70px',
                                                      'background-color': '#f15c2b',
                                                      'margin-bottom' : '15px',
                                                      'border_shadow' : 'white',
                                                      'color' : 'white',
                                                      'width' : '50%',
                                                      
                                                   } 
                                                )
                                ),
                              ]
                           ),
                        ],               
                )

],className = 'row',
        style = {'height' : '4%',
                 'margin-left' : '100px',
                 'margin-bottom' : '30px',
                 'magin-top' : '30px',
                 'background-color' : '#e2dfdf',
                 'box-shadow' : '15px 15px 15px' ,
                 'width' : '90%',
                 'border-radius' : '50px'})

header = html.Div(
    [
     html.Div([], className = 'col-2'), 

        html.Div([
            html.H1(children = 'Performance Dashboard :',
                    style = {'textAlign' : 'center',
                             'text-decoration' : 'underline',
                             'margin-bottom' : '30px'}
            )],
            className = 'col-8',
            style = {'padding-top' : '1%'}
        ),

        html.Div([
            html.Img(
                    src = app.get_asset_url('groupama_logo.svg'),
                    height = 'auto',
                    width = 'auto',
                    style = {'margin-right' : '15px',
                             'margin-top' : '20px',
                
                })
            ],
            className = 'col-2',
            style = {
                    'align-items' : 'center',
                    'padding-top' : '1%',
                    'height' : 'auto'})

        ],
        className = 'row',
        style = {'height' : '4%',
                'background-color' : '#e2dfdf',
                'margin-bottom' : '30px'}
        )

graph = html.Div(
    [    dbc.Row([
                    dbc.Col( 
                        
                                    dcc.Graph(id = 'pie_1', figure = {"layout" : {
                                                                    'plot_bgcolor' : '#e2dfdf',
                                                                    'paper_bgcolor' : '#e2dfdf',
                                                                    }}, 
                                        style = {"height":490,
                                                 'margin-left' : '8%',
                                                 'margin-top' : '20px',
                                                  'margin-bottom' : '20px',
                                                 'text-align' : 'center',
                                                 "width" :'85%',
                                                  }),
                                    
                                  
                    ),
                    dbc.Col( 
                        
                                    dcc.Graph(id = 'graph_1', figure = {"layout" : {
                                                                    'plot_bgcolor' : '#e2dfdf',
                                                                    'paper_bgcolor' : '#e2dfdf',
                                                                    }}, 
                                        style = {"height":490,
                                                 'margin-left' : '8%',
                                                 'margin-top' : '20px',
                                                  'margin-bottom' : '20px',
                                                 'text-align' : 'center',
                                                 "width" :'85%',
                                                  }),
                  
                                )],style = {
                                             'margin-left' : '100px',
                                             'margin-bottom' : '30px',
                                             'magin-top' : '30px',
                                            'background-color' : '#e2dfdf',
                                            'box-shadow' : '15px 15px 15px' ,
                                            'width' : '90%',
                                            "border-radius" : "50px"} 
                                    ),    
                             
        dbc.Row([
                    dbc.Col( 
                        
                                    dcc.Graph(id = 'graph_2', figure = {"layout" : {
                                                                    'plot_bgcolor' : '#e2dfdf',
                                                                    'paper_bgcolor' : '#e2dfdf',
                                                                    }}, 
                                        style = {"height":490,
                                                 'margin-left' : '8%',
                                                 'margin-top' : '20px',
                                                  'margin-bottom' : '20px',
                                                 'text-align' : 'center',
                                                 "width" :'85%',
                                                  }
                                            ),
                    
                         ),
                    dbc.Col( 
                        
                                    dcc.Graph(id = 'graph_3', figure = {"layout" : {
                                                                    'plot_bgcolor' : '#e2dfdf',
                                                                    'paper_bgcolor' : '#e2dfdf',
                                                                    }}, 
                                        style = {"height":490,
                                                 'margin-left' : '8%',
                                                 'margin-top' : '20px',
                                                  'margin-bottom' : '20px',
                                                 'text-align' : 'center',
                                                 "width" :'85%',
                                                  }
                                            )
                            )
                         
                    ], style = {
                                             'margin-left' : '100px',
                                             'margin-bottom' : '30px',
                                             'magin-top' : '30px',
                                            'background-color' : '#e2dfdf',
                                            'box-shadow' : '15px 15px 15px' ,
                                            'width' : '90%',
                                            "border-radius" : "50px"} 
                        ),                            
                                    
                                    
                
         dbc.Row(
                [
                       dbc.Col( 
                        
                                    dcc.Graph(id = 'pie_2', figure = {"layout" : {
                                                                    'plot_bgcolor' : '#e2dfdf',
                                                                    'paper_bgcolor' : '#e2dfdf',
                                                                                }
                                                                    }, 
                                        style = {"height":490,
                                                 'margin-left' : '8%',
                                                 'margin-top' : '20px',
                                                  'margin-bottom' : '20px',
                                                 'text-align' : 'center',
                                                 "width" :'85%',
                                                  }
                                            ),
                                    
                         
                            ),
                       dbc.Col( 
                        
                                    dcc.Graph(id = 'pie_3', figure = {"layout" : {
                                                                    'plot_bgcolor' : '#e2dfdf',
                                                                    'paper_bgcolor' : '#e2dfdf',
                                                                                }
                                                                    }, 
                                        style = {"height":490,
                                                 'margin-left' : '8%',
                                                 'margin-top' : '20px',
                                                  'margin-bottom' : '20px',
                                                 'text-align' : 'center',
                                                 "width" :'85%',
                                                  }
                                            )
                                ) 
                       ],style = {
                                             'margin-left' : '100px',
                                             'margin-bottom' : '30px',
                                             'magin-top' : '30px',
                                            'background-color' : '#e2dfdf',
                                            'box-shadow' : '15px 15px 15px' ,
                                            'width' : '90%',
                                            "border-radius" : "50px"} 
                           ),               
        dbc.Row(
                [
                    dbc.Col(
                        
                        
                                    dcc.Graph(id = 'graph_4', figure = {"layout" : {
                                            'plot_bgcolor' : '#e2dfdf',
                                            'paper_bgcolor' : '#e2dfdf',
                                                                            }
                                                            }
                                        , style = {"height" : 490,
                                                   'margin-left' : '10px',
                                                   'margin-top' : '20px',
                                                   'margin-bottom' : '20px'
                                                   
                                                   }
                                        )
                            ),
                                            
                    dbc.Col(
                        
                        
                                    dcc.Graph(id = 'pie_4', figure = {"layout" : {
                                            'plot_bgcolor' : '#e2dfdf',
                                            'paper_bgcolor' : '#e2dfdf',
                                                                        }
                                                                }
                                        , style={"height":490,
                                                 'margin-left' : '10px',
                                                 'margin-top' : '20px',
                                                 'margin-bottom' : '20px'
                                                   
                                                }
                                        )
                        )
                                                    
                ],style = {
                 'margin-left' : '100px',
                 'margin-bottom' : '30px',
                 'magin-top' : '30px',
                 'background-color' : '#e2dfdf',
                 'box-shadow' : '15px 15px 15px' ,
                 'width' : '90%',
                 "border-radius" : "50px"} 
            ),
       dbc.Row(
                [
                    dbc.Col(
                        
                                [
                                    dcc.Graph(id = 'graph_5', figure = {"layout" : {
                                                'plot_bgcolor' : '#e2dfdf',
                                            'paper_bgcolor' : '#e2dfdf',
                                            
                                                                            }
                                                                            }
                                        , style={"height" : 490,
                                                 'margin-left' : '10px',
                                                 'margin-top' : '20px',
                                                 'margin-bottom' : '20px'
                                                              })
                                                     ]),
                        
                   dbc.Col(
                        
                        
                                [
                                    dcc.Graph(id = 'graph_6', figure = {"layout" : {
                                            'plot_bgcolor' : '#e2dfdf',
                                            'paper_bgcolor' : '#e2dfdf',
                                                                    }
                                                            }
                                        , style={"height":490,
                                                   'margin-left' : '10px',
                                                   'margin-top' : '20px',
                                                   'margin-bottom' : '20px'
                                                              })
                                                     
                        
                                ],
                            ),
                            ], style = {
                                     'margin-left' : '100px',
                                     'margin-bottom' : '30px',
                                     'magin-top' : '30px',
                                     'background-color' : '#e2dfdf',
                                     'box-shadow': '15px 15px 15px' ,
                                     'width' : '90%',
                                     "border-radius" : "50px"}  
                                ),
        dbc.Row(   
                    [
                        dbc.Col(
                        
                        
                                [
                                    dcc.Graph(id = 'graph_7', figure = {"layout" : {
                                            'plot_bgcolor' : '#e2dfdf',
                                            'paper_bgcolor' : '#e2dfdf',
                                        }}, style = {"height" : 490,
                                                     'margin-left' : '10px',
                                                     'margin-top' : '20px',
                                                     'margin-bottom' : '20px'
                                                   
                                                              })
                                                     ]),
                        
                    dbc.Col(
                       
                       
                                [
                                    dcc.Graph(id = 'graph_8', figure = {"layout" : {
                                            'plot_bgcolor' : '#e2dfdf',
                                            'paper_bgcolor' : '#e2dfdf',
                                                                        }
                                                                    }
                                        , style={"height":490,
                                                 'margin-left' : '10px',
                                                 'margin-top' : '20px',
                                                 'margin-bottom' : '20px'
                                                   
                                                  }
                                            )
                                ]
                            ),
                            ],style = {
                                 'margin-left' : '100px',
                                 'margin-bottom' : '30px',
                                 'magin-top' : '30px',
                                 'background-color' : '#e2dfdf',
                                 'box-shadow' : '15px 15px 15px' ,
                                 'width' : '90%',
                                 "border-radius" : "50px"}      
            ),
                                            
        dbc.Row(
                [
                    dbc.Col(
                        
                               [ 
                                    dcc.Graph(id = 'graph_9', figure = {"layout" : {
                                            'plot_bgcolor' : '#e2dfdf',
                                            'paper_bgcolor' : '#e2dfdf',
                                                                            }
                                        }, style={"height" : 490,
                                                  'margin-left' : '10px',
                                                  'margin-top' : '20px',
                                                  'margin-bottom' : '20px'
                                                   
                                                 }
                                            )           
                            ]
                        ),
                        
                    dbc.Col(
                       
                            [
                                
                                    dcc.Graph(id = 'pie_5', figure = {"layout" : {
                                            'plot_bgcolor' : '#e2dfdf',
                                            'paper_bgcolor' : '#e2dfdf',
                                                                        }
                                                                },
                                         style={"height" : 490,
                                                'margin-left' : '10px',
                                                'margin-top' : '20px',
                                                'margin-bottom' : '20px'
                                                   
                                                              })
                                    ]),
                    ],style = {
                 'margin-left' : '100px',
                 'margin-bottom' : '30px',
                 'magin-top' : '30px',
                 'background-color' : '#e2dfdf',
                 'box-shadow' : '15px 15px 15px' ,
                 'width' : '90%',
                 "border-radius" : "50px"} ),
                        
         dbc.Row(
                 [
                    
                    dbc.Col(
                       
                        
                              [  
                                    dcc.Graph(id = 'graph_10', figure = {"layout" : {
                                            'plot_bgcolor' : '#e2dfdf',
                                            'paper_bgcolor' : '#e2dfdf',
                                        }}, style = {"height":490,
                                                   'margin-left' : '10px',
                                                   'margin-top' : '20px',
                                                   'margin-bottom' : '20px'
                                                   
                                                              })
                                                     ]),
                        
                    dbc.Col(
                       
                       
                                [
                                    dcc.Graph(id = 'pie_6', figure = {"layout" : {
                                            'plot_bgcolor' : '#e2dfdf',
                                            'paper_bgcolor' : '#e2dfdf',
                                        }},style={"height":490,
                                                   'margin-left' : '10px',
                                                   'margin-top' : '20px',
                                                   'margin-bottom' : '20px'
                                                   
                                                              })
                                                    ]
                            )],style = {
                                             'margin-left' : '100px',
                                             'margin-bottom' : '30px',
                                             'magin-top' : '30px',
                                             'background-color' : '#e2dfdf',
                                             'box-shadow' : '15px 15px 15px' ,
                                             'width' : '90%',
                                             "border-radius" : "50px"} 
                                               ),      
                                                  
        dbc.Row(
                          [
                    dbc.Col(
                                [
                        
                                    dcc.Graph(id = 'graph_11', figure = {"layout" : {
                                            'plot_bgcolor' : '#e2dfdf',
                                            'paper_bgcolor' : '#e2dfdf',
                                        }}, style={"height":490,
                                                   'margin-left' : '10px',
                                                   'margin-top' : '20px',
                                                   'margin-bottom' : '20px'
                                                              }
                                                   )]
                            ),
                                            
                   dbc.Col(
                            [
                        
                                    dcc.Graph(id = 'pie_7', figure = {"layout": {
                                            'plot_bgcolor' : '#e2dfdf',
                                            'paper_bgcolor' : '#e2dfdf',
                                        }}, style={"height":490,
                                                   'margin-left' : '10px',
                                                   'margin-top' : '20px',
                                                   'margin-bottom' : '20px',          
                                                   'magin-right' : '-25px',
                                                              }
                                                   )]
                                            )
                                                    
                                            ] ,style = {
                                                     'margin-left' : '100px',
                                                     'margin-bottom' : '30px',
                                                     'magin-top' : '30px',
                                                     'background-color' : '#e2dfdf',
                                                     'box-shadow' : '15px 15px 15px' ,
                                                     'width' : '90%',
                                                     "border-radius" : "50px"}   
                                    ),                              
                                ])    
                            
#007b7c vert
#e2dfdf gris 
            
     # --layout of the app--
app.layout = html.Div([header, cards, graph, dcc.Store(id = 'update_df')],
                      style={'height' : '100%',
                             'backgroundColor' : '#007b7c', })

     # --Update of the trader's list according to the choice of type of brokers--

def update_liste_traders(dropdown_data_value) :
    
    if dropdown_data_value == 'Wheel' :
        Liste_traders = Liste_traders_wheel
        
    elif dropdown_data_value == 'Algo_IS' :
        Liste_traders = Liste_traders_is
    
    return Liste_traders

   # --Update of the broker's list according to the choice of type of brokers--
def update_liste_brokers(dropdown_data_value) :
    
    if dropdown_data_value == 'Wheel' :
        Liste_brokers = Liste_brokers_wheel
        
    elif dropdown_data_value == 'Algo_IS' :
        Liste_brokers = Liste_brokers_is
    
    return  Liste_brokers

    # --Average for every brokers  'cas' can only take the value 'Last' and 'Avg'--
def moyenne_brok(df_update, Liste_brokers, cas) :  

    a= f'{cas}' +"/" +"Entree"
    avg = np.array([pd.concat([df_update[(df_update['Broker_Name'] == i) &
                                  (df_update['Side'] == 'Buy')][a], 
                               df_update[(df_update['Broker_Name'] == i) &
                                  (df_update['Side'] == 'Sell')][a]*(-1)]).mean() 
                                        for i in (Liste_brokers)])*100
    return avg

    # --Average for every brokers and taraders 'cas' can only take the value 'Last' and 'Avg'--
def trader_brok(df_update, dropdown_brokers_value, Liste_brokers, cas ):    
    a= f'{cas}' +"/" +"Entree"

    last = np.array([pd.concat([df_update[(df_update['Broker_Name'] == i) &
                                                 (df_update['Trader_Name'] == dropdown_brokers_value) & 
                                                 (df_update['Side']=='Buy')][a],
                                       df_update[(df_update['Broker_Name'] == i) & 
                                                 (df_update['Trader_Name'] == dropdown_brokers_value) &
                                                 (df_update['Side']=='Sell')][a]*(-1)]).mean() 
                                                    for i in (Liste_brokers)])*100
    return last
   # --We create the banalized list of brokers--
def liste_banalise(Liste_brokers, dropdown_brokers_value):
    a = 0
    Liste_brokers_banalisée = []
    for i in Liste_brokers :
        if i != dropdown_brokers_value :
            Liste_brokers_banalisée.append("Broker " f'{a+1}')
            a += 1
        else :
                Liste_brokers_banalisée.append(dropdown_brokers_value)
    return Liste_brokers_banalisée
    
 #  --Upadting of the value of the second dropdown--
@app.callback(
    Output('dropdown_brokers', 'options'),
    Input('dropdown_data', 'value'),
    Input('dropdown_vue', 'value'),
    
    )

def update_dropdown_brok( dropdown_data_value, dropdown_vue_value):
    Liste_brokers = update_liste_brokers(dropdown_data_value)
    Liste_traders = update_liste_traders(dropdown_data_value) 
    if dropdown_data_value == 'Wheel' :
        if dropdown_vue_value == 'Vue gam':
            return options_brok_gam_wheel
        elif  dropdown_vue_value == 'Vue broker':
            return options_brok_wheel
        else :
            return options_trader_wheel
    elif dropdown_data_value == 'Algo_IS' :
        if dropdown_vue_value == 'Vue gam':
            return options_brok_gam_is
        elif  dropdown_vue_value == 'Vue broker':
            return options_brok_is
        else :
            return options_trader_is
        

@app.callback(
    Output('tab', 'data'),
    Input('submit-button-state', 'n_clicks'),
    State('dropdown_data', 'value'),
    State('dropdown_venue', 'value'),
    State('calendar', 'start_date'),
    State('calendar', 'end_date'),
    State('dropdown_brokers', 'value'),
    State('dropdown_vue', 'value')
    
    )

def update_data(n_clicks,dropdown_data_value,dropdown_venue_value, start_date, end_date, dropdown_brokers_value, dropdown_vue_value) :
    df_update = pd.DataFrame(columns = ['Broker_ID', 'Broker_Name', 'Tmin', 'Tmax', 'AskTmin' , 'BidTmin', 'Avg', 'Side', 'market_cap',
                                        'volatility', 'Trader_Name', '%complete', '%DV', 'Venue_type', 'Nb_Shares', 'Val_order', 'AskTmax',
                                        'BidTmax', 'Avg/Entree', 'Last/Entree', 'catÃ©gorie','categorie'])
    if dropdown_data_value == 'Wheel' :
        df_update= df_wheel
        
        if dropdown_venue_value == 'Tous les types' :
            df_update= df_wheel
            
        else : 
            df_update = df_wheel[df_wheel['Venue_type'] == dropdown_venue_value]
        
            
    elif dropdown_data_value == 'Algo_IS' :
        df_update = df_is
        
        if dropdown_venue_value == 'Tous les types' :
            df_update= df_is
        else : 
            df_update = df_is[df_is['Venue_type'] == dropdown_venue_value]
    

    if dropdown_vue_value == 'Vue gam':
        if dropdown_brokers_value != 'Tous les brokers' :
             df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) & (df_update['Broker_Name'] ==dropdown_brokers_value)]
             
        else :
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) ]
            
    elif dropdown_vue_value == 'Vue broker' :
        df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date)& (df_update['Broker_Name'] ==dropdown_brokers_value)]
        
    elif dropdown_vue_value == 'Vue Trader': 
        if dropdown_brokers_value == 'Tous les traders' : 
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date)]
            
        else : 
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) & (
                           df_update['Trader_Name'] == dropdown_brokers_value)]
    
    return df_update

@app.callback(
    Output('pie_1', 'figure'),
    Input('submit-button-state', 'n_clicks'),
    State('dropdown_data', 'value'),
    State('dropdown_venue', 'value'),
    State('calendar', 'start_date'),
    State('calendar', 'end_date'),
    State('dropdown_brokers', 'value'),
    State('dropdown_vue', 'value')
    )

def update_pie_1(n_clicks,dropdown_data_value,dropdown_venue_value, start_date, end_date, dropdown_brokers_value, dropdown_vue_value):
    # df_update is the df which represents the user's choice 
    Liste_brokers = update_liste_brokers(dropdown_data_value)
    Liste_traders = update_liste_traders(dropdown_data_value)
    categorie = ['0-50K', '50K-100K', '100K-200K', '200K-500K', '500K-1M', '1M-3M', '>3M']
    
    
    fig = go.Figure()
    df_update = pd.DataFrame(columns = ['Broker_ID', 'Broker_Name', 'Tmin', 'Tmax', 'AskTmin' , 'BidTmin', 'Avg', 'Side', 'market_cap',
                                        'volatility', 'Trader_Name', '%complete', '%DV', 'Venue_type', 'Nb_Shares', 'Val_order', 'AskTmax',
                                        'BidTmax', 'Avg/Entree', 'Last/Entree', 'catÃ©gorie','categorie'])
    if dropdown_data_value == 'Wheel' :
        df_update= df_wheel
        
        if dropdown_venue_value == 'Tous les types' :
            df_update= df_wheel
            
        else : 
            df_update = df_wheel[df_wheel['Venue_type'] == dropdown_venue_value]
        
            
    elif dropdown_data_value == 'Algo_IS' :
        df_update = df_is
        
        if dropdown_venue_value == 'Tous les types' :
            df_update= df_is
        else : 
            df_update = df_is[df_is['Venue_type'] == dropdown_venue_value]
    df_update2 = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) ]

    if dropdown_vue_value == 'Vue gam':
        if dropdown_brokers_value != 'Tous les brokers' :
             df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) & (df_update['Broker_Name'] ==dropdown_brokers_value)]
             
        else :
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) ]
            
    elif dropdown_vue_value == 'Vue broker' :
        df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date)& (df_update['Broker_Name'] ==dropdown_brokers_value)]
        
    elif dropdown_vue_value == 'Vue Trader': 
        if dropdown_brokers_value == 'Tous les traders' : 
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date)]
            
        else : 
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) & (
                           df_update['Trader_Name'] == dropdown_brokers_value)]
    
   
    
    if dropdown_brokers_value == 'Tous les traders'  or dropdown_brokers_value == 'Tous les brokers' :
        fig = go.Figure()
        L2 = []
        
        categorie = df_update['categorie'].unique()
        Liste_traders = df_update['Trader_Name'].unique()
        for v in range(len(categorie)) :
            
            b = len(df_update[df_update['categorie'] == categorie[v]])
            L2.append(b)
        for i in Liste_traders : 
            L3 = []
            for v in range(len(categorie)) :
                c = len(df_update[(df_update['categorie'] == categorie[v])& (df_update['Trader_Name'] == i) ])
                L3.append(c)
            L3 = np.array(L3)
            fig.add_trace(go.Scatterpolar(
            r=(L3/sum(L3))*100,
            theta = categorie,
            fill='toself',
            name=f'{i}'))
            
                
            
        L2 = np.array(L2)
        fig.add_trace(go.Scatterpolar(
        r=(L2/sum(L2))*100,
        theta = categorie,
        fill='toself',
        name='Ref Gam'))
                
        
    else : 
        fig = go.Figure()
        L= []
        L2 = []
       
                                                    
        if dropdown_vue_value == 'Vue broker' or dropdown_vue_value == 'Vue gam':
            categorie = df_update['categorie'].unique()
            for v in range(len(categorie)) :
                a= len(df_update[(df_update['categorie'] == categorie[v]) & (
                                                            df_update['Broker_Name'] == dropdown_brokers_value)])
                b= len(df_update2[df_update2['categorie'] == categorie[v]])
                L.append(a)
                L2.append(b)
                
        else : 
            for v in range(len(categorie)) :
                a= len(df_update[(df_update['categorie'] == categorie[v]) & (
                                                            df_update['Trader_Name'] == dropdown_brokers_value)])
                b= len(df_update2[df_update2['categorie'] == categorie[v]])
                L.append(a)
                L2.append(b)
            
        L, L2 = np.array(L), np.array(L2)  
        
        fig.add_trace(go.Scatterpolar(
        r=(L/sum(L))*100,
        theta = categorie,
        fill='toself',
        name=f'{dropdown_brokers_value}'))
        
        fig.add_trace(go.Scatterpolar(
        r=(L2/sum(L2))*100,
        theta = categorie,
        fill='toself',
        name='Ref Gam'))
        
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
              visible=True,
              range=[0, 100]
            )),
          showlegend=True,
          title_text = "Répartition par taille d'ordres :",
          title_font_family="Times New Roman",
          
          
                                    plot_bgcolor = 	'#e2dfdf',
                                    paper_bgcolor = '#e2dfdf',
                                    margin = dict(t = 80, b = 20),
                                    font = dict(color = 'black',
                                                size = 13,
                                                family="Times New Roman"),
                                    legend=dict(
        
                                traceorder="reversed",
                                title = " Trader : ",
                                title_font_family="Times New Roman",
                                font=dict(
                                    family="Times New Roman",
                                    size=12,
                                    color="black"
                                ),
                                bgcolor="LightSteelBlue",
                                bordercolor="Black",
                                borderwidth=2
                            )       
        ),    
    return fig
        
@app.callback(
    Output('graph_1', 'figure'),
    Input('submit-button-state', 'n_clicks'),
    State('dropdown_data', 'value'),
    State('dropdown_venue', 'value'),
    State('calendar', 'start_date'),
    State('calendar', 'end_date'),
    State('dropdown_brokers', 'value'),
    State('dropdown_vue', 'value')
    )

def update_graph_1(n_clicks,dropdown_data_value,dropdown_venue_value, start_date, end_date, dropdown_brokers_value, dropdown_vue_value):
    df_update = pd.DataFrame(columns = ['Broker_ID', 'Broker_Name', 'Tmin', 'Tmax', 'AskTmin' , 'BidTmin', 'Avg', 'Side', 'market_cap',
                                        'volatility', 'Trader_Name', '%complete', '%DV', 'Venue_type', 'Nb_Shares', 'Val_order', 'AskTmax',
                                        'BidTmax', 'Avg/Entree', 'Last/Entree', 'catÃ©gorie','categorie'])
    categorie = ['0-50K', '50K-100K', '100K-200K', '200K-500K', '500K-1M', '1M-3M', '>3M']
    if dropdown_data_value == 'Wheel' :
        df_update= df_wheel
        
        if dropdown_venue_value == 'Tous les types' :
            df_update= df_wheel
            
        else : 
            df_update = df_wheel[df_wheel['Venue_type'] == dropdown_venue_value]
            
    elif dropdown_data_value == 'Algo_IS' :
        df_update = df_is
        
        if dropdown_venue_value == 'Tous les types' :
            df_update= df_is
        else : 
            df_update = df_is[df_is['Venue_type'] == dropdown_venue_value]
    df_copie = df_update.copy()
    df_copie = df_copie[(df_copie['Tmin'] >= start_date ) & (df_copie['Tmin'] <= end_date) ]
    df_gam  = pd.DataFrame(columns = ['categorie', 'compte'])
    df_gam['categorie'] = categorie
    compte_gam =[]
    for i in (categorie) : 
        a= df_copie[df_copie['categorie'] == i]
        compte_gam.append(len(a))
    df_gam['compte'] = compte_gam
    df_gam['Nom'] = ['gam']*(len(df_gam))
        
    if dropdown_vue_value == 'Vue gam':
        if dropdown_brokers_value != 'Tous les brokers' :
             df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) & (df_update['Broker_Name'] ==dropdown_brokers_value)]
             
        else :
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) ]
            
    elif dropdown_vue_value == 'Vue broker' :
        df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date)& (df_update['Broker_Name'] ==dropdown_brokers_value)]
        
    elif dropdown_vue_value == 'Vue Trader': 
        if dropdown_brokers_value == 'Tous les traders' : 
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date)]
            
        else : 
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date)]
            
    if dropdown_brokers_value == 'Tous les traders'  or dropdown_brokers_value == 'Tous les brokers' :
        
        Liste_brokers = df_update['Broker_Name'].unique()
        categorie = ['0-50K', '50K-100K', '100K-200K', '200K-500K', '500K-1M', '1M-3M', '>3M']
        df_update['compte'] = [1]*len(df_update)
        
        df_sec = df_update.groupby(['categorie', 'Broker_Name'], as_index = False ).agg({'compte' : sum})
        df_sec['rapport'] = ''
        
        for i in range(len(df_sec)):
             df_sec.loc[i,'rapport'] = round(((df_sec.loc[i, 'compte']/ df_sec[df_sec['categorie'] == df_sec.loc[i, 'categorie']]['compte'].sum())*100),2)
        df_graph = pd.DataFrame(columns = ['Broker_Name', "categorie", 'compte', 'rapport'])
        for  i in range(len(categorie)) :
             dfp = df_sec[df_sec['categorie'] == categorie[i]]
             dfp.sort_values( by = ['rapport'], inplace = True,)
             
             df_graph = pd.concat([df_graph, dfp]) 
        
        fig = px.bar(df_graph,
                       x="categorie",
                       y = 'rapport',
                       color = 'Broker_Name', 
                       text = 'rapport', 
                       hover_data  = ['Broker_Name','compte'], 
                       color_discrete_sequence = px.colors.sequential.RdBu,
                       labels= {"Broker_Name" : "Broker"},
                       title="Proportion du nombre d'ordres en fonction de leur taille :")
        
    else : 
        
        df_update['compte'] = [1]*len(df_update)
        if dropdown_vue_value == 'Vue Trader':
            df_sec = df_update.groupby(['categorie', 'Trader_Name'], as_index = False ).agg({'compte' : sum}).copy()
            df_sec = df_sec[df_sec['Trader_Name'] == dropdown_brokers_value]
            
        else :
            df_sec = df_update.groupby(['categorie', 'Broker_Name'], as_index = False ).agg({'compte' : sum}).copy()
            df_sec = df_sec[df_sec['Broker_Name'] == dropdown_brokers_value]
        df_sec['Nom'] = [f'{dropdown_brokers_value}']*(len(df_sec))
        df_final = pd.concat([df_sec, df_gam])
        df_final = df_final[df_final['compte'] != 0]
        df_final.reset_index(inplace = True)
        fig = px.bar(df_final,
                       x="categorie",
                       y = 'compte',
                       color = 'Nom', 
                       text = 'compte', 
                       barmode='group',
                       
                       title="Proportion du nombre d'ordres en fonction de leur taille :")
        
    fig.update_layout(title_font_family="Times New Roman",
                          plot_bgcolor = 	'#e2dfdf',
                          paper_bgcolor = '#e2dfdf',
                          margin = dict(t = 80, b = 20),
                          font = dict(color = 'black',size = 13),
                          legend=dict(
        
                                traceorder="reversed",
                                title = " Broker : ",
                                title_font_family="Times New Roman",
                                font=dict(
                                    family="Times New Roman",
                                    size=12,
                                    color="black"
                                ),
                                bgcolor="LightSteelBlue",
                                bordercolor="Black",
                                borderwidth=2
                            )
                         )
        
    return fig
           
@app.callback(
    Output('graph_2', 'figure'),
    Input('submit-button-state', 'n_clicks'),
    State('dropdown_data', 'value'),
    State('dropdown_venue', 'value'),
    State('calendar', 'start_date'),
    State('calendar', 'end_date'),
    State('dropdown_brokers', 'value'),
    State('dropdown_vue', 'value')
    )

def update_graph_2(n_clicks,dropdown_data_value,dropdown_venue_value, start_date, end_date, dropdown_brokers_value, dropdown_vue_value):
    df_update = pd.DataFrame(columns = ['Broker_ID', 'Broker_Name', 'Tmin', 'Tmax', 'AskTmin' , 'BidTmin', 'Avg', 'Side', 'market_cap',
                                        'volatility', 'Trader_Name', '%complete', '%DV', 'Venue_type', 'Nb_Shares', 'Val_order', 'AskTmax',
                                        'BidTmax', 'Avg/Entree', 'Last/Entree', 'catÃ©gorie','categorie'])
    Liste_brokers = []
    Liste_brokers = update_liste_brokers(dropdown_data_value)
    Liste_traders = update_liste_traders(dropdown_data_value) 
    if dropdown_data_value == 'Wheel' :
        df_update= df_wheel
        
        if dropdown_venue_value == 'Tous les types' :
            df_update= df_wheel
            
        else : 
            df_update = df_wheel[df_wheel['Venue_type'] == dropdown_venue_value]
            
    elif dropdown_data_value == 'Algo_IS' :
        df_update = df_is
        
        if dropdown_venue_value == 'Tous les types' :
            df_update= df_is
        else : 
            df_update = df_is[df_is['Venue_type'] == dropdown_venue_value]

    if dropdown_vue_value == 'Vue gam':
        if dropdown_brokers_value != 'Tous les brokers' :
             df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) ]
             
        else :
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) ]
            
    elif dropdown_vue_value == 'Vue broker' :
        df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date)]
        
    elif dropdown_vue_value == 'Vue Trader': 
        if dropdown_brokers_value == 'Tous les traders' : 
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date)]
            
        else : 
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) & (
                           df_update['Trader_Name'] == dropdown_brokers_value)]
    
    cout_avg =[]
    cout_last =[]
    Liste_brokers_banalisée = liste_banalise(Liste_brokers, dropdown_brokers_value)
        
    if dropdown_vue_value == 'Vue gam':
        for i in Liste_brokers :
            a = df_update[(df_update['Broker_Name'] == i) & (df_update['Side'] == 'Buy')]['cout_avg']
            b = df_update[(df_update['Broker_Name'] == i) & (df_update['Side'] == 'Sell')]['cout_avg']
            cout_avg.append(round(a.sum()-b.sum(),2))
            a = df_update[(df_update['Broker_Name'] == i) & (df_update['Side'] == 'Buy')]['cout_last']
            b = df_update[(df_update['Broker_Name'] == i) & (df_update['Side'] == 'Sell')]['cout_last']
            cout_last.append(round(a.sum()-b.sum(),2))
    
        ecart=  [round(x - y, 2) for x, y in zip(cout_last, cout_avg)]
        
            
        compte = []
        freq = df_update['Broker_Name'].value_counts()
        for i in Liste_brokers :
            if df_update['Broker_Name'].str.contains(i).any() :
                compte.append(freq[i])
            else :
                compte.append(0)
        df_new = pd.DataFrame ({'Liste_brokers' : Liste_brokers,
                                'Liste_brokers_banalisée' : Liste_brokers_banalisée,
                                'compte' : compte,
                                'cout_last' : cout_last,
                                'cout_avg' : cout_avg,
                                'ecart' : ecart} )
        df_new = df_new[df_new['compte'] != 0]
        df_new.sort_values(by = 'ecart', ascending = False, inplace = True)
        Liste_brokers = df_new['Liste_brokers']
        df_new.reset_index(inplace = True)
        nb_brokers = len(Liste_brokers)
        classement = df_new.index[df_new['Liste_brokers'] == dropdown_brokers_value].tolist()
        
        if dropdown_brokers_value == 'Tous les brokers' :
            
            index = [f'{df_new["Liste_brokers"][i]}' + " " + f'{[df_new["compte"][i]]}' for i in range(len(df_new['Liste_brokers'].tolist()))]
        
        else :
            df0 = pd.DataFrame({'Liste_brokers' : [0],
                                'Liste_brokers_banalisée' : [0],
                                'cout_avg' : round(df_new['cout_avg'].mean(),2),
                                'cout_last' : round(df_new['cout_last'].mean(),2),
                                'ecart' : round(df_new['ecart'].mean(),2),
                                'compte' : df_new['compte'].sum() })
            df1 = df_new.head(1)
            df2 = df_new[df_new['Liste_brokers'] == dropdown_brokers_value]
            df3 = df_new.tail(1)
            df_new = pd.concat([df0, df1, df2, df3])
            df_new.reset_index(inplace = True)
            index = ["Moyenne Gam ", " Premier : "f'{df_new["Liste_brokers"][1]} ' ,
                     "Position : " f'{classement[0]+1 }' +' sur '+f'{ nb_brokers }',
                     "Dernier : "f'{df_new["Liste_brokers"][3]}']
    
    elif dropdown_vue_value == 'Vue broker' :
        for i in Liste_brokers :
            a = df_update[(df_update['Broker_Name'] == i) & (df_update['Side'] == 'Buy')]['cout_avg']
            b = df_update[(df_update['Broker_Name'] == i) & (df_update['Side'] == 'Sell')]['cout_avg']
            cout_avg.append(round(a.sum()-b.sum(),2))
            a = df_update[(df_update['Broker_Name'] == i) & (df_update['Side'] == 'Buy')]['cout_last']
            b = df_update[(df_update['Broker_Name'] == i) & (df_update['Side'] == 'Sell')]['cout_last']
            cout_last.append(round(a.sum()-b.sum(),2))
    
        ecart=  [round(x - y, 2) for x, y in zip(cout_last, cout_avg)]
        
            
        compte = []
        freq = df_update['Broker_Name'].value_counts()
        for i in Liste_brokers :
            if df_update['Broker_Name'].str.contains(i).any() :
                compte.append(freq[i])
            else :
                compte.append(0)
        df_new = pd.DataFrame ({'Liste_brokers' : Liste_brokers,
                                'Liste_brokers_banalisée' : Liste_brokers_banalisée,
                                'compte' : compte,
                                'cout_last' : cout_last,
                                'cout_avg' : cout_avg,
                                'ecart' : ecart} )
        df_new = df_new[df_new['compte'] != 0]
        df_new.sort_values(by = 'ecart', ascending = False, inplace = True)
        Liste_brokers = df_new['Liste_brokers']
        df_new.reset_index(inplace = True)
        nb_brokers = len(Liste_brokers)
        classement = df_new.index[df_new['Liste_brokers'] == dropdown_brokers_value].tolist()
        
        
        df0 = pd.DataFrame({'Liste_brokers' : [0],
                                'Liste_brokers_banalisée' : [0],
                                'cout_avg' : round(df_new['cout_avg'].mean(),2),
                                'cout_last' : round(df_new['cout_last'].mean(),2),
                                'ecart' : round(df_new['ecart'].mean(),2),
                                'compte' : df_new['compte'].sum() })
        df1 = df_new.head(1)
        df2 = df_new[df_new['Liste_brokers_banalisée'] == dropdown_brokers_value]
        df3 = df_new.tail(1)
        df_new = pd.concat([df0, df1, df2, df3])
        df_new.reset_index(inplace = True)
        index = [" Moyenne Gam ", " Premier " ,
                 "  position : " f'{classement[0] +1}' +' sur '+f'{ nb_brokers +1}', "Dernier "]
        
    else : 
        if dropdown_brokers_value == 'Tous les traders' : 
            
            for i in (Liste_traders) :
                a = df_update[(df_update['Trader_Name'] == i) & (df_update['Side'] == 'Buy')]['cout_avg']
                b = df_update[(df_update['Trader_Name'] == i) & (df_update['Side'] == 'Sell')]['cout_avg']
                cout_avg.append(round(a.sum()-b.sum(),2))
                a = df_update[(df_update['Trader_Name'] == i) & (df_update['Side'] == 'Buy')]['cout_last']
                b = df_update[(df_update['Trader_Name'] == i) & (df_update['Side'] == 'Sell')]['cout_last']
                cout_last.append(round(a.sum()-b.sum(),2))
            
            ecart=  [round(x - y, 2) for x, y in zip(cout_last, cout_avg)]
            compte = []
            freq = df_update['Trader_Name'].value_counts()
            for i in Liste_traders :
                if df_update['Trader_Name'].str.contains(i).any() :
                    compte.append(freq[i])
                else :
                        compte.append(0)
            
            
            df_new = pd.DataFrame ({'Liste_traders' : Liste_traders,
                                'compte' : compte,
                                'cout_last' : cout_last,
                                'cout_avg' : cout_avg,
                                'ecart' : ecart} )
            df_new = df_new[df_new['compte'] != 0]
            df_new.sort_values(by = 'ecart', ascending = False, inplace = True)
            
            df_new.reset_index(inplace = True)
            nb_brokers = len(Liste_brokers)
            index = [f'{df_new["Liste_traders"][i]}' + " " + f'{[df_new["compte"][i]]}' 
                     for i in range(len(df_new['Liste_traders'].tolist()))]
            
            
        else : 
            for i in (Liste_brokers) :
                a = df_update[(df_update['Broker_Name'] == i) & (df_update['Trader_Name'] ==dropdown_brokers_value) &
                              (df_update['Side'] == 'Buy')]['cout_avg']
                b = df_update[(df_update['Broker_Name'] == i) & (df_update['Trader_Name'] ==dropdown_brokers_value) &
                              (df_update['Side'] == 'Sell')]['cout_avg']
                cout_avg.append(round(a.sum()-b.sum(),2))
                a = df_update[(df_update['Broker_Name'] == i) & (df_update['Trader_Name'] ==dropdown_brokers_value) &
                              (df_update['Side'] == 'Buy')]['cout_last']
                b = df_update[(df_update['Broker_Name'] == i) & (df_update['Trader_Name'] ==dropdown_brokers_value) &
                              (df_update['Side'] == 'Sell')]['cout_last']
                cout_last.append(round(a.sum()-b.sum(),2))
                
            ecart=  [round(x - y, 2) for x, y in zip(cout_last, cout_avg)]
            compte = []
            freq = df_update['Broker_Name'].value_counts()
            for i in Liste_brokers :
                if df_update['Broker_Name'].str.contains(i).any() :
                    compte.append(freq[i])
                else :
                        compte.append(0)
            df_new = pd.DataFrame ({'Liste_brokers' : Liste_brokers, 
                                    'Liste_brokers_banalisée' : Liste_brokers_banalisée,
                                    'cout_avg' : cout_avg,
                                    'cout_last' : cout_last,
                                    'ecart' : ecart,
                                    'compte' : compte })
            df_new = df_new[df_new['compte'] != 0]
            df_new.sort_values(by = 'ecart', ascending = False, inplace = True)
            Liste_brokers = df_new['Liste_brokers']
            df_new.reset_index(inplace = True)
            index = [f'{df_new["Liste_brokers"][i]}' + " " + f'{[df_new["compte"][i]]}' for i in range(len(df_new['Liste_brokers'].tolist()))]
            
    figure = {
                    'data': [
                        {'x' : index, 'y' : df_new['cout_avg'].tolist(),
                         'type' : 'bar', 'name': 'Avg', 'weight' : '30px',
                         'text' : df_new['cout_avg'].tolist(), 'textposition' : 'outside', 'textfont_size' : 16,
                         'marker' : {'size' : 12, 'line' : {'width' : 2,
                                                            'color' : 'DarkSlateGrey'}}
                         
                         
                         },
                        {'x' : index, 'y' : df_new['cout_last'].tolist(),
                         'type': 'bar', 'name': u'last', 'text' : df_new['cout_last'].tolist(),
                         'textposition' : 'outside', 'textfont_size' : 16,
                         'marker' :{'size' : 20, 'line' : {'width' : 2,
                                                           'color' : 'DarkSlateGrey'}}
                         
                         },
                       {'x' : index, 'y' : df_new['ecart'].tolist(),
                         'type': 'bar', 'name': u'ecart', 'text' : df_new['ecart'].tolist(), 'textposition' : 'outside',
                        'textfont_size' : 16, 'marker' : {'color' : 'grey',
                                                          'size' : 12,
                                                          'line' : {'width' : 2,
                                                                    'color' : 'DarkSlateGrey'}}
                         
                         },
                        
                    ],
                    'layout' : {
                        'title' :  " Coût par rapport à l'entrée du  " f'{start_date}' " au " f'{end_date} ' ":" ,
                        'title_font_family' : "Times New Roman",
                        'plot_bgcolor' : 	'#e2dfdf',
                        'paper_bgcolor' : '#e2dfdf',
                        'font' : dict(color = 'black',
                                      size = 12,
                                      family="Times New Roman"),
                        'automargin' : True,
                        'legend' : dict(
        
                                traceorder="reversed",
                                title = " Broker : ",
                                title_font_family="Times New Roman",
                                font=dict(
                                    family="Times New Roman",
                                    size=12,
                                    color="black"
                                ),
                                bgcolor="LightSteelBlue",
                                bordercolor="Black",
                                borderwidth=2
                            ) 
                    }
                }
          
    return figure

@app.callback(
    Output('graph_3', 'figure'),
    Input('submit-button-state', 'n_clicks'),
    State('dropdown_data', 'value'),
    State('dropdown_venue', 'value'),
    State('calendar', 'start_date'),
    State('calendar', 'end_date'),
    State('dropdown_brokers', 'value'),
    State('dropdown_vue', 'value')
    )

def update_graph_3(n_clicks,dropdown_data_value,dropdown_venue_value, start_date, end_date, dropdown_brokers_value, dropdown_vue_value):
    df_update = pd.DataFrame(columns = ['Broker_ID', 'Broker_Name', 'Side', 'traded_Shares', 'Transaction_Time',
                  'Ask_Bench_Px', 'Bid_Bench_Px', 'Average', 'market_cap', 'volatility', 'Trader_Name', '%complete', '%DV', 'Venue_type', 'Nb_Shares', 'categorie' ])
    if dropdown_data_value == 'Wheel' :
        df_update= df_wheel
        
        if dropdown_venue_value == 'Tous les types' :
            df_update= df_wheel
            
        else : 
            df_update = df_wheel[df_wheel['Venue_type'] == dropdown_venue_value]
            
    elif dropdown_data_value == 'Algo_IS' :
        df_update = df_is
        
        if dropdown_venue_value == 'Tous les types' :
            df_update= df_is
        else : 
            df_update = df_is[df_is['Venue_type'] == dropdown_venue_value]

    if dropdown_vue_value == 'Vue gam':
        if dropdown_brokers_value != 'Tous les brokers' :
             df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) & (df_update['Broker_Name'] ==dropdown_brokers_value)]
             
        else :
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) ]
            
    elif dropdown_vue_value == 'Vue broker' :
        df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date)& (df_update['Broker_Name'] ==dropdown_brokers_value)]
        
    elif dropdown_vue_value == 'Vue Trader': 
        if dropdown_brokers_value == 'Tous les traders' : 
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date)]
            
        else : 
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) & (
                           df_update['Trader_Name'] == dropdown_brokers_value)]
            
            
    df_update.reset_index(inplace = True)
    df_new = pd.DataFrame()
    
    for i in (range(len(df_update))) : 
        if df_update.loc[i, 'Side'] == 'Sell' :
            df_update.loc[i, 'cout_last'] = df_update.loc[i, 'cout_last']*(-1)
            df_update.loc[i, 'cout_avg'] = df_update.loc[i, 'cout_avg']*(-1)
        df_update.loc[i,'ecart'] = df_update.loc[i, 'cout_last'] - df_update.loc[i, 'cout_avg']
    df_new = pd.DataFrame()
    df_new['ecart'] = df_update['ecart'].cumsum(axis =0)
    df_update['coût du last'] = df_update['cout_last'].cumsum(axis =0) 
    df_update["coût de l'avg"] = df_update['cout_avg'].cumsum(axis =0) 
    df_new["coût de l'avg pour tous"] = df_update['cout_avg'].cumsum(axis =0)  
    df_new['coût du last'] = df_update['cout_last'].cumsum(axis =0) 

    df_new['Tmin'] =df_update['Tmin']
    Time = df_new['Tmin'].tolist()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=Time, y=df_new["coût de l'avg pour tous"].tolist(),
                        mode='lines',
                        name='avg'))
    fig.add_trace(go.Scatter(x=Time, y=df_new['coût du last'].tolist(),
                        mode='lines',
                        name='last'))
    fig.add_trace(go.Scatter(x=Time, y=df_new['ecart'].tolist(),
                        mode='lines', name='ecart'))

    fig.update_layout(title_text = "Evolution du coût par ordre par rapport au cours d'entrée :",
                                    title_font_family="Times New Roman",
                                    plot_bgcolor = 	'#e2dfdf',
                                    paper_bgcolor = '#e2dfdf',
                                    margin = dict(t = 80, b = 20),
                                    font = dict(color = 'black',
                                                size = 13,
                                                family="Times New Roman"),
                                    legend=dict(
        
                                traceorder="reversed",
                                title = " Legend : ",
                                title_font_family="Times New Roman",
                               
                                font=dict(
                                    family="Times New Roman",
                                    size=12,
                                    color="black"
                                ),
                                bgcolor="LightSteelBlue",
                                bordercolor="Black",
                                borderwidth=2
                            )
                         )
    return fig
     
     
@app.callback(
    Output('pie_2', 'figure'),
    Input('submit-button-state', 'n_clicks'),
    State('dropdown_data', 'value'),
    State('dropdown_venue', 'value'),
    State('calendar', 'start_date'),
    State('calendar', 'end_date'),
    State('dropdown_brokers', 'value'),
    State('dropdown_vue', 'value')
    )

def update_pie_2(n_clicks,dropdown_data_value,dropdown_venue_value, start_date, end_date, dropdown_brokers_value, dropdown_vue_value):
    df_update = pd.DataFrame(columns = ['Broker_ID', 'Broker_Name', 'Side', 'traded_Shares', 'Transaction_Time',
                  'Ask_Bench_Px', 'Bid_Bench_Px', 'Average', 'market_cap', 'volatility', 'Trader_Name', '%complete', '%DV', 'Venue_type', 'Nb_Shares', 'categorie' ])
    if dropdown_data_value == 'Wheel' :
        df_update= df_wheel
        
        if dropdown_venue_value == 'Tous les types' :
            df_update= df_wheel
            
        else : 
            df_update = df_wheel[df_wheel['Venue_type'] == dropdown_venue_value]
            
    elif dropdown_data_value == 'Algo_IS' :
        df_update = df_is
        
        if dropdown_venue_value == 'Tous les types' :
            df_update= df_is
        else : 
            df_update = df_is[df_is['Venue_type'] == dropdown_venue_value]

    if dropdown_vue_value == 'Vue gam':
        if dropdown_brokers_value != 'Tous les brokers' :
             df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) & (df_update['Broker_Name'] ==dropdown_brokers_value)]
             
        else :
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) ]
            
    elif dropdown_vue_value == 'Vue broker' :
        df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date)& (df_update['Broker_Name'] ==dropdown_brokers_value)]
        
    elif dropdown_vue_value == 'Vue Trader': 
        if dropdown_brokers_value == 'Tous les traders' : 
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date)]
            
        else : 
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) & (
                           df_update['Trader_Name'] == dropdown_brokers_value)]
            
    if dropdown_brokers_value == 'Tous les traders'  or dropdown_brokers_value == 'Tous les brokers' :
    
        figure = px.sunburst(df_update, path = ['Broker_Name', 'Venue_type'],
                             color_discrete_sequence = px.colors.sequential.RdBu)
        figure.update_traces(textinfo = "label+percent parent"),
        figure.update_layout(title_text = "Proportion par Venue_type :",
                                    plot_bgcolor = 	'#e2dfdf',
                                    paper_bgcolor = '#e2dfdf',
                                    margin = dict(t = 80, b = 20),
                                    font = dict(color = 'black',
                                                size = 13,
                                                family = 'Times New Roman'),
                                    legend=dict(
        
                                traceorder="reversed",
                                title = " Broker : ",
                                title_font_family="Times New Roman",
                                font=dict(
                                    family="Times New Roman",
                                    size=12,
                                    color="black"
                                ),
                                bgcolor="LightSteelBlue",
                                bordercolor="Black",
                                borderwidth=2
                            )
                         )
        return figure 
    else : 
        figure = px.sunburst(df_update, path = ['Venue_type'],
                             color_discrete_sequence = px.colors.sequential.RdBu)
        figure.update_traces(textinfo = "label+percent parent"),
        figure.update_layout(title_text = "Proportion par Venue_type :",
                                    plot_bgcolor = 	'#e2dfdf',
                                    paper_bgcolor = '#e2dfdf',
                                    margin = dict(t = 80, b = 20),
                                    font = dict(color = 'black',
                                                size = 13,
                                                family="Times New Roman"),
                                    legend=dict(
        
                                traceorder="reversed",
                                title = " Broker : ",
                                title_font_family="Times New Roman",
                                font=dict(
                                    family="Times New Roman",
                                    size=12,
                                    color="black"
                                ),
                                bgcolor="LightSteelBlue",
                                bordercolor="Black",
                                borderwidth=2
                            )
                         )
        return figure 
        
@app.callback(
    Output('pie_3', 'figure'),
    Input('submit-button-state', 'n_clicks'),
    State('dropdown_data', 'value'),
    State('dropdown_venue', 'value'),
    State('calendar', 'start_date'),
    State('calendar', 'end_date'),
    State('dropdown_brokers', 'value'),
    State('dropdown_vue', 'value')
    )
def update_pie_3(n_clicks,dropdown_data_value,dropdown_venue_value, start_date, end_date, dropdown_brokers_value, dropdown_vue_value):

    df_update = pd.DataFrame(columns = ['Broker_ID', 'Broker_Name', 'Side', 'traded_Shares', 'Transaction_Time',
                  'Ask_Bench_Px', 'Bid_Bench_Px', 'Average', 'market_cap', 'volatility', 'Trader_Name', '%complete', '%DV', 'Venue_type', 'Nb_Shares', 'categorie' ])
    if dropdown_data_value == 'Wheel' :
        df_update= df_wheel
    elif dropdown_data_value == 'Algo_IS' :
        df_update = df_is
        
    df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) ]   
    figure = px.sunburst(df_update, path = ['Venue_type'],
                         color_discrete_sequence = px.colors.sequential.RdBu)
    figure.update_traces(textinfo = "label+percent parent"),
    figure.update_layout(title_text = "Proportion réfèrence :",
                                plot_bgcolor = 	'#e2dfdf',
                                paper_bgcolor = '#e2dfdf',
                                margin = dict(t = 80, b = 20),
                                font = dict(color = 'black',
                                            size = 13,
                                            family="Times New Roman"),
                                legend = dict(
                                              font = dict(color = 'black')
                                             )
                                )
    return figure 


@app.callback(
    Output('graph_4', 'figure'),
    Input('submit-button-state', 'n_clicks'),
    State('dropdown_data', 'value'),
    State('dropdown_venue', 'value'),
    State('calendar','start_date'),
    State('calendar','end_date'),
    State('dropdown_brokers','value'),
    State('dropdown_vue','value')
    
    )

def update_graph_4(n_clicks, dropdown_data_value, dropdown_venue_value, start_date, end_date, dropdown_brokers_value, dropdown_vue_value) :
    Liste_brokers = update_liste_brokers(dropdown_data_value)
    Liste_traders = update_liste_traders(dropdown_data_value) 
    df_update = pd.DataFrame(columns = ['Broker_ID', 'Broker_Name', 'Side', 'traded_Shares', 'Transaction_Time',
                  'Ask_Bench_Px', 'Bid_Bench_Px', 'Average', 'market_cap', 'volatility', 'Trader_Name', '%complete', '%DV', 'Venue_type', 'Nb_Shares', 'categorie' ])
    if dropdown_data_value == 'Wheel' :
        df_update= df_wheel
        
        if dropdown_venue_value == 'Tous les types' :
            df_update= df_wheel
            
        else : 
            df_update = df_wheel[df_wheel['Venue_type'] == dropdown_venue_value]
            
    elif dropdown_data_value == 'Algo_IS' :
        df_update = df_is
        
        if dropdown_venue_value == 'Tous les types' :
            df_update= df_is
        else : 
            df_update = df_is[df_is['Venue_type'] == dropdown_venue_value]

    if dropdown_vue_value == 'Vue gam':
        if dropdown_brokers_value != 'Tous les brokers' :
             df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) ]
             
        else :
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) ]
            
    elif dropdown_vue_value == 'Vue broker' :
        df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date)]
        
    elif dropdown_vue_value == 'Vue Trader': 
        if dropdown_brokers_value == 'Tous les traders' : 
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date)]
            
        else : 
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) & (
                           df_update['Trader_Name'] == dropdown_brokers_value)]
           
    
    Liste_brokers_banalisée = liste_banalise(Liste_brokers, dropdown_brokers_value)
    
    if dropdown_brokers_value == 'Tous les traders' :
        avg = trader_brok(df_update, dropdown_brokers_value, Liste_brokers, "Avg" )
        last = trader_brok(df_update, dropdown_brokers_value, Liste_brokers, "Last" )
    else : 
        avg = moyenne_brok(df_update, Liste_brokers, "Avg")
        last = moyenne_brok(df_update, Liste_brokers, "Last")
        
        
    if dropdown_vue_value == 'Vue gam':
        ecart = []
        for i in range(len(avg)):
            if last[i] >= 0 :
                ecart.append( last[i] - avg[i])
            else :
                ecart.append(-(last[i] - avg[i]))
                      
        
        for i in range(len(avg)) :
            avg[i] = round(avg[i],2)
            last[i] = round(last[i],2)
            ecart[i] = round(ecart[i],2)

        compte = []
        freq = df_update['Broker_Name'].value_counts()
        for i in Liste_brokers :
            if df_update['Broker_Name'].str.contains(i).any() :
                compte.append(freq[i])
            else :
                compte.append(0)
        df_new = pd.DataFrame ({'Liste_brokers' : Liste_brokers,
                                'avg' : avg,
                                'last' : last,
                                'ecart' : ecart,
                                'compte' : compte })
        df_new = df_new[df_new['compte'] != 0]
        df_new.sort_values(by = 'ecart', ascending = False, inplace = True)
        Liste_brokers = df_new['Liste_brokers']
        df_new.reset_index(inplace = True)
        nb_brokers = len(Liste_brokers)
        classement = df_new.index[df_new['Liste_brokers'] == dropdown_brokers_value].tolist()
        
        if dropdown_brokers_value == 'Tous les brokers' :
            
            index = [f'{df_new["Liste_brokers"][i]}' + " " + f'{[df_new["compte"][i]]}' for i in range(len(df_new['Liste_brokers'].tolist()))]
        
        else :
            df0 = pd.DataFrame({'Liste_brokers' : [0],
                                'Liste_brokers_banalisée' : [0],
                                'avg' : round(df_new['avg'].mean(),2), 'last' : round(df_new['last'].mean(),2),
                                'ecart' : round(df_new['ecart'].mean(),2), 'compte' : df_new['compte'].sum() })
            df1 = df_new.head(1)
            df2 = df_new[df_new['Liste_brokers'] == dropdown_brokers_value]
            df3 = df_new.tail(1)
            df_new = pd.concat([df0, df1, df2, df3])
            df_new.reset_index(inplace = True)
            index = ["Moyenne Gam ", " Premier : "f'{df_new["Liste_brokers"][1]} ' ,
                     "Position : " f'{classement[0] +1 }' +' sur '+f'{ nb_brokers }',
                     "Dernier : "f'{df_new["Liste_brokers"][3]}']
            
            
        
    elif dropdown_vue_value == 'Vue broker' :
                                                                     
        ecart = []
        for i in range(len(avg)):
            if last[i] >= 0 :
                ecart.append( last[i] - avg[i])
            else :
                ecart.append(-(last[i] - avg[i]))
                      
        
        for i in range(len(avg)) :
            avg[i] = round(avg[i],2)
            last[i] = round(last[i],2)
            ecart[i] = round(ecart[i],2)

        compte =[]
        freq = df_update['Broker_Name'].value_counts()
        for i in Liste_brokers :
            if df_update['Broker_Name'].str.contains(i).any() :
                compte.append(freq[i])
            else :
                compte.append(0)
        df_new = pd.DataFrame ({'Liste_brokers' : Liste_brokers,
                                'Liste_brokers_banalisée' : Liste_brokers_banalisée,
                                'avg' : avg,
                                'last' : last,
                                'ecart' : ecart,
                                'compte' : compte })
        df_new = df_new[df_new['compte'] !=0]
        df_new.sort_values(by = 'ecart', ascending = False, inplace = True)
        Liste_brokers = df_new['Liste_brokers']
        df_new.reset_index(inplace = True)
        nb_brokers = len(Liste_brokers)
        classement = df_new.index[df_new['Liste_brokers'] == dropdown_brokers_value].tolist()
        df0 = pd.DataFrame({'Liste_brokers' : [0],
                                'Liste_brokers_banalisée' : [0],
                                'avg' : round(df_new['avg'].mean(),2),
                                'last' : round(df_new['last'].mean(),2),
                                'ecart' : round(df_new['ecart'].mean(), 2),
                                'compte' : df_new['compte'].sum() })
        df1 = df_new.head(1)
        df2 = df_new[df_new['Liste_brokers_banalisée'] == dropdown_brokers_value]
        df3 = df_new.tail(1)
        df_new = pd.concat([df0, df1, df2, df3])
        df_new.reset_index(inplace = True)
        index = [" Moyenne Gam ", " Premier " ,
                 "  position : " f'{classement[0] +1}' +' sur '+f'{ nb_brokers }', "Dernier "]
        
        
    else : 
        if dropdown_brokers_value == 'Tous les traders' : 
            avg = np.array([pd.concat([df_update[(df_update['Trader_Name'] == i) &
                                                 (df_update['Side'] == 'Buy')]['Avg/Entree'], 
                                       df_update[(df_update['Trader_Name'] == i) &
                                                 (df_update['Side'] == 'Sell')]['Avg/Entree']*(-1)]).mean() 
                                                    for i in (Liste_traders)])*100
                                                                          
            last = np.array([pd.concat([df_update[(df_update['Trader_Name'] == i) &
                                                  (df_update['Side'] == 'Buy')]['Last/Entree'], 
                                        df_update[(df_update['Trader_Name'] == i) &
                                                  (df_update['Side'] == 'Sell')]['Last/Entree']*(-1)]).mean() 
                                                     for i in (Liste_traders)])*100
            
                                                                           
            ecart = []
            for i in range(len(avg)):
                if last[i] >= 0 :
                    ecart.append( last[i] - avg[i])
                else :
                    ecart.append(-(last[i] - avg[i]))
                          
            
            for i in range(len(avg)) :
                avg[i] = round(avg[i], 2)
                last[i] = round(last[i], 2)
                ecart[i] = round(ecart[i], 2)
    
            compte = []
            freq = df_update['Trader_Name'].value_counts()
            for i in Liste_traders :
                if df_update['Trader_Name'].str.contains(i).any() :
                    compte.append(freq[i])
                else :
                    compte.append(0)
            df_new = pd.DataFrame ({'Liste_traders' : Liste_traders,
                                    'avg' : avg,
                                    'last' : last,
                                    'ecart' : ecart,
                                    'compte' : compte })
            df_new.sort_values(by = 'ecart', ascending = False, inplace = True)
            df_new.reset_index(inplace = True)
            index = [f'{df_new["Liste_traders"][i]}' + " " + f'{[df_new["compte"][i]]}' 
                     for i in range(len(df_new['Liste_traders'].tolist()))]
            
        else : 
            avg = trader_brok(df_update, dropdown_brokers_value, Liste_brokers, "Avg" )
            last = trader_brok(df_update, dropdown_brokers_value, Liste_brokers, "Last" )
            ecart = []
            for i in range(len(avg)):
                if last[i] >= 0 :
                    ecart.append( last[i] - avg[i])
                else :
                    ecart.append(-(last[i] - avg[i]))
                          
        
            
            for i in range(len(avg)) :
                avg[i] = round(avg[i],2)
                last[i] = round(last[i],2)
                ecart[i] = round(ecart[i],2)
    
            compte = []
            
            for i in Liste_brokers :
                if df_update['Broker_Name'].str.contains(i).any() :
                    compte.append(df_update['Broker_Name'].value_counts()[i])
                else :
                    compte.append(0)
            df_new = pd.DataFrame ({'Liste_brokers' : Liste_brokers, 
                                    'Liste_brokers_banalisée' : Liste_brokers_banalisée,
                                    'avg' : avg,
                                    'last' : last,
                                    'ecart' : ecart,
                                    'compte' : compte })
            df_new = df_new[df_new['compte'] != 0]
            df_new.sort_values(by = 'ecart', ascending = False, inplace = True)
            Liste_brokers = df_new['Liste_brokers']
            df_new.reset_index(inplace = True)
            index = [f'{df_new["Liste_brokers"][i]}' + " " + f'{[df_new["compte"][i]]}' for i in range(len(df_new['Liste_brokers'].tolist()))]
            
            
            
    
        
    figure = {
                    'data': [
                        {'x' : index, 'y' : df_new['avg'].tolist(),
                         'type' : 'bar', 'name': 'Avg', 'weight' : '30px',
                         'text' : df_new['avg'].tolist(), 'textposition' : 'outside', 'textfont_size' : 16,
                         'marker' : {'size' : 12, 'line' : {'width' : 2,
                                                            'color' : 'DarkSlateGrey'}}
                         
                         
                         },
                        {'x' : index, 'y' : df_new['last'].tolist(),
                         'type': 'bar', 'name': u'last', 'text' : df_new['last'].tolist(),
                         'textposition' : 'outside', 'textfont_size' : 16,
                         'marker' :{'size' : 20, 'line' : {'width' : 2,
                                                           'color' : 'DarkSlateGrey'}}
                         
                         },
                        {'x' : index, 'y' : df_new['ecart'].tolist(),
                         'type': 'bar', 'name': u'ecart', 'text' : df_new['ecart'].tolist(), 'textposition' : 'outside',
                        'textfont_size' : 16, 'marker' : {'color' : 'grey',
                                                          'size' : 12,
                                                          'line' : {'width' : 2,
                                                                    'color' : 'DarkSlateGrey'}}
                         
                         },
                        
                    
                    ],
                    'layout' : {
                        'title' :  " Moyennes  du  " f'{start_date}' " au " f'{end_date}' ":" ,
                        'plot_bgcolor' : 	'#e2dfdf',
                        'paper_bgcolor' : '#e2dfdf',
                        'font' : dict(color = 'black',
                                      size = 12,
                                      family="Times New Roman"),
                        'automargin' : True,
                        'legend' : dict(
        
                                traceorder="reversed",
                                title = " Broker : ",
                                title_font_family="Times New Roman",
                                font=dict(
                                    family="Times New Roman",
                                    size=12,
                                    color="black"
                                ),
                                bgcolor="LightSteelBlue",
                                bordercolor="Black",
                                borderwidth=2
                        ) 
                    }
                }
          
    return figure
    


@app.callback(
    Output('pie_4', 'figure'),
    Input('submit-button-state', 'n_clicks'),
    State('dropdown_data', 'value'),
    State('dropdown_venue', 'value'),
    State('calendar', 'start_date'),
    State('calendar', 'end_date'),
    State('dropdown_brokers', 'value'),
    State('dropdown_vue', 'value')
    )

def update_pie_4(n_clicks, dropdown_data_value, dropdown_venue_value, start_date, end_date, dropdown_brokers_value, dropdown_vue_value):
    Liste_brokers = update_liste_brokers(dropdown_data_value)
    Liste_traders = update_liste_traders(dropdown_data_value) 
    df_update = pd.DataFrame(columns = ['Broker_ID', 'Broker_Name', 'Side', 'traded_Shares', 'Transaction_Time',
                  'Ask_Bench_Px', 'Bid_Bench_Px', 'Average', 'market_cap', 'volatility', 'Trader_Name', '%complete', '%DV', 'Venue_type', 'Nb_Shares', 'categorie' ])
    if dropdown_data_value == 'Wheel' :
        df_update= df_wheel
        
        if dropdown_venue_value == 'Tous les types' :
            df_update= df_wheel
            
        else : 
            df_update = df_wheel[df_wheel['Venue_type'] == dropdown_venue_value]
            
    elif dropdown_data_value == 'Algo_IS' :
        df_update = df_is
        
        if dropdown_venue_value == 'Tous les types' :
            df_update= df_is
        else : 
            df_update = df_is[df_is['Venue_type'] == dropdown_venue_value]

    if dropdown_vue_value == 'Vue gam':
        if dropdown_brokers_value != 'Tous les brokers' :
             df_update = df_update[(df_update['Tmin'] >= start_date ) ]
             
        else :
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) ]
            
    elif dropdown_vue_value == 'Vue broker' :
        df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date)]
        
    elif dropdown_vue_value == 'Vue Trader': 
        if dropdown_brokers_value == 'Tous les traders' : 
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date)]
            
        else : 
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) & (
                           df_update['Trader_Name'] == dropdown_brokers_value)]
            
    
    
    Liste_brokers_banalisée = liste_banalise(Liste_brokers, dropdown_brokers_value)
    
    if dropdown_vue_value == 'Vue gam' :
        Liste_brok = Liste_brokers
        compte = np.array([len(df_update[df_update['Broker_Name'] == i]) for i in Liste_brokers])
        df_vol = pd.DataFrame((zip( Liste_brok, compte)), columns  = ['Liste_brok', 'compte'])
        df_vol = df_vol[df_vol['compte'] != 0]
        figure =  px.pie(df_vol, values = 'compte', names = 'Liste_brok',
                         hole = .3, color_discrete_sequence = px.colors.sequential.RdBu)
        figure.update_layout(title_text = "Proportion par brokers :",
                             title_font_family="Times New Roman",
                                plot_bgcolor = 	'#e2dfdf',
                                paper_bgcolor = '#e2dfdf',
                                margin = dict(t = 80, b = 20),
                                font = dict(color = 'black',
                                            size = 13, 
                                            family = 'Times New Roman'),
                                legend=dict(
        
                                traceorder="reversed",
                                title = " Broker : ",
                                title_font_family="Times New Roman",
                                font=dict(
                                    family="Times New Roman",
                                    size=12,
                                    color="black"
                                ),
                                bgcolor="LightSteelBlue",
                                bordercolor="Black",
                                borderwidth=2
                            )
                         )
        
        return figure
        
    elif dropdown_vue_value == 'Vue Trader':
        Liste_brok = Liste_brokers
        if  dropdown_brokers_value == 'Tous les traders': 
            
            compte = np.array([len(df_update[df_update['Trader_Name'] == i]) for i in Liste_traders])
            df_vol = pd.DataFrame((zip( Liste_traders, compte)), columns  = [ 'Liste_traders', 'compte'])
            df_vol = df_vol[df_vol['compte'] != 0]
            figure =  px.pie(df_vol, values = 'compte', names = 'Liste_traders',
                             hole=.3, color_discrete_sequence = px.colors.sequential.RdBu)
            figure.update_layout(title_text = "Proportion par trader :",
                                 title_font_family="Times New Roman",
                                    plot_bgcolor = 	'#e2dfdf',
                                    paper_bgcolor = '#e2dfdf',
                                    margin = dict(t=80, b=20),
                                    font = dict(color = 'black',
                                                size = 13, 
                                                family = 'Times New Roman'),
                                    legend=dict(
        
                                traceorder="reversed",
                                title = " Broker : ",
                                title_font_family="Times New Roman",
                                font=dict(
                                    family="Times New Roman",
                                    size=12,
                                    color="black"
                                ),
                                bgcolor="LightSteelBlue",
                                bordercolor="Black",
                                borderwidth=2
                            )
                         )
            return figure 
        else :  
            
            compte = np.array([len(df_update[df_update['Broker_Name'] == i])for i in Liste_brok])
            df_vol = pd.DataFrame((zip( Liste_brok,compte)), columns  = [ 'Liste_brok', 'compte'])
            df_vol = df_vol[df_vol['compte'] != 0]
            figure =  px.pie(df_vol, values='compte', names = 'Liste_brok',
                             hole=.3, color_discrete_sequence = px.colors.sequential.RdBu)
            figure.update_layout(title_text = "Proportion par brokers :",
                                plot_bgcolor = 	'#e2dfdf',
                                paper_bgcolor = '#e2dfdf',
                                margin = dict(t = 80, b = 20),
                                font = dict(color = 'black',
                                            size = 13, 
                                            family = 'Times New Roman'),
                                legend=dict(
        
                                traceorder="reversed",
                                title = " Broker : ",
                                title_font_family="Times New Roman",
                                font=dict(
                                    family="Courier",
                                    size=12,
                                    color="black"
                                ),
                                bgcolor="LightSteelBlue",
                                bordercolor="Black",
                                borderwidth=2
                            )
                         )
            return figure 
    elif dropdown_vue_value == 'Vue broker' : 
        Liste_brok = Liste_brokers_banalisée
   
        
        compte = np.array([len(df_update[df_update['Broker_Name'] == i])for i in Liste_brokers])
        df_vol = pd.DataFrame((zip( Liste_brok, compte)), columns  = ['Liste_brok', 'compte'])
        df_vol = df_vol[df_vol['compte'] != 0]
        figure =  px.pie(df_vol, values='compte', names = 'Liste_brok',
                         hole = .3, color_discrete_sequence = px.colors.sequential.RdBu)
        figure.update_layout(title_text = "Proportion par brokers :",
                             title_font_family = 'Times New Roman',
                                plot_bgcolor = 	'#e2dfdf',
                                paper_bgcolor = '#e2dfdf',
                                margin = dict(t = 80, b = 20),
                                font = dict(color = 'black',
                                            size = 12, 
                                            family = 'Times New Roman'),
                                legend=dict(
        
                                traceorder="reversed",
                                title = " Broker : ",
                                title_font_family="Times New Roman",
                                font=dict(
                                    family="Courier",
                                    size=13,
                                    color="black"
                                ),
                                bgcolor="LightSteelBlue",
                                bordercolor="Black",
                                borderwidth=2
                            )
                         )
        
        return figure
    

   #---Callback for the second graph ---
@app.callback(
    Output('graph_5', 'figure'),
    Input('submit-button-state', 'n_clicks'),
    State('dropdown_data', 'value'),
    State('dropdown_venue', 'value'),
    State('calendar', 'start_date'),
    State('calendar', 'end_date'),
    State('dropdown_brokers', 'value'),
    State('dropdown_vue', 'value')
    
    )

def update_graph_5(n_clicks, dropdown_data_value, dropdown_venue_value, start_date, end_date, dropdown_brokers_value, dropdown_vue_value):
    
    Liste_brokers = update_liste_brokers(dropdown_data_value)
    Liste_traders = update_liste_traders(dropdown_data_value) 
    df_update = pd.DataFrame(columns = ['Broker_ID', 'Broker_Name', 'Side', 'traded_Shares', 'Transaction_Time',
                  'Ask_Bench_Px', 'Bid_Bench_Px', 'Average', 'market_cap', 'volatility', 'Trader_Name', '%complete', '%DV', 'Venue_type', 'Nb_Shares', 'categorie' ])
    if dropdown_data_value == 'Wheel' :
        df_update= df_wheel
        
        if dropdown_venue_value == 'Tous les types' :
            df_update= df_wheel
            
        else : 
            df_update = df_wheel[df_wheel['Venue_type'] == dropdown_venue_value]
            
    elif dropdown_data_value == 'Algo_IS' :
        df_update = df_is
        
        if dropdown_venue_value == 'Tous les types' :
            df_update= df_is
        else : 
            df_update = df_is[df_is['Venue_type'] == dropdown_venue_value]

    if dropdown_vue_value == 'Vue gam':
        if dropdown_brokers_value != 'Tous les brokers' :
             df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) ]
             
        else :
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) ]
            
    elif dropdown_vue_value == 'Vue broker' :
        df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date)]
        
    elif dropdown_vue_value == 'Vue Trader': 
        if dropdown_brokers_value == 'Tous les traders' : 
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date)]
            
        else : 
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) & (
                           df_update['Trader_Name'] == dropdown_brokers_value)]
    
   
            
    
    df_update = df_update[(df_update['Side'] == 'Buy') & 
                             (df_update['AskTmin'] <= df_update['AskTmax'])]
    
    Liste_brokers_banalisée = liste_banalise(Liste_brokers, dropdown_brokers_value)
    if dropdown_brokers_value == 'Tous les traders' :
        avg = trader_brok(df_update, dropdown_brokers_value, Liste_brokers, "Avg" )
        last = trader_brok(df_update, dropdown_brokers_value, Liste_brokers, "Last" )
    else : 
        avg = moyenne_brok(df_update, Liste_brokers, "Avg")
        last = moyenne_brok(df_update, Liste_brokers, "Last")
        
        
    if dropdown_vue_value == 'Vue gam':
                    
        ecart = []
        for i in range(len(avg)):
            if last[i] >= 0 :
                ecart.append( last[i] - avg[i])
            else :
                ecart.append(-(last[i] - avg[i]))
        for i in range(len(avg)) :
            avg[i] = round(avg[i], 2)
            last[i] = round(last[i], 2)
            ecart[i] = round(ecart[i], 2)

        compte =[]
        freq = df_update['Broker_Name'].value_counts()
        for i in Liste_brokers :
            if df_update['Broker_Name'].str.contains(i).any() :
                compte.append(freq[i])
            else :
                compte.append(0)
        df_new = pd.DataFrame ({'Liste_brokers' : Liste_brokers,
                                'Liste_brokers_banalisée' : Liste_brokers_banalisée,
                                'avg' : avg,
                                'last' : last,
                                'ecart' : ecart,
                                'compte' : compte })
        df_new = df_new[df_new['compte'] !=0]
        df_new.sort_values(by = 'ecart', ascending = False, inplace = True)
        Liste_brokers = df_new['Liste_brokers']
        df_new.reset_index(inplace = True)
        nb_brokers = len(Liste_brokers)
        classement = np.where(Liste_brokers == dropdown_brokers_value)[0]
        
        if dropdown_brokers_value == 'Tous les brokers' :
            
            index = [f'{df_new["Liste_brokers"][i]}' + " " + f'{[df_new["compte"][i]]}' for i in range(len(df_new['Liste_brokers'].tolist()))]
            
        else :
            df0 = pd.DataFrame({'Liste_brokers' : [0],
                                'Liste_brokers_banalisée' : [0],
                                'avg' : round(df_new['avg'].mean(),2),
                                'last' : round(df_new['last'].mean(),2),
                                'ecart' : round(df_new['ecart'].mean(),2),
                                'compte' : df_new['compte'].sum() })
            
            df1 = df_new.head(1)
            df2 = df_new[df_new['Liste_brokers'] == dropdown_brokers_value]
            df3 = df_new.tail(1)
            df_new = pd.concat([df0, df1, df2, df3])
            df_new.reset_index(inplace = True)
            index = [" Moyenne Gam ", " Premier : "f'{df_new["Liste_brokers"][1]} ' ,
                     "  position : " f'{classement[0] +1}' +' sur '+f'{ nb_brokers }', "Dernier : "f'{df_new["Liste_brokers"][3]}']
                      
        
    elif dropdown_vue_value == 'Vue broker' :
        
                                                                     
        ecart = []
        for i in range(len(avg)):
            if last[i] >= 0 :
                ecart.append( last[i] - avg[i])
            else :
                ecart.append(-(last[i] - avg[i]))
        for i in range(len(avg)) :
            avg[i] = round(avg[i],2)
            last[i] = round(last[i],2)
            ecart[i] = round(ecart[i],2)

        compte =[]
        freq = df_update['Broker_Name'].value_counts()
        for i in Liste_brokers :
            if df_update['Broker_Name'].str.contains(i).any() :
                compte.append(freq[i])
            else :
                compte.append(0)
        df_new = pd.DataFrame ({'Liste_brokers' : Liste_brokers,
                                'Liste_brokers_banalisée' : Liste_brokers_banalisée,
                                'avg' : avg,
                                'last' : last,
                                'ecart' : ecart,
                                'compte' : compte })
        df_new = df_new[df_new['compte'] != 0]
        df_new.sort_values(by = 'ecart', ascending = False, inplace = True)
        Liste_brokers = df_new['Liste_brokers']
        df_new.reset_index(inplace = True)
        nb_brokers = len(Liste_brokers)
        classement = np.where(Liste_brokers == dropdown_brokers_value)[0]
        df0 = pd.DataFrame({'Liste_brokers' : [0],
                                'Liste_brokers_banalisée' : [0],
                                'avg' : round(df_new['avg'].mean(),2),
                                'last' : round(df_new['last'].mean(),2),
                                'ecart' : round(df_new['ecart'].mean(),2),
                                'compte' : df_new['compte'].sum() })
        df0 = df0[df0['compte'] != 0]
        df1 = df_new.head(1)
        df2 = df_new[df_new['Liste_brokers_banalisée'] == dropdown_brokers_value]
        df3 = df_new.tail(1)
        df_new = pd.concat([df0, df1, df2, df3])
        df_new.reset_index(inplace = True)
        index = [" Moyenne Gam ", " Premier " ,
                 "  position : " f'{classement[0] +1}' +' sur '+f'{ nb_brokers }', "Dernier "]
        
        
    else : 
        if dropdown_brokers_value == 'Tous les traders' : 
            avg = np.array([pd.concat([df_update[(df_update['Trader_Name'] == i) &
                                                 (df_update['Side'] == 'Buy')]['Avg/Entree'], 
                                       df_update[(df_update['Trader_Name'] == i) &
                                                 (df_update['Side'] == 'Sell')]['Avg/Entree']*(-1)]).mean() 
                                                    for i in (Liste_traders)])*100
                                                                          
            last = np.array([pd.concat([df_update[(df_update['Trader_Name'] == i) &
                                                  (df_update['Side'] == 'Buy')]['Last/Entree'], 
                                        df_update[(df_update['Trader_Name'] == i) &
                                                  (df_update['Side'] == 'Sell')]['Last/Entree']*(-1)]).mean() 
                                                     for i in (Liste_traders)])*100
                                                                         
            ecart = []
            for i in range(len(avg)):
                if last[i] >= 0 :
                    ecart.append( last[i] - avg[i])
                else :
                    ecart.append(-(last[i] - avg[i]))
            for i in range(len(avg)) :
                avg[i] = round(avg[i], 2)
                last[i] = round(last[i], 2)
                ecart[i] = round(ecart[i], 2)
    
            compte =[]
            freq = df_update['Trader_Name'].value_counts()
            for i in Liste_traders :
                if df_update['Trader_Name'].str.contains(i).any() :
                    compte.append(freq[i])
                else :
                    compte.append(0)
            df_new = pd.DataFrame ({'Liste_traders' : Liste_traders,
                                    'avg' : avg,
                                    'last' : last,
                                    'ecart' : ecart,
                                    'compte' : compte })
            df_new = df_new[df_new['compte'] != 0]
            df_new.sort_values(by = 'ecart', ascending = False, inplace = True)
            df_new.reset_index(inplace = True)
            index = [f'{df_new["Liste_traders"][i]}' + " " + f'{[df_new["compte"][i]]}' 
                     for i in range(len(df_new['Liste_traders'].tolist()))]
            
        else : 
            avg = trader_brok(df_update, dropdown_brokers_value, Liste_brokers, "Avg" )
                                                                        
            last = trader_brok(df_update, dropdown_brokers_value, Liste_brokers, "Last" )
            ecart = []
            for i in range(len(avg)):
                if last[i] >= 0 :
                    ecart.append( last[i] - avg[i])
                else :
                    ecart.append(-(last[i] - avg[i]))
                    
            
            for i in range(len(avg)) :
                avg[i] = round(avg[i], 2)
                last[i] = round(last[i], 2)
                ecart[i] = round(ecart[i], 2)
    
            compte =[]
            freq = df_update['Broker_Name'].value_counts()
            for i in Liste_brokers :
                if df_update['Broker_Name'].str.contains(i).any() :
                    compte.append(freq[i])
                else :
                    compte.append(0)
            df_new = pd.DataFrame ({'Liste_brokers' : Liste_brokers, 
                                    'Liste_brokers_banalisée' : Liste_brokers_banalisée,
                                    'avg' : avg,
                                    'last' : last,
                                    'ecart' : ecart,
                                    'compte' : compte })
            df_new = df_new[df_new['compte'] != 0]
            df_new.sort_values(by = 'ecart', ascending = False, inplace = True)
            Liste_brokers = df_new['Liste_brokers']
            df_new.reset_index(inplace = True)
            index = [f'{df_new["Liste_brokers"][i]}' + " " + f'{[df_new["compte"][i]]}' for i in range(len(df_new['Liste_brokers'].tolist()))]
       
          
    figure = {
                    'data': [
                        {'x' : index, 'y' : df_new['avg'].tolist(),
                         'type' : 'bar', 'name': 'Avg', 'weight' : '30px',
                         'text' : df_new['avg'].tolist(), 'textposition' : 'outside', 'textfont_size' : 16,
                         'marker' :
                             {'size' : 12,
                              'line' : {'width' : 2,
                                        'color' : 'DarkSlateGrey'}}
                         
                         },
                        {'x' : index, 'y' : df_new['last'].tolist(),
                         'type': 'bar', 'name': u'last', 'text' : df_new['last'].tolist(),
                         'textposition' : 'outside', 'textfont_size' : 16,
                         'marker' :
                             {'size' : 12,
                              'line' : {'width' : 2,
                                        'color' : 'DarkSlateGrey'}}
                         },
                        {'x' : index, 'y' : df_new['ecart'].tolist(),
                         'type': 'bar', 'name': u'ecart', 'text' : df_new['ecart'].tolist(), 'textposition' : 'outside',
                        'textfont_size' : 16, 'marker' : { 'color' : 'grey',
                                                          'size' : 12,
                                                          'line' : 
                                                              {'width' : 2,
                                                               'color' : 'DarkSlateGrey'}}
                         },   
                    ],
                    'layout' : {
                        'title' :  " Achats momentums  du  " f'{start_date}' " au " f'{end_date}' " :" ,
                        'plot_bgcolor' : 	'#e2dfdf',
                        'paper_bgcolor' : '#e2dfdf',
                        'font' : dict(color = 'black',
                                      size = 12,
                                      family="Times New Roman",),
                        'automargin' : True,
                        'legend' :dict(
        
                                traceorder="reversed",
                                title = " Broker : ",
                                title_font_family="Times New Roman",
                                font=dict(
                                    family="Times New Roman",
                                    size=13,
                                    color="black"
                                ),
                                bgcolor="LightSteelBlue",
                                bordercolor="Black",
                                borderwidth=2
                        ) 
                    }
                }
          
    return figure
   
  # Callback for the third graph
@app.callback(
    Output('graph_7', 'figure'),
    Input('submit-button-state', 'n_clicks'),
    State('dropdown_data', 'value'),
    State('dropdown_venue', 'value'),
    State('calendar', 'start_date'),
    State('calendar', 'end_date'),
    State('dropdown_brokers', 'value'),
    State('dropdown_vue', 'value')
    
    )

def update_graph_7(n_clicks, dropdown_data_value, dropdown_venue_value, start_date, end_date, dropdown_brokers_value, dropdown_vue_value):
    
    
    Liste_brokers = update_liste_brokers(dropdown_data_value)
    Liste_traders = update_liste_traders(dropdown_data_value) 
    df_update = pd.DataFrame(columns = ['Broker_ID', 'Broker_Name', 'Side', 'traded_Shares', 'Transaction_Time',
                  'Ask_Bench_Px', 'Bid_Bench_Px', 'Average', 'market_cap', 'volatility', 'Trader_Name', '%complete', '%DV', 'Venue_type', 'Nb_Shares', 'categorie' ])
    if dropdown_data_value == 'Wheel' :
        df_update= df_wheel
        
        if dropdown_venue_value == 'Tous les types' :
            df_update= df_wheel
            
        else : 
            df_update = df_wheel[df_wheel['Venue_type'] == dropdown_venue_value]
            
    elif dropdown_data_value == 'Algo_IS' :
        df_update = df_is
        
        if dropdown_venue_value == 'Tous les types' :
            df_update= df_is
        else : 
            df_update = df_is[df_is['Venue_type'] == dropdown_venue_value]

    if dropdown_vue_value == 'Vue gam':
        if dropdown_brokers_value != 'Tous les brokers' :
             df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) ]
             
        else :
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) ]
            
    elif dropdown_vue_value == 'Vue broker' :
        df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date)]
        
    elif dropdown_vue_value == 'Vue Trader': 
        if dropdown_brokers_value == 'Tous les traders' : 
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date)]
            
        else : 
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) & (
                           df_update['Trader_Name'] == dropdown_brokers_value)]
    
    Liste_brokers_banalisée = liste_banalise(Liste_brokers, dropdown_brokers_value)
    df_update = df_update[(df_update['Side'] == 'Buy') & 
                             (df_update['AskTmin'] > df_update['AskTmax'])]
    
    
   
    if dropdown_brokers_value == 'Tous les traders' :
        avg = trader_brok(df_update, dropdown_brokers_value, Liste_brokers, "Avg" )
        last = trader_brok(df_update, dropdown_brokers_value, Liste_brokers, "Last" )
    else : 
        avg = moyenne_brok(df_update, Liste_brokers, "Avg")
        last = moyenne_brok(df_update, Liste_brokers, "Last")
        
    if dropdown_vue_value == 'Vue gam':
                    
        ecart = []
        for i in range(len(avg)):
            if last[i] >= 0 :
                ecart.append( last[i] - avg[i])
            else :
                ecart.append(-(last[i] - avg[i]))
        for i in range(len(avg)) :
            avg[i] = round(avg[i], 2)
            last[i] = round(last[i], 2)
            ecart[i] = round(ecart[i], 2)

        compte =[]
        freq = df_update['Broker_Name'].value_counts()
        for i in Liste_brokers :
            if df_update['Broker_Name'].str.contains(i).any() :
                compte.append(freq[i])
            else :
                compte.append(0)
        df_new = pd.DataFrame ({'Liste_brokers' : Liste_brokers,
                                'Liste_brokers_banalisée' : Liste_brokers_banalisée,
                                'avg' : avg,
                                'last' : last,
                                'ecart' : ecart,
                                'compte' : compte })
        df_new = df_new[df_new['compte'] !=0]
        df_new.sort_values(by = 'ecart', ascending = False, inplace = True)
        Liste_brokers = df_new['Liste_brokers']
        df_new.reset_index(inplace = True)
        nb_brokers = len(Liste_brokers)
        classement = np.where(Liste_brokers == dropdown_brokers_value)[0]
        
        if dropdown_brokers_value == 'Tous les brokers' :
            
            index = [f'{df_new["Liste_brokers"][i]}' + " " + f'{[df_new["compte"][i]]}' for i in range(len(df_new['Liste_brokers'].tolist()))]
            
        else :
            df0 = pd.DataFrame({'Liste_brokers' : [0],
                                'Liste_brokers_banalisée' : [0],
                                'avg' : round(df_new['avg'].mean(),2),
                                'last' : round(df_new['last'].mean(),2),
                                'ecart' : round(df_new['ecart'].mean(),2),
                                'compte' : df_new['compte'].sum() })
            
            df1 = df_new.head(1)
            df2 = df_new[df_new['Liste_brokers'] == dropdown_brokers_value]
            df3 = df_new.tail(1)
            df_new = pd.concat([df0, df1, df2, df3])
            df_new.reset_index(inplace = True)
            index = [" Moyenne Gam ", " Premier : "f'{df_new["Liste_brokers"][1]} ' ,
                     "  position : " f'{classement[0] +1}' +' sur '+f'{ nb_brokers }', "Dernier : "f'{df_new["Liste_brokers"][3]}']
                      
        
    elif dropdown_vue_value == 'Vue broker' :
        
                                                                     
        ecart = []
        for i in range(len(avg)):
            if last[i] >= 0 :
                ecart.append( last[i] - avg[i])
            else :
                ecart.append(-(last[i] - avg[i]))
        for i in range(len(avg)) :
            avg[i] = round(avg[i],2)
            last[i] = round(last[i],2)
            ecart[i] = round(ecart[i],2)

        compte =[]
        freq = df_update['Broker_Name'].value_counts()
        for i in Liste_brokers :
            if df_update['Broker_Name'].str.contains(i).any() :
                compte.append(freq[i])
            else :
                compte.append(0)
        df_new = pd.DataFrame ({'Liste_brokers' : Liste_brokers,
                                'Liste_brokers_banalisée' : Liste_brokers_banalisée,
                                'avg' : avg,
                                'last' : last,
                                'ecart' : ecart,
                                'compte' : compte })
        df_new = df_new[df_new['compte'] != 0]
        df_new.sort_values(by = 'ecart', ascending = False, inplace = True)
        Liste_brokers = df_new['Liste_brokers']
        df_new.reset_index(inplace = True)
        nb_brokers = len(Liste_brokers)
        classement = np.where(Liste_brokers == dropdown_brokers_value)[0]
        df0 = pd.DataFrame({'Liste_brokers' : [0],
                                'Liste_brokers_banalisée' : [0],
                                'avg' : round(df_new['avg'].mean(),2),
                                'last' : round(df_new['last'].mean(),2),
                                'ecart' : round(df_new['ecart'].mean(),2),
                                'compte' : df_new['compte'].sum() })
        df0 = df0[df0['compte'] != 0]
        df1 = df_new.head(1)
        df2 = df_new[df_new['Liste_brokers_banalisée'] == dropdown_brokers_value]
        df3 = df_new.tail(1)
        df_new = pd.concat([df0, df1, df2, df3])
        df_new.reset_index(inplace = True)
        index = [" Moyenne Gam ", " Premier " ,
                 "  position : " f'{classement[0] +1}' +' sur '+f'{ nb_brokers }', "Dernier "]
        
        
    else : 
        if dropdown_brokers_value == 'Tous les traders' : 
            avg = np.array([pd.concat([df_update[(df_update['Trader_Name'] == i) &
                                                 (df_update['Side'] == 'Buy')]['Avg/Entree'], 
                                       df_update[(df_update['Trader_Name'] == i) &
                                                 (df_update['Side'] == 'Sell')]['Avg/Entree']*(-1)]).mean() 
                                                    for i in (Liste_traders)])*100
                                                                          
            last = np.array([pd.concat([df_update[(df_update['Trader_Name'] == i) &
                                                  (df_update['Side'] == 'Buy')]['Last/Entree'], 
                                        df_update[(df_update['Trader_Name'] == i) &
                                                  (df_update['Side'] == 'Sell')]['Last/Entree']*(-1)]).mean() 
                                                     for i in (Liste_traders)])*100
                                                                         
            ecart = []
            for i in range(len(avg)):
                if last[i] >= 0 :
                    ecart.append( last[i] - avg[i])
                else :
                    ecart.append(-(last[i] - avg[i]))
            for i in range(len(avg)) :
                avg[i] = round(avg[i], 2)
                last[i] = round(last[i], 2)
                ecart[i] = round(ecart[i], 2)
    
            compte =[]
            freq = df_update['Trader_Name'].value_counts()
            for i in Liste_traders :
                if df_update['Trader_Name'].str.contains(i).any() :
                    compte.append(freq[i])
                else :
                    compte.append(0)
            df_new = pd.DataFrame ({'Liste_traders' : Liste_traders,
                                    'avg' : avg,
                                    'last' : last,
                                    'ecart' : ecart,
                                    'compte' : compte })
            df_new = df_new[df_new['compte'] != 0]
            df_new.sort_values(by = 'ecart', ascending = False, inplace = True)
            df_new.reset_index(inplace = True)
            index = [f'{df_new["Liste_traders"][i]}' + " " + f'{[df_new["compte"][i]]}' 
                     for i in range(len(df_new['Liste_traders'].tolist()))]
            
        else : 
            avg = trader_brok(df_update, dropdown_brokers_value, Liste_brokers, "Avg" )
                                                                        
            last = trader_brok(df_update, dropdown_brokers_value, Liste_brokers, "Last" )
            ecart = []
            for i in range(len(avg)):
                if last[i] >= 0 :
                    ecart.append( last[i] - avg[i])
                else :
                    ecart.append(-(last[i] - avg[i]))
                    
            
            for i in range(len(avg)) :
                avg[i] = round(avg[i], 2)
                last[i] = round(last[i], 2)
                ecart[i] = round(ecart[i], 2)
    
            compte =[]
            freq = df_update['Broker_Name'].value_counts()
            for i in Liste_brokers :
                if df_update['Broker_Name'].str.contains(i).any() :
                    compte.append(freq[i])
                else :
                    compte.append(0)
            df_new = pd.DataFrame ({'Liste_brokers' : Liste_brokers, 
                                    'Liste_brokers_banalisée' : Liste_brokers_banalisée,
                                    'avg' : avg,
                                    'last' : last,
                                    'ecart' : ecart,
                                    'compte' : compte })
            df_new = df_new[df_new['compte'] != 0]
            df_new.sort_values(by = 'ecart', ascending = False, inplace = True)
            Liste_brokers = df_new['Liste_brokers']
            df_new.reset_index(inplace = True)
            index = [f'{df_new["Liste_brokers"][i]}' + " " + f'{[df_new["compte"][i]]}' for i in range(len(df_new['Liste_brokers'].tolist()))]
            
            
    
        
    figure = {
                    'data': [
                        {'x' : index, 'y' : df_new['avg'].tolist(),
                         'type' : 'bar', 'name': 'Avg', 'weight' : '30px',
                         'text' : df_new['avg'].tolist(), 'textposition' : 'outside', 'textfont_size' : 16,
                         'marker' :
                             {'size' : 12,
                              'line' : {'width' : 2,
                                        'color' : 'DarkSlateGrey'}}
                         
                         },
                        {'x' : index, 'y' : df_new['last'].tolist(),
                         'type': 'bar', 'name': u'last', 'text' : df_new['last'].tolist(),
                         'textposition' : 'outside', 'textfont_size' : 16,
                         'marker' :
                             {'size' : 12,
                              'line' : {'width' : 2,
                                        'color' : 'DarkSlateGrey'}}
                         },
                        {'x' : index, 'y' : df_new['ecart'].tolist(),
                         'type': 'bar', 'name': u'ecart', 'text' : df_new['ecart'].tolist(), 'textposition' : 'outside',
                        'textfont_size' : 16, 'marker' : { 'color' : 'grey',
                                                          'size' : 12,
                                                          'line' : 
                                                              {'width' : 2,
                                                               'color' : 'DarkSlateGrey'}}
                         },   
                    ],
                    'layout' : {
                        'title' :  " Achats contrariants  du  " f'{start_date}' " au " f'{end_date}' " :" ,
                        'plot_bgcolor' : 	'#e2dfdf',
                        'paper_bgcolor' : '#e2dfdf',
                        'font' : dict(color = 'black',
                                      size= 12,
                                      family="Times New Roman"),
                        'automargin' : True,
                        'legend' : dict(
        
                                traceorder="reversed",
                                title = " Broker : ",
                                title_font_family="Times New Roman",
                                font=dict(
                                    family="Times New Roman",
                                    size=13,
                                    color="black"
                                ),
                                bgcolor="LightSteelBlue",
                                bordercolor="Black",
                                borderwidth=2
                        )  
                    }
                }
          
    return figure
    
   
  # Callback for the fourth graph
@app.callback(
    Output('graph_8', 'figure'),
    Input('submit-button-state', 'n_clicks'),
    State('dropdown_data', 'value'),
    State('dropdown_venue', 'value'),
    State('calendar', 'start_date'),
    State('calendar', 'end_date'),
    State('dropdown_brokers', 'value'),
    State('dropdown_vue', 'value')
    )

def update_graph_8(n_clicks, dropdown_data_value, dropdown_venue_value, start_date, end_date, dropdown_brokers_value, dropdown_vue_value):
    
    
    Liste_brokers = update_liste_brokers(dropdown_data_value)
    Liste_traders = update_liste_traders(dropdown_data_value) 
    df_update = pd.DataFrame(columns = ['Broker_ID', 'Broker_Name', 'Side', 'traded_Shares', 'Transaction_Time',
                  'Ask_Bench_Px', 'Bid_Bench_Px', 'Average', 'market_cap', 'volatility', 'Trader_Name', '%complete', '%DV', 'Venue_type', 'Nb_Shares', 'categorie' ])
    if dropdown_data_value == 'Wheel' :
        df_update= df_wheel
        
        if dropdown_venue_value == 'Tous les types' :
            df_update= df_wheel
            
        else : 
            df_update = df_wheel[df_wheel['Venue_type'] == dropdown_venue_value]
            
    elif dropdown_data_value == 'Algo_IS' :
        df_update = df_is
        
        if dropdown_venue_value == 'Tous les types' :
            df_update= df_is
        else : 
            df_update = df_is[df_is['Venue_type'] == dropdown_venue_value]

    if dropdown_vue_value == 'Vue gam':
        if dropdown_brokers_value != 'Tous les brokers' :
             df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) ]
             
        else :
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) ]
            
    elif dropdown_vue_value == 'Vue broker' :
        df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date)]
        
    elif dropdown_vue_value == 'Vue Trader': 
        if dropdown_brokers_value == 'Tous les traders' : 
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date)]
            
        else : 
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) & (
                           df_update['Trader_Name'] == dropdown_brokers_value)]
    
    Liste_brokers_banalisée = liste_banalise(Liste_brokers, dropdown_brokers_value)
    df_update = df_update[(df_update['Side'] == 'Sell') & 
                             (df_update['BidTmin'] < df_update['BidTmax'])]
    
    
    
    if dropdown_brokers_value == 'Tous les traders' :
        avg = trader_brok(df_update, dropdown_brokers_value, Liste_brokers, "Avg" )
        last = trader_brok(df_update, dropdown_brokers_value, Liste_brokers, "Last" )
    else : 
        avg = moyenne_brok(df_update, Liste_brokers, "Avg")
        last = moyenne_brok(df_update, Liste_brokers, "Last")
        
        
    if dropdown_vue_value == 'Vue gam':
                    
        ecart = []
        for i in range(len(avg)):
            if last[i] >= 0 :
                ecart.append( last[i] - avg[i])
            else :
                ecart.append(-(last[i] - avg[i]))
        for i in range(len(avg)) :
            avg[i] = round(avg[i], 2)
            last[i] = round(last[i], 2)
            ecart[i] = round(ecart[i], 2)

        compte =[]
        freq = df_update['Broker_Name'].value_counts()
        for i in Liste_brokers :
            if df_update['Broker_Name'].str.contains(i).any() :
                compte.append(freq[i])
            else :
                compte.append(0)
        df_new = pd.DataFrame ({'Liste_brokers' : Liste_brokers,
                                'Liste_brokers_banalisée' : Liste_brokers_banalisée,
                                'avg' : avg,
                                'last' : last,
                                'ecart' : ecart,
                                'compte' : compte })
        df_new = df_new[df_new['compte'] !=0]
        df_new.sort_values(by = 'ecart', ascending = False, inplace = True)
        Liste_brokers = df_new['Liste_brokers']
        df_new.reset_index(inplace = True)
        nb_brokers = len(Liste_brokers)
        classement = np.where(Liste_brokers == dropdown_brokers_value)[0]
        
        if dropdown_brokers_value == 'Tous les brokers' :
            
            index = [f'{df_new["Liste_brokers"][i]}' + " " + f'{[df_new["compte"][i]]}' for i in range(len(df_new['Liste_brokers'].tolist()))]
            
        else :
            df0 = pd.DataFrame({'Liste_brokers' : [0],
                                'Liste_brokers_banalisée' : [0],
                                'avg' : round(df_new['avg'].mean(),2),
                                'last' : round(df_new['last'].mean(),2),
                                'ecart' : round(df_new['ecart'].mean(),2),
                                'compte' : df_new['compte'].sum() })
            
            df1 = df_new.head(1)
            df2 = df_new[df_new['Liste_brokers'] == dropdown_brokers_value]
            df3 = df_new.tail(1)
            df_new = pd.concat([df0, df1, df2, df3])
            df_new.reset_index(inplace = True)
            index = [" Moyenne Gam ", " Premier : "f'{df_new["Liste_brokers"][1]} ' ,
                     "  position : " f'{classement[0] +1}' +' sur '+f'{ nb_brokers }', "Dernier : "f'{df_new["Liste_brokers"][3]}']
                      
        
    elif dropdown_vue_value == 'Vue broker' :
        
                                                                     
        ecart = []
        for i in range(len(avg)):
            if last[i] >= 0 :
                ecart.append( last[i] - avg[i])
            else :
                ecart.append(-(last[i] - avg[i]))
        for i in range(len(avg)) :
            avg[i] = round(avg[i],2)
            last[i] = round(last[i],2)
            ecart[i] = round(ecart[i],2)

        compte =[]
        freq = df_update['Broker_Name'].value_counts()
        for i in Liste_brokers :
            if df_update['Broker_Name'].str.contains(i).any() :
                compte.append(freq[i])
            else :
                compte.append(0)
        df_new = pd.DataFrame ({'Liste_brokers' : Liste_brokers,
                                'Liste_brokers_banalisée' : Liste_brokers_banalisée,
                                'avg' : avg,
                                'last' : last,
                                'ecart' : ecart,
                                'compte' : compte })
        df_new = df_new[df_new['compte'] != 0]
        df_new.sort_values(by = 'ecart', ascending = False, inplace = True)
        Liste_brokers = df_new['Liste_brokers']
        df_new.reset_index(inplace = True)
        nb_brokers = len(Liste_brokers)
        classement = np.where(Liste_brokers == dropdown_brokers_value)[0]
        df0 = pd.DataFrame({'Liste_brokers' : [0],
                                'Liste_brokers_banalisée' : [0],
                                'avg' : round(df_new['avg'].mean(),2),
                                'last' : round(df_new['last'].mean(),2),
                                'ecart' : round(df_new['ecart'].mean(),2),
                                'compte' : df_new['compte'].sum() })
        df0 = df0[df0['compte'] != 0]
        df1 = df_new.head(1)
        df2 = df_new[df_new['Liste_brokers_banalisée'] == dropdown_brokers_value]
        df3 = df_new.tail(1)
        df_new = pd.concat([df0, df1, df2, df3])
        df_new.reset_index(inplace = True)
        index = [" Moyenne Gam ", " Premier " ,
                 "  position : " f'{classement[0] +1}' +' sur '+f'{ nb_brokers }', "Dernier "]
        
        
    else : 
        if dropdown_brokers_value == 'Tous les traders' : 
            avg = np.array([pd.concat([df_update[(df_update['Trader_Name'] == i) &
                                                 (df_update['Side'] == 'Buy')]['Avg/Entree'], 
                                       df_update[(df_update['Trader_Name'] == i) &
                                                 (df_update['Side'] == 'Sell')]['Avg/Entree']*(-1)]).mean() 
                                                    for i in (Liste_traders)])*100
                                                                          
            last = np.array([pd.concat([df_update[(df_update['Trader_Name'] == i) &
                                                  (df_update['Side'] == 'Buy')]['Last/Entree'], 
                                        df_update[(df_update['Trader_Name'] == i) &
                                                  (df_update['Side'] == 'Sell')]['Last/Entree']*(-1)]).mean() 
                                                     for i in (Liste_traders)])*100
                                                                         
            ecart = []
            for i in range(len(avg)):
                if last[i] >= 0 :
                    ecart.append( last[i] - avg[i])
                else :
                    ecart.append(-(last[i] - avg[i]))
            for i in range(len(avg)) :
                avg[i] = round(avg[i], 2)
                last[i] = round(last[i], 2)
                ecart[i] = round(ecart[i], 2)
    
            compte =[]
            freq = df_update['Trader_Name'].value_counts()
            for i in Liste_traders :
                if df_update['Trader_Name'].str.contains(i).any() :
                    compte.append(freq[i])
                else :
                    compte.append(0)
            df_new = pd.DataFrame ({'Liste_traders' : Liste_traders,
                                    'avg' : avg,
                                    'last' : last,
                                    'ecart' : ecart,
                                    'compte' : compte })
            df_new = df_new[df_new['compte'] != 0]
            df_new.sort_values(by = 'ecart', ascending = False, inplace = True)
            df_new.reset_index(inplace = True)
            index = [f'{df_new["Liste_traders"][i]}' + " " + f'{[df_new["compte"][i]]}' 
                     for i in range(len(df_new['Liste_traders'].tolist()))]
            
        else : 
            avg = trader_brok(df_update, dropdown_brokers_value, Liste_brokers, "Avg" )
                                                                        
            last = trader_brok(df_update, dropdown_brokers_value, Liste_brokers, "Last" )
            ecart = []
            for i in range(len(avg)):
                if last[i] >= 0 :
                    ecart.append( last[i] - avg[i])
                else :
                    ecart.append(-(last[i] - avg[i]))
                    
            
            for i in range(len(avg)) :
                avg[i] = round(avg[i], 2)
                last[i] = round(last[i], 2)
                ecart[i] = round(ecart[i], 2)
    
            compte =[]
            freq = df_update['Broker_Name'].value_counts()
            for i in Liste_brokers :
                if df_update['Broker_Name'].str.contains(i).any() :
                    compte.append(freq[i])
                else :
                    compte.append(0)
            df_new = pd.DataFrame ({'Liste_brokers' : Liste_brokers, 
                                    'Liste_brokers_banalisée' : Liste_brokers_banalisée,
                                    'avg' : avg,
                                    'last' : last,
                                    'ecart' : ecart,
                                    'compte' : compte })
            df_new = df_new[df_new['compte'] != 0]
            df_new.sort_values(by = 'ecart', ascending = False, inplace = True)
            Liste_brokers = df_new['Liste_brokers']
            df_new.reset_index(inplace = True)
            index = [f'{df_new["Liste_brokers"][i]}' + " " + f'{[df_new["compte"][i]]}' for i in range(len(df_new['Liste_brokers'].tolist()))]
           
    avg = df_new['avg'].tolist()
    last = df_new['last'].tolist()
    ecart = df_new['ecart'].tolist() 
    figure = {
                    'data': [
                        {'x' : index, 'y' : [i*(-1) for i in avg],
                         'type' : 'bar', 'name': 'Avg', 'weight' : '30px',
                         'text' : [i*(-1) for i in avg], 'textposition' : 'outside', 'textfont_size' : 16,
                         'marker' :
                             {'size' : 12,
                              'line' : {'width' : 2,
                                        'color' : 'DarkSlateGrey'}}
                         
                         },
                        {'x' : index, 'y' : [i*(-1) for i in last],
                         'type': 'bar', 'name': u'last', 'text' : [i*(-1) for i in last],
                         'textposition' : 'outside', 'textfont_size' : 16,
                         'marker' :
                             {'size' : 12,
                              'line' : {'width' : 2,
                                        'color' : 'DarkSlateGrey'}}
                         },
                        {'x' : index, 'y' : [i*(-1) for i in ecart],
                         'type': 'bar', 'name': u'ecart', 'text' : [i*(-1) for i in ecart], 'textposition' : 'outside',
                        'textfont_size' : 16, 'marker' : 
                            { 'color' : 'grey',
                             'size' : 12,
                              'line' : {'width' : 2,
                                        'color' : 'DarkSlateGrey'}}
                         },
                        
                    ],
                    'layout' : {
                        'title' :  " Ventes contrariants  du  " f'{start_date}' " au " f'{end_date}' " :" ,
                        'plot_bgcolor' : 	'#e2dfdf',
                        'paper_bgcolor' : '#e2dfdf',
                        'font' : dict(color = 'black',
                                      size= 12,
                                      family="Times New Roman"),
                        'automargin' : True,
                        'legend' : dict(
        
                                traceorder="reversed",
                                title = " Broker : ",
                                title_font_family="Times New Roman",
                                font=dict(
                                    family="Times New Roman",
                                    size=13,
                                    color="black"
                                ),
                                bgcolor="LightSteelBlue",
                                bordercolor="Black",
                                borderwidth=2
                        )  
                    }
                }
    
    return figure
    
    
 
  
# Callback for the fifth graph   
@app.callback(
    Output('graph_6', 'figure'),
    Input('submit-button-state', 'n_clicks'),
    State('dropdown_data', 'value'),
    State('dropdown_venue', 'value'),
    State('calendar', 'start_date'),
    State('calendar', 'end_date'),
    State('dropdown_brokers', 'value'),
    State('dropdown_vue', 'value')
    )

def update_graph_6(n_clicks, dropdown_data_value ,dropdown_venue_value, start_date, end_date, dropdown_brokers_value, dropdown_vue_value):
    
     
    Liste_brokers = update_liste_brokers(dropdown_data_value)
    Liste_traders = update_liste_traders(dropdown_data_value) 
    df_update = pd.DataFrame(columns = ['Broker_ID', 'Broker_Name', 'Side', 'traded_Shares', 'Transaction_Time',
                  'Ask_Bench_Px', 'Bid_Bench_Px', 'Average', 'market_cap', 'volatility', 'Trader_Name', '%complete', '%DV', 'Venue_type', 'Nb_Shares', 'categorie' ])
    if dropdown_data_value == 'Wheel' :
        df_update= df_wheel
        
        if dropdown_venue_value == 'Tous les types' :
            df_update= df_wheel
            
        else : 
            df_update = df_wheel[df_wheel['Venue_type'] == dropdown_venue_value]
            
    elif dropdown_data_value == 'Algo_IS' :
        df_update = df_is
        
        if dropdown_venue_value == 'Tous les types' :
            df_update= df_is
        else : 
            df_update = df_is[df_is['Venue_type'] == dropdown_venue_value]

    if dropdown_vue_value == 'Vue gam':
        if dropdown_brokers_value != 'Tous les brokers' :
             df_update = df_update[(df_update['Tmin'] >= start_date ) ]
             
        else :
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) ]
            
    elif dropdown_vue_value == 'Vue broker' :
        df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date)]
        
    elif dropdown_vue_value == 'Vue Trader': 
        if dropdown_brokers_value == 'Tous les traders' : 
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date)]
            
        else : 
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) & (
                           df_update['Trader_Name'] == dropdown_brokers_value)]
    
    Liste_brokers_banalisée = liste_banalise(Liste_brokers, dropdown_brokers_value)
    df_update = df_update[(df_update['Side'] == 'Sell') & 
                             (df_update['BidTmin'] >= df_update['BidTmax'])]
    
    
    if dropdown_brokers_value == 'Tous les traders' :
        avg = trader_brok(df_update, dropdown_brokers_value, Liste_brokers, "Avg" )
        last = trader_brok(df_update, dropdown_brokers_value, Liste_brokers, "Last" )
    else : 
        avg = moyenne_brok(df_update, Liste_brokers, "Avg")
        last = moyenne_brok(df_update, Liste_brokers, "Last")
        
    if dropdown_vue_value == 'Vue gam':
        
        ecart = []
        for i in range(len(avg)):
            if last[i] >= 0 :
                ecart.append( last[i] - avg[i])
            else :
                ecart.append(-(last[i] - avg[i]))
        for i in range(len(avg)) :
            avg[i] = round(avg[i],2)
            last[i] = round(last[i],2)
            ecart[i] = round(ecart[i],2)
        avg = [i*(-1) for i in avg]
        last = [i*(-1) for i in last]
        ecart = [i*(-1) for i in ecart]

        compte =[]
        freq = df_update['Broker_Name'].value_counts()
        for i in Liste_brokers :
            if df_update['Broker_Name'].str.contains(i).any() :
                compte.append(freq[i])
            else :
                compte.append(0)
        df_new = pd.DataFrame ({'Liste_brokers' : Liste_brokers,
                                'Liste_brokers_banalisée' : Liste_brokers_banalisée,
                                'avg' : avg,
                                'last' : last,
                                'ecart' : ecart,
                                'compte' : compte })
        df_new = df_new[df_new['compte'] !=0]
        df_new.sort_values(by = 'ecart', ascending = True, inplace = True)
        Liste_brokers = df_new['Liste_brokers']
        df_new.reset_index(inplace = True)
        nb_brokers = len(Liste_brokers)
        classement = np.where(Liste_brokers == dropdown_brokers_value)[0]
        
        if dropdown_brokers_value == 'Tous les brokers' :
            
            index = [f'{df_new["Liste_brokers"][i]}' + " " + f'{[df_new["compte"][i]]}' for i in range(len(df_new['Liste_brokers'].tolist()))]
            
        else :
            df0 = pd.DataFrame({'Liste_brokers' : [0],
                                'Liste_brokers_banalisée' : [0],
                                'avg' : round(df_new['avg'].mean(),2),
                                'last' : round(df_new['last'].mean(),2),
                                'ecart' : round(df_new['ecart'].mean(),2),
                                'compte' : df_new['compte'].sum() })
            df0 = df0[df0['compte'] != 0]
            df1 = df_new.head(1)
            df2 = df_new[df_new['Liste_brokers']==dropdown_brokers_value]
            df3 = df_new.tail(1)
            df_new = pd.concat([df0, df1, df2, df3])
            df_new.reset_index(inplace = True)
            index = ["Moyenne Gam ", " Premier : "f'{df_new["Liste_brokers"][1]} ' ,
                     "Position : " f'{classement[0] +1}' +' sur '+f'{ nb_brokers }',
                     "Dernier : "f'{df_new["Liste_brokers"][3]}']
         
    elif dropdown_vue_value == 'Vue broker' :
                                                                 
        ecart = []
        for i in range(len(avg)):
            if last[i] >= 0 :
                ecart.append( last[i] - avg[i])
            else :
                ecart.append(-(last[i] - avg[i]))
        for i in range(len(avg)) :
            avg[i] = round(avg[i],2)
            last[i] = round(last[i],2)
            ecart[i] = round(ecart[i],2)
        avg = [i*(-1) for i in avg]
        last = [i*(-1) for i in last]
        ecart = [i*(-1) for i in ecart]

        compte =[]
        freq = df_update['Broker_Name'].value_counts()
        for i in Liste_brokers :
            if df_update['Broker_Name'].str.contains(i).any() :
                compte.append(freq[i])
            else :
                compte.append(0)
        df_new = pd.DataFrame ({'Liste_brokers' : Liste_brokers,
                                'Liste_brokers_banalisée' : Liste_brokers_banalisée,
                                'avg' : avg,
                                'last' : last,
                                'ecart' : ecart,
                                'compte' : compte })
        df_new = df_new[df_new['compte'] !=0]
        df_new.sort_values(by = 'ecart', ascending = True, inplace = True)
        Liste_brokers = df_new['Liste_brokers']
        df_new.reset_index(inplace = True)
        nb_brokers = len(Liste_brokers)
        classement = np.where(Liste_brokers == dropdown_brokers_value)[0]
        df0 = pd.DataFrame({'Liste_brokers' : [0],
                                'Liste_brokers_banalisée' : [0],
                                'avg' : round(df_new['avg'].mean(),2),
                                'last' : round(df_new['last'].mean(),2),
                                'ecart' : round(df_new['ecart'].mean(),2),
                                'compte' : df_new['compte'].sum() })
        df0 = df0[df0['compte'] != 0]
        df1 = df_new.head(1)
        df2 = df_new[df_new['Liste_brokers_banalisée']==dropdown_brokers_value]
        df3 = df_new.tail(1)
        df_new = pd.concat([df0, df1, df2, df3])
        df_new.reset_index(inplace = True)
        index = [" Moyenne Gam ", " Premier " ,
                 "position : " f'{classement[0] +1}' +' sur '+f'{ nb_brokers }', "Dernier "]
        
        
    else : 
        if dropdown_brokers_value == 'Tous les traders' : 
            avg = np.array([pd.concat([df_update[(df_update['Trader_Name'] == i) &
                                                 (df_update['Side'] == 'Buy')]['Avg/Entree'], 
                                       df_update[(df_update['Trader_Name'] == i) &
                                                 (df_update['Side'] == 'Sell')]['Avg/Entree']*(-1)]).mean() 
                                                    for i in (Liste_traders)])*100
                                                                          
            last = np.array([pd.concat([df_update[(df_update['Trader_Name'] == i) &
                                                  (df_update['Side'] == 'Buy')]['Last/Entree'], 
                                        df_update[(df_update['Trader_Name'] == i) &
                                                  (df_update['Side'] == 'Sell')]['Last/Entree']*(-1)]).mean() 
                                                     for i in (Liste_traders)])*100
            
                                                                           
            ecart = []
            for i in range(len(avg)):
                if last[i] >= 0 :
                    ecart.append( last[i] - avg[i])
                else :
                    ecart.append(-(last[i] - avg[i]))
            for i in range(len(avg)) :
                avg[i] = round(avg[i], 2)
                last[i] = round(last[i], 2)
                ecart[i] = round(ecart[i], 2)
            avg = [i*(-1) for i in avg]
            last = [i*(-1) for i in last]
            ecart = [i*(-1) for i in ecart]
            compte =[]
            freq = df_update['Trader_Name'].value_counts()
            for i in Liste_traders :
                if df_update['Trader_Name'].str.contains(i).any() :
                    compte.append(freq[i])
                else :
                    compte.append(0)
            df_new = pd.DataFrame ({'Liste_traders' : Liste_traders,
                                    'avg' : avg,
                                    'last' : last,
                                    'ecart' : ecart,
                                    'compte' : compte })
            df_new = df_new[df_new['compte'] !=0]
            df_new.sort_values(by = 'ecart', ascending = True, inplace = True)
            df_new.reset_index(inplace = True)
            index = [f'{df_new["Liste_traders"][i]}' + " " + f'{[df_new["compte"][i]]}' 
                     for i in range(len(df_new['Liste_traders'].tolist()))]
            
        else : 
            avg = trader_brok(df_update, dropdown_brokers_value, Liste_brokers, "Avg" )
                                                                        
            last = trader_brok(df_update, dropdown_brokers_value, Liste_brokers, "Last" )
            ecart = []
            for i in range(len(avg)):
                if last[i] >= 0 :
                    ecart.append( last[i] - avg[i])
                else :
                    ecart.append(-(last[i] - avg[i]))
                    
            for i in range(len(avg)) :
                avg[i] = round(avg[i], 2)
                last[i] = round(last[i], 2)
                ecart[i] = round(ecart[i], 2)
            avg = [i*(-1) for i in avg]
            last = [i*(-1) for i in last]
            ecart = [i*(-1) for i in ecart]
            compte =[]
            freq = df_update['Broker_Name'].value_counts()
            for i in Liste_brokers :
                if df_update['Broker_Name'].str.contains(i).any() :
                    compte.append(freq[i])
                else :
                    compte.append(0)
            df_new = pd.DataFrame ({'Liste_brokers' : Liste_brokers, 
                                    'Liste_brokers_banalisée' : Liste_brokers_banalisée,
                                    'avg' : avg,
                                    'last' : last,
                                    'ecart' : ecart,
                                    'compte' : compte })
            df_new = df_new[df_new['compte'] !=0]
            df_new.sort_values(by = 'ecart', ascending = True, inplace = True)
            Liste_brokers = df_new['Liste_brokers']
            df_new.reset_index(inplace = True)
            index = [f'{df_new["Liste_brokers"][i]}' + " " + f'{[df_new["compte"][i]]}' for i in range(len(df_new['Liste_brokers'].tolist()))]
    avg = df_new['avg'].tolist()
    last = df_new['last'].tolist()
    ecart = df_new['ecart'].tolist() 
    figure = {
                    'data': [
                        {'x' : index, 'y' : [i*(-1) for i in avg],
                         'type' : 'bar', 'name': 'Avg', 'weight' : '30px',
                         'text' : [i*(-1) for i in avg], 'textposition' : 'outside', 'textfont_size' : 16,
                         'marker' :
                             {'size' : 12,
                              'line' : {'width' : 2,
                                        'color' : 'DarkSlateGrey'}}
                         
                         },
                        {'x' : index, 'y' : [i*(-1) for i in last],
                         'type': 'bar', 'name': u'last', 'text' : [i*(-1) for i in last],
                         'textposition' : 'outside', 'textfont_size' : 16,
                         'marker' :
                             {'size' : 12,
                              'line' : {'width' : 2,
                                        'color' : 'DarkSlateGrey'}}
                         },
                        {'x' : index, 'y' : [i*(-1) for i in ecart],
                         'type': 'bar', 'name': u'ecart', 'text' : [i*(-1) for i in ecart], 'textposition' : 'outside',
                        'textfont_size' : 16, 'marker' : 
                            { 'color' : 'grey',
                             'size' : 12,
                              'line' : {'width' : 2,
                                        'color' : 'DarkSlateGrey'}}
                         },
                        
                    ],
                    'layout' : {
                        'title' :  " Ventes momentums  du  " f'{start_date}' " au " f'{end_date}' " :" ,
                        'plot_bgcolor' : 	'#e2dfdf',
                        'paper_bgcolor' : '#e2dfdf',
                        'font' : dict(color = 'black',
                                      size= 12,
                                      family = 'Times New Roman'),
                        'automargin' : True,
                        'legend' : dict(
        
                                traceorder="reversed",
                                title = " Broker : ",
                                title_font_family="Times New Roman",
                                font=dict(
                                    family="Times New Roman",
                                    size=13,
                                    color="black"
                                ),
                                bgcolor="LightSteelBlue",
                                bordercolor="Black",
                                borderwidth=2
                        )
                    }
                }
    return figure
          


@app.callback(
    Output('graph_9', 'figure'),
    Input('submit-button-state', 'n_clicks'),
    State('dropdown_data', 'value'),
    State('dropdown_venue', 'value'),
    State('calendar', 'start_date'),
    State('calendar', 'end_date'),
    State('dropdown_brokers', 'value'),
    State('dropdown_vue', 'value')
    )

def update_graph_9(n_clicks, dropdown_data_value, dropdown_venue_value, start_date, end_date, dropdown_brokers_value, dropdown_vue_value):
    
    df_update = pd.DataFrame(columns = ['Broker_ID', 'Broker_Name', 'Side', 'traded_Shares', 'Transaction_Time',
                  'Ask_Bench_Px', 'Bid_Bench_Px', 'Average', 'market_cap', 'volatility', 'Trader_Name', '%complete', '%DV', 'Venue_type', 'Nb_Shares', 'categorie' ])
    if dropdown_data_value == 'Wheel' :
        df_update= df_wheel
        
        if dropdown_venue_value == 'Tous les types' :
            df_update= df_wheel
            
        else : 
            df_update = df_wheel[df_wheel['Venue_type'] == dropdown_venue_value]
            
    elif dropdown_data_value == 'Algo_IS' :
        df_update = df_is
        
        if dropdown_venue_value == 'Tous les types' :
            df_update= df_is
        else : 
            df_update = df_is[df_is['Venue_type'] == dropdown_venue_value]

    if dropdown_vue_value == 'Vue gam':
        if dropdown_brokers_value != 'Tous les brokers' :
             df_update = df_update[(df_update['Tmin'] >= start_date )& (df_update['Broker_Name'] == dropdown_brokers_value) ]
             
        else :
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) ]
            
    elif dropdown_vue_value == 'Vue broker' :
        df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date)& (df_update['Broker_Name'] == dropdown_brokers_value)]
        
    elif dropdown_vue_value == 'Vue Trader': 
        if dropdown_brokers_value == 'Tous les traders' : 
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date)]
            
        else : 
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) & (
                           df_update['Trader_Name'] == dropdown_brokers_value)]
    market_cap = df_update['market_cap'].unique()
    
    if dropdown_vue_value =='Vue gam':
        if dropdown_brokers_value == 'Tous les brokers' :
            avg = np.array([pd.concat([df_update[(df_update['market_cap'] == i) &
                                                 (df_update['Side'] == 'Buy')]['Avg/Entree'],
                                       df_update[(df_update['market_cap'] == i)&
                                                 (df_update['Side'] == 'Sell')]['Avg/Entree']*(-1)]).mean() 
                                                    for i in (market_cap)])*100
            
            last = np.array([pd.concat([df_update[(df_update['market_cap'] == i) &
                                                  (df_update['Side']=='Buy')]['Last/Entree'],
                                        df_update[(df_update['market_cap'] == i)&
                                                  (df_update['Side']=='Sell')]['Last/Entree']*(-1)]).mean()
                                                     for i in (market_cap)])*100
            
            ecart = []
            for i in range(len(avg)):
                if last[i] >= 0 :
                    ecart.append( last[i] - avg[i])
                else :
                    ecart.append(-(last[i] - avg[i]))
            for i in range(len(avg)) :
                avg[i] = round(avg[i], 2)
                last[i] = round(last[i], 2)
                ecart[i] = round(ecart[i], 2)
    
    

            compte =[]
            freq = df_update['market_cap'].value_counts()
            for i in market_cap :
                if df_update['market_cap'].str.contains(i, regex = False).any() :
                    compte.append(freq[i])
                else :
                    compte.append(0)
            df_new = pd.DataFrame ({'market_cap' : market_cap,
                                    'avg' : avg,
                                    'last' : last,
                                    'ecart' : ecart,
                                    'compte' : compte })
            df_new = df_new[df_new['compte'] != 0]
            df_new.sort_values(by = 'ecart', ascending = False, inplace = True)
            df_new.reset_index(inplace = True)
            index = [f'{df_new["market_cap"][i]}' + " " + f'{[df_new["compte"][i]]}' for i in range(len(df_new['market_cap'].tolist()))]
            
        else :
            avg = np.array([pd.concat([df_update[(df_update['Broker_Name'] == dropdown_brokers_value) & 
                                                 (df_update['market_cap'] == i) &
                                                 (df_update['Side']=='Buy')]['Avg/Entree'],
                                       df_update[(df_update['Broker_Name'] == dropdown_brokers_value) & 
                                                 (df_update['market_cap'] == i)&
                                                 (df_update['Side']=='Sell')]['Avg/Entree']*(-1)]).mean() 
                                                    for i in (market_cap)])*100
            
            last = np.array([pd.concat([df_update[(df_update['Broker_Name'] == dropdown_brokers_value) & 
                                                  (df_update['market_cap'] == i)&
                                                  (df_update['Side']=='Buy')]['Last/Entree'],
                                        df_update[(df_update['Broker_Name'] == dropdown_brokers_value) & 
                                                  (df_update['market_cap'] == i)&
                                                  (df_update['Side']=='Sell')]['Last/Entree']*(-1)]).mean() 
                                                     for i in (market_cap) ])*100
            
            ecart = []
            for i in range(len(avg)):
                if last[i] >= 0 :
                    ecart.append( last[i] - avg[i])
                else :
                    ecart.append(-(last[i] - avg[i]))
            for i in range(len(avg)) :
                avg[i] = round(avg[i], 2)
                last[i] = round(last[i], 2)
                ecart[i] = round(ecart[i], 2)
    
            compte = []
            freq = df_update['market_cap'].value_counts()
            for i in market_cap :
                if df_update['market_cap'].str.contains(i, regex = False).any() :
                    compte.append(freq[i])
                else :
                    compte.append(0)
            df_new = pd.DataFrame ({ 'market_cap' : market_cap,
                                    'avg' : avg,
                                    'last' : last,
                                    'ecart' : ecart,
                                    'compte' : compte })
            df_new = df_new[df_new['compte'] != 0]
            df_new.sort_values(by = 'ecart', ascending = False, inplace = True)
            df_new.reset_index(inplace = True)
            index = [f'{df_new["market_cap"][i]}' + " " + f'{[df_new["compte"][i]]}' for i in range(len(df_new['market_cap'].tolist()))]
           
            
    elif dropdown_vue_value == 'Vue broker' :
        avg = np.array([pd.concat([df_update[(df_update['market_cap'] == i) & 
                                             (df_update['Broker_Name'] ==dropdown_brokers_value) &
                                             (df_update['Side']=='Buy')]['Avg/Entree'],
                                   df_update[(df_update['market_cap'] == i) &
                                             (df_update['Broker_Name'] ==dropdown_brokers_value) &
                                             (df_update['Side']=='Sell')]['Avg/Entree']*(-1)]).mean() 
                                                for i in (market_cap)])*100
        
        last = np.array([pd.concat([df_update[(df_update['market_cap'] == i) &
                                              (df_update['Broker_Name'] ==dropdown_brokers_value) &
                                              (df_update['Side']=='Buy')]['Last/Entree'],
                                    df_update[(df_update['market_cap'] == i) &
                                              (df_update['Broker_Name'] ==dropdown_brokers_value) &
                                              (df_update['Side']=='Sell')]['Last/Entree']*(-1)]).mean() 
                                                 for i in (market_cap)])*100
        ecart = []
        for i in range(len(avg)):
            if last[i] >= 0 :
                ecart.append( last[i] - avg[i])
            else :
                ecart.append(-(last[i] - avg[i]))
        for i in range(len(avg)) :
            avg[i] = round(avg[i], 2)
            last[i] = round(last[i], 2)
            ecart[i] = round(ecart[i], 2)
        compte = []
        freq = df_update['market_cap'].value_counts()
        for i in market_cap :
            if df_update['market_cap'].str.contains(i, regex = False ).any() :
                compte.append(freq[i])
            else :
                compte.append(0)
        df_new = pd.DataFrame ({ 'market_cap' : market_cap,
                                'avg' : avg,
                                'last' : last,
                                'ecart' : ecart,
                                'compte' : compte })
        df_new = df_new[df_new['compte'] != 0]
        df_new.sort_values(by = 'ecart', ascending= False, inplace =True)
        df_new.reset_index(inplace=True)
        index = [f'{df_new["market_cap"][i]}' + " " + f'{[df_new["compte"][i]]}' for i in range(len(df_new['market_cap'].tolist()))]
        
    else : 
        if dropdown_brokers_value == 'Tous les traders' : 
            
            avg = np.array([pd.concat([df_update[(df_update['market_cap'] == i) &
                                                 (df_update['Side']=='Buy')]['Avg/Entree'],
                                       df_update[(df_update['market_cap'] == i) &
                                                 (df_update['Side']=='Sell')]['Avg/Entree']*(-1)]).mean() 
                                                    for i in (market_cap)])*100
            
            last = np.array([pd.concat([df_update[(df_update['market_cap'] == i) &
                                                  (df_update['Side']=='Buy')]['Last/Entree'],
                                        df_update[(df_update['market_cap'] == i) &
                                                  (df_update['Side']=='Sell')]['Last/Entree']*(-1)]).mean() 
                                                     for i in (market_cap)])*100
            
            ecart = []
            for i in range(len(avg)):
                if last[i] >= 0 :
                    ecart.append( last[i] - avg[i])
                else :
                    ecart.append(-(last[i] - avg[i]))
            for i in range(len(avg)) :
                avg[i] = round(avg[i],2)
                last[i] = round(last[i],2)
                ecart[i] = round(ecart[i],2)
    
            compte = []
            freq = df_update['market_cap'].value_counts()
            for i in market_cap :
                if df_update['market_cap'].str.contains(i, regex = False).any() :
                    compte.append(freq[i])
                else :
                    compte.append(0)
            df_new = pd.DataFrame ({'market_cap' : market_cap,
                                    'avg' : avg,
                                    'last' : last,
                                    'ecart' : ecart,
                                    'compte' : compte })
            df_new = df_new[df_new['compte'] != 0]
            df_new.sort_values(by = 'ecart', ascending= False, inplace =True)
            df_new.reset_index(inplace=True)
            index = [f'{df_new["market_cap"][i]}' + " " + f'{[df_new["compte"][i]]}' for i in range(len(df_new['market_cap'].tolist()))]
            
        else : 
            avg = np.array([pd.concat([df_update[(df_update['market_cap'] == i) & 
                                                 (df_update['Trader_Name'] == dropdown_brokers_value) &
                                                 (df_update['Side']=='Buy')]['Avg/Entree'],
                                       df_update[(df_update['market_cap'] == i) & 
                                                 (df_update['Trader_Name'] == dropdown_brokers_value) &
                                                 (df_update['Side']=='Sell')]['Avg/Entree']*(-1)]).mean() 
                                                    for i in (market_cap)])*100
            
            last = np.array([pd.concat([df_update[(df_update['market_cap'] == i) & 
                                                  (df_update['Trader_Name'] == dropdown_brokers_value)&
                                                  (df_update['Side']=='Buy')]['Last/Entree'],
                                        df_update[(df_update['market_cap'] == i) & 
                                                  (df_update['Trader_Name'] == dropdown_brokers_value) &
                                                  (df_update['Side']=='Sell')]['Last/Entree']*(-1)]).mean() 
                                                     for i in (market_cap)])*100
            ecart = []
            for i in range(len(avg)):
                if last[i] >= 0 :
                    ecart.append( last[i] - avg[i])
                else :
                    ecart.append(-(last[i] - avg[i]))
            for i in range(len(avg)) :
                avg[i] = round(avg[i], 2)
                last[i] = round(last[i], 2)
                ecart[i] = round(ecart[i], 2)
    
            compte =[]
            freq = df_update['market_cap'].value_counts()
            for i in market_cap :
                if df_update['market_cap'].str.contains(i, regex = False ).any() :
                    compte.append(freq[i])
                else :
                    compte.append(0)
            df_new = pd.DataFrame ({'market_cap' : market_cap,
                                    'avg' : avg,
                                    'last' : last,
                                    'ecart' : ecart,
                                    'compte' : compte })
            df_new = df_new[df_new['compte'] != 0]
            df_new.sort_values(by = 'ecart', ascending = False, inplace = True)
            df_new.reset_index(inplace = True)
            index = [f'{df_new["market_cap"][i]}' + " " + f'{[df_new["compte"][i]]}' for i in range(len(df_new['market_cap'].tolist()))]
    
    figure = {
                    'data': [
                        {'x' : index, 'y' : df_new['avg'].tolist(),
                         'type' : 'bar', 'name': 'Avg', 'weight' : '30px',
                         'text' : df_new['avg'].tolist(), 'textposition' : 'outside', 'textfont_size' : 14,
                         'marker' :
                             {'size' : 12,
                              'line' : {'width' : 2,
                                        'color' : 'DarkSlateGrey'}}
                         
                         },
                        {'x' : index, 'y' : df_new['last'].tolist(),
                         'type': 'bar', 'name' : u'last', 'text' : df_new['last'].tolist(),
                         'textposition' : 'outside', 'textfont_size' : 14,
                         'marker' :
                             {'size' : 12,
                              'line' : {'width' : 2,
                                        'color' : 'DarkSlateGrey'}}
                         },
                        {'x' : index, 'y' : df_new['ecart'].tolist(),
                         'type': 'bar', 'name': u'ecart', 'text' : df_new['ecart'].tolist(), 'textposition' :'outside',
                        'textfont_size' : 14, 'marker' : 
                            { 'color' : 'grey',
                             'size' : 12,
                              'line' : {'width' : 2,
                                        'color' : 'DarkSlateGrey'}
                              }
                         },
                        
                    
                    ],
                    'layout' : {
                        'title' :  " Moyennes par market cap du  " f'{start_date}' " au " f'{end_date}' " :" ,
                        'plot_bgcolor' : 	'#e2dfdf',
                        'paper_bgcolor' : '#e2dfdf',
                        'font' : dict(color = 'black',
                                      size = 13,
                                      family = 'Times New Roman'),
                        'automargin' : True,
                        'legend' : dict(
        
                                traceorder="reversed",
                                title = " Broker : ",
                                title_font_family="Times New Roman",
                                font=dict(
                                    family="Times New Roman",
                                    size=12,
                                    color="black"
                                ),
                                bgcolor="LightSteelBlue",
                                bordercolor="Black",
                                borderwidth=2,
                        ), 
                    }
                }
    return figure
   
@app.callback(
    Output('pie_5','figure'),
    Input('submit-button-state', 'n_clicks'),
    State('dropdown_data', 'value'),
    State('dropdown_venue', 'value'),
    State('calendar','start_date'),
    State('calendar','end_date'),
    State('dropdown_brokers','value'),
    State('dropdown_vue','value')
    )

def update_pie_5(n_clicks, dropdown_data_value, dropdown_venue_value, start_date, end_date, dropdown_brokers_value, dropdown_vue_value):
    
    df_update = pd.DataFrame(columns = ['Broker_ID', 'Broker_Name', 'Side', 'traded_Shares', 'Transaction_Time',
                  'Ask_Bench_Px', 'Bid_Bench_Px', 'Average', 'market_cap', 'volatility', 'Trader_Name', '%complete', '%DV', 'Venue_type', 'Nb_Shares', 'categorie' ])
    if dropdown_data_value == 'Wheel' :
        df_update= df_wheel
        
        if dropdown_venue_value == 'Tous les types' :
            df_update= df_wheel
            
        else : 
            df_update = df_wheel[df_wheel['Venue_type'] == dropdown_venue_value]
            
    elif dropdown_data_value == 'Algo_IS' :
        df_update = df_is
        
        if dropdown_venue_value == 'Tous les types' :
            df_update= df_is
        else : 
            df_update = df_is[df_is['Venue_type'] == dropdown_venue_value]

    if dropdown_vue_value == 'Vue gam':
        if dropdown_brokers_value != 'Tous les brokers' :
             df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date)& (df_update['Broker_Name'] == dropdown_brokers_value)]
             df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) ]
             figure = px.sunburst(df_update, path = ['market_cap', 'Trader_Name', 'categorie'],
                                     color_discrete_sequence = px.colors.sequential.RdBu)
             figure.update_traces(textinfo = "label+percent parent"),
             figure.update_layout(title_text = "Proportion par market_cap :",
                                        plot_bgcolor = 	'#e2dfdf',
                                        paper_bgcolor = '#e2dfdf',
                                        margin = dict(t = 80, b = 20),
                                        font = dict(color = 'black',
                                                    size = 13,
                                                    family = 'Times New Roman'),
                                        legend=dict(
            
                                    traceorder="reversed",
                                    title = " Broker : ",
                                    title_font_family="Times New Roman",
                                    font=dict(
                                        family="Times New Roman",
                                        size=12,
                                        color="black"
                                    ),
                                    bgcolor="LightSteelBlue",
                                    bordercolor="Black",
                                    borderwidth=2
                                )
                             )
        else :
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) ]
            figure = px.sunburst(df_update, path = ['market_cap', 'Trader_Name', 'Broker_Name'],
                                 color_discrete_sequence = px.colors.sequential.RdBu)
            figure.update_traces(textinfo = "label+percent parent"),
            figure.update_layout(title_text = "Proportion par market_cap :",
                                    plot_bgcolor = 	'#e2dfdf',
                                    paper_bgcolor = '#e2dfdf',
                                    margin = dict(t = 80, b = 20),
                                    font = dict(color = 'black',
                                                size = 13,
                                                family = 'Times New Roman'),
                                    legend=dict(
        
                                traceorder="reversed",
                                title = " Broker : ",
                                title_font_family="Times New Roman",
                                font=dict(
                                    family="Times New Roman",
                                    size=12,
                                    color="black"
                                ),
                                bgcolor="LightSteelBlue",
                                bordercolor="Black",
                                borderwidth=2
                            )
                         )
         
    
    elif dropdown_vue_value == 'Vue broker' :
        df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date)& (df_update['Broker_Name'] == dropdown_brokers_value)]
        figure = px.sunburst(df_update, path = ['market_cap', 'Trader_Name', 'categorie'], 
                                     color_discrete_sequence = px.colors.sequential.RdBu)
        figure.update_traces(textinfo="label+percent parent"),
        figure.update_layout(title_text = "Proportion par market_cap :",
                                    plot_bgcolor = 	'#e2dfdf',
                                    paper_bgcolor = '#e2dfdf',
                                    margin = dict(t = 80, b = 20),
                                    font = dict(color = 'black',
                                                size = 13,
                                                family = 'Times New Roman'),
                                    legend=dict(
        
                                traceorder="reversed",
                                title = " Broker : ",
                                title_font_family="Times New Roman",
                                font=dict(
                                    family="Times New Roman",
                                    size=12,
                                    color="black"
                                ),
                                bgcolor="LightSteelBlue",
                                bordercolor="Black",
                                borderwidth=2
                            )
                        )
        
    elif dropdown_vue_value == 'Vue Trader': 
        if dropdown_brokers_value == 'Tous les traders' : 
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date)]
            figure = px.sunburst(df_update, path = ['market_cap', 'Broker_Name', 'Trader_Name'],
                                  color_discrete_sequence =  px.colors.sequential.RdBu)
            figure.update_traces(textinfo = "label+percent parent"),
            figure.update_layout(title_text = "Proportion par market_cap :",
                                    plot_bgcolor = 	'#e2dfdf',
                                    paper_bgcolor = '#e2dfdf',
                                    margin = dict(t = 80, b = 20),
                                    font = dict(color = 'black',
                                                size = 13,
                                                family =  'Times New Roman'),
                                    legend=dict(
        
                                traceorder="reversed",
                                title = " Broker : ",
                                title_font_family="Times New Roman",
                                font=dict(
                                    family="Times New Roman",
                                    size=12,
                                    color="black"
                                ),
                                bgcolor="LightSteelBlue",
                                bordercolor="Black",
                                borderwidth=2
                            )
                        )
        else : 
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) & (
                           df_update['Trader_Name'] == dropdown_brokers_value)]
    
            figure = px.sunburst(df_update, path = ['market_cap', 'Broker_Name', 'categorie'],
                                  color_discrete_sequence =  px.colors.sequential.RdBu)
            figure.update_traces(textinfo = "label+percent parent"),
            figure.update_layout(title_text = "Proportion par market_cap :",
                                    plot_bgcolor = 	'#e2dfdf',
                                    paper_bgcolor = '#e2dfdf',
                                    margin = dict(t = 80, b = 20),
                                    font = dict(color = 'black',
                                                size = 13,
                                                family =  'Times New Roman'),
                                    legend=dict(
        
                                traceorder="reversed",
                                title = " Broker : ",
                                title_font_family="Times New Roman",
                                font=dict(
                                    family="Times New Roman",
                                    size=12,
                                    color="black"
                                ),
                                bgcolor="LightSteelBlue",
                                bordercolor="Black",
                                borderwidth=2
                            )
                        )
    
    return figure
                         
    
 
@app.callback(
    Output('graph_10','figure'),
    Input('submit-button-state', 'n_clicks'),
    State('dropdown_data', 'value'),
    State('dropdown_venue', 'value'),
    State('calendar','start_date'),
    State('calendar','end_date'),
    State('dropdown_brokers','value'),
    State('dropdown_vue','value')
    )

def update_graph_10(n_clicks, dropdown_data_value, dropdown_venue_value, start_date, end_date, dropdown_brokers_value, dropdown_vue_value):
    
    df_update = pd.DataFrame(columns = ['Broker_ID', 'Broker_Name', 'Side', 'traded_Shares', 'Transaction_Time',
                  'Ask_Bench_Px', 'Bid_Bench_Px', 'Average', 'market_cap', 'volatility', 'Trader_Name', '%complete', '%DV', 'Venue_type', 'Nb_Shares', 'categorie' ])
    if dropdown_data_value == 'Wheel' :
        df_update= df_wheel
        
        if dropdown_venue_value == 'Tous les types' :
            df_update= df_wheel
            
        else : 
            df_update = df_wheel[df_wheel['Venue_type'] == dropdown_venue_value]
            
    elif dropdown_data_value == 'Algo_IS' :
        df_update = df_is
        
        if dropdown_venue_value == 'Tous les types' :
            df_update= df_is
        else : 
            df_update = df_is[df_is['Venue_type'] == dropdown_venue_value]

    if dropdown_vue_value == 'Vue gam':
        if dropdown_brokers_value != 'Tous les brokers' :
             df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date)& (df_update['Broker_Name'] == dropdown_brokers_value) ]
             
        else :
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) ]
            
    elif dropdown_vue_value == 'Vue broker' :
        df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date)& (df_update['Broker_Name'] == dropdown_brokers_value)]
        
    elif dropdown_vue_value == 'Vue Trader': 
        if dropdown_brokers_value == 'Tous les traders' : 
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date)]
            
        else : 
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) & (
                           df_update['Trader_Name'] == dropdown_brokers_value)]
    
    volatility = df_update['volatility'].unique()
    
    if dropdown_vue_value == 'Vue gam':
        if dropdown_brokers_value == 'Tous les brokers' :
            avg = np.array([pd.concat([df_update[(df_update['volatility'] == i) &
                                                 (df_update['Side'] == 'Buy')]['Avg/Entree'],
                                       df_update[(df_update['volatility'] == i) &
                                                 (df_update['Side'] == 'Sell')]['Avg/Entree']*(-1)]).mean() 
                                                    for i in (volatility)])*100
            
            last = np.array([pd.concat([df_update[(df_update['volatility'] == i) &
                                                  (df_update['Side'] == 'Buy')]['Last/Entree'],
                                        df_update[(df_update['volatility'] == i) &
                                                  (df_update['Side'] == 'Sell')]['Last/Entree']*(-1)]).mean() 
                                                     for i in (volatility)])*100
            
            ecart = []
            for i in range(len(avg)):
                if last[i] >= 0 :
                    ecart.append( last[i] - avg[i])
                else :
                    ecart.append(-(last[i] - avg[i]))
            for i in range(len(avg)) :
                avg[i] = round(avg[i], 2)
                last[i] = round(last[i], 2)
                ecart[i] = round(ecart[i], 2)
    
            compte =[]
            freq = df_update['volatility'].value_counts()
            for i in volatility :
                if df_update['volatility'].str.contains(i, regex = False).any() :
                    compte.append(freq[i])
                else :
                    compte.append(0)
            df_new = pd.DataFrame ({'volatility' : volatility,
                                    'avg' : avg,
                                    'last' : last,
                                    'ecart' : ecart,
                                    'compte' : compte })
            df_new = df_new[df_new['compte'] != 0]
            df_new.sort_values(by = 'ecart', ascending = False, inplace = True)
            df_new.reset_index(inplace = True)
            index = [f'{df_new["volatility"][i]}' + " " + f'{[df_new["compte"][i]]}' for i in range(len(df_new['volatility'].tolist()))]
            
        else :
            avg = np.array([pd.concat([df_update[(df_update['Broker_Name'] == dropdown_brokers_value) & 
                                                 (df_update['volatility'] == i) &
                                                 (df_update['Side'] == 'Buy')]['Avg/Entree'],
                                       df_update[(df_update['Broker_Name'] == dropdown_brokers_value) & 
                                                 (df_update['volatility'] == i) &
                                                 (df_update['Side']=='Sell')]['Avg/Entree']*(-1)]).mean() 
                                                    for i in (volatility)])*100
            
            last = np.array([pd.concat([df_update[(df_update['Broker_Name'] == dropdown_brokers_value)& 
                                                  (df_update['volatility'] == i) &
                                                  (df_update['Side'] == 'Buy')]['Last/Entree'],
                                        df_update[(df_update['Broker_Name'] == dropdown_brokers_value)& 
                                                  (df_update['volatility'] == i) &
                                                  (df_update['Side'] == 'Sell')]['Last/Entree']*(-1)]).mean() 
                                                     for i in (volatility) ])*100
            
            ecart = []
            for i in range(len(avg)):
                if last[i] >= 0 :
                    ecart.append( last[i] - avg[i])
                else :
                    ecart.append(-(last[i] - avg[i]))
            for i in range(len(avg)) :
                avg[i] = round(avg[i], 2)
                last[i] = round(last[i], 2)
                ecart[i] = round(ecart[i], 2)
    
            compte = []
            freq = df_update['volatility'].value_counts()
            for i in volatility :
                if df_update['volatility'].str.contains(i, regex = False).any() :
                    compte.append(freq[i])
                else :
                    compte.append(0)
            df_new = pd.DataFrame ({ 'volatility' : volatility,
                                    'avg' : avg,
                                    'last' : last,
                                    'ecart' : ecart,
                                    'compte' : compte })
            df_new = df_new[df_new['compte'] != 0]
            df_new.sort_values(by = 'ecart', ascending= False, inplace = True)
            df_new.reset_index(inplace = True)
            index = [f'{df_new["volatility"][i]}' + " " + f'{[df_new["compte"][i]]}' for i in range(len(df_new['volatility'].tolist())) ]
            
    elif dropdown_vue_value == 'Vue broker' :
        avg = np.array([pd.concat([df_update[(df_update['volatility'] == i) &
                                             (df_update['Broker_Name'] == dropdown_brokers_value)&
                                             (df_update['Side']=='Buy')]['Avg/Entree'],
                                   df_update[(df_update['volatility'] == i) &
                                             (df_update['Broker_Name'] == dropdown_brokers_value)&
                                             (df_update['Side']=='Sell')]['Avg/Entree']*(-1)]).mean() 
                                                for i in (volatility)])*100
        
        last = np.array([pd.concat([df_update[(df_update['volatility'] == i) &
                                              (df_update['Broker_Name'] ==dropdown_brokers_value) &
                                              (df_update['Side']=='Buy')]['Last/Entree'],
                                    df_update[(df_update['volatility'] == i) & 
                                              (df_update['Broker_Name'] ==dropdown_brokers_value) &
                                              (df_update['Side']=='Sell')]['Last/Entree']*(-1)]).mean() 
                                                 for i in (volatility)])*100
        
        ecart = []
        for i in range(len(avg)):
            if last[i] >= 0 :
                ecart.append( last[i] - avg[i])
            else :
                ecart.append(-(last[i] - avg[i]))
        for i in range(len(avg)) :
            avg[i] = round(avg[i], 2)
            last[i] = round(last[i], 2)
            ecart[i] = round(ecart[i], 2)
        compte =[]
        freq = df_update['volatility'].value_counts()
        for i in volatility :
            if df_update['volatility'].str.contains(i, regex = False ).any() :
                compte.append(freq[i])
            else :
                compte.append(0)
        df_new = pd.DataFrame ({ 'volatility' : volatility,
                                'avg' : avg,
                                'last' : last,
                                'ecart' : ecart,
                                'compte' : compte })
        df_new = df_new[df_new['compte'] != 0]
        df_new.sort_values(by = 'ecart', ascending = False, inplace = True)
        df_new.reset_index(inplace = True)
        index = [f'{df_new["volatility"][i]}' + " " + f'{[df_new["compte"][i]]}' for i in range(len(df_new['volatility'].tolist()))]
        
    else : 
        if dropdown_brokers_value == 'Tous les traders' : 
            
            avg = np.array([pd.concat([df_update[(df_update['volatility'] == i) &
                                                 (df_update['Side'] == 'Buy')]['Avg/Entree'],
                                       df_update[(df_update['volatility'] == i) &
                                                 (df_update['Side'] == 'Sell')]['Avg/Entree']*(-1)]).mean() 
                                                    for i in (volatility)])*100
            
            last = np.array([pd.concat([df_update[(df_update['volatility'] == i) &
                                                  (df_update['Side'] == 'Buy')]['Last/Entree'],
                                        df_update[(df_update['volatility'] == i) &
                                                  (df_update['Side'] == 'Sell')]['Last/Entree']*(-1)]).mean() 
                                                     for i in (volatility)])*100
            
            ecart = []
            for i in range(len(avg)):
                if last[i] >= 0 :
                    ecart.append( last[i] - avg[i])
                else :
                    ecart.append(-(last[i] - avg[i]))
            for i in range(len(avg)) :
                avg[i] = round(avg[i], 2)
                last[i] = round(last[i], 2)
                ecart[i] = round(ecart[i], 2)
    
            compte =[]
            freq = df_update['volatility'].value_counts()
            for i in volatility :
                if df_update['volatility'].str.contains(i, regex = False).any() :
                    compte.append(freq[i])
                else :
                    compte.append(0)
            df_new = pd.DataFrame ({'volatility' : volatility,
                                    'avg' : avg,
                                    'last' : last,
                                    'ecart' : ecart,
                                    'compte' : compte })
            df_new = df_new[df_new['compte'] != 0]
            df_new.sort_values(by = 'ecart', ascending = False, inplace = True)
            df_new.reset_index(inplace = True)
            index = [f'{df_new["volatility"][i]}' + " " + f'{[df_new["compte"][i]]}' for i in range(len(df_new['volatility'].tolist()))]
            
        else : 
            avg = np.array([pd.concat([df_update[(df_update['volatility'] == i) & 
                                                 (df_update['Trader_Name'] == dropdown_brokers_value) &
                                                 (df_update['Side'] == 'Buy')]['Avg/Entree'],
                                       df_update[(df_update['volatility'] == i) & 
                                                 (df_update['Trader_Name'] == dropdown_brokers_value) &
                                                 (df_update['Side'] == 'Sell')]['Avg/Entree']*(-1)]).mean() 
                                                    for i in (volatility)])*100
            
            last = np.array([pd.concat([df_update[(df_update['volatility'] == i) & 
                                                  (df_update['Trader_Name'] == dropdown_brokers_value)&
                                                  (df_update['Side'] == 'Buy')]['Last/Entree'],
                                        df_update[(df_update['volatility'] == i)& 
                                                  (df_update['Trader_Name'] == dropdown_brokers_value)&
                                                  (df_update['Side'] == 'Sell')]['Last/Entree']*(-1)]).mean() 
                                                     for i in (volatility)])*100
            
            ecart = []
            for i in range(len(avg)):
                if last[i] >= 0 :
                    ecart.append( last[i] - avg[i])
                else :
                    ecart.append(-(last[i] - avg[i]))
            for i in range(len(avg)) :
                avg[i] = round(avg[i], 2)
                last[i] = round(last[i], 2)
                ecart[i] = round(ecart[i], 2)
    
            compte = []
            freq = df_update['volatility'].value_counts()
            for i in volatility :
                if df_update['volatility'].str.contains(i, regex = False ).any() :
                    compte.append(freq[i])
                else :
                    compte.append(0)
            df_new = pd.DataFrame ({'volatility' : volatility,
                                    'avg' : avg,
                                    'last' : last,
                                    'ecart' : ecart,
                                    'compte' : compte })
            df_new = df_new[df_new['compte'] != 0]
            df_new.sort_values(by = 'ecart', ascending = False, inplace = True)
            df_new.reset_index(inplace=True)
            index = [f'{df_new["volatility"][i]}' + " " + f'{[df_new["compte"][i]]}' for i in range(len(df_new['volatility'].tolist()))]
    
   
       
        
    figure = {
                    'data': [
                        {'x' : index, 'y' : df_new['avg'].tolist(),
                         'type' : 'bar', 'name': 'Avg', 'weight' : '30px',
                         'text' : df_new['avg'].tolist(), 'textposition' :'outside', 'textfont_size' : 14,
                         'marker' :
                             {'size' : 12,
                              'line' : {'width' : 2,
                                        'color' : 'DarkSlateGrey'}}
                         
                         },
                        {'x' : index, 'y' : df_new['last'].tolist(),
                         'type': 'bar', 'name' : u'last', 'text' : df_new['last'].tolist(),
                         'textposition' : 'outside', 'textfont_size' : 14,
                         'marker' :
                             {'size' : 12,
                              'line' : {'width' : 2,
                                        'color' : 'DarkSlateGrey'}}
                         },
                        {'x' : index, 'y' : df_new['ecart'].tolist(),
                         'type': 'bar', 'name': u'ecart', 'text' : df_new['ecart'].tolist(), 'textposition' :'outside',
                        'textfont_size' : 14, 'marker' : 
                            { 'color' : 'grey',
                             'size' : 12,
                              'line' : {'width' : 2,
                                        'color' : 'DarkSlateGrey'}} 
                         },
                    ],
                    'layout' : {
                        'title' :  " Moyennes par volatilité du  " f'{start_date}' " au " f'{end_date}' " :" ,
                        'plot_bgcolor' : 	'#e2dfdf',
                        'paper_bgcolor' : '#e2dfdf',
                        'font' : dict(color = 'black',
                                      size = 13,
                                      family = 'Times New Roman'),
                        'automargin' : True,
                        'legend' : dict(
        
                                traceorder="reversed",
                                title = " Broker : ",
                                title_font_family="Times New Roman",
                                font=dict(
                                    family="Times New Roman",
                                    size=12,
                                    color="black"
                                ),
                                bgcolor="LightSteelBlue",
                                bordercolor="Black",
                                borderwidth=2
                        )  
                    }
                }
        
    return figure
    
    
@app.callback(
    Output('pie_6', 'figure'),
    Input('submit-button-state', 'n_clicks'),
    State('dropdown_data', 'value'),
    State('dropdown_venue', 'value'),
    State('calendar', 'start_date'),
    State('calendar', 'end_date'),
    State('dropdown_brokers', 'value'),
    State('dropdown_vue', 'value')
    )

def update_pie_6(n_clicks, dropdown_data_value, dropdown_venue_value, start_date, end_date, dropdown_brokers_value, dropdown_vue_value):
   
    

    df_update = pd.DataFrame(columns = ['Broker_ID', 'Broker_Name', 'Side', 'traded_Shares', 'Transaction_Time',
                  'Ask_Bench_Px', 'Bid_Bench_Px', 'Average', 'market_cap', 'volatility', 'Trader_Name', '%complete', '%DV', 'Venue_type', 'Nb_Shares', 'categorie' ])
    if dropdown_data_value == 'Wheel' :
        df_update= df_wheel
        
        if dropdown_venue_value == 'Tous les types' :
            df_update= df_wheel
            
        else : 
            df_update = df_wheel[df_wheel['Venue_type'] == dropdown_venue_value]
            
    elif dropdown_data_value == 'Algo_IS' :
        df_update = df_is
        
        if dropdown_venue_value == 'Tous les types' :
            df_update= df_is
        else : 
            df_update = df_is[df_is['Venue_type'] == dropdown_venue_value]

    if dropdown_vue_value == 'Vue gam':
        if dropdown_brokers_value != 'Tous les brokers' :
             df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date)& (df_update['Broker_Name'] == dropdown_brokers_value)]
             
        else :
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) ]
            
    elif dropdown_vue_value == 'Vue broker' :
        df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date)& (df_update['Broker_Name'] == dropdown_brokers_value)]
        
    elif dropdown_vue_value == 'Vue Trader': 
        if dropdown_brokers_value == 'Tous les traders' : 
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date)]
            
        else : 
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) & (
                           df_update['Trader_Name'] == dropdown_brokers_value)]
    if dropdown_vue_value == 'Vue broker' :    
        
            
        figure = px.sunburst(df_update, path = ['volatility', 'Trader_Name', 'categorie'],
                             color_discrete_sequence = px.colors.sequential.RdBu)
        figure.update_traces(textinfo="label+percent parent"),
        figure.update_layout(title_text = "Proportion par volatility :",
                                    plot_bgcolor = 	'#e2dfdf',
                                    paper_bgcolor = '#e2dfdf',
                                    margin = dict(t = 80, b = 20),
                                    font = dict(color = 'black',
                                                size = 13,
                                                family = 'Times New Roman'),
                                    legend=dict(
        
                                traceorder="reversed",
                                title = " Broker : ",
                                title_font_family="Times New Roman",
                                font = dict(
                                    family="Times New Roman",
                                    size=12,
                                    color="black"
                                ),
                                bgcolor="LightSteelBlue",
                                bordercolor="Black",
                                borderwidth=2
                            )
                         )
         
    elif dropdown_vue_value == 'Vue Trader' :
        if dropdown_brokers_value == 'Tous les traders' :
            df_update = df_update
        else :
            df_update = df_update[df_update['Trader_Name'] == dropdown_brokers_value]
        
        figure = px.sunburst(df_update, path = ['volatility', 'Broker_Name', 'categorie'],
                              color_discrete_sequence = px.colors.sequential.RdBu)
        figure.update_traces(textinfo = "label+percent parent"),
        figure.update_layout(title_text = "Proportion par volatility :",
                                    plot_bgcolor = 	'#e2dfdf',
                                    paper_bgcolor = '#e2dfdf',
                                    margin = dict(t = 80, b = 20),
                                    font = dict(color = 'black',
                                                size = 13,
                                                family = 'Times New Roman'),
                                    legend = dict(
        
                                traceorder="reversed",
                                title = " Broker : ",
                                title_font_family="Times New Roman",
                                font=dict(
                                    family="Times New Roman",
                                    size=12,
                                    color="black"
                                ),
                                bgcolor="LightSteelBlue",
                                bordercolor="Black",
                                borderwidth=2
                            )
                         )
         
    
    elif dropdown_vue_value == 'Vue gam': 
        if dropdown_brokers_value != 'Tous les brokers' : 
        
            figure = px.sunburst(df_update, path = ['volatility', 'Trader_Name', 'categorie'],
                                  color_discrete_sequence = px.colors.sequential.RdBu)
            figure.update_traces(textinfo = "label+percent parent"),
            figure.update_layout(title_text = "Proportion par volatility :",
                                        plot_bgcolor = 	'#e2dfdf',
                                        paper_bgcolor = '#e2dfdf',
                                        margin = dict(t = 80, b = 20),
                                        font = dict(color = 'black',
                                                    size = 13,
                                                    family = 'Times New Roman'),
                                        legend =  dict(
            
                                    traceorder="reversed",
                                    title = " Broker : ",
                                    title_font_family="Times New Roman",
                                    font = dict(
                                        family="Times New Roman",
                                        size=12,
                                        color="black"
                                    ),
                                    bgcolor="LightSteelBlue",
                                    bordercolor="Black",
                                    borderwidth=2
                                )
                             )
        else :
            figure = px.sunburst(df_update, path = ['volatility', 'Trader_Name', 'Broker_Name'],
                                  color_discrete_sequence = px.colors.sequential.RdBu)
            figure.update_traces(textinfo = "label+percent parent"),
            figure.update_layout(title_text = "Proportion par volatility :",
                                        plot_bgcolor = 	'#e2dfdf',
                                        paper_bgcolor = '#e2dfdf',
                                        margin = dict(t = 80, b = 20),
                                        font = dict(color = 'black',
                                                    size = 13,
                                                    family = 'Times New Roman'),
                                        legend =  dict(
            
                                    traceorder="reversed",
                                    title = " Broker : ",
                                    title_font_family="Times New Roman",
                                    font = dict(
                                        family="Times New Roman",
                                        size=12,
                                        color="black"
                                    ),
                                    bgcolor="LightSteelBlue",
                                    bordercolor="Black",
                                    borderwidth=2
                                )
                             )
            
    return figure 
 

@app.callback(
    Output('graph_11', 'figure'),
    Input('submit-button-state', 'n_clicks'),
    State('dropdown_data', 'value'),
    State('dropdown_venue', 'value'),
    State('calendar', 'start_date'),
    State('calendar', 'end_date'),
    State('dropdown_brokers', 'value'),
    State('dropdown_vue', 'value')
    )

def update_graph_11(n_clicks, dropdown_data_value, dropdown_venue_value, start_date, end_date, dropdown_brokers_value, dropdown_vue_value):
    
    df_update = pd.DataFrame(columns = ['Broker_ID', 'Broker_Name', 'Side', 'traded_Shares', 'Transaction_Time',
                  'Ask_Bench_Px', 'Bid_Bench_Px', 'Average', 'market_cap', 'volatility', 'Trader_Name', '%complete', '%DV', 'Venue_type', 'Nb_Shares', 'categorie' ])
    if dropdown_data_value == 'Wheel' :
        df_update= df_wheel
        
        if dropdown_venue_value == 'Tous les types' :
            df_update= df_wheel
            
        else : 
            df_update = df_wheel[df_wheel['Venue_type'] == dropdown_venue_value]
            
    elif dropdown_data_value == 'Algo_IS' :
        df_update = df_is
        
        if dropdown_venue_value == 'Tous les types' :
            df_update= df_is
        else : 
            df_update = df_is[df_is['Venue_type'] == dropdown_venue_value]

    if dropdown_vue_value == 'Vue gam':
        if dropdown_brokers_value != 'Tous les brokers' :
             df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Broker_Name'] == dropdown_brokers_value)]
             
        else :
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) ]
            
    elif dropdown_vue_value == 'Vue broker' :
        df_update = df_update[(df_update['Tmin'] >= start_date )& (df_update['Broker_Name'] == dropdown_brokers_value) ]
        
    elif dropdown_vue_value == 'Vue Trader': 
        if dropdown_brokers_value == 'Tous les traders' : 
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date)]
            
        else : 
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) & (
                           df_update['Trader_Name'] == dropdown_brokers_value)]
    
    DV = df_update['%DV'].unique()
    
    if dropdown_vue_value == 'Vue gam':
        if dropdown_brokers_value == 'Tous les brokers' :
            avg = np.array([pd.concat([df_update[(df_update['%DV'] == i) &
                                                 (df_update['Side'] == 'Buy')]['Avg/Entree'],
                                       df_update[(df_update['%DV'] == i) &
                                                 (df_update['Side'] == 'Sell')]['Avg/Entree']*(-1)]).mean() 
                                                    for i in (DV)])*100
            
            last = np.array([pd.concat([df_update[(df_update['%DV'] == i) &
                                                  (df_update['Side'] == 'Buy')]['Last/Entree'],
                                        df_update[(df_update['%DV'] == i) &
                                                  (df_update['Side'] == 'Sell')]['Last/Entree']*(-1)]).mean() 
                                                     for i in (DV)])*100
            
            ecart = [y-x for x,y in zip(avg, last)]
            for i in range(len(avg)) :
                avg[i] = round(avg[i], 2)
                last[i] = round(last[i], 2)
                ecart[i] = round(ecart[i], 2)
    
            compte =[]
            freq = df_update['%DV'].value_counts()
            for i in DV :
                if df_update['%DV'].str.contains(i, regex = False).any() :
                    compte.append(freq[i])
                else :
                    compte.append(0)
            df_new = pd.DataFrame ({'%DV' : DV,
                                    'avg' : avg,
                                    'last' : last,
                                    'ecart' : ecart,
                                    'compte' : compte })
            df_new = df_new[df_new['compte'] != 0]
            df_new.sort_values(by = 'ecart', ascending = False, inplace =True)
            df_new.reset_index(inplace=True)
            index = [f'{df_new["%DV"][i]}' + " " + f'{[df_new["compte"][i]]}' for i in range(len(DV))]
            
        else :
            avg = np.array([pd.concat([df_update[(df_update['Broker_Name'] == dropdown_brokers_value) & 
                                                 (df_update['%DV'] == i) &
                                                 (df_update['Side'] == 'Buy')]['Avg/Entree'],
                                       df_update[(df_update['Broker_Name'] == dropdown_brokers_value) & 
                                                 (df_update['%DV'] == i) &
                                                 (df_update['Side']=='Sell')]['Avg/Entree']*(-1)]).mean() 
                                                    for i in (DV)])*100
            
            last = np.array([pd.concat([df_update[(df_update['Broker_Name'] == dropdown_brokers_value)& 
                                                  (df_update['%DV'] == i) &
                                                  (df_update['Side'] == 'Buy')]['Last/Entree'],
                                        df_update[(df_update['Broker_Name'] == dropdown_brokers_value)& 
                                                  (df_update['%DV'] == i) &
                                                  (df_update['Side'] == 'Sell')]['Last/Entree']*(-1)]).mean() 
                                                     for i in (DV) ])*100
            
            ecart = [y-x for x,y in zip(avg, last)]
            for i in range(len(avg)) :
                avg[i] = round(avg[i], 2)
                last[i] = round(last[i], 2)
                ecart[i] = round(ecart[i], 2)
    
            compte =[]
            freq = df_update['%DV'].value_counts()
            for i in DV :
                if df_update['%DV'].str.contains(i, regex = False).any() :
                    compte.append(freq[i])
                else :
                    compte.append(0)
            df_new = pd.DataFrame ({ '%DV' : DV,
                                    'avg' : avg,
                                    'last' : last,
                                    'ecart' : ecart,
                                    'compte' : compte })
            df_new = df_new[df_new['compte'] != 0]
            df_new.sort_values(by = 'ecart', ascending= False, inplace =True)
            df_new.reset_index(inplace=True)
            index = [f'{df_new["%DV"][i]}' + " " + f'{[df_new["compte"][i]]}' for i in range(len(df_new['%DV'].tolist())) ]
            
    elif dropdown_vue_value == 'Vue broker' :
        avg = np.array([pd.concat([df_update[(df_update['%DV'] == i) &
                                             (df_update['Broker_Name'] == dropdown_brokers_value)&
                                             (df_update['Side']=='Buy')]['Avg/Entree'],
                                   df_update[(df_update['%DV'] == i) &
                                             (df_update['Broker_Name'] == dropdown_brokers_value)&
                                             (df_update['Side']=='Sell')]['Avg/Entree']*(-1)]).mean() 
                                                for i in (DV)])*100
        
        last = np.array([pd.concat([df_update[(df_update['%DV'] == i) &
                                              (df_update['Broker_Name'] == dropdown_brokers_value) &
                                              (df_update['Side']=='Buy')]['Last/Entree'],
                                    df_update[(df_update['%DV'] == i) & 
                                              (df_update['Broker_Name'] == dropdown_brokers_value) &
                                              (df_update['Side']=='Sell')]['Last/Entree']*(-1)]).mean() 
                                                 for i in (DV)])*100
        
        ecart = [y-x for x,y in zip(avg, last)]
        for i in range(len(avg)) :
            avg[i] = round(avg[i], 2)
            last[i] = round(last[i], 2)
            ecart[i] = round(ecart[i], 2)
        compte =[]
        freq = df_update['%DV'].value_counts()
        for i in DV :
            if df_update['%DV'].str.contains(i, regex = False ).any() :
                compte.append(freq[i])
            else :
                compte.append(0)
        df_new = pd.DataFrame ({ '%DV' : DV,
                                'avg' : avg,
                                'last' : last,
                                'ecart' : ecart,
                                'compte' : compte })
        df_new = df_new[df_new['compte'] != 0]
        df_new.sort_values(by = 'ecart', ascending = False, inplace = True)
        df_new.reset_index(inplace = True)
        index = [f'{df_new["%DV"][i]}' + " " + f'{[df_new["compte"][i]]}' for i in range(len(df_new['%DV'].tolist()))]
        
    else : 
        if dropdown_brokers_value == 'Tous les traders' : 
            
            avg = np.array([pd.concat([df_update[(df_update['%DV'] == i) &
                                                 (df_update['Side'] == 'Buy')]['Avg/Entree'],
                                       df_update[(df_update['%DV'] == i) &
                                                 (df_update['Side'] == 'Sell')]['Avg/Entree']*(-1)]).mean() 
                                                    for i in (DV)])*100
            
            last = np.array([pd.concat([df_update[(df_update['%DV'] == i) &
                                                  (df_update['Side'] == 'Buy')]['Last/Entree'],
                                        df_update[(df_update['%DV'] == i) &
                                                  (df_update['Side'] == 'Sell')]['Last/Entree']*(-1)]).mean() 
                                                     for i in (DV)])*100
            
            ecart = [y-x for x,y in zip(avg, last)]
            for i in range(len(avg)) :
                avg[i] = round(avg[i], 2)
                last[i] = round(last[i], 2)
                ecart[i] = round(ecart[i], 2)
            compte =[]
            freq = df_update['%DV'].value_counts()
            for i in DV :
                if df_update['%DV'].str.contains(i, regex = False).any() :
                    compte.append(freq[i])
                else :
                    compte.append(0)
            df_new = pd.DataFrame ({'%DV' : DV,
                                    'avg' : avg,
                                    'last' : last,
                                    'ecart' : ecart,
                                    'compte' : compte })
            df_new = df_new[df_new['compte'] != 0]
            df_new.sort_values(by = 'ecart', ascending = False, inplace = True)
            df_new.reset_index(inplace = True)
            index = [f'{df_new["%DV"][i]}' + " " + f'{[df_new["compte"][i]]}' for i in range(len(df_new['%DV'].tolist()))]
            
        else : 
            avg = np.array([pd.concat([df_update[(df_update['%DV'] == i) & 
                                                 (df_update['Trader_Name'] == dropdown_brokers_value) &
                                                 (df_update['Side'] == 'Buy')]['Avg/Entree'],
                                       df_update[(df_update['%DV'] == i) & 
                                                 (df_update['Trader_Name'] == dropdown_brokers_value) &
                                                 (df_update['Side'] == 'Sell')]['Avg/Entree']*(-1)]).mean() 
                                                    for i in (DV)])*100
            
            last = np.array([pd.concat([df_update[(df_update['%DV'] == i) & 
                                                  (df_update['Trader_Name'] == dropdown_brokers_value)&
                                                  (df_update['Side'] == 'Buy')]['Last/Entree'],
                                        df_update[(df_update['%DV'] == i) & 
                                                  (df_update['Trader_Name'] == dropdown_brokers_value)&
                                                  (df_update['Side'] == 'Sell')]['Last/Entree']*(-1)]).mean() 
                                                     for i in (DV)])*100
            
            ecart = [y-x for x,y in zip(avg, last)]
            for i in range(len(avg)) :
                avg[i] = round(avg[i], 2)
                last[i] = round(last[i], 2)
                ecart[i] = round(ecart[i], 2)
    
            compte =[]
            freq = df_update['%DV'].value_counts()
            for i in DV :
                if df_update['%DV'].str.contains(i, regex = False ).any() :
                    compte.append(freq[i])
                else :
                    compte.append(0)
            df_new = pd.DataFrame ({'%DV' : DV,
                                    'avg' : avg,
                                    'last' : last,
                                    'ecart' : ecart,
                                    'compte' : compte })
            df_new.sort_values(by = 'ecart', ascending = False, inplace = True)
            df_new = df_new[df_new['compte'] != 0]
            df_new.reset_index(inplace = True)
            index = [f'{df_new["%DV"][i]}' + " " + f'{[df_new["compte"][i]]}' for i in range(len(df_new['%DV'].tolist()))]
    
   
       
        
    figure = {
                    'data': [
                        {'x' : index, 'y' : df_new['avg'].tolist(),
                         'type' : 'bar', 'name': 'Avg', 'weight' : '30px',
                         'text' : df_new['avg'].tolist(), 'textposition' : 'outside', 'textfont_size' : 14,
                         'marker' :
                             {'size' : 12,
                              'line' : {'width' : 2,
                                        'color' : 'DarkSlateGrey'}}
                         
                         },
                        {'x' : index, 'y' : df_new['last'].tolist(),
                         'type': 'bar', 'name': u'last', 'text' : df_new['last'].tolist(),
                         'textposition' :'outside', 'textfont_size' : 14,
                         'marker' :
                             {'size' : 12,
                              'line' : {'width' : 2,
                                        'color' : 'DarkSlateGrey'}}
                         },
                        {'x' : index, 'y' : df_new['ecart'].tolist(),
                         'type': 'bar', 'name': u'ecart', 'text' : df_new['ecart'].tolist(), 'textposition' :'outside',
                        'textfont_size' : 14, 'marker' : 
                            { 'color' : 'grey',
                             'size' : 12,
                              'line' : {'width' : 2,
                                        'color' : 'DarkSlateGrey'}
                              }
                         },
                        
                    
                    ],
                    'layout' : {
                        'title' :  " Moyennes par % de daily volume du  " f'{start_date}' " au " f'{end_date}' " :" ,
                        'plot_bgcolor' : 	'#e2dfdf',
                        'paper_bgcolor' : '#e2dfdf',
                        'font' : dict(color = 'black',
                                      size = 13,
                                      family = 'Times New Roman'),
                        'automargin' : True,
                        'legend' : dict(
        
                                traceorder="reversed",
                                title = " Broker : ",
                                title_font_family="Times New Roman",
                                font=dict(
                                    family="Times New Roman",
                                    size=12,
                                    color="black"
                                ),
                                bgcolor="LightSteelBlue",
                                bordercolor="Black",
                                borderwidth=2
                        )
                    }
                }
       
              
                 
    return figure
    
    
@app.callback(
    Output('pie_7', 'figure'),
    Input('submit-button-state', 'n_clicks'),
    State('dropdown_data', 'value'),
    State('dropdown_venue', 'value'),
    State('calendar', 'start_date'),
    State('calendar', 'end_date'),
    State('dropdown_brokers', 'value'),
    State('dropdown_vue', 'value')
    )

def update_pie_7(n_clicks, dropdown_data_value, dropdown_venue_value, start_date, end_date, dropdown_brokers_value, dropdown_vue_value):
   
    df_update = pd.DataFrame(columns = ['Broker_ID', 'Broker_Name', 'Side', 'traded_Shares', 'Transaction_Time',
                  'Ask_Bench_Px', 'Bid_Bench_Px', 'Average', 'market_cap', 'volatility', 'Trader_Name', '%complete', '%DV', 'Venue_type', 'Nb_Shares', 'categorie' ])
    if dropdown_data_value == 'Wheel' :
        df_update= df_wheel
        
        if dropdown_venue_value == 'Tous les types' :
            df_update= df_wheel
            
        else : 
            df_update = df_wheel[df_wheel['Venue_type'] == dropdown_venue_value]
            
    elif dropdown_data_value == 'Algo_IS' :
        df_update = df_is
        
        if dropdown_venue_value == 'Tous les types' :
            df_update= df_is
        else : 
            df_update = df_is[df_is['Venue_type'] == dropdown_venue_value]

    if dropdown_vue_value == 'Vue gam':
        if dropdown_brokers_value != 'Tous les brokers' :
             df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Broker_Name'] == dropdown_brokers_value)]
             
        else :
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) ]
            
    elif dropdown_vue_value == 'Vue broker' :
        df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Broker_Name'] == dropdown_brokers_value)]
        
    elif dropdown_vue_value == 'Vue Trader': 
        if dropdown_brokers_value == 'Tous les traders' : 
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date)]
            
        else : 
            df_update = df_update[(df_update['Tmin'] >= start_date ) & (df_update['Tmin'] <= end_date) & (
                           df_update['Trader_Name'] == dropdown_brokers_value)]
  
    if dropdown_vue_value == 'Vue broker' :    
        
            
        figure = px.sunburst(df_update, path = ['%DV', 'Trader_Name', 'categorie'],
                             color_discrete_sequence = px.colors.sequential.RdBu)
        
    elif   dropdown_vue_value == 'Vue Trader' :
        
        
        figure = px.sunburst(df_update, path = ['%DV', 'Broker_Name', 'categorie'],
                              color_discrete_sequence = px.colors.sequential.RdBu)
        
        
    elif dropdown_vue_value == 'Vue gam': 
        if dropdown_brokers_value != 'Tous les brokers' :
            figure = px.sunburst(df_update, path = ['%DV', 'Trader_Name', 'categorie'],
                                  color_discrete_sequence = px.colors.sequential.RdBu)
            
        else : 
            figure = px.sunburst(df_update, path = ['%DV', 'Trader_Name', 'Broker_Name'],
                                  color_discrete_sequence = px.colors.sequential.RdBu)
            
    figure.update_traces(textinfo = "label+percent parent"),
    figure.update_layout(title_text = "Proportion par % daily volume :",
                                 title_font_family = 'Times New Roman',
                                        plot_bgcolor = 	'#e2dfdf',
                                        paper_bgcolor = '#e2dfdf',
                                        margin = dict(t = 80, b = 20),
                                        font = dict(color = 'black',
                                                    size = 13,
                                                    family = 'Times New Roman'),
                                        legend = dict(
                  
                                            font = dict(color = 'black'))
                                        )
    return figure
    
    
  


if __name__ == '__main__':
    app.run_server(debug = False )  