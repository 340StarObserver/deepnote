### 接口设计 ###



01.　获取短信验证码  

        请求地址 : http://ip:port/action  

        请求体 :  
        
        {  
            action_id : 101,  
            # 请求类型的代号  
            
            phone     : 用户的手机号  
        }  

        响应头 :  
        
        其中的 Set-Cookie 字段的值类似于 "session=xxxx; HttpOnly; Path=/"  

        响应体 :  
        
        {  
            code : 验证码  
        }  



02.　注册  

        请求地址 : http://ip:port/action  

        请求体 :  
        
        {  
            action_id : 102,  
            
            usr       : 用户的手机号,  
            
            pwd       : 用户的密码的md5加密,  
            
            nick      : 昵称,  
            
            code      : 短信验证码  
        }  
        
        响应体 :  
        
        {  
            result : 是否成功,  
            # true or false  
            
            reason : 失败原因  
            # 仅当 result==false，此值才存在  
            # 1 : 验证码错误  
            # 2 : 手机号或密码格式错误  
            # 3 : 昵称为空  
            # 4 : 手机号已经存在  
        }  



03.　获取RSA公钥  

        请求地址 : http://ip:port/action  

        请求体 :  
        
        {  
            action_id : 103  
        }  
        
        响应头 :  
        
        其中的 Set-Cookie 字段的值类似于 "session=xxxx; HttpOnly; Path=/"  
        
        响应体 :  
        
        {  
            rsa_n : 公钥的n值,  
            
            rsa_e : 公钥的e值  
            # 根据这这两个值，就可以创建出对应的公钥对象  
        }  



04.　登录  

        请求地址 : http://ip:port/action  

        请求体 :  
        
        {  
            action_id : 104,  
            
            usr       : 手机号,  
            
            pwd       : 密码原文先用md5加密，再用RSA公钥加密  
        }  
        
        响应头 :  
        
        其中的 Set-Cookie 字段的值类似于 "session=xxxx; HttpOnly; Path=/"  
        
        响应体 :  
        
        {  
            result      : 是否成功,  
            # true or false  
            
            reason      : 失败原因,  
            # 仅当 result==false，此值才存在  
            # 1 : 用户不存在  
            # 2 : 密码错误  
            
            nick        : 用户的昵称,  
            # 仅当 result==true，此值才存在  
            
            signup_time : 该用户的注册时间戳（秒）,  
            # 仅当 result==true，此值才存在  
            
            signature   : 该用户的读书格言,  
            # 仅当 result==true，此值才存在  
            
            token       : 下次敏感操作的令牌  
            # 仅当 result==true，此值才存在  
        }  



05.　注销  

        请求地址 : http://ip:port/action  

        请求体 :  
        
        {  
            action_id : 105,  
        }  
        
        响应体 :  
        
        {  
            result : true  
        }  



06.　获取某人的信息  

        请求地址 : http://ip:port/action  

        请求体 :  
        
        {  
            action_id : 106,  
            
            usr       : 那人的用户名（手机号）  
        }  
        
        响应体 :  
        
        {  
            result      : 是否找到,  
            # true or false  
            
            _id         : 那人的手机号,  
            # 仅当 result==true，此值才存在  
            
            nick        : 那人的昵称,  
            # 仅当 result==true，此值才存在  
            
            signup_time : 那人的注册时间戳（秒）,  
            # 仅当 result==true，此值才存在  
            
            signature   : 那人的读书格言  
            # 仅当 result==true，此值才存在  
        }  
        


07.　设置读书格言  

        请求地址 : http://ip:port/action  

        请求体 :  
        
        {  
            action_id : 107,  
            
            signature : 新的读书格言  
        }  
        
        响应体 :  
        
        {  
            result : 是否成功,  
            # true or false  
            
            reason : 失败原因,  
            # 仅当 result==false，此值才存在  
            # 1 : 未登陆  
        }  
        


08.　设置头像  

        请求地址 : http://ip:port/action  

        请求体 :  
        
        {  
            action_id : 108,  
            
            head      : 头像图片的base64编码后的字符串,  
            
            token     : 之前获得的令牌  
        }  
        
        响应头 :  
        
        其中的 Set-Cookie 字段的值类似于 "session=xxxx; HttpOnly; Path=/"  
        
        响应体 :  
        
        {  
            result : 是否成功,  
            # true or false  
            
            reason : 失败原因,  
            # 仅当 result==false，此值才存在  
            # 1 : 未登陆  
            # 2 : 令牌错误  
            # 3 : 头像数据解析错误  
            # 4 : 头像保存失败  
            
            token  : 新的令牌  
            # 仅当 result==true，此值才存在  
        }  



09.　重设密码  

        请求地址 : http://ip:port/action  

        请求体 :  
        
        {  
            action_id : 109,  
            
            old_pwd   : 原密码的md5加密,  
            
            new_pwd   : 新密码的md5加密,  
            
            token     : 之前获得的令牌  
        }  
        
        响应头 :  
                
        其中的 Set-Cookie 字段的值类似于 "session=xxxx; HttpOnly; Path=/"  
        
        响应体 :  
        
        {  
            result : 是否成功,  
            # true or false  
            
            reason : 失败原因,  
            # 仅当 result==false，此值才存在  
            # 1 : 未登陆  
            # 2 : 令牌错误  
            # 3 : 新密码不符合要求  
            # 4 : 原密码错误  
            
            token  : 新的令牌  
            # 仅当　result==true，此值才存在  
        }  



10.　忘记密码  

        请求地址 : http://ip:port/action  

        请求体 :  
        
        {  
            action_id : 110,  
            
            usr       : 用户的手机号,  
            
            pwd       : 新密码的md5加密,  
            
            code      : 短信验证码  
        }  
        
        响应体 :  
        
        {  
            result : 是否成功,  
            # true or false  
            
            reason : 失败原因,  
            # 仅当 result==false，此值才存在  
            # 1 : 验证码错误  
            # 2 : 新密码不符合要求  
            # 3 : 该用户不存在  
        }  



11.　发布读书笔记  

        请求体 :  
        
        {  
            action_id   : 201,  
            
            token       : 之前获得的令牌,  
            
            title       : 这篇读书笔记的标题,  
            
            labels      : 这篇读书笔记的标签们,  
            # 以逗号分隔，形如 "label1,label2,label3"  
            
            source_link : 这篇读书笔记的原文链接,  
            
            source_ref  : 这篇读书笔记的原文引用,  
            
            feel        : 这篇读书笔记的个人感悟  
        }  
        
        响应头 :  
                
        其中的 Set-Cookie 字段的值类似于 "session=xxxx; HttpOnly; Path=/"  
        
        响应体 :  
        
        {  
            result   : 成功与否,  
            # true or false  
            
            reason   : 失败原因,  
            # 仅当 result==false，此值才存在  
            # 1 : 未登陆  
            # 2 : 令牌错误  
            # 3 : 标题为空  
            # 4 : 个人感悟为空  
            
            # 以下字段均仅当 result==true，才会存在  
            
            token    : 新的令牌  
            
            note_id  : 这篇新的读书笔记的id,  
            pub_time : 这篇新的读书笔记的发布时间戳（秒）  
        }  



12.　查询某人的读书笔记列表  

        请求体 :  
        
        {  
            action_id : 202,  
            
            who_usr   : 该用户的用户名（手机号）,  
            
            page_id   : 第几页,  
            # 一开始默认是第一页，此后向后翻页便加一，向前翻页便减一  
            
            page_size : 页面大小  
            # 即这页中客户端希望最多拿到多少条数据  
        }  
        
        响应体 :  
        
        {  
            notes :  
            [  
                {  
                    _id      : 这篇读书笔记的id,  
                    
                    title    : 这篇读书笔记的标题,  
                    
                    own_id   : 这篇读书笔记的所属人的用户名（手机）,  
                    
                    own_nick : 这篇读书笔记的所属人的昵称,  
                    
                    pub_time : 这篇读书笔记的发布时间戳（秒）,  
                    
                    labels   : 这篇读书笔记的标签们,  
                    # 以逗号分隔，形如 "label1,label2,label3"  
                    
                    feel     : 这篇读书笔记的个人感悟  
                },  
                {  
                    另一篇读书笔记的...  
                }  
            ]  
        }  



13.　修改某篇读书笔记  

        请求体 :  
        
        {  
            action_id   : 203,  
            
            token       : 之前获得的令牌,  
            
            note_id     : 你想修改的那篇读书笔记的id,  
            
            labels      : 新的标签们,  
            # 以逗号分隔，形如 "label1,label2,label3"  
            
            source_link : 新的原文链接,  
            
            source_ref  : 新的原文引用,  
            
            feel        : 新的个人感悟  
        }  

        响应头 :  
                
        其中的 Set-Cookie 字段的值类似于 "session=xxxx; HttpOnly; Path=/"  

        响应体 :  
        
        {  
            result  : 成功与否,  
            # true or false  
            
            reason  : 失败原因,  
            # 仅当 result==false，此值才存在  
            # 1 : 未登陆  
            # 2 : 令牌错误  
            # 3 : 个人感悟为空  
            # 4 : 该读书笔记不存在  
            # 5 : 该读书笔记不是你的  
            
            token   : 新的令牌  
            # 仅当 result==true，此值才存在  
        }  



14.　删除某篇读书笔记  

        请求体 :  
        
        {  
            action_id   : 204,  
            
            token       : 之前获得的令牌,  
            
            note_id     : 你想删除的那篇读书笔记的id  
        }  

        响应头 :  
                
        其中的 Set-Cookie 字段的值类似于 "session=xxxx; HttpOnly; Path=/"  

        响应体 :  
        
        {  
            result  : 成功与否,  
            # true or false  
            
            reason  : 失败原因,  
            # 仅当 result==false，此值才存在  
            # 1 : 未登陆  
            # 2 : 令牌错误  
            # 3 : 该读书笔记不存在  
            # 4 : 该读书笔记不是你的  
            
            token   : 新的令牌  
            # 仅当 result==true，此值才存在  
        }  



15.　同步（强制重新加载）自己的全部的读书笔记  

        请求体 :  
        
        {  
            action_id   : 205,  
            
            token       : 之前获得的令牌  
        }  

        响应头 :  
                
        其中的 Set-Cookie 字段的值类似于 "session=xxxx; HttpOnly; Path=/"  

        响应体 :  
        
        {  
            result  : 成功与否,  
            # true or false  
            
            reason  : 失败原因,  
            # 仅当 result==false，此值才存在  
            # 1 : 未登陆  
            # 2 : 令牌错误  
            
            token   : 新的令牌,  
            # 仅当 result==true，此值才存在  
            
            notes   :  
            [  
                {  
                    _id         : 这篇读书笔记的id,  
                    
                    title       : 这篇读书笔记的标题,  
                    
                    own_id      : 这篇读书笔记的所属人的用户名（手机）,  
                    
                    own_nick    : 这篇读书笔记的所属人的昵称,  
                    
                    pub_time    : 这篇读书笔记的发布时间戳（秒）,  
                    
                    labels      : 这篇读书笔记的标签们,  
                    # 以逗号分隔，形如 "label1,label2,label3"  
                    
                    feel        : 这篇读书笔记的个人感悟,  
                    
                    source_link : 这篇读书笔记的原文链接,  
                    
                    source_ref  : 这篇读书笔记的原文引用  
                },  
                {  
                    另一篇读书笔记的...  
                }  
            ]  
            # 你的全部的读书笔记的信息  
            # 仅当 result==true，此值才存在  
        }  



16.　分页浏览读书笔记  

        请求体 :  
        
        {  
            action_id : 301,  
            
            page_size : 页面大小,  
            # 客户端希望这一页中最多显示多少条数据  
            
            time_max  : 最大时间戳（秒）  
            # 若是要浏览第一页，则该值填当前时间戳  
            # 假设 page_size=3, 某次time_max=1445599887, 这一次获取第n页的数据 :  
            # 这一页上的3条读书笔记的发布时间分别是 1445599886,1445599885,1445599884  
            # 则 :  
            # 翻下一页（即获取第n+1页的数据），time_max应填 1445599884  
            # 翻上一页（即获取第n-1页的数据），time_max应填　上一次的time_max（注意，上一次并不是1445599887，它是本次的）  
        }  

        响应体 :  
        
        {  
            notes :  
            [  
                {  
                    _id      : 这篇读书笔记的id,  
                    
                    title    : 这篇读书笔记的标题,  
                    
                    own_id   : 这篇读书笔记的所属人的用户名（手机）,  
                    
                    own_nick : 这篇读书笔记的所属人的昵称,  
                    
                    pub_time : 这篇读书笔记的发布时间戳（秒）,  
                    
                    labels   : 这篇读书笔记的标签们,  
                    # 以逗号分隔，形如 "label1,label2,label3"  
                    
                    feel     : 这篇读书笔记的个人感悟  
                },  
                {  
                    另一篇读书笔记的...  
                }  
            ]  
        }  



17.　根据关键词搜索读书笔记  

        请求体 :  
        
        {  
            action_id  : 302,  
            
            keywords   : 输入的关键词,  
            # 以逗号分隔，形如 "关键词1,关键词2,关键词3"  
            
            page_size  : 页面大小,  
            
            popularity : 最大热度  
            # 第一次搜索时填 1.0  
            # 假设 某次搜索的时候该参数填的是0.95, page_size=3, 第n次搜索结果的3篇读书笔记的热度分别是 0.9, 0.8, 0.7  
            # 则 :  
            # 翻下一页（即第n+1页），该参数应该填 0.7  
            # 翻上一页（即第n-1页），该参数应该填 上一次的值（注意，0.95是本次的值，并非上一次的值）  
        }  

        响应体 :  
        
        {  
            notes :  
            [  
                {  
                    _id        : 这篇读书笔记的id,  
                    
                    title      : 这篇读书笔记的标题,  
                    
                    own_id     : 这篇读书笔记的所属人的用户名（手机）,  
                    
                    own_nick   : 这篇读书笔记的所属人的昵称,  
                    
                    pub_time   : 这篇读书笔记的发布时间戳（秒）,  
                    
                    labels     : 这篇读书笔记的标签们,  
                    # 以逗号分隔，形如 "label1,label2,label3"  
                    
                    feel       : 这篇读书笔记的个人感悟,  
                    
                    popularity : 这篇读书笔记的热度  
                },  
                {  
                    另一篇读书笔记的...  
                }  
            ]  
        }  



18.　查看某篇读书笔记的具体内容  

        请求体 :  
        
        {  
            action_id : 303,  
            
            note_id   : 读书笔记的id  
        }  
        
        响应体 :  
        
        {  
            result : 是否找到,  
            # true or false  
            
            # 以下字段，均仅当 result==true，才存在  
            
            _id         : 这篇读书笔记的id,  
            title       : 这篇读书笔记的标题,  
            labels      : 这篇读书笔记的标签们（以逗号分隔）,  
            own_id      : 这篇读书笔记的所属人的用户名（手机）,  
            own_nick    : 这篇读书笔记的所属人的昵称,  
            pub_time    : 这篇读书笔记的发布时间戳（秒）,  
            source_link : 这篇读书笔记的原文链接,  
            source_ref  : 这篇读书笔记的原文引用,  
            feel        : 这篇读书笔记的个人感悟,  
            agree_num   : 这篇读书笔记的赞同数,  
            oppose_num  : 这篇读书笔记的反对数,  
            collect_num : 这篇读书笔记的收藏数,  
            comment_num : 这篇读书笔记的评论数  
        }  



19.　分页查看某篇读书笔记的评论或子评论  

        请求体 :  
        
        {  
            action_id   : 304,  
            
            note_id     : 读书笔记的id,  
            
            ancestor_id : 祖先评论的id,  
            # 若是要翻页地查直接针对这篇读书笔记的评论，则该值填"0"  
            # 若是要翻页地查针对评论的评论（即找子评论），则该值填那条评论的id  
            
            page_id   : 第几页,  
            # 一开始默认是第一页，此后向后翻页便加一，向前翻页便减一  
            
            page_size : 页面大小  
            # 即这页中客户端希望最多拿到多少条数据  
        }  
        
        响应体 :  
        
        {  
            comments :  
            [  
                {  
                    _id          : 这条评论的id,  
                    
                    note_id      : 这条评论位于的读书笔记的id,  
                    
                    ancestor_id  : 这条评论的祖先评论的id,  
                    
                    time         : 这条评论的时间戳（秒）,  
                    
                    content      : 这条评论的内容,  
                    
                    send_id      : 评论者的用户名（手机）,  
                    
                    send_nick    : 评论者的昵称,  
                    
                    replyed_nick : 被回复者的昵称,  
                    # 若 ancestor_id=="0"，则该值无意义  
                    # 若 ancestor_id!="0"，则该值表示这条评论是回复另一条评论的（并且该值就是那一条评论的评论者的昵称）  
                    
                    recv_ids     : [ user_id1, user_id2, user_id3 ]  
                    # 消息接受者的用户名列表  
                    # 它表示如果之后有谁回复这条评论，那么哪些人会收到消息  
                },  
                {  
                    另一条评论的...  
                }  
            ]  
        }  



20.　对某篇读书笔记点赞 or 取消点赞  

        请求体 :  
        
        {  
            action_id  : 401,  
            
            note_id    : 那篇读书笔记的id,  
            
            note_title : 那篇读书笔记的标题,  
            
            own_id     : 那篇读书笔记的所属人的用户名  
        }  
        
        响应体 :  
        
        {  
            result : 是否成功,  
            # true or false  
            
            reason : 失败原因  
            # 仅当 result==false，此值才存在  
            # 1 : 未登陆  
            # 2 : 该读书笔记不存在  
            # 3 : 你已经反对了该读书笔记，就不能同时又赞同  
        }  



21.　对某篇读书笔记反对 or 取消反对  

        请求体 :  
        
        {  
            action_id  : 402,  
            
            note_id    : 那篇读书笔记的id,  
            
            note_title : 那篇读书笔记的标题,  
            
            own_id     : 那篇读书笔记的所属人的用户名  
        }  
        
        响应体 :  
        
        {  
            result : 是否成功,  
            # true or false  
            
            reason : 失败原因  
            # 仅当 result==false，此值才存在  
            # 1 : 未登陆  
            # 2 : 该读书笔记不存在  
            # 3 : 你已经赞同了该读书笔记，就不能同时又反对  
        }  



22.　对某篇读书笔记收藏 or 取消收藏  

        请求体 :  
        
        {  
            action_id : 403,  
            
            note_id    : 那篇读书笔记的id,  
            
            note_title : 那篇读书笔记的标题,  
            
            own_id     : 那篇读书笔记的所属人的用户名  
        }  
        
        响应体 :  
        
        {  
            result : 是否成功,  
            # true or false  
            
            reason : 失败原因  
            # 仅当 result==false，此值才存在  
            # 1 : 未登陆  
            # 2 : 该读书笔记不存在  
        }  



23.　我的收藏列表  

        请求体 :  
        
        {  
            action_id : 404,  
            
            page_id   : 第几页,  
            # 一开始默认是第一页，此后向后翻页便加一，向前翻页便减一  
            
            page_size : 页面大小  
            # 即这页中客户端希望最多拿到多少条数据  
        }  
        
        响应体 :  
        
        {  
            notes :  
            [  
                {  
                    _id      : 这篇读书笔记的id,  
                    
                    title    : 这篇读书笔记的标题,  
                    
                    own_id   : 这篇读书笔记的所属人的用户名（手机）,  
                    
                    own_nick : 这篇读书笔记的所属人的昵称,  
                    
                    pub_time : 这篇读书笔记的发布时间戳（秒）,  
                    
                    labels   : 这篇读书笔记的标签们,  
                    # 以逗号分隔，形如 "label1,label2,label3"  
                    
                    feel     : 这篇读书笔记的个人感悟  
                },  
                {  
                    另一篇读书笔记的...  
                }  
            ]  
        }  



24.　对读书笔记发表评论 or 对评论发表子评论  

        请求体 :  
        
        {  
            action_id    : 405,  
            
            note_id      : 读书笔记的id,  
            
            note_title   : 读书笔记的标题,  
            
            ancestor_id  : 祖先评论的id,  
            
            content      : 这条评论的内容,  
            
            replyed_nick : 被回复者的昵称,  
            
            recv_ids     : "user_id1,user_id2,user_id3"  
            # 以逗号分隔  
            
            # 若你想要（直接针对读书笔记）评论，则 :  
            # ancestor_id  填 "0"  
            # replyed_nick 填 ""  
            # recv_ids     填 这篇读书笔记的所属人的用户名  
            
            # 若你想要针对该读书笔记下的（某条直系评论）发表子评论，则 :  
            # ancestor_id  填 那条直系评论的id  
            # replyed_nick 填 那条直系评论的评论者的昵称  
            # recv_ids     填 那条直系评论的recv_ids  
            
            # 若你想要针对该读书笔记下的（某条子评论）发表子评论，则 :  
            # ancestor_id  填 那条子评论的ancestor_id  
            # replyed_nick 填 那条子评论的评论者的昵称  
            # recv_ids     填 那条子评论的recv_ids  
        }  
        
        响应体 :  
        
        {  
            result : 是否成功,  
            # true or false  
            
            reason : 失败原因  
            # 仅当 result==false，此值才存在  
            # 1 : 未登陆  
            # 2 : 该读书笔记不存在  
            # 3 : 评论内容为空  
        }  



25.　分页查看与我相关的消息  

        请求体 :  
        
        {  
            action_id : 406,  
            
            page_id   : 第几页,  
            # 一开始默认是第一页，此后向后翻页便加一，向前翻页便减一  
            
            page_size : 页面大小  
            # 即这页中客户端希望最多拿到多少条数据  
        }  
        
        响应体 :  
        
        {  
            messages :  
            [  
                {  
                    who_id     : 对方的用户名,  
                    
                    who_nick   : 对方的昵称,  
                    
                    time       : 时间戳（秒）,  
                    
                    note_id    : 与该消息相关的读书笔记的id,  
                    
                    note_title : 与该消息相关的读书笔记的标题,  
                    
                    action_id  : 消息类型代号,  
                    #  0  : 评论  
                    #  1  : 赞同  
                    #  2  : 取消赞同  
                    #  3  : 反对  
                    #  4  : 取消反对  
                    #  5  : 收藏  
                    #  6  : 取消收藏  
                    #  7  : 关注  
                    #  8  : 取消关注  
                    #  未完待续...  
                    
                    content    : 评论内容  
                    # action_id==0，此值才有意义  
                },  
                {  
                    另一条消息的...  
                }  
            ]  
        }  



26.　关注某人 or 取消关注  

        请求体 :  
        
        {  
            action_id  : 501,  
            
            cared_id   : 被关注者的用户名（手机号）,  
            
            cared_nick : 被关注者的昵称  
        }  
        
        响应体 :  
        
        {  
            result : 是否成功,  
            # true or false  
            
            reason : 失败原因  
            # 仅当 result==false，此值才存在  
            # 1 : 未登陆  
        }  



27.　分页查看我的关注列表  

        请求体 :  
        
        {  
            action_id : 502,  
            
            page_id   : 第几页,  
            # 一开始默认是第一页，此后向后翻页便加一，向前翻页便减一  
            
            page_size : 页面大小  
            # 即这页中客户端希望最多拿到多少条数据  
        }  
        
        响应体 :  
        
        {  
            cares :  
            [  
                {  
                    _id         : 某人的用户名,  
                    
                    nick        : 某人的昵称,  
                    
                    signup_time : 某人的注册时间戳（秒）,  
                    
                    signature   : 某人的读书格言  
                },  
                {  
                    关注的另一个人的...  
                }  
            ]  
        }  


