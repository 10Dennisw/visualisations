# Importing the libraries
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Loading data
df = pd.read_csv(r"C:\Users\denni\OneDrive\Desktop\DS-projects&coursework\Dash-Related\african-economics-dashboard\africa_economics_v2.csv")

# Creating the app and the layout
app = dash.Dash(__name__)
app.layout = html.Div(style={'backgroundColor': 'white', 'color': '#FFFFFF', 'margin': '0'}, children=[
    html.H1("African GDP Dashboard", style={'textAlign': 'center', 'color': 'black', 'fontFamily': 'sans-serif',  'paddingTop': '30px'}),

    # Creating a slider for each year, allowing the user to filter
    dcc.Slider(
        id='year-slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].min(),
        marks={str(year): str(year) for year in range(df['Year'].min(), df['Year'].max() + 1)},
        step=1,
    ),

    # Creating a chloropleth and bar chart, to be side by side - using 49% width
    html.Div(style={'display': 'flex', 'backgroundColor': 'white'}, children=[
        # Chloropleth map
        dcc.Graph(
            id='world-map',
            style={'border': '1px solid black', 'height': '400px', 'width': '100%', 'margin-top': '20px', 'margin-bottom': '10px', 'backgroundColor': '#000000'}
        ),
    ]),
    
    html.Div(style={'display': 'flex', 'backgroundColor': 'white'}, children=[   

        # Bar chart
        dcc.Graph(
            id='gdp-bar-chart',
            style={'border': '1px solid black', 'height': '400px', 'width': '49%', 'float': 'right', 'margin-right': '5px', 'margin-bottom': '20px', 'backgroundColor': '#000000'}         
        ),

        # Pie chart
        dcc.Graph(
            id='gdp-pie-chart',
            style={'border': '1px solid black', 'height': '400px', 'width': '49%',  'float': 'left','margin-left': '5px', 'margin-right': '10px', 'margin-bottom': '20px', 'backgroundColor': '#000000'}
        ),
    ]),
])

# Using callbacks to update choropleth map and bar chart based on selected year
@app.callback(
    [Output('world-map', 'figure'),
     Output('gdp-bar-chart', 'figure'),
     Output('gdp-pie-chart', 'figure')],
    [Input('year-slider', 'value')]
)
def update_charts(selected_year):
    filtered_df = df.loc[df['Year'] == selected_year]

    # Features of the choropleth Map
    map_fig = px.choropleth(
        filtered_df,
        locations='Code',
        color='GDP (USD)',
        hover_name='Country',
        color_continuous_scale=px.colors.sequential.Plasma,
        projection='orthographic',
        title='',
        template='plotly'
    )

    # Filtering and Sorting data frame to get top five values
    top_five_df = filtered_df.sort_values(by='GDP (USD)', ascending=False).head(5)

    # Features of the bar chart Map
    bar_fig = px.bar(
        top_five_df,
        x='Country',
        y='GDP (USD)',
        title=f'Largest 5 African Economies in {selected_year}',
        labels={'GDP (USD)': 'GDP (USD in Billions)'},
    )

    # Rotating the angle of the x-axis labels to 25 degrees
    bar_fig.update_layout(xaxis_tickangle=25)

    # Addinga black outline of each bar, setting the width to 2
    bar_fig.update_traces(marker_line_color='black', marker_line_width=2)
    
    # Sorting and filtering the filtered dataframe to show 6 values, largest 5 economies and the other economies 
    pie_df = filtered_df.sort_values(by='GDP (USD)', ascending=False)
    top5_indices = pie_df['GDP (USD)'].nlargest(5).index
    pie_df.loc[~pie_df.index.isin(top5_indices), 'Country'] = 'Other'

    # Features of the pie chart
    pie_fig = px.pie(
        pie_df,
        names='Country',
        values='GDP (USD)',
        title=f'GDP Distribution in {selected_year}'
    )

    map_fig.update_traces(marker=dict(line={"color": "#d1d1d1", "width": 0.5}))

    map_fig.update_layout(geo=dict(showframe=False,
                                    showcoastlines=False,
                                    showcountries=True,
                                    countrycolor="#d1d1d1",
                                    showocean=True,
                                    oceancolor="#c9d2e0",
                                    showlakes=True,
                                    lakecolor="#99c0db",
                                    showrivers=True,
                                    rivercolor="#99c0db",
                                    resolution=110),
        coloraxis_colorbar=dict(title="GDP"),
        paper_bgcolor = "white",
        font=dict(color="black"),
        margin=dict(l=20, r=20, t=10, b=10)
    )
    
    # setting the map to focus on Africa
    map_fig.update_geos(projection_rotation=dict(lon=17, lat=0))

    bar_fig.update_layout(
        paper_bgcolor = "white",
        font=dict(color="black"),
        title=dict(x=0.5),
        margin=dict(l=30, r=30, t=60, b=60)
    )

    pie_fig.update_layout(
        paper_bgcolor="white",
        font=dict(color="black"),
        title=dict(x=0.5),
        margin=dict(l=30, r=30, t=60, b=60)
    )

    # Adding a black outline around each section of the piece, and setting the width to black
    pie_fig.update_traces(marker=dict(line=dict(color='black', width=2)))

    # returning the map figure and bar chart
    return map_fig, bar_fig, pie_fig

# running the app, as defined above
if __name__ == '__main__':
    app.run_server(debug=True)


