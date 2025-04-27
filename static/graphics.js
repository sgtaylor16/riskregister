import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";



export function cubecolor(i,j){
    //function to return the risk color of the cell
    //i is the row number and j is the column number
    //i and j are 0 indexed
    if(j==0 && i==0){
        return "green";
    }else if(j==0 && i==1){
        return "yellow";
    }else if(j==0 && i>=1){
        return "red";
    }else if(j==1 && i==0){
        return "green"
    }else if(j==1 && i>-1 && i<3){
        return "yellow";
    }else if(j==1 && i>=3){
        return "red";
    }else if(j==2 && i <2){
        return "green";
    }else if(j==2 && i>=2 && i<4){
        return "yellow";
    }else if(j==2 && i>=4){
        return "red";
    }else if(j==3 && i<3){
        return "green";
    }else if(j==3 && i>=3){
        return "yellow";
    }else if(j==4){
        return "green";
    }
}

function convertframe(i,j){
    //function to convert from the 1-5 scale of the risk matrices to the 0-4 scale of the risk cube
    const imap = {
        1:4,
        2:3,
        3:2,
        4:1,
        5:0
    }
    return [i-1,imap[j]];
}

export class RiskCube{
    constructor(size,selector,margin=10){
        this.size = size;
        this.selector = selector;
        this.margin = margin;
        this.cubewidth = size - 2*margin
    }
    coordinates(prob,impact){
        //function to conver probability and impact "coordinates" to screen coordinates
        //inputs are on 1-5 scale
        if(prob < 1 || prob > 5 || impact < 1 || impact > 5){
            throw new Error("probability and impact must be between 1 and 5");
        }
        cubewidth = (this.size - 2*this.margin)/5;
        xpt = (prob - 1)*cubewidth + this.margin + cubewidth/2;
        ypt = (5 - impact)*cubewidth + this.margin + cubewidth/2;
        return [xpt,ypt];
    }

    draw(){
        const width = this.size;
        const height = this.size;
        const margin = 10;
        const cubewidth = (width - 2*margin)/5;

        const svg = d3.select(this.selector)
                    .append("svg")
                    .attr("width",width)
                    .attr("height",height);

        for (let i=0;i<5;i++){
            for(let j=0;j<5;j++){
                svg.append("rect")
                    .attr("x",i*cubewidth + margin)
                    .attr("y",j*cubewidth + margin)
                    .attr("width",cubewidth)
                    .attr("height",cubewidth)
                    .attr('stroke','black')
                    .attr("fill",cubecolor(i,j))
            }
        }
        this.cubesvg = svg;
    }
    plotpoint(prob,impact){
        //function to plot the point on the risk cube
        //prob is the probability and impact is the impact
        let [xpt,ypt] = this.coordinates(prob,impact);

        this.cubesvg.append("circle")
            .attr("cx",xpt)
            .attr("cy",ypt)
            .attr("r",cubewidth/3)
            .attr("fill","black")
        }
    plottext(prob,impact,text){
        //function to plot the text on the risk cube
        //prob is the probability and impact is the impact
        let [xpt,ypt] = this.coordinates(prob,impact);

        this.cubesvg.append("text")
            .attr("x",xpt)
            .attr("y",ypt)
            .attr("text-anchor","middle")
            .attr("font-size",cubewidth/3)
            .text(text)
    }
}

export function drawriskBox(size,svgselector,prob,impact,plotcircle=true,counts=null){

    const width = size;
    const height = size;
    const margin = 10;
    const cubewidth = (width - 2*margin)/5;

    const svg = d3.select(svgselector)
                .append("svg")
                .attr("width",width)
                .attr("height",height);


    for (let i=0;i<5;i++){
        for(let j=0;j<5;j++){
            svg.append("rect")
                .attr("x",i*cubewidth + margin)
                .attr("y",j*cubewidth + margin)
                .attr("width",cubewidth)
                .attr("height",cubewidth)
                .attr('stroke','black')
                .attr("fill",cubecolor(i,j))
            if(counts != null){
                let jconver = {1:5,2:4,3:3,4:2,5:1};
                svg.append("text")
                    .attr("x",i*cubewidth + margin + cubewidth/2)
                    .attr("y",j*cubewidth + margin + cubewidth/2)
                    .attr("text-anchor","middle")
                    .attr("font-size",cubewidth/3)
                    .text(counts[i+1][jconver[j+1]])
            }
        }
    }
        if(plotcircle){
            let [newprob,newimpact] = convertframe(prob,impact);
        
            svg.append("circle")
                .attr("cx",cubewidth*newprob+ margin + cubewidth/2)
                .attr("cy",cubewidth*newimpact + margin + cubewidth/2)
                .attr("r",cubewidth/3)
                .attr("fill","black")
            }
}


export function plotRisk(size,svgselector,prob,impact){

    const width = size;
    const height = size;
    const margin = 10;

    const cubewidth = (width - 2*margin)/5;

    drawriskBox(size,svgselector);

    const svg = d3.select(svgselector)
                .select("svg");

        
}

export function riskRow(element,id,ifstatement,thenstatement,program,prob,impact,mitigationlist,person){
    let riskrow = d3.select(element).append("div").attr("class","riskrow")

    let idcolumn = riskrow.append("div").attr("class","riskid")
    idcolumn.append('p').append("a").attr('href',"/editrisk/" + id).text(id);

    let programcolumn = riskrow.append("div").attr("class","program")
    programcolumn.append("p").text(program)
    programcolumn.append("br");
    programcolumn.append("p").text(person);

    let ifcolumn = riskrow.append("div").attr("class","ifthen")
    ifcolumn.append("p").text(ifstatement);

    let thencolumn= riskrow.append("div").attr("class","ifthen")
    thencolumn.append("p").text(thenstatement);

    riskrow.append("div").attr("class","riskcube").attr("id","riskrow"+id);

    let selector = "#riskrow"+ id
    drawriskBox(100,selector,prob,impact);

    let form = riskrow.append("form")
            .attr("action","/newmit/" + id)
            .attr("method","POST")
    
    form.append("input")
        .attr("type","submit")
        .attr("value","+Mitigation")

    let mitdiv = riskrow.append("div").attr("class","mitigations")
    if (mitigationlist.length > 0){
        mitigationlist.forEach(mitigation => {
            mitdiv.append("p").append("a").attr("href","/editmit/" + mitigation.id).text(mitigation.id)
            mitdiv.append("p").text(mitigation.description)
            mitdiv.append("p").text(mitigation.probability);
            mitdiv.append("p").text(mitigation.impact);
            mitdiv.append("p").text(mitigation.date);
            mitdiv.append("p").text(mitigation.complete);
        })
    }

}
