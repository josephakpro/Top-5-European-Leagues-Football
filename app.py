import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# -----------------------------------------------------------------------------
# 1. Data Initialization & Pre-Processing
# -----------------------------------------------------------------------------
# Load your final exported dataset
df = pd.read_csv("final_dashboard_data.csv", encoding='latin1')

# Rename columns for front-end executive readability
rename_dict = {
    'Performance_Axis': 'Performance Score',
    'Game_Control_Axis': 'Game Control Score',
    'Cluster_Label': 'Tactical Archetype',
    'Average_salary(€m)': 'Average Salary (€M)'
}
df = df.rename(columns=rename_dict)

# Ensure Tactical Archetype is treated as a categorical string, not a continuous number
df['Tactical Archetype'] = df['Tactical Archetype'].astype(str)

# Radar Chart Variables
radar_cols = [
    'Possession(%)', 'Pass/90', 'Long_balls/90', 'Crosses/90', 
    'Clearances/90', 'Possession_won_midfield/90', 
    'Possession_won_attacking_3rd/90', 'Touches_in_opposition_box/90', 
    'Tackles/90', 'Interceptions/90', 'Saves/90'
]

# Pre-calculate Min-Max for Radar Chart Normalization (0 to 1 scale)
radar_min = df[radar_cols].min()
radar_max = df[radar_cols].max()

# Pre-calculate Macro League Health metrics using Mean Absolute Deviation (MAD)
# This calculates the MAD for Strength Gap (Performance) and Tactical Diversity (Game Control)
mad_df = df.groupby('League').apply(
    lambda x: pd.Series({
        'Strength Gap': (x['Performance Score'] - x['Performance Score'].mean()).abs().mean(),
        'Tactical Diversity': (x['Game Control Score'] - x['Game Control Score'].mean()).abs().mean()
    })
).reset_index()

# Create a Dictionary for Chained Dropdowns: {League: [Team1, Team2, ...]}
league_team_dict = df.groupby('League')['Team'].apply(list).to_dict()

# -----------------------------------------------------------------------------
# 2. Dash App Layout
# -----------------------------------------------------------------------------
app = dash.Dash(__name__)
server = app.server
app.title = "European Football Benchmarking"

app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'padding': '20px'}, children=[
    html.H1("European Football Tactical & Financial Benchmarking", style={'textAlign': 'center'}),
    html.Hr(),

    # --- SECTION 5: MACRO CONTEXT (LEAGUE HEALTH) ---
    # Placed at the top so it acts as a global filter
    html.H3("Macro Context: League Health & Competitiveness"),
    html.P("Click on a specific league's bar to filter the Market Map and Efficiency Matrix below. Double-click to reset."),
    html.Div([
        dcc.Graph(
            id='macro-bar-chart',
            figure=px.bar(mad_df, x='League', y=['Strength Gap', 'Tactical Diversity'], 
                          barmode='group', title="League MAD Coefficients (Click to Filter)")
        )
    ]),
    html.Hr(),

    # --- SECTION 1: THE MARKET MAP ---
    html.H3("The Market Map: Game Control vs. Performance"),
    html.Div([
        html.Label("Color By:"),
        dcc.RadioItems(
            id='market-map-color-toggle',
            options=[{'label': ' Domestic League ', 'value': 'League'}, 
                     {'label': ' Tactical Archetype ', 'value': 'Tactical Archetype'}],
            value='League',
            inline=True
        ),
        html.Br(),
        html.Label("Bubble Size:"),
        dcc.RadioItems(
            id='market-map-size-toggle',
            options=[{'label': ' Uniform Size ', 'value': 'Uniform'}, 
                     {'label': ' Scale by Average Salary ', 'value': 'Average Salary (€M)'}],
            value='Uniform',
            inline=True
        ),
    ], style={'paddingBottom': '10px'}),
    dcc.Graph(id='market-map-scatter'),
    html.Hr(),

    # --- SECTION 4: THE EFFICIENCY MATRIX ---
    html.H3("The Efficiency Matrix: Budget vs. Execution"),
    html.P("This chart automatically filters based on your selection in the Macro Context chart above."),
    dcc.Graph(id='efficiency-matrix-scatter'),
    html.Hr(),

    # --- GLOBAL DROPDOWNS FOR SECTIONS 2 & 3 ---
    html.H3("Micro Analysis: Tactical Twins & DNA"),
    html.Div([
        html.Div([
            html.Label("1. Select League:"),
            dcc.Dropdown(
                id='league-dropdown',
                options=[{'label': k, 'value': k} for k in league_team_dict.keys()],
                value='England'
            ),
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '2%'}),
        
        html.Div([
            html.Label("2. Select Target Team (Team A):"),
            dcc.Dropdown(id='team-a-dropdown'),
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '2%'}),

        html.Div([
            html.Label("3. Select Comparison Team (Team B) [Optional]:"),
            dcc.Dropdown(
                id='team-b-dropdown',
                options=[{'label': t, 'value': t} for t in df['Team'].sort_values()],
                placeholder="Select a team to compare..."
            ),
        ], style={'width': '30%', 'display': 'inline-block'}),
    ]),
    html.Br(),

    # --- SECTION 2: TACTICAL TWIN FINDER ---
    html.H4("Tactical Twin Finder"),
    html.P("Top 3 closest teams mathematically based exclusively on the Game Control PCA Score absolute difference."),
    html.Div(id='tactical-twin-output', style={'display': 'flex', 'gap': '20px'}),
    html.Br(),

    # --- SECTION 3: TACTICAL DNA (RADAR CHART) ---
    html.H4("Tactical DNA: Stats/90 Drill-Down"),
    dcc.Checklist(
        id='cluster-avg-toggle',
        options=[{'label': ' Overlay Team A\'s Tactical Archetype Average', 'value': 'Show'}],
        value=[]
    ),
    dcc.Graph(id='dna-radar-chart')
])

# -----------------------------------------------------------------------------
# 3. Callbacks
# -----------------------------------------------------------------------------

# Callback to chain League dropdown to Team A dropdown
@app.callback(
    [Output('team-a-dropdown', 'options'),
     Output('team-a-dropdown', 'value')],
    Input('league-dropdown', 'value')
)
def update_team_dropdown(selected_league):
    if not selected_league:
        return [], None
    teams = league_team_dict[selected_league]
    return [{'label': t, 'value': t} for t in teams], teams[0]

# Callback to update Market Map and Efficiency Matrix based on Macro Chart Clicks
@app.callback(
    [Output('market-map-scatter', 'figure'),
     Output('efficiency-matrix-scatter', 'figure')],
    [Input('macro-bar-chart', 'clickData'),
     Input('market-map-color-toggle', 'value'),
     Input('market-map-size-toggle', 'value')]
)
def update_scatter_plots(clickData, color_by, size_by):
    # Determine if a league is filtered via click
    filtered_df = df.copy()
    title_suffix = "(All Europe)"
    
    if clickData:
        clicked_league = clickData['points'][0]['x']
        filtered_df = df[df['League'] == clicked_league]
        title_suffix = f"(Filtered: {clicked_league})"
    
    # Market Map Figure
    size_col = size_by if size_by != 'Uniform' else None
    market_fig = px.scatter(
        filtered_df, x='Game Control Score', y='Performance Score',
        color=color_by, size=size_col, hover_name='Team',
        hover_data=['League', 'Tactical Archetype', 'Average Salary (€M)'],
        title=f"Market Map {title_suffix}"
    )
    
    # Efficiency Matrix Figure (Salary vs Performance with Trendline)
    eff_fig = px.scatter(
        filtered_df, x='Average Salary (€M)', y='Performance Score',
        color='League', hover_name='Team', trendline='ols',
        title=f"Efficiency Matrix: Payroll vs. Execution {title_suffix}"
    )
    
    return market_fig, eff_fig

# Callback to calculate Tactical Twins
@app.callback(
    Output('tactical-twin-output', 'children'),
    Input('team-a-dropdown', 'value')
)
def find_tactical_twins(target_team):
    if not target_team:
        return ""
    
    # Get target team's Game Control Score
    target_gc = df[df['Team'] == target_team]['Game Control Score'].values[0]
    
    # Calculate absolute difference for all teams except the target team
    twin_df = df[df['Team'] != target_team].copy()
    twin_df['GC_Diff'] = (twin_df['Game Control Score'] - target_gc).abs()
    
    # Sort and get top 3
    top_3 = twin_df.sort_values('GC_Diff').head(3)
    
    # Create HTML Cards for output
    cards = []
    for _, row in top_3.iterrows():
        card = html.Div(style={'border': '1px solid #ccc', 'padding': '15px', 'borderRadius': '5px', 'width': '30%'}, children=[
            html.H3(f"1. {row['Team']}", style={'marginTop': '0'}),
            html.P(f"League: {row['League']}"),
            html.P(f"Tactical Archetype: {row['Tactical Archetype']}"),
            html.P(f"Game Control Delta: {row['GC_Diff']:.3f}", style={'fontWeight': 'bold', 'color': '#007BFF'})
        ])
        cards.append(card)
        
    return cards

# Callback to generate the normalized Radar Chart
@app.callback(
    Output('dna-radar-chart', 'figure'),
    [Input('team-a-dropdown', 'value'),
     Input('team-b-dropdown', 'value'),
     Input('cluster-avg-toggle', 'value')]
)
def update_radar(team_a, team_b, show_cluster_avg):
    fig = go.Figure()
    
    def add_radar_trace(team_name, color, fill='toself', name_override=None):
        team_data = df[df['Team'] == team_name].iloc[0]
        raw_vals = team_data[radar_cols].values
        # Min-Max Normalization so all shapes fit cleanly on the 0-1 scale axis
        scaled_vals = (raw_vals - radar_min) / (radar_max - radar_min)
        
        display_name = name_override if name_override else team_name
        
        fig.add_trace(go.Scatterpolar(
            r=scaled_vals,
            theta=radar_cols,
            fill=fill,
            name=display_name,
            line_color=color,
            customdata=raw_vals,
            hovertemplate="<b>%{theta}</b><br>Raw Value: %{customdata:.2f}<br>Normalized Scale: %{r:.2f}<extra></extra>"
        ))
    
    # Add Team A
    if team_a:
        add_radar_trace(team_a, color='blue')
        
        # Add Cluster Average if toggled
        if 'Show' in show_cluster_avg:
            cluster_id = df[df['Team'] == team_a]['Tactical Archetype'].values[0]
            cluster_df = df[df['Tactical Archetype'] == cluster_id]
            avg_raw_vals = cluster_df[radar_cols].mean().values
            avg_scaled_vals = (avg_raw_vals - radar_min) / (radar_max - radar_min)
            
            fig.add_trace(go.Scatterpolar(
                r=avg_scaled_vals,
                theta=radar_cols,
                fill=None,
                mode='lines',
                line=dict(color='gray', dash='dash'),
                name=f'Cluster {cluster_id} Average',
                customdata=avg_raw_vals,
                hovertemplate="<b>%{theta}</b><br>Cluster Avg: %{customdata:.2f}<extra></extra>"
            ))
            
    # Add Team B
    if team_b:
        add_radar_trace(team_b, color='red', fill=None)

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=False, range=[0, 1])),
        showlegend=True,
        title="Tactical DNA (Normalized 0-1 Scale)"
    )
    return fig

# -----------------------------------------------------------------------------
# 4. Run Server
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=False)
