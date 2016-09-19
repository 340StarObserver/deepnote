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
            
            signup_time : 该用户的注册时间戳,  
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
            
            signup_time : 那人的注册时间戳,  
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
            
            type        : 这篇读书笔记的分类名,  
            
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
            pub_time : 这篇新的读书笔记的发布时间戳  
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
                    
                    type     : 这篇读书笔记的分类名,  
                    
                    own_id   : 这篇读书笔记的所属人的用户名（手机）,  
                    
                    own_nick : 这篇读书笔记的所属人的昵称,  
                    
                    pub_time : 这篇读书笔记的发布时间戳,  
                    
                    labels   : 这篇读书笔记的标签们,  
                    # 以逗号分隔，形如 "label1,label2,label3"  
                    
                    feel     : 这篇读书笔记的个人感悟  
                },  
                {  
                    另一篇读书笔记的...  
                }  
            ]  
            # 读书笔记列表  
        }  



13.　修改某篇读书笔记  

        请求体 :  
        
        {  
            action_id   : 203,  
            
            token       : 之前获得的令牌,  
            
            note_id     : 你想修改的那篇读书笔记的id,  
            
            type        : 新的分类名,  
            
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
                    _id      : 这篇读书笔记的id,  
                    
                    title    : 这篇读书笔记的标题,  
                    
                    type     : 这篇读书笔记的分类名,  
                    
                    own_id   : 这篇读书笔记的所属人的用户名（手机）,  
                    
                    own_nick : 这篇读书笔记的所属人的昵称,  
                    
                    pub_time : 这篇读书笔记的发布时间戳,  
                    
                    labels   : 这篇读书笔记的标签们,  
                    # 以逗号分隔，形如 "label1,label2,label3"  
                    
                    feel     : 这篇读书笔记的个人感悟  
                },  
                {  
                    另一篇读书笔记的...  
                }  
            ]  
            # 你的全部的读书笔记的概要信息  
            # 仅当 result==true，此值才存在  
        }  


