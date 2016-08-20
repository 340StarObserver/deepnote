## 一. 数据库设计 ##


### 1-1. 用户数据 user_info ###

        位于 ： mongodb  
        
        架构 ： 复制集  
        
        索引 ： { _id : 1 }  

        {  
            _id               : 用户名,  
            
            password          : 密码的MD5加密密文,  
            
            signup_time       : 注册时间,  
            # 形如 xxxx-xx-xx  
            
            head              : 头像链接地址,  
            # 链接到对象存储  
            
            invite_code       : 邀请码,  
            
            invite_code_limit : 该邀请码的剩余使用次数,  
            # 用户每次修改邀请码的时候，自动变为一个定值，而后每次别人用你的邀请码注册，该值就减一  
            # 为零时，该邀请码不可用  
            
            note_collect      : [ note_id1, note_id2, note_id3, ... ]  
            # 我的笔记收藏列表，内部每个元素都是一篇读书笔记的id  
            # 默认为 [ ]  
        }  


### 1-2. 读书笔记的概要信息部分 note_overview ###

        位于 : mongodb  
        
        架构 : 复制集  
        
        索引 : { _id : 1 }, { own_user : 1 }, { pub_time : -1 }  

        {  
            _id          : mongodb自动生成的随机字符串,  
            
            title        : 读书笔记的标题,  
            
            type         : 分类名,  
            
            own_user     : 所属用户的用户名,  
            
            own_head     : 所属用户的头像链接,  
            
            public       : 是否公开（true of false）,  
            
            pub_time     : 发布时间（形如 2016-08-07 16:35）,  
            
            feel         : 我的感悟,  
            
            labels       : "label1,label2,label3"  
            # 标签列表，用逗号分隔  
        }  


### 1-3. 读书笔记的细节信息部分 note_detail ###

        位于 : mongodb  
        
        架构 : 复制集  
        
        索引 : { note_id : 1 }, { own_user : 1 }  

        {  
            _id          : mongodb自动生成的随机字符串,  
            
            note_id      : 对应读书笔记的概要信息部分的_id,  
            
            own_user     : 我的用户名,  
            
            source       : 原文出处,  
            
            source_link  : 原文链接,  
            
            ref          : 引用原文段落,  
            
            agree_num    : 赞同数,  
            
            oppose_num   : 反对数,  
            
            collect_num  : 收藏数,  
            
            comment_num  : 评论数,  
            
            all_comments :  
            [  
                {  
                    id        : "kdafi4",  
                    parent_id : "0",  
                    who_user  : "seven",  
                    who_head  : a url,  
                    time      : 1445599887,  
                    content   : "the first comment"  
                },  
                {  
                    id        : "dfajeg",  
                    parent_id : "kdafi4",  
                    who_user  : "shangyang",  
                    who_head  : a url,  
                    time      : 1461288776,  
                    content   : "the second comment"  
                }  
            ]  
            # 全部评论，其中每条评论 :  
            # id        是该条评论的id，通过时间戳和评论者用户名的联合哈希计算得到  
            # parent_id 是该条评论的父评论的id，若为"0"则表示该评论是针对笔记的，否则是针对parent_id所代表的那条评论  
            # who_user  是该条评论的评论者的用户名  
            # who_head  是该条评论的评论者的头像链接  
            # time      是该条评论的时间戳  
            # content   是该条评论的内容  
            # 这样一来，评论便可嵌套  
        }  


### 1-4. 读书笔记的分词部分 note_word ###

        位于 : elasticsearch  
        
        架构 : cluster  
        
        索引 : 全文索引  

        {  
            _id          : 对应读书笔记的概要信息部分中的_id,  
                        
            public       : 是否公开（true of false）,  
            
            popularity   : 热度,  
            
            title        : 读书笔记的标题,  
            # 需要使用ik分词器进行 粗粒度 的分词  
            
            source       : 原文出处,  
            # 需要使用ik分词器进行 粗粒度 的分词  
            
            ref          : 引用原文段落,  
            # 需要使用ik分词器进行 细粒度 的分词  
            
            feel         : 我的感悟,  
            # 需要使用ik分词器进行 细粒度 的分词  
            
            labels       : "label1,label2,label3",  
            # 标签列表，以逗号分隔  
            # 需要使用ik分词器进行 细粒度 的分词  
        }  


### 1-5. 读书笔记的赞同反对记录表 note_action ###

        位于 : mongodb  
        
        架构 : 复制集,  
        
        索引 : { note_id : 1, user : 1, action_id : 1 }  

        {  
            _id       : mongodb自动生成的随机字符串,  
            
            note_id   : 对应读书笔记的概要信息部分的_id,  
            
            user      : 发起动作的用户名,  
            
            action_id : 行为代号  
            # 0 代表 赞同  
            # 1 代表 反对  
            # 使用整数，而不是bool值，以便将来扩展其他行为  
        }  


### 1-6. 与我相关的消息表 about_me ###

        位于 : mongodb  
        
        架构 : 复制集,  
        
        索引 : { username : 1, time : -1 }  

        {  
            _id        : mongodb自动生成的随机字符串,  
            
            username   : 与谁相关（他的用户名）,  
            
            time       : 时间戳,  

            who_user   : 对方的用户名,  
            
            who_head   : 对方的头像链接,  
            
            note_id    : 和哪一篇读书笔记相关（读书笔记的概要信息部分的_id）,  
            
            note_title : 和哪一篇读书笔记相关（笔记标题）,  
            
            action_id  : 行为代号,  
            # 0 代表赞同  
            # 1 代表反对  
            # 2 代表收藏  
            # 3 代表评论  
            
            content    : 评论内容  
            # action_id==3，此值才有意义  
            # 为了方便客户端解析，当action_id不等于3的时候，此值为""  
        }  



## 二. 缓存设计 ##

### 2-1. 最新评论提醒缓存 ###

        评论的缓存池  : redis  
        
        缓存的 key   : 关于谁，那个人的用户名  
        
        缓存的 value :  
        
        [  
            '{ "id" : 相关的笔记id, "title" : 笔记标题, "who" : 谁回复了我, "head" : 回复我的人的头像链接, "time" : 时间, "content" : 内容 }',  
            '{ "id" : 相关的笔记id, "title" : 笔记标题, "who" : 谁回复了我, "head" : 回复我的人的头像链接, "time" : 时间, "content" : 内容 }'  
        ]  
        # value内部的每个元素是一个json形式的字符串  

        # 首先，把最新评论放在缓存中，加快了查询的速度  
        # 其次，摒弃了之前由客户端每隔一定时间轮询服务器的做法，采用捎带应答机制，在用户做其他请求的时候，顺带去查一下缓存  
        # 每次查缓存，都要把关于这个人的最新评论缓存清空  

