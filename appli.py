# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 10:32:56 2022

@author: LArib
"""

from dash import Dash, html, dcc
import dash

app = Dash(__name__, use_pages=True)




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
                    'height' : 'auto'}),
        

        ],
        className = 'row',
        style = {'height' : '4%',
                'background-color' : '#e2dfdf',
                'margin-bottom' : '30px'}
        ),

contenu = html.H1(('Bienvenue sur ce dashboard intéractif'), style = {
                                                     'color' : 'blue',
                                                     'text-align' : 'center'})
app.layout = html.Div([header, contenu, dash.page_container], style={'height' : '100%',
                             'backgroundColor' : '#007b7c', })

    


if __name__ == '__main__':
	app.run_server(debug=True)