import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import random
import pymongo
#Token Mapbox
token = '''this is your Map Box's Token | Ini token Map Box mu'''
#Connect to DB | Koneksi ke DB (In this case, I use MongoDB | Pada project ini, saya menggunakan MongoDB)
client= pymongo.MongoClient('insert your connection MongoDB connection url | Masukkan url penghubung ke MongoDB')
db=client['tempmap']
collection=db['tempmap']

#Start to build Dash | Mulai membuat Dash
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title='Lokamandhala | Live Web Map'

## Build a map | Membuat peta
# Create classes for  the map | Membuat kelas untuk dimasukkan ke peta
latitude=[]
longitude=[]
properties=['Project 1','Project 2', 'Project 3', 'Project 4','Project 5','Project 6','Project 7','Project 8','Project 9','Project 10','Project 11','Project 12','Project 13',]
#I call my data from DB to append latitude and longitude, there are many ways to do this | Saya memanggil data dari MongoDB, banyak cara utk mengisi ini 
for x in collection.find_one({'_id':'json_awal'})['features']:
    longitude.append(x['geometry']['coordinates'][0])
    latitude.append(x['geometry']['coordinates'][1])
peta = go.Figure(go.Scattermapbox(
        lat=latitude,
        lon=longitude,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=14,
        ),
        text=properties,
    ))
peta.update_layout(
    mapbox_style="open-street-map",
    hovermode='closest',
    mapbox=dict(
        # accesstoken=token,
        bearing=0,
        center=go.layout.mapbox.Center(
                    lat=0.509140943251138,
                    lon=101.4474105834961
            ),
        pitch=0,
        zoom=10
    )
)

##Start to make a radar | Mulai membuat radar
#Initialize the first random data | Menginisiasi data random pertama
rad = [1, 2, 3, 4, 5]
for sx in range(0, 4):
    rad[sx] = random.randint(1, 10)
#Customize the radar | Mengatur radar
radar=go.Figure()
radar.add_trace(go.Scatterpolar(
          r=rad,
          theta=['processing cost', 'mechanical properties', 'chemical stability',
                 'thermal stability', 'device integration'],
          fill='toself',
          name='Product A'
      ))
#Customize its layout | Mengatur layoutnya
radar_layout=radar.update_layout(
              polar=dict(
                radialaxis=dict(
                  visible=True,
                  range=[0, 10]
                )),
              showlegend=False
            )
            
#Create dict for slider | Membuat dit untuk slider
marks_dict={1:{'label':'1'},2:{'label':'2'},3:{'label':'3'},4:{'label':'4'},5:{'label':'5'},
        6:{'label':'6'},7:{'label':'7'},8:{'label':'8'},9:{'label':'9'},10:{'label':'10'},11:{'label':'11'}
        ,12:{'label':'12'}}

#Start to design the layout | Mulai merancang tata letaknya
app.layout=html.Div([
                dbc.Container(
                    dbc.Row([
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    dbc.Row([
                                        dbc.Col([
                                            html.H1('LIVE MAP DEMO', style={'color':'#ad2303','font-family':'Segoe UI','font-size':'2rem'}),
                                            html.H5('Dengan data random yang secara otomatis diregenerasi', style={'color':'#ad2303', 'font-size':'.7rem'}),
                                        ], sm=11),
                                        dbc.Col(
                                            html.Img(style={'right': '0', 'margin': 'auto'}, src='assets/favicon.ico',
                                                         width='60em', height='60em', title='Lokamandhala Karya Konsultan'), sm=1)
                                    ]),
                                )),
                            sm=12),
                        dbc.Col(
                            dbc.Card([
                                dbc.CardHeader(
                                    html.H5('PETA TITIK PROJECT KOTA PEKANBARU', style={'color':'white','text-align':'center'}), style={'background-color':'#ad2303'}
                                ),
                                dbc.CardBody(
                                    dcc.Graph(
                                                id='peta_id',figure=peta, config={'displayModeBar': False, 'scrollZoom': True},
                                                style={'margin':'0','height':'75.5vh'}
                                    ),
                                )]), md=7),
                        dbc.Col(
                            dbc.Card([
                                dbc.CardHeader(
                                    html.H5('DATA TITIK PROJECT KOTA PEKANBARU', style={'color':'white','text-align':'center'}), style={'background-color':'#ad2303'}
                                ),
                                dbc.CardBody(
                                   dbc.Row([
                                       dbc.Col(
                                            dcc.Graph(figure=radar, id='radar_id', config={'displayModeBar': False}
                                          ),
                                       md=12),
                                       dbc.Col(
                                            html.Div('Bulan Ke-'),
                                       md=2),
                                       dbc.Col(
                                            dcc.Slider(id='slider_id',min=1, max=12, step=None, marks=marks_dict, included=False),
                                       md=10)
                                   ]))
                            ]),md=5)
                    ]),style={'margin-top':'3%','margin-bottom':'3%'})
])
#Callback
@app.callback(
    dash.dependencies.Output('radar_id','figure'),
    [dash.dependencies.Input('slider_id', 'value'),
     dash.dependencies.Input('peta_id', 'hoverData')]
    )
def mechanism_id(selected_marks,selected_marker):
      for sx in range(0, 4):
          rad[sx] = random.randint(1, 10)                           #Randomize the data
      radar_gen=go.Figure()
      radar_gen.add_trace(go.Scatterpolar(
              r=rad,
              theta=['Progress A', 'Progress B', 'Progress C',
                     'Progress D', 'Progress E'],
              fill='toself'
          ))
      return radar_gen

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)
