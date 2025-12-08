# BAKERY DASHBOARD FOR OLDER ADULTS (65+)


import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# LOAD DATA

# Load cleaned bakery dataset
bakery = pd.read_csv("Bakery_cleaned.csv")

# Load Apriori rules
rules_apriori = pd.read_csv("apriori_rules.csv")

# Convert antecedents/consequents to readable strings
rules_apriori['antecedents_str'] = rules_apriori['antecedents'].apply(lambda x: ', '.join(eval(x)))
rules_apriori['consequents_str'] = rules_apriori['consequents'].apply(lambda x: ', '.join(eval(x)))


# PREPARE DATA FOR DASHBOARD


# Top 10 most purchased items
top_items = bakery['Items'].value_counts().head(10)

# Transactions by Daypart
daypart_df = bakery.groupby("Daypart").size().reset_index(name="count")


# DASH APP

app = Dash(__name__)

app.layout = html.Div([

    # TITLE
  
    html.H1(
        "Bakery Sales Dashboard (65+ Users)",
        style={
            "textAlign": "center",
            "fontSize": "40px",
            "fontWeight": "bold",
            "marginBottom": "40px"
        }
    ),


    # TOP 10 PURCHASED ITEMS
 
    html.H2(
        "Top 10 Most Purchased Items",
        style={"fontSize": "32px", "marginTop": "20px"}
    ),

    dcc.Graph(
        id="top-items-bar",
        figure=px.bar(
            x=top_items.index,
            y=top_items.values,
            labels={"x": "Item", "y": "Purchase Count"},
            title="Most Popular Products",
            color=top_items.values,
            color_continuous_scale="Blues"
        ).update_layout(
            title_font_size=26,
            xaxis_title_font_size=20,
            yaxis_title_font_size=20
        )
    ),


    # TOP CO-PURCHASE RULES
 
    html.H2(
        "Top Co-Purchase Patterns (Apriori)",
        style={"fontSize": "32px", "marginTop": "40px"}
    ),

    dcc.Graph(
        id="co-purchase-bar",
        figure=px.bar(
            rules_apriori.head(10),
            x="antecedents_str",
            y="lift",
            color="confidence",
            labels={
                "antecedents_str": "Item(s) Bought",
                "lift": "Lift Score",
                "confidence": "Confidence"
            },
            title="Most Significant Co-Purchase Patterns",
            color_continuous_scale="Viridis"
        ).update_layout(
            title_font_size=26,
            xaxis_title_font_size=20,
            yaxis_title_font_size=20
        )
    ),


    # TRANSACTIONS BY DAY PART

    html.H2(
        "Transactions by Time of Day",
        style={"fontSize": "32px", "marginTop": "40px"}
    ),

    dcc.Graph(
        id="daypart-pie",
        figure=px.pie(
            daypart_df,
            names="Daypart",
            values="count",
            title="Distribution of Transactions by Day-Time",
            color="Daypart",
            color_discrete_sequence=px.colors.qualitative.Set3
        ).update_layout(
            title_font_size=26
        )
    )
])


if __name__ == "__main__":
    app.run_server(debug=True)
