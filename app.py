from dash import Dash, html, dcc
from plotlytools import addcube
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbcode.dbtools import Risks, Persons, Mitigations


def create_risk_row(ifstatement:str,riskstatement:str,prob:int,impact:int):
    return html.Div(
        className="grid-container"
    )

#Get Risks from the database
engine = create_engine('sqlite:///dbcode/riskregister.db')
Session = sessionmaker(bind=engine)
session = Session()
risks = session.query(Risks).all()

risklist = []
for risk in risks:
    tempfig = addcube(275,risk.probability,risk.impact)
    risklist.append(html.P(risk.id))
    risklist.append(html.P(risk.ifstatement))
    risklist.append(html.P(risk.thenstatement))
    #Mitigations
    mitlist = []
    riskmit = session.query(Mitigations).filter(Mitigations.risk_id == risk.id).all()
    for mit in riskmit:
        if mit.complete:
            mitlist.append(html.P(mit.description,style={"text-decoration": "line-through"}))
            mitlist.append(html.P(mit.date,style={"text-decoration": "line-through"}))
        else:
            mitlist.append(html.P(mit.description))
            mitlist.append(html.P(mit.date))
    risklist.append(html.Div(className="mit-container", children=mitlist))
    risklist.append(dcc.Graph(figure=tempfig))

app = Dash()


app.layout = html.Div(children = [
    html.H1("Risk Register"),
    html.Div(className="grid-container", children=risklist)
])

if __name__ == "__main__":
    app.run(debug=True)