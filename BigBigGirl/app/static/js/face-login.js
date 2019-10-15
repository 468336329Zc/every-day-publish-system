


//弹窗
var pop =document.getElementsByClassName('mainD')[0];
popUp();

function faceloginshow(){
   //获取摄像头权限
    getMedia();

}

//弹窗
function popUp() {
        let shadowButton = document.getElementById('info-yes');
        let closeButton = document.getElementById('info-sl');
        let closeButton2 = document.getElementById('info-no');
        let flag = 0;
        shadowButton.addEventListener('click', function () {
            pop.className = 'mainD active';
            flag = 1;
        });
        closeButton.addEventListener('click', function(){
            popDown()
        });
        closeButton2.addEventListener('click', function(){
            popDown()
        })
    }
    function popDown(){
        pop.className = 'mainD';
        flag = 0;
        console.log(1);
    }




function getMedia(){
      // 老的浏览器可能根本没有实现 mediaDevices，所以我们可以先设置一个空的对象
        if (navigator.mediaDevices === undefined) {
            navigator.mediaDevices = {};
        }
        if (navigator.mediaDevices.getUserMedia === undefined) {
            navigator.mediaDevices.getUserMedia = function (constraints) {
                // 首先，如果有getUserMedia的话，就获得它
                var getUserMedia = navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;

                // 一些浏览器根本没实现它 - 那么就返回一个error到promise的reject来保持一个统一的接口
                if (!getUserMedia) {
                    return Promise.reject(new Error('getUserMedia is not implemented in this browser'));
                }



                // 否则，为老的navigator.getUserMedia方法包裹一个Promise
                return new Promise(function (resolve, reject) {
                    getUserMedia.call(navigator, constraints, resolve, reject);
                });
            }
        }
        const constraints = {
            video: true,

        };
        let videoPlaying = false;
        let v = document.getElementById('v');
        let promise = navigator.mediaDevices.getUserMedia(constraints);
        promise.then(stream => {
            // 旧的浏览器可能没有srcObject
            if ("srcObject" in v) {
                v.srcObject = stream;
            } else {
                // 防止再新的浏览器里使用它，应为它已经不再支持了
                v.src = window.URL.createObjectURL(stream);
            }
            v.onloadedmetadata = function (e) {
                v.play();
                videoPlaying = true;
            };
        }).catch(err => {
            console.error(err.name + ": " + err.message);
        })

     }
  // 拍照
    function takePhoto() {
        //获得Canvas对象
        let video = document.getElementById('v');
        let canvas = document.getElementById('canvas');
        let ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, 300, 240);


    }

function login(){
    //将图片转化为base64格式，并以ajax的方式向后台发送到指定函数处理
    takePhoto();
     let canvas = document.getElementById("canvas");
    var dataURL = canvas.toDataURL("image/jpeg");
    //base64对图片编码会生成前面多余的，所以需要删除
    dataURL = dataURL.replace("data:image/jpeg;base64,", "");
    my_data={"face_id":dataURL};
    $.ajax( {
        url:"/face_login/get_face",
        type: "POST",
        data: my_data,
        success: function(data){

                if (data['status']=== "1"){
                        window.location.href="/own_center";
                }else if (data['status'] === "-1"){
                    alert("服务器后台错误");
                }else if(data['status']==="0"){
                    alert("对不起，没认出你来！");
                }else if(data['status']==='-2'){
                    alert('你还未注册！即将跳转到界面。。。');
                    window.location='/';
                }
        },
        error: function(){
            alert("服务器连接失败！");
        }
    });
}



