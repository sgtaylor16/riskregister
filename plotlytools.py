import plotly.graph_objs as go



def addcube(figwidth:float,prob:int,risk:int) -> go.Figure:

    fig = go.Figure()

    botleft = [0,0]

    def colorselector(i,j):
        if j==0:
            return "green"
        elif j == 1:
            if i <= 2:
                return "green"
            else:
                return "yellow"
        elif j== 2:
            if i <=1:
                return "green"
            elif i > 1 and i <= 3:
                return "yellow"
            else :
                return "red"
        elif j == 3:
            if i <= 1:
                return "green"
            elif i > 1 and i <= 2:
                return "yellow"
            else:
                return "red"
        else:
            if i == 0:
                return "green"
            elif i == 1:
                return "yellow"
            else:
                return "red"

    boxwidth = figwidth/5
    for j in range(5):
        for i in range(5):
            fig.add_shape(type="rect",x0=botleft[0]+i*boxwidth,y0=botleft[1]+j*boxwidth,
                          x1=botleft[0]+(i+1)*boxwidth,y1=botleft[1]+(j+1)*boxwidth,fillcolor=colorselector(i,j),opacity=1.0,line=dict(width=2,color="black"))
            
    #Now add the circle
    x0 = (prob-1 + .30)*boxwidth
    y0 = (risk-1 + .30)*boxwidth
    x1 = (prob-1 + .70)*boxwidth
    y1 = (risk-1 + .70)*boxwidth
    fig.add_shape(type="circle",x0=x0,y0=y0,x1=x1,y1=y1,fillcolor="black",opacity=1.0,line=dict(width=2,color="black"))

    
    fig.update_layout(autosize=False,height=figwidth,width=figwidth,
                    xaxis=dict(visible=False),
                    yaxis=dict(visible=False),
                    showlegend=False)
    



    fig.update_xaxes(range = [0, figwidth])
    fig.update_yaxes(range = [0, figwidth])

    return fig

