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
    const imap = {
        1:4,
        2:3,
        3:2,
        4:1,
        5:0
    }
    return [i-1,imap[j]];
}

export function drawriskBox(size,svgselector,prob,impact){

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
                .attr("fill",cubecolor(i,j));
        }
    }

    let [newprob,newimpact] = convertframe(prob,impact);
    
    svg.append("circle")
        .attr("cx",cubewidth*newprob+ margin + cubewidth/2)
        .attr("cy",cubewidth*newimpact + margin + cubewidth/2)
        .attr("r",cubewidth/3)
        .attr("fill","black")
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

export function riskRow(element,id,ifstatement,thenstatement,program,prob,impact){
    let riskrow = d3.select(element).append("div").attr("class","riskrow")

    let idcolumn = riskrow.append("div").attr("class","riskid")
    idcolumn.append("p").text(id);

    let programcolumn = riskrow.append("div").attr("class","program")
    programcolumn.append("p").text(program);

    let ifcolumn = riskrow.append("div").attr("class","ifthen")
    ifcolumn.append("p").text(ifstatement);

    let thencolumn= riskrow.append("div").attr("class","ifthen")
    thencolumn.append("p").text(thenstatement);

    riskrow.append("div").attr("class","riskcube").attr("id","riskrow"+id);

    let selector = "#riskrow"+ id
    console.log(selector)
    drawriskBox(100,selector,prob,impact);

}
