from dash import Dash, html, dcc
from plotlytools import addcube
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbcode.dbtools import Risks, Persons


def create_risk_row(ifstatement:str,riskstatement:str,prob:int,impact:int):
    return html.Div(
        className="grid-container"
    )

#Get Risks from the database
engine = create_engine('sqlite:///dbcode/riskregister.db')
Session = sessionmaker(bind=engine)
session = Session()
risks = session.query(Risks).all()

for risk in risks:
    tempfig = addcube(275,risk.probability,risk.impact)
    newlist = []
    newlist.append(html.P(risk.ifstatement))
    newlist.append(html.P(risk.thenstatement))
    newlist.append(html.P("Mitigations"))
    newlist.append(dcc.Graph(figure=tempfig))

app = Dash()

fig1 = addcube(275,3,3)
fig2 = addcube(275,1,1)

app.layout = html.Div(children = [
    html.H1("Risk Register"),
    html.Div(className="grid-container", children=[
        html.P("My First Risk"),
        html.P("Then Statement"),
        html.P("Mitigations"),
        html.Div(dcc.Graph(figure=fig1))
    ]),
    html.Div(className="grid-container", children=[
        html.P("My Second Risk"),
        html.P("Then Statement"),
        html.P("Mitigations"),
        dcc.Graph(figure=fig2)
    ])
])

if __name__ == "__main__":
    app.run(debug=True)