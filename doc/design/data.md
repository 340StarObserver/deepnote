## 一. 数据库设计 ##


### 1-1. 用户数据表 user_info ###

        位于 ： mongodb  
        
        片键 ： { username : hashed }  
        
        索引 ： { username : hashed }  

        {  
            "_id"               : mongodb自动生成的随机字符串,  
            
            "username"          : 用户名,  
            
            "password"          : 密码的MD5加密密文,  
            
            "signup_time"       : 注册时间,  
            // 形如 xxxx-xx-xx  
            
            "head"              : 头像图片的base64编码（默认为系统头像的base64编码）,  
            
            "invite_code"       : 邀请码,  
            
            "invite_code_limit" : 该邀请码的剩余使用次数,  
            // 用户每次修改邀请码的时候，自动变为一个定值，而后每次别人用你的邀请码注册，该值就减一  
            // 为零时，该邀请码不可用  
            
            "note_collect"      : [ note_id1, note_id2, note_id3, ... ]  
            // 我的笔记收藏列表，内部每个元素都是一篇读书笔记的id  
            // 默认为 [ ]  
        }  


### 1-2. 读书笔记表 note_info ###

        位于 : elasticsearch  
        
        片键 : { _id : hashed }  

        {  
            "_id"          : elasticsearch自动生成的随机字符串,  
            
            "title"        : 读书笔记的标题,  
            // 需要使用ik分词器进行 粗粒度 的分词  
            
            "type"         : 分类名,  
            
            "user"         : 所属用户的用户名,  
            
            "public"       : 是否公开（true of false）,  
            
            "pub_time"     : 发布时间（形如 2016-08-07 16:35）,  
            
            "source"       : 原文出处,  
            // 需要使用ik分词器进行 粗粒度 的分词  
            
            "source_link"  : 原文链接,  
            
            "ref"          : 引用原文段落,  
            // 需要使用ik分词器进行 细粒度 的分词  
            
            "feel"         : 我的感悟,  
            // 需要使用ik分词器进行 细粒度 的分词  
            
            "labels"       : [ label1, label2, label3, ... ],  
            // 标签列表  
            // 需要使用ik分词器进行 细粒度 的分词  
            
            "agree_num"    : 赞同数,  
            
            "oppose_num"   : 反对数,  
            
            "collect_num"  : 收藏数,  
            
            "read_num"     : 阅读数,  
            
            "comment_num"  : 评论数,  
            
            "all_comments" :  
            [  
                {  
                    "id"        : "kdafi4",  
                    "parent_id" : "0",  
                    "commenter" : "seven",  
                    "time"      : 1445599887,  
                    "content"   : "the first comment"  
                },  
                {  
                    "id"        : "dfajeg",  
                    "parent_id" : "kdafi4",  
                    "commenter" : "shangyang",  
                    "time"      : 1461288776,  
                    "content"   : "the second comment"  
                }  
            ]  
            // 全部评论，其中每条评论 :  
            // id        是该条评论的id，通过时间戳和评论者用户名的联合哈希计算得到  
            // parent_id 是该条评论的父评论的id，若为"0"则表示该评论是针对笔记的，否则是针对parent_id所代表的那条评论  
            // commenter 是该条评论的评论者的用户名  
            // time      是该条评论的时间戳  
            // content   是该条评论的内容  
            // 这样一来，评论便可嵌套  
        }  


### 1-3. 读书笔记的赞同反对记录表 note_action ###

        位于 : mongodb  
        
        片键 : { _id : hashed }  
        
        索引 : { note_id : 1, user : 1 }  

        {  
            "_id"       : mongodb自动生成的随机字符串,  
            
            "note_id"   : 对应读书笔记的_id,  
            
            "user"      : 发起动作的用户名,  
            
            "action_id" : 行为代号  
            // 0 代表 赞同  
            // 1 代表 反对  
            // 使用整数，而不是bool值，以便将来扩展其他行为  
        }  


--------------------------------------------------


## 二. 消息设计 ##

### 2-1. 阅读消息 ###

        消息池       : kafka  
        
        消息的topic  : read_msg  
        
        消息的 key   : 无  
        
        消息的 value : 对应的读书笔记的_id  

        // 大量的阅读请求，不可能对每个请求都实时地更新笔记的阅读数  
        // 而且阅读数这个属性，只要有百分之九十的准确度就行  
        // 所以，使用 kafka 来作为消息缓冲，每当请求阅读一篇读书笔记，只要很快速地向kafka写入一条消息  
        // 消息的消费端，每隔一定时间，去拿出相当多的消息，再去批量更新数据库  


--------------------------------------------------


## 三. 缓存设计 ##

### 3-1. 最新评论提醒缓存 ###

        评论的缓存池  : redis  
        
        缓存的 key   : 关于谁，那个人的用户名  
        
        缓存的 value :  
        
        [  
            '{ "id" : 相关的笔记id, "title" : 笔记标题, "who" : 谁回复了我, "time" : 时间, "content" : 内容 }',  
            '{ "id" : 相关的笔记id, "title" : 笔记标题, "who" : 谁回复了我, "time" : 时间, "content" : 内容 }'  
        ]  
        // value内部的每个元素是一个json形式的字符串  

        // 首先，把最新评论放在缓存中，加快了查询的速度  
        // 其次，摒弃了之前由客户端每隔一定时间轮询服务器的做法，采用捎带应答机制，在用户做其他请求的时候，顺带去查一下缓存  
        // 每次查缓存，都要把关于这个人的最新评论缓存清空  
