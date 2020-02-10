#!/usr/bin/env python

# coding: utf-8

#--------------------Библиотеки----------------------------------

from io import BytesIO

import pandas as pd
import numpy as np

import requests

import dash

from dash.dependencies import Input, Output

import dash_core_components as dcc

import dash_bootstrap_components as dbc

import dash_html_components as html

import plotly.graph_objs as go

#--------------------/Библиотеки---------------------------------- 



# download df

def get_df():
    r = requests.get('https://docs.google.com/spreadsheets/d/1x85oldnFJr2SqHQhvhTVYj08T62FbIiwL9ub2QB9TZY/export?format=csv')
    data = r.content
    df = pd.read_csv(BytesIO(data), index_col=0).reset_index()
    df.columns = ['timestamp','gender','age','city','most_difficult_theme','quality_rate','job_rate','review', 'cohort_number']
    df['timestamp']= pd.to_datetime(df['timestamp'], format='%d.%m.%Y %H:%M:%S')
    df['day'] = df['timestamp'].astype('datetime64[D]')
    df['review'] = df['review'].fillna(df.review.mean())
    df['cohort_number'] = df['cohort_number'].fillna(5)
    df = df.dropna().reset_index(drop=True)
    df['pr_rate']= df.quality_rate*df.job_rate*df.review

    return df


#---------------------словарь цветов-----------------------------

colors = {
    'background': '#27292d',
    'H':'white',
    'text': '#e8f0fc',
    'lines' :'red',
    'grid' : '#59616e'
}

#---------------------/словарь цветов----------------------------- 

tab_style = {
    'borderBottom': '3px solid crimson',
    'padding': '15px',
    'fontWeight': 'bold',
    'color':'#e8f0fc',
    'backgroundColor': '#191a1a',
    'border-left': '0px',
    'border-right': '0px',
    'border-top': '0px'
    
    
    
}

tab_selected_style = {
    'borderTop': '3px solid #6b648f',
    'backgroundColor': '#27292d',
    'color': '#e8f0fc',
    'padding': '15px',
    'border-left': '0px',
    'border-right': '0px',
    'border-bottom': '0px'
} 

#---------------------CSS + app---------------------------------- 

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__)
server = app.server
#---------------------/CSS + app---------------------------------- 

 

#--------------------------------------------------------layout-------------------------------------------------------

        
app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.A([
                        html.Img(
                            src=app.get_asset_url("12.png"),
                            id="plotly-image",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ], href="https://praktikum.yandex.ru", target="_blank",
		    )],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "5th cohort",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Data-analyst", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        #
        html.Div(
            [
                html.Div(
                    [
                        
                        html.H1(
                            "Привет!",
                            className="control_label",
                        ),
                        html.H1(
                            "",
                            className="shifted",
                        ),
                        
                        html.H6(
                            "• Этот dashboard отражает текущий рейтинг курса 'Аналитик данных' от Яндекс.Практикум",
                            className="control_label",
                        ),
                        html.H6(
                            "• Построен на основе опроса учащихся",
                            className="control_label",
                        ),
                        html.H1(
                            "",
                            className="shifted",
                        
                        ),
                        html.P(
                            "• Обновляется автоматически",
                            className="control_label",
                        ),
                        html.P(
                            "• Опрос можно пройти здесь",
                            className="control_label",
                        ),
                        html.H1(
                            "",
                            className="shifted2",
                        
                        ),
                        html.Div(
                    [
                        html.A(
                            html.Button("опрос", id="1learn-more-button"),
                            href="https://docs.google.com/forms/d/e/1FAIpQLScwuHIxILazCP_K6_kM-R-aNdlVPblrM1_dddvNF_lrC8G6Eg/viewform", target="_blank",
                        )
                    ],
                    id="1button",
                ),
                        html.P(),
                        html.P(
                            "• От студентов для студентов"
                            , className="control_label_green")
                    ],
                    className="pretty_container four columns",
                    id="cross-filter-options",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [html.H6(id = 'met', style={'font-weight': 'bold'}), html.P("Количество респондентов")],
                                    id="wells",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id = 'man', style={'font-weight': 'bold'}), html.P("Количество мужчин")],
                                    id="gas",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id = 'woman', style={'font-weight': 'bold'}), html.P("Количество женщин")],
                                    id="oil",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id = 'mean_age', style={'font-weight': 'bold'}), html.P("Средний возраст респондента")],
                                    id="water",
                                    className="mini_container",
                                ),
                            ],
                            id="info-container",
                            className="row container-display",
                        ),
                        html.Div([
                            dcc.Tabs([
                                dcc.Tab(label='Качество программы', children=[
                        html.Div(
                            [dcc.Graph(id="rating_plot")]
                        )
                                ],style=tab_style, selected_style=tab_selected_style
                                       ),
                        dcc.Tab(label='Уверенность в трудоустройстве', children=[
                        html.Div(
                            [dcc.Graph(id="job_plot")]
                        )
                                ],style=tab_style, selected_style=tab_selected_style
                                       ),
                        dcc.Tab(label='Качество проверки проектов', children=[
                        html.Div(
                            [dcc.Graph(id="review_plot")]
                        )
                                ],style=tab_style, selected_style=tab_selected_style
                                       ),
                            ]
                            )
                        ],id="countGraphContainer",
                            className="pretty_container",),
                    ],
                    id="right-column",
                    className="eight columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [html.H6(
                            "Наиболее сложная тема",
                            className="control_label"),
                     dcc.Graph(id="diff_theme_pie_plot")],
                    className="pretty_container six columns",
                ),
                html.Div(
                    [html.H6(
                            "Местонахождение респондентов",
                            className="control_label"),
                        dcc.Loading(dcc.Graph(id='map'))],
                    className="pretty_container six columns",
                ),
            ],
            className="row flex-display",
        ),
        #
        html.Div([
        dcc.Interval(
            id='interval-component',
            interval=10*1000, # in milliseconds
            n_intervals=0
        ),
        dcc.Interval(
            id='map-interval-component',
            interval=20*60000, #(каждые 20 минут, наверное можно сделать еще больше период)
            n_intervals=0
        )
    ]
),
    html.Div(
            [
                
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Made by:",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Aleksei Beltiukov & Aleksei Komissarov", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title2",
                ),
                
            ],
            id="headerr",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
    
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
    
)
        


#----------------------метрики--------------------------------------
##
@app.callback(Output('met', 'children'),
              [Input('interval-component', 'n_intervals')])

def u_met(n):
    df = get_df()
    met = df['timestamp'].count()
    return "{}".format(met)
##
@app.callback(Output('man', 'children'),
              [Input('interval-component', 'n_intervals')])

def u_men(n):
    df = get_df()
    men = df[df['gender']=='М']['gender'].count()
    return "{}".format(men)

@app.callback(Output('woman', 'children'),
              [Input('interval-component', 'n_intervals')])

def u_women(n):
    df = get_df()
    women = df[df['gender']=='Ж']['gender'].count()
    return "{}".format(women)

@app.callback(Output('mean_age', 'children'),
              [Input('interval-component', 'n_intervals')])

def u_mean_age(n):
    df = get_df()
    mean_age=df['age'].mean()
    return "{:.0f}".format(mean_age)
   
#-------------------------------------рейтинг----------------------------------------------------
@app.callback(Output('rating_plot', 'figure'),
              [Input('interval-component', 'n_intervals')])

def update_graph_live(n):
    df = get_df()
    # rating
    fig = go.Figure()

    #1
    fig.add_trace(go.Scatter(x=df.index, y=df['quality_rate'], marker_color = 'crimson', hoverinfo='y'))
    # indicator of change
    prev_quality_rate_mean = round(df.iloc[:-2:,5].mean(), 2)
    new_quality_rate_mean = round(df.iloc[:,5].mean(), 2)
    #2
    fig.add_trace(go.Indicator(mode = 'number+delta', value = new_quality_rate_mean, delta = {"reference": prev_quality_rate_mean, "valueformat": ".2f"},
                               title = {"text": "Praktikum rate"}, domain = {'y': [0, 1], 'x': [0.0, 1.0]}))

    # mean_line
    #3
    fig.add_trace(go.Scatter(x=list(df.index), y=([df['quality_rate'].mean()] * len(df.index)),
                            line=dict(color="#6b648f", dash="dash"), name = 'mean', mode="lines"))

    # config layout
    fig.update_layout(plot_bgcolor=colors['background'], paper_bgcolor = colors['background'], font=dict(color=colors['text']),
		       xaxis=dict(gridcolor=colors['grid'], showgrid=False),
                      title="Оценки пользователей / текущий средний рейтинг",
		       yaxis=dict(gridcolor=colors['grid'], range=[0,10]), showlegend=False,
		     )

    return fig


#----------------------rating_plot--------------------------------------/#


#----------------------job_plot--------------------------------------/#
@app.callback(Output('job_plot', 'figure'),
              [Input('interval-component', 'n_intervals')])

def update_graph_live(n):
    df = get_df()
    # rating
    fig = go.Figure()

    #1
    fig.add_trace(go.Scatter(x=df.index, y=df['job_rate'], marker_color = 'crimson', hoverinfo='y'))
    # indicator of change
    prev_job_rate_mean = round(df.iloc[:-2:,6].mean(), 2)
    new_job_rate_mean = round(df.iloc[:,6].mean(), 2)
    #2
    fig.add_trace(go.Indicator(mode = 'number+delta', value = new_job_rate_mean, delta = {"reference": prev_job_rate_mean, "valueformat": ".2f"},
                               title = {"text": "Job rate"}, domain = {'y': [0, 1], 'x': [0.0, 1.0]}))

    # mean_line
    #3
    fig.add_trace(go.Scatter(x=list(df.index), y=([df['job_rate'].mean()] * len(df.index)),
                            line=dict(color="#6b648f", dash="dash"), name = 'mean', mode="lines"))

    # config layout
    fig.update_layout(plot_bgcolor=colors['background'], paper_bgcolor = colors['background'], font=dict(color=colors['text']),
		       xaxis=dict(gridcolor=colors['grid'], showgrid=False), 
                    title="Оценки пользователей / текущий средний рейтинг",
		       yaxis=dict(gridcolor=colors['grid'], range=[0,10]), showlegend=False,
		     )

    return fig

#----------------------job_plot--------------------------------------/#



#----------------------review_plot--------------------------------------/#

@app.callback(Output('review_plot', 'figure'),
              [Input('interval-component', 'n_intervals')])

def update_graph_live(n):
    df = get_df()
    # rating
    fig = go.Figure()

    #1
    fig.add_trace(go.Scatter(x=df.index, y=df['review'], marker_color = 'crimson', hoverinfo='y'))
    # indicator of change
    prev_review_rate_mean = round(df.iloc[:-2:,7].mean(), 2)
    new_review_rate_mean = round(df.iloc[:,7].mean(), 2)
    #2
    fig.add_trace(go.Indicator(mode = 'number+delta', value = new_review_rate_mean, delta = {"reference": prev_review_rate_mean, "valueformat": ".2f"},
                               title = {"text": "Review rate"}, domain = {'y': [0, 1], 'x': [0.0, 1.0]}))

    # mean_line
    #3
    fig.add_trace(go.Scatter(x=list(df.index), y=([df['review'].mean()] * len(df.index)),
                            line=dict(color="#6b648f", dash="dash"), name = 'mean', mode="lines"))

    # config layout
    fig.update_layout(plot_bgcolor=colors['background'], paper_bgcolor = colors['background'], font=dict(color=colors['text']),
		       xaxis=dict(gridcolor=colors['grid'], showgrid=False),
                      title="Оценки пользователей / текущий средний рейтинг",
		       yaxis=dict(gridcolor=colors['grid'], range=[0,10]), showlegend=False,
		     )

    return fig

#----------------------review_plot--------------------------------------/#
#----------------------diff_theme_pie_plot--------------------------------------


@app.callback(Output('diff_theme_pie_plot', 'figure'),
              [Input('interval-component', 'n_intervals')])

def update_graph_live(n):
    df = get_df()

    # theme
    most_dif = df.groupby('most_difficult_theme')['gender'].count().reset_index()
    most_dif.columns = ['most_difficult_theme', 'count']
    most_dif = most_dif.reindex([0,1,2,4,3])
    
    def add_break(cell):
        cell_list = cell.split()
        past_to = round(len(cell_list)/2)
        cell_list.insert(past_to, '<br>')
        return ' '.join(cell_list)

    most_dif['labels'] = most_dif['most_difficult_theme'].apply(add_break)
    
    x = most_dif['labels']
    y = most_dif['count']
#     max_y = y.max() # max value to give it red color
#     bar_colors = ['crimson' if rate == max_y else 'lightslategray' for rate in y]
    pulls = [0.1 if rate == max_y else 0 for rate in y]

    # draw it
    fig = go.Figure()
    fig.add_trace(go.Pie(labels=x, values=y, hole=0.35, pull=pulls,
		  	 textinfo='percent+label'))
    fig.update_traces(textfont_size=10, marker=dict(line=dict(color='#000000', width=1)))

    # config layout
    fig.update_layout(plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font=dict(color=colors['text']),
		       xaxis=dict(gridcolor=colors['grid'], showgrid=False), 
		       yaxis=dict(gridcolor=colors['grid'], range=[0,10]), showlegend=False,
		     )

    return fig

#----------------------diff_theme_pie_plot--------------------------------------/#



#----------------------map_plot-----------------------------------------

@app.callback(Output('map', 'figure'),

              [Input('map-interval-component', 'n_intervals')])

def update_graph_live(n):

    df = get_df()
    list_of_cities = df['city']

    token_Geocoder = 'c29e4b87-39fb-4f54-9689-ccc8cec48cd7'
    url = 'https://geocode-maps.yandex.ru/1.x/?format=json&apikey={}&geocode='.format(token_Geocoder)

    latitudes = []
    longitudes = []

    for city in list_of_cities:
        if city == city: # чтоб не столкнуться с nan
            url_formatted = url + city
            response = requests.get(url_formatted).json()
            data1 = response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point'].get('pos')
            latitude = (float(data1.split()[1]))
            longitude = (float(data1.split()[0]))
            latitudes.append(latitude)
            longitudes.append(longitude)
        else:
            latitudes.append('')
            longitudes.append('')

    df['x'] = latitudes
    df['y'] = longitudes
    size = df.groupby('city')['city'].count()
    size.name = 'size'
    df = df.merge(size,on = 'city')

    # логика для карты

    mapbox_access_token =   "pk.eyJ1IjoiYWxiZWw5OTk5IiwiYSI6ImNrNmI0M2NydTA1YjAzZnBha2dtcnJ1YmYifQ.7H3jZRqSGUnb88yeLgkN_A"


#-------------------------------------

    data = go.Scattermapbox(lat=df['x'], lon=df['y'],
                              mode='markers+text',
                              hovertext=df['size'],
                              textfont=dict(color='#e8f0fc'),
                              marker=dict(size=df['size']+20,
                              color = 'crimson'),
                              text=df['city'])

    layout = go.Layout( mapbox_style='dark',
                        autosize=True,
                        hovermode='closest',
                        mapbox=dict(accesstoken=mapbox_access_token,
                                    bearing=0,
                                    center=dict(lat=55, lon=55),
                                    pitch=0, zoom=2.3),
                        plot_bgcolor = colors['background'],
                        paper_bgcolor = colors['background'],
			margin=dict(l=0, r=0, t=0, b=0))

    fig = go.Figure(data=data, layout=layout)

    return fig

#----------------------/map_plot----------------------------------------

#--------------------------------------------------------/layout-------------------------------------------------------   

 


 

 

# условная конструкция и запуск

if __name__ == '__main__':
    app.run_server(debug=False, port=8050) # or whatever you choose
