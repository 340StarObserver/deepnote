### 服务端代码模块结构划分 ###


一. conf  配置层  

        conf/server.conf  是服务端的配置文件  



二. entrance  入口层  

        entrance/main.py  是服务端的启动入口  



三. handler  处理器层  

        handler/base_handler.py  是基类处理器  
        handler/handler_factory.py  是处理器工厂  
        handler/xxx_handler.py  是各种具体的处理器  



四. model  数据层  

        model/conf_model.py  是配置数据的模型  
        model/valid_model.py  是合法性检查的模型  
        ...  



// 注意 :  
// conf目录 & entrance目录 下的文件不要改动，若非要改，请先发出申请  
// handler/base_handler.py 这个文件不要改动，若非要改，请先发出申请  
// handler/handler_factory.py 这个文件不要改动，若非要改，请先发出申请  
// 各人只能改自己那部分的代码，若需要进行迁一发动全身的改动，请先发出申请并开会且多数人同意  



### 处理器层详解 handler/ ###

        01. verifycode_handler.py  
        
            负责发送短信验证码给用户手机  
        
        02. regist_handler.py  
        
            负责处理用户注册  
        
        03. login_handler.py  
        
            负责处理用户登录  
        
        04. logout_handler.py  
        
            负责处理用户登出  
        
        05. userinfo_handler.py  
        
            负责查询某个用户的基本信息  
        
        06. setsignature_handler.py  
        
            负责设置用户的读书格言  
        
        07. sethead_handler.py  
        
            负责设置用户的头像  
        
        08. setpwd_handler.py  
        
            负责处理用户记得密码时候的重设密码  
        
        09. forgetpwd_handler.py  
        
            负责处理用户忘记密码时候的重设密码  
        
        10. addnote_handler.py  
        
            负责用户新增一篇读书笔记  
        
        11. getnotebyuser_handler.py  
        
            负责按时间降序分页查询某个用户的读书笔记  
        
        12. modifynote_handler.py  
        
            负责用户修改一篇读书笔记  
        
        13. rmnote_handler.py  
        
            负责用户删除一篇读书笔记  
        
        14. syncnote_handler.py  
        
            负责用户同步（拉到客户端）自己的全部读书笔记的详细信息  
        
        15. getnotebytime_handler.py  
        
            负责按时间降序分页查询平台内全部的读书笔记  
        
        16. searchnote_handler.py  
        
            负责根据一句话来搜索合适的读书笔记  
        
        17. notedetail_handler.py  
        
            负责查询某篇读书笔记的具体内容  
        
        18. getcomment_handler.py  
        
            负责按时间降序分页查看某篇读书笔记的表层评论or内层评论  
        
        19. agree_handler.py  
        
            负责用户给某篇读书笔记点赞or取消点赞  
        
        20. oppose_handler.py  
        
            负责用户给某篇读书笔记反对or取消反对  
        
        21. collect_handler.py  
        
            负责用户收藏某篇读书笔记or取消收藏  
        
        22. getcollect_handler.py  
        
            负责按时间降序分页查看我的笔记收藏  
        
        23. writecomment_handler.py  
        
            负责用户对某篇读书笔记写一条表层评论or内层评论  
        
        24. message_handler.py  
        
            负责用户查看与我相关的消息(按时间降序分页)  
        
        25. care_handler.py  
        
            负责用户关注某人or取消关注  
        
        26. getcare_handler.py  
        
            负责用户查看自己关注的人(按时间降序分页)  



### 模型层详解 model/ ###

        01. conf_model.py  
        
            负责读取服务端配置文件  
        
        02. valid_model.py  
        
            a. 手机号合法性判定  
            b. 密码合法性判定  
            c. 昵称合法性判定  
            d. 读书笔记的标题的合法性判定  
            e. 读书笔记的感悟的合法性判定  
        
        03. mongoconn_model.py  
        
            负责创建mongodb的连接  
        
        04. account_model.py  
        
            a. 判断某账户是否存在  
            b. 获取某账户的信息  
            c. 设置某账户的密码  
            d. 上传头像到oss  
        
        05. note_model.py  
        
            a. 插入一篇读书笔记到mongo和elasticsearch的相关集合中  
            b. 判断某篇读书笔记是否存在  
            c. 修改mongo和elasticsearch中某篇读书笔记的内容  
            d. 删除一篇读书笔记在mongo和elasticsearch中的内容  
        
        06. search_model.py  
        
            a. 根据一句话从elasticsearch中分页地模糊搜索出若干篇笔记的id  
            b. 根据笔记id来找出那篇读书笔记的基本信息  
            c. 根据笔记id来找出那篇读书笔记的详细信息  
        
        07. interact_model.py  
        
            a. 根据笔记id,字段名,增值，来让某篇读书笔记的某个字段加一或减一  
            b. 查询某人对某篇笔记的点赞反对记录  
            c. 增加一条某人点赞or反对某篇读书笔记的记录  
            d. 删除一条某条点赞or反对某篇读书笔记的记录  
            e. 判断某人是否收藏过某篇读书笔记  
            f. 判断某人是否关注过某人  

