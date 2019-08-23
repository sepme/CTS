var c = document.getElementById("ChamranTeamLoader");
var ctx = c.getContext("2d");
var sArc;
var eArc;
var i;
var count;
ctx.lineWidth = 2;
var points = [{cpx:0 , cpy:0 , x:7, y:64}, {cpx:8 , cpy:59 , x:11, y:59}, {cpx:13.5 , cpy:59 , x:16, y:59}, {cpx:19 , cpy:59 , x:21, y:55}, {cpx:21 , cpy:53 , x:26, y:55}
, {cpx:32 , cpy:63 , x:34, y:57}, {cpx:35 , cpy:43 , x:36, y:27}, {cpx:38 , cpy:22 , x:40, y:27}, {cpx:39 , cpy:22 , x:43, y:64}, {cpx:45 , cpy:69 , x:46, y:69}, {cpx:47 , cpy:69 , x:48, y:64}
, {cpx:47 , cpy:69 , x:49, y:60}, {cpx:51 , cpy:58 , x:53, y:57}, {cpx:55 , cpy:57 , x:57, y:51}, {cpx:60 , cpy:49 , x:61, y:51}, {cpx:61 , cpy:52 , x:66, y:58}, {cpx:68 , cpy:59 , x:69, y:59}
, {cpx:68 , cpy:59 , x:76, y:59}, {cpx:77 , cpy:59 , x:79, y:55}, {cpx:81 , cpy:53 , x:83, y:55}, {cpx:83 , cpy:57 , x:85, y:59}, {cpx:91 , cpy:59 , x:94, y:54}, {cpx:94 , cpy:53 , x:95, y:49}
, {cpx:94 , cpy:46 , x:95, y:45}];
// setTimeout(drawLogo, 2500);
drawLogo();
rotate(1);
function rotate(time) {
    $(".page-loader > .loader > canvas").css({
        "transform" : "rotateY(90deg)",
        "transition" : "all ease 0.3s"
    }).css({
        "transform" : "rotateY(180deg)",
        "transition" : "all ease 0.3s"
    }).css({
        "transform" : "rotateY(270deg)",
        "transition" : "all ease 0.3s"
    }).css({
        "transform" : "rotateY(360deg)",
        "transition" : "all ease 0.3s"
    }).css({
        "transform" : "rotateY(0deg)"
    });
}
function drawLogo(time) {
    eArc = Math.PI * 0.09; //=> Math.PI*0.90
    requestAnimationFrame(bottomArc);
    function bottomArc(time){
        ctx.clearRect(0,0,100,100);
        bottomArcDraw(eArc);
        eArc += Math.PI * 0.03;
        if(eArc >= Math.PI*0.90){i = 1;
        requestAnimationFrame(centerCurve);
        } else{requestAnimationFrame(bottomArc);
        }
    }
    function centerCurve(time){
        ctx.clearRect(0,0,100,100);
        bottomArcDraw(Math.PI*0.90);
        centerCurveDraw(i);
        i ++;
        if ( i === 24 ) {arrowLeftDraw();
            arrowRightDraw();
            eArc = -Math.PI*0.10;// Math.PI*0.95
            requestAnimationFrame(topArc);
        } else {requestAnimationFrame(centerCurve);
        }
    }
    function topArc(time){
        ctx.clearRect(0,0,100,100);
        bottomArcDraw(Math.PI*0.90);
        centerCurveDraw(23);
        arrowLeftDraw();
        arrowRightDraw();
        topArcDraw(eArc);
        eArc -= 0.04;
        if( eArc > - Math.PI*1.04)
            requestAnimationFrame(topArc)
    }
}
function bottomArcDraw(eArc){
    ctx.beginPath();
    ctx.strokeStyle = "#E82727";
    ctx.arc(50, 50, 45, Math.PI*0.09, eArc);
    ctx.stroke();
}
function centerCurveDraw(i){
    ctx.beginPath();
    ctx.strokeStyle = "#E82727";
    ctx.moveTo(points[0].x, points[0].y);
    count = 1;
    while (i) {
        ctx.quadraticCurveTo(points[count].cpx, points[count].cpy, points[count].x, points[count].y);
        count ++;
        i--;
    }
    ctx.stroke();
}
function arrowLeftDraw(){
    ctx.beginPath();
    ctx.strokeStyle = "#E82727";
    ctx.moveTo(95, 45);
    ctx.quadraticCurveTo(95, 43, 93, 49);
    ctx.stroke();
}
function arrowRightDraw(){
    ctx.beginPath();
    ctx.strokeStyle = "#E82727";
    ctx.moveTo(95, 45);
    ctx.quadraticCurveTo(95, 45, 97, 49);
    ctx.stroke();
}
function topArcDraw(eArc){
    ctx.beginPath();
    ctx.strokeStyle = "#50D234";
    ctx.arc(50, 50, 45, -Math.PI*0.07, eArc, true);
    ctx.stroke();
}