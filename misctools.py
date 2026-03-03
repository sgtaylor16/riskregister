from dbcode.models import Risks
from typing import Dict
from datetime import datetime
import sqlite3
import pandas as pd
from io import BytesIO

def score(prob:int,imp:int) -> int:
    """
    Function to calculate the risk score based on probability and impact.
    """
    probd = {}
    probd[1] = {}
    probd[2] = {}
    probd[3] = {}
    probd[4] = {}
    probd[5] = {}
    probd[1][1] = 1
    probd[1][2] = 6
    probd[1][3] = 11
    probd[1][4] = 16
    probd[1][5] = 21
    probd[2][1] = 3
    probd[2][2] = 8
    probd[2][3] = 13
    probd[2][4] = 18
    probd[2][5] = 23
    probd[3][1] = 5
    probd[3][2] = 10
    probd[3][3] = 15
    probd[3][4] = 19
    probd[3][5] = 25
    probd[4][1] = 7
    probd[4][2] = 12
    probd[4][3] = 17
    probd[4][4] = 22
    probd[4][5] = 27
    probd[5][1] = 9
    probd[5][2] = 14
    probd[5][3] = 20
    probd[5][4] = 24
    probd[5][5] = 29
    return probd[prob][imp]

def currentriskstatus(risk:Risks,date:datetime) -> Dict[str,int]:
    if len(risk.mitigations) == 0:
        return {"probability":risk.probability,"impact":risk.impact}
    else:
        #Sort mitigations by date
        sortedrisks = risk.mitigations.sort(key=lambda x: x.date)
        for risk in sortedrisks:
            if risk.date >= date:
                latestrisk = risk
        return {"probability":latestrisk.probability,"impact":latestrisk.impact}

def currentriskscore(risk:Risks,date:datetime) -> int:
    riskstatus = currentriskstatus(risk,date)
    return score(riskstatus["probability"],riskstatus["impact"])

def createSpreadsheet(output_path: str):
    if output_path and not output_path.endswith('.xlsx'):
        raise ValueError("Output path must end with .xlsx")
    with sqlite3.connect('dbcode/riskregister.db') as conn:
        risksdf = pd.read_sql_query("""SELECT id, ifstatement,thenstatement,probability,impact, date FROM risks
                               WHERE archive = 0""", conn)
        
        risksdf['Score'] = risksdf.apply(lambda row: score(row['probability'], row['impact']), axis=1)
        
        mitigationsdf = pd.read_sql_query("""SELECT description,probability mitigation_probability,impact mitigation_risk,risk_id,date mitigation_date,complete 
                                         FROM mitigations""",conn)
        
        mitigationsdf['Score'] = mitigationsdf.apply(lambda row: score(row['mitigation_probability'], row['mitigation_risk']), axis=1)   
        
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        risksdf.to_excel(writer, sheet_name='Risks', index=False)
        mitigationsdf.to_excel(writer, sheet_name='Mitigations', index=False)

    return None