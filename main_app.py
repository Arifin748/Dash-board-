import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd


student_data = pd.read_csv('student.csv')

map_data = pd.read_csv('map.csv')

merged_data = pd.merge(student_data, map_data, left_on='schools_province', right_on='province')

merged_data.rename(columns={
    "totalstd": "รวมทั้งหมด",
    "totalmale": "นักเรียนชาย",
    "totalfemale": "นักเรียนหญิง"
}, inplace=True)

map_fig = px.scatter_mapbox(
    merged_data,
    lat="latitude",
    lon="longitude",
    hover_name="schools_province",
    hover_data={"รวมทั้งหมด": True, "นักเรียนชาย": True, "นักเรียนหญิง": True, "latitude": False, "longitude": False},
    size="รวมทั้งหมด",
    color="รวมทั้งหมด",
    color_continuous_scale=px.colors.cyclical.IceFire,
    size_max=30,
    zoom=5,
    mapbox_style="carto-positron",
    height=500
)


def create_pie_chart(male_count, female_count):
    pie_data = pd.DataFrame({
        "Category": ["ชาย", "หญิง"],
        "Count": [male_count, female_count],
        "Color": ["#1f77b4", "#ff7f0e"]
    })

    pie_fig = px.pie(
        pie_data,
        names='Category',
        values='Count',
        color='Category',
        color_discrete_map={
            "ชาย": "#1f77b4",
            "หญิง": "#ff7f0e"
        },
        labels={"Category": "ประเภท", "Count": "จำนวน"},
        title="การแจกแจงนักเรียนชายและนักเรียนหญิง"
    )
    pie_fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    return pie_fig


province_options = [{'label': province, 'value': province} for province in merged_data['schools_province'].unique()]


bar_fig = px.bar(
    pd.DataFrame(columns=["Category", "Count"]),
    x="Category",
    y="Count",
    labels={"Category": "ประเภท", "Count": "จำนวน"},
    title="กราฟแท่ง"
)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1(
        "แดชบอร์ดการศึกษา: การแสดงผลข้อมูลนักเรียน",
        style={
            'textAlign': 'center',
            'color': '#ffffff',
            'font-family': 'Arial, sans-serif',
            'padding': '20px',
            'backgroundColor': '#1c1c1c'
        }
    ),

    html.H2(
        "แผนที่แสดงจำนวนนักเรียนและข้อมูลนักเรียนในแต่ละจังหวัด",
        style={
            'textAlign': 'center',
            'color': '#ffffff',
            'font-family': 'Arial, sans-serif',
            'padding': '10px',
            'backgroundColor': '#333333'
        }
    ),
    
    dcc.Graph(
        id='map',
        figure=map_fig,
        style={'height': '150vh', 'width': '100%'}
    ),
    
    html.Div([
        html.Label(
            "เลือกจังหวัด:",
            style={'font-family': 'Arial, sans-serif', 'font-size': '18px', 'padding': '10px', 'color': '#ffffff'}
        ),
        dcc.Dropdown(
            id='province-dropdown',
            options=province_options,
            value=['นราธิวาส'],
            multi=True,
            style={'font-family': 'Arial, sans-serif', 'width': '50%', 'margin': 'auto', 'color': '#1c1c1c'}
        )
    ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': '#333333'}),
    
    html.Div([
        html.Div([
            dcc.Graph(
                id='bar',
                figure=bar_fig,
                style={'height': '45vh', 'width': '100%'}
            )
        ], style={'width': '50%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Graph(
                id='pie-chart',
                figure=create_pie_chart(0, 0),
                style={'height': '45vh', 'width': '100%'}
            )
        ], style={'width': '50%', 'display': 'inline-block'})
    ], style={'display': 'flex', 'padding': '20px'}),
    
    html.Div([
        html.Label(
            "เลือกประเภทข้อมูล:",
            style={'font-family': 'Arial, sans-serif', 'font-size': '18px', 'padding': '10px', 'color': '#ffffff'}
        ),
        dcc.Dropdown(
            id='data-type-dropdown',
            options=[
                {'label': 'นักเรียนชาย', 'value': 'นักเรียนชาย'},
                {'label': 'นักเรียนหญิง', 'value': 'นักเรียนหญิง'},
                {'label': 'รวมทั้งหมด', 'value': 'รวมทั้งหมด'}
            ],
            value='นักเรียนชาย',  # ค่าตั้งต้น
            style={'font-family': 'Arial, sans-serif', 'width': '50%', 'margin': 'auto', 'color': '#1c1c1c'}
        ),
        dcc.Graph(
            id='total-bar',
            figure=bar_fig,
            style={'height': '45vh', 'width': '100%'}
        ),
        dcc.Graph(
            id='total-pie',
            figure=create_pie_chart(0, 0),
            style={'height': '45vh', 'width': '100%'}
        )
    ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': '#333333'})
], style={'backgroundColor': '#1c1c1c'})

@app.callback(
    [Output('bar', 'figure'),
     Output('pie-chart', 'figure'),
     Output('total-bar', 'figure'),
     Output('total-pie', 'figure')],
    [Input('province-dropdown', 'value'),
     Input('data-type-dropdown', 'value')]
)
def update_charts(selected_provinces, selected_data_type):
    if not selected_provinces:
        return bar_fig, create_pie_chart(0, 0), bar_fig, create_pie_chart(0, 0)
    
    filtered_data = merged_data[merged_data['schools_province'].isin(selected_provinces)]
    
    bar_data = pd.DataFrame({
        "Category": ["ชาย", "หญิง", "รวม"],
        "Count": [filtered_data['นักเรียนชาย'].sum(), filtered_data['นักเรียนหญิง'].sum(), filtered_data['รวมทั้งหมด'].sum()],
        "Color": ["#1f77b4", "#ff7f0e", "#2ca02c"]
    })
    
    new_bar_fig = px.bar(
        bar_data,
        x="Category",
        y="Count",
        color="Category",
        color_discrete_map={
            "ชาย": "#1f77b4",
            "หญิง": "#ff7f0e",
            "รวม": "#2ca02c"
        },
        labels={"Category": "ประเภท", "Count": "จำนวน"},
        title=f"จำนวนนักเรียนชาย, นักเรียนหญิง และรวมในจังหวัด {' และ '.join(selected_provinces)}"
    )
    
    new_bar_fig.update_traces(marker=dict(line=dict(width=2, color='black')))
    new_bar_fig.update_layout(xaxis_title='ประเภท', yaxis_title='จำนวน', xaxis_tickangle=-45)
    
    male_count = filtered_data['นักเรียนชาย'].sum()
    female_count = filtered_data['นักเรียนหญิง'].sum()
    
    pie_fig = create_pie_chart(male_count, female_count)
    
    total_data = merged_data.groupby('schools_province').sum().reset_index()
    total_data = total_data[total_data['schools_province'].isin(selected_provinces)]
    
    total_bar_fig = px.bar(
        total_data,
        x="schools_province",
        y=selected_data_type,
        labels={"schools_province": "จังหวัด", "value": "จำนวน"},
        title=f"จำนวน {selected_data_type} ในทุกจังหวัดที่เลือก"
    )
    
    total_pie_data = total_data[['schools_province', selected_data_type]].copy()
    total_pie_data.rename(columns={'schools_province': 'จังหวัด', selected_data_type: 'จำนวน'}, inplace=True)
    
    total_pie_fig = px.pie(
        total_pie_data,
        names='จังหวัด',
        values='จำนวน',
        title=f"เปอร์เซ็นต์ {selected_data_type} ในแต่ละจังหวัดที่เลือก"
    )
    
    return new_bar_fig, pie_fig, total_bar_fig, total_pie_fig

if __name__ == '__main__':
    app.run_server(debug=True)
