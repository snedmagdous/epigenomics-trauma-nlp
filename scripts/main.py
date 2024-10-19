import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load Data and Preprocess
def load_and_preprocess_data():
    df = pd.read_csv('data/pubmed_articles.csv')
    # Assuming pubmed_articles.csv contains predefined columns like 'Mental_Health_Terms', 'Epigenetic_Terms', 'Socioeconomic_Terms', etc.
    # Adjust preprocessing to focus on filtering and visualizing predefined topics.
    return df

# Build the interactive 3D topic visualization with Plotly
def create_3d_topic_visualization(df, topic_x='Mental_Health_Terms', topic_y='Epigenetic_Terms', topic_z='Socioeconomic_Terms'):
    # Use the actual data from the dataset for 3D scatter visualization
    fig = px.scatter_3d(df,
                        x=topic_x,
                        y=topic_y,
                        z=topic_z,
                        color='Ethnographic_Terms',  # Color based on race/ethnicity
                        hover_name='Journal',  # Display journal or other relevant info on hover
                        size='Correlation_Strength',  # Adjust size based on some correlation strength
                        title='3D Topic Visualization: Epigenetics, Mental Health, Socioeconomic Factors'
                        )

    fig.update_layout(
        scene=dict(
            xaxis_title='Mental Health Terms',
            yaxis_title='Epigenetic Changes',
            zaxis_title='Socioeconomic Disparities'
        ),
        margin=dict(l=0, r=0, b=0, t=40)
    )
    return fig

# Dash app setup
app = dash.Dash(__name__)

# Load and preprocess the data
df = load_and_preprocess_data()

# Layout for the Dash app
app.layout = html.Div([
    html.H1("Epigenetics and Mental Health Correlation Exploration"),

    # 3D Topic Visualization Graph
    dcc.Graph(
        id='3d_scatter',
        figure=create_3d_topic_visualization(df)
    ),
    
    # Dropdown for choosing which axis to visualize
    html.Label("Select X-axis (Mental Health Terms)"),
    dcc.Dropdown(
        id='xaxis_dropdown',
        options=[{'label': 'Depression', 'value': 'depression'},
                 {'label': 'Anxiety', 'value': 'anxiety'},
                 {'label': 'PTSD', 'value': 'ptsd'},
                 {'label': 'Suicide', 'value': 'suicide'},
                 {'label': 'Bipolar Disorder', 'value': 'bipolar'}],
        value='depression'  # Default value
    ),

    html.Label("Select Y-axis (Epigenetic Terms)"),
    dcc.Dropdown(
        id='yaxis_dropdown',
        options=[{'label': 'DNA Methylation', 'value': 'dna_methylation'},
                 {'label': 'Histone Modification', 'value': 'histone_modification'},
                 {'label': 'Gene Expression', 'value': 'gene_expression'}],
        value='dna_methylation'  # Default value
    ),

    html.Label("Select Z-axis (Socioeconomic Terms)"),
    dcc.Dropdown(
        id='zaxis_dropdown',
        options=[{'label': 'Socioeconomic Status', 'value': 'socioeconomic_status'},
                 {'label': 'Poverty', 'value': 'poverty'},
                 {'label': 'Income Inequality', 'value': 'income_inequality'}],
        value='socioeconomic_status'  # Default value
    ),

    # Explanation for relevance metric and saliency
    html.Div([
        html.P("Explore how mental health disorders and epigenetic changes manifest differently across various socioeconomic and ethnographic factors.")
    ])
])

# Define the callback for interactivity
@app.callback(
    Output('3d_scatter', 'figure'),
    [Input('xaxis_dropdown', 'value'),
     Input('yaxis_dropdown', 'value'),
     Input('zaxis_dropdown', 'value')]
)
def update_graph(xaxis, yaxis, zaxis):
    # Update 3D scatter plot based on dropdown selections
    return create_3d_topic_visualization(df, topic_x=xaxis, topic_y=yaxis, topic_z=zaxis)

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
