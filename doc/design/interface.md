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




















