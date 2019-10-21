每日报告发布系统
人脸识别登录使用face_recognition
windows+ubuntu下环境配置看：
https://zhangchuanjun.cn/articles/detail/ubunutu+Windows%E4%B8%8B%E5%AE%89%E8%A3%85%E9%85%8D%E7%BD%AE%E4%BD%BF%E7%94%A8%E5%BC%80%E6%BA%90%E4%BA%BA%E8%84%B8%E8%AF%86%E5%88%AB%E5%BA%93face_recognition/
或者：
https://blog.csdn.net/qq_38228830/article/details/80231702


登录界面（也作为主界面）

人脸识别登录的后台逻辑：
 前端通过ajax将拍摄的图片base_64编码后传送到后台，解码并保存至/static/images/confirm里
 从数据库获得与之前注册时的照片，保存至/static/images/register里，使用face-recognition库的compare_faces比两张照片。





后台界面功能
1.发布功能
2.修改当日报告功能
3.修改密码功能

（1）发布功能后台逻辑：
先根据登录session 的admin_id 判断谁登录，根据admin_id 删除report表内的相对应用户的记录
再增加新发布的报告的记录。
（2）修改当日报告后台逻辑：
根据登录之后保存的cookie信息  admin_id判断谁登录，以此根据admin_id获得之前发布最新的报告，然后显示在用户发表报告的框内
之后用户适当修改，然后发布，替换之前的报告。


展示界面

展示界面后台逻辑：
 按照时间倒序只显示6条数据（当初我们小组6个人）
 
 
 bug：
 1.人脸识别界面摄像头再本地能打开，放到服务器上不能打开的原因：基于http协议的，浏览器禁止了摄像头的权限，只有去百度配一个ssl证书，才可以允许你打开。
 2.摄像头就算打开了，不能连接后台原因：待考察，初步认为是发送到后台的东西太大了，或许需要适当压缩。

3.有时候偷懒，哪天不发布都可以，因为展示界面一直会显示你之前发布的，只有当你去新发布的时候，才会触发一个删除功能。
 

