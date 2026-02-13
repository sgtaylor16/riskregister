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
        this.cubewidth = (size - 2*margin)/5;
    }
    coordinates(prob,impact){
        //function to conver probability and impact "coordinates" to screen coordinates
        //inputs are on 1-5 scale
        if(prob < 1 || prob > 5 || impact < 1 || impact > 5){
            throw new Error("probability and impact must be between 1 and 5");
        }
        const xpt = (prob - 1)*this.cubewidth + this.margin + this.cubewidth/2;
        const ypt = (5 - impact)*this.cubewidth + this.margin + this.cubewidth/2;
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
            .attr("r",this.cubewidth/3)
            .attr("fill","black")
        }
    plottext(prob,impact,text){
        //function to plot the text on the risk cube
        //prob is the probability and impact is the impact
        let [xpt,ypt] = this.coordinates(prob,impact);

        this.cubesvg.append("text")
            .attr("x",xpt)
            .attr("y",ypt + this.cubewidth/4)
            .attr("text-anchor","middle")
            .attr("font-size",this.cubewidth/1.2)
            .text(text)
    }
}

export function drawriskBox(size,svgselector,prob,impact,mitigationlist,plotcircle=true,counts=null){

    let onecube = new RiskCube(size,svgselector)
    onecube.draw();

    if(plotcircle){
        onecube.plotpoint(prob,impact);
    }
    if(mitigationlist.length > 0){
        mitigationlist.forEach(mitigation => {
            onecube.plottext(mitigation.probability,mitigation.impact,mitigation.id);
        })
    }
}

export function pigSummary(size,svgselector,counts){

    let onecube = new RiskCube(size,svgselector)
    onecube.draw();
    for (let prob=1;prob<6;prob++){
        for(let impact=1;impact<6;impact++){
            if(counts[prob][impact] > 0){
            onecube.plottext(prob,impact,counts[prob][impact]);
            }
        }
    }
}

export function riskRow(element,id,ifstatement,thenstatement,program,prob,impact,mitigationlist,person){
    let riskrow = d3.select(element).append("div").attr("class","riskrow")

    let idcolumn = riskrow.append("div").attr("class","riskid")
    idcolumn.append('p').append("a").attr('href',"/editrisk/" + id).text(id);

    let deletebutton = idcolumn.append("form").attr("type","submit")
        .attr("action","/deleterisk/" + id)
        .attr("method","POST");
    deletebutton.append("input")
        .attr("type","submit")
        .attr("value","Delete");

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
    drawriskBox(100,selector,prob,impact,mitigationlist);

    let formdiv = riskrow.append("div").attr("class","formdiv")

    let newmit_button = formdiv.append("button")
        .attr("type","button")
        .text("New Mitigation")
        .on("click", function() {
            window.location.href = "/newmit/" + id;
        });

    let waterfallbutton = formdiv.append("button")
        .attr("type","button")
        .text("Waterfall")
        .on("click", function() {
            window.location.href = "/waterfall/" + id;
        });

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

export function plotWaterfall(size,svgselector,data){
    data.forEach(d =>{
        d.date = new Date(d.date);
    })
    console.log(typeof(data[0].date))

    let svg = d3.select(svgselector)
        .append("svg")
        .attr("width",size)
        .attr("height",size);

    let margin = {top: 10, right: 10, bottom: 30, left: 30}

    let yScale = d3.scaleLinear()
        .domain([0, 1.05 * d3.max(data, function(d) { return d.score; })])
        .range([size - margin.bottom, margin.top]);

    let xScale = d3.scaleTime()
        .domain(d3.extent(data, function(d) { return d.date; }))
        .range([margin.left, size - margin.right]);

    let xAxis = d3.axisBottom(xScale)
        .ticks(5)
        .tickFormat(d3.timeFormat("%Y-%m-%d"));
    let yAxis = d3.axisLeft(yScale)
    let sorteddata = data.sort((a,b) => a.date - b.date);

    const line = d3.line()
        .x(d => xScale(d.date))
        .y(d => yScale(d.score))
        .curve(d3.curveStepAfter);

    svg.append("path")
        .attr("d", line(sorteddata))
        .attr("stroke", "steelblue")
        .attr("fill", "none")

    svg.append('g')
        .attr('class', 'x axis')
        .attr('transform', 'translate(0,' + (size - margin.bottom) + ')')
        .call(xAxis);

    svg.append('g')
        .attr('class', 'y axis')
        .attr('transform', 'translate(' + margin.left + ',0)')
        .call(yAxis);
}