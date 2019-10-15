var imgs = ["/static/images/background/1.jpg",

    "/static/images/background/2.png",
    "/static/images/background/3.jpg",
    "/static/images/background/4.jpg"];    //（设定想要显示的图片）

function time() {
    var i = Math.floor(Math.random() * (4 + 0) + 0); //（获取随机数，设置m~n的随机，此处3是代表n，0处是m，可以替换）
    document.body.style.backgroundImage = "URL(" + imgs[i] + ")";


}

time();
setInterval("time()", 5000);



//字体动画
var index=0;
var word=document.getElementById("w").innerHTML;
function type(){
    document.getElementById("aa").innerText = word.substring(0,index++);
}

setInterval(type, 250);


//字体轮播




