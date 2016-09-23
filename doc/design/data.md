## 一. 数据库设计 ##


### 1-1. 用户数据 user_info ###

        位于 ： mongodb  
        
        架构 ： 复制集  
        
        索引 ： { _id : 1 }  

        {  
            _id               : 手机号,  
            
            password          : 密码的MD5的加密密文,  
            
            nick              : 昵称,  
            
            head              : 头像的完整链接地址,  
            # 该数据是虚数据（实际不存在该项），它由手机号就可以唯一确定  
            # 例如 http://deepnote.oss-cn-shanghai.aliyuncs.com/user_head/13915497202.jpg  
            # 若加载图片失败，就使用默认图片  
            
            signup_time       : 注册时间戳,  
            
            signature         : 读书格言  
        }  


### 1-2. 读书笔记的基本信息部分 note_base ###

        位于 : mongodb  
        
        架构 : 复制集  
        
        索引 : { _id : 1 }, { own_id : 1, pub_time : -1 }, { pub_time : -1 }  

        {  
            _id          : mongodb自动生成的随机字符串,  
            
            title        : 读书笔记的标题,  
            
            own_id       : 所属用户的用户名（手机号）,  
            
            own_nick     : 所属用户的昵称,  
            
            pub_time     : 发布时间戳（最后一次修改的时候）,  
            
            feel         : 我的感悟,  
            
            labels       : "label1,label2,label3"  
            # 标签列表，用逗号分隔  
        }  



### 1-3. 读书笔记的扩展信息部分 note_extra ###

        位于 : mongodb  
        
        架构 : 复制集  
        
        索引 : { _id : 1 }  

        {  
            _id          : 对应读书笔记的基本信息部分（note_base）的_id,  
            
            source_link  : 原文链接,  
            
            source_ref   : 引用原文段落,  
            
            agree_num    : 赞同数,  
            
            oppose_num   : 反对数,  
            
            collect_num  : 收藏数,  
            
            comment_num  : 评论数  
        }  



### 1-4. 读书笔记的分词部分 note_word ###

        位于 : elasticsearch  
        
        架构 : cluster  
        
        索引 : 全文索引  

        {  
            _id          : 对应读书笔记的基本信息部分（note_base）中的_id,  
            
            title        : 读书笔记的标题,  
            # 需要使用ik分词器进行 粗粒度 的分词  
            
            source_ref   : 引用原文段落,  
            # 需要使用ik分词器进行 细粒度 的分词  
            
            feel         : 我的感悟,  
            # 需要使用ik分词器进行 细粒度 的分词  
            
            labels       : "label1,label2,label3"  
            # 标签列表，以逗号分隔  
            # 需要使用ik分词器进行 细粒度 的分词  
        }  


### 1-5. 读书笔记的赞同反对记录  note_action ###

        位于 : mongodb  
        
        架构 : 复制集  
        
        索引 : { user_id : 1, note_id : 1 }  

        {  
            _id          : mongodb自动生成的随机字符串,  
            
            user_id      : 某人的用户名（手机）,  
            
            note_id      : 对应读书笔记的基本信息部分（note_base）中的_id,  
            
            action_type  : 行为类型  
            #  0  :  赞同  
            #  1  :  反对　　
            #  未完待续...  
        }  


### 1-6. 读书笔记的收藏记录 note_collect ###

        位于 : mongodb  
        
        架构 : 复制集  
        
        索引 : { user_id : 1, time : -1 }  

        {  
            _id          : mongodb自动生成的随机字符串,  
            
            user_id      : 某人的用户名（手机）,  
            
            time         : 收藏时刻的时间戳,  
            
            note_id      : 对应读书笔记的基本信息部分（note_base）中的_id  
        }  


### 1-7. 评论记录表 comment_record ###

        位于 : mongodb  
        
        架构 : 复制集  
        
        索引 : { note_id : 1, ancestor_id : 1, time : -1 }  
        
        {  
            _id          : 这条评论的id（由mongodb自动生成）,  
            
            note_id      : 对应读书笔记的基本信息部分（note_base）中的_id,   
            
            ancestor_id  : 祖先评论的id,  
            
            time         : 这条评论的时间戳,  
            
            content      : 这条评论的内容,  
            
            send_id      : 评论者的用户名（手机）,  
            send_nick    : 评论者的昵称,  
            
            replyed_nick : 被回复者的昵称,  
            
            recv_ids     : [ user_id1, user_id2, ... ]  
            # 消息接受者的用户名列表  
            # 它表示如果之后有谁回复这条评论，那么哪些人会收到消息  
            
            # 若这条评论是针对读书笔记的 :  
            #     ancestor_id   为 "0"  
            #     replyed_nick  为 ""  
            #     recv_ids      为 [ 这篇读书笔记的所有者的id, 此评论者的id ]  
            
            # 若这条评论是针对某条评论的 :  
            #     ancestor_id   为那条评论的祖先的_id，即 :  
            #         if 那条评论是表层评论（ancestor_id == "0"），则这条评论的ancestor_id取那条评论的_id  
            #         if 那条评论是内层评论（ancestor_id != "0"），则这条评论的ancestor_id取那条评论的ancestor_id  
            #     replyed_nick  为你要回复的那条评论的用户昵称  
            #     recv_ids      为那条评论的recv_ids加上你的id  
        }  


### 1-8. 与我相关的消息表 message_record ###

        位于 : mongodb  
        
        架构 : 复制集  
        
        索引 : { user_ids : 1, time : -1 }  

        {  
            _id        : mongodb自动生成的随机字符串,  
            
            user_ids   : 与谁相关，他们的用户名列表,  
            # 形如 [ user_id1, user_id2, ... ]  
            
            time       : 时间戳,  

            who_id     : 对方的用户名,   
            who_nick   : 对方的昵称,  
            
            note_id    : 和哪一篇读书笔记相关（读书笔记的基本信息部分的_id）,   
            note_title : 和哪一篇读书笔记相关（笔记标题）,  
            
            action_id  : 行为代号,  
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
            # 为了方便客户端解析，当action_id不等于0的时候，此值为""  
        }  


### 1-9. 关注表 care_record ###

        位于 : mongodb  
        
        架构 : 复制集  
        
        索引 : { carer_id : 1, time : -1 }  
        
        {  
            _id        : mongodb自动生成的随机字符串,  
            
            carer_id   : 关注者的用户名,  
            
            time       : 在什么时候关注的（时间戳）,  
            
            cared_id   : 被关注者的用户名,  
            
            cared_nick : 被关注者的昵称  
        }  

