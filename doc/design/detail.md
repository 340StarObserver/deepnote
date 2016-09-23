### 详细设计 ###




001.　服务端架构（未引入用户行为分析）  

                           nginx  
                             |  
        ---------------------------------------------  
        |              |            |               |  
        server1     server2      server3      server4  
        
        
        应用层  
                 |                         |  
        ---------------------------------------------  
                 |                         |  
        数据层  
        
               mongo主               elasticsearch1  
                 |                         |  
        -------------------          elasticsearch2  
        |     |     |     |  
        从1   从2   从3   仲裁  
        
        # 引入用户行为分析后，需要加入 spark & hadoop  




002.　服务端工厂模式下的业务处理  

        各种业务的处理器类 :  
        
        class XXX_Handler :  
            def __init__(self,post_data,post_files,usr_sessions,server_conf):  
                self._post_data = post_data  
                self._post_files = post_files  
                self._usr_sessions = usr_sessions  
                self._server_conf = server_conf  
            def perform(self):  
                # 业务处理  
                # 最后统一返回一个dict  
        
        对外的工厂类 :  
        
        class Handler_Factory :  
            @staticmethod  
            def get_handler(handler_id,post_data,post_files,usr_sessions,server_conf):  
                # 根据 handler_id 创建并返回对应的对象  




101.　安卓端配置类的封装  

        a. 静态单例对象  
        
        b. 配置文件中包含 :  
            b1. 统一的服务端请求地址，例如 http://ip:port/action  
            b2. 用户的头像的前缀地址，例如 http://deepnote.oss-cn-shanghai.aliyuncs.com/user_head/  
            b3. 请求超时时间限制  
            b4. 其他客户端里出现频率较高的一些数据  
        
        c. 该单例在被创建的时候需要是线程安全的（创建后是只读的，所以对象创建后无需关心线程安全问题），形如 :  
        
            public class BaseConf {  
                private static BaseConf _instance = new BaseConf();  
                // 该静态成员在类加载的时候就被创建了，所以创建它的时候是线程安全的  
                
                private BaseConf() {  
                // 此处读取配置文件  
                }  
                
                public static BaseConf getInstance() {  
                    return _instance;  
                }  
            }  




102.　安卓端的读书笔记草稿的封装  

        a. 包含 :  
            state           这篇草稿的状态  
            id              这篇草稿的id  
            time            这篇草稿的时间戳（秒）  
            title           这篇草稿的标题  
            labels          这篇草稿的标签们（以逗号分隔）  
            source_link     这篇草稿的原文链接  
            source_ref      这篇草稿的原文引用  
            feel            这篇草稿的个人感悟  
            
            # 若这篇草稿是尚未提交过的，则 :  
            # state = 1  
            # id     由客户端自己生成并保证唯一性  
            # time   是客户端写这篇草稿时候的时间戳  
            # 之后提交是发起（创建读书笔记）的请求  
            
            # 若这篇草稿是你修改了某篇已发布的读书笔记，但是还未提交此次修改or修改请求失败，而暂存在草稿区，则 :  
            # state = 2  
            # id     是之前从服务端那里获得的这篇读书笔记的id  
            # time   是客户端修改这篇草稿时候的时间戳  
            # 之后提交是发起（更新读书笔记）的请求  




103.　安卓端的已发布读书笔记的封装  

        a. 包含 :  
            id              这篇读书笔记的id  
            title           这篇读书笔记的标题  
            own_id          这篇读书笔记的所属人的用户名  
            own_nick        这篇读书笔记的所属人的昵称  
            pub_time        这篇读书笔记的发布时间戳  
            labels          这篇读书笔记的标签们，以逗号分隔  
            source_link     这篇读书笔记的原文链接  
            source_ref      这篇读书笔记的原文引用  
            feel            这篇读书笔记的个人感悟  




104.　安卓端的本地数据库管理器的封装  

        a. 封装了数据库的名称，各表的表名，数据库的版本等基本信息  
        
        b. 静态单例对象，形如 :  
        
            public class DbManger {  
                private static DbManager _instance = new DbManger();  
                // 该静态成员在类加载的时候就被创建了，所以创建它的时候是线程安全的  
                
                private DbManger() {  
                // 此处创建连接，检查库和各表是否存在，不存在则创建并初始化  
                }  
                
                public static DbManger getInstance() {  
                    return _instance;  
                }  
            }  
        
        c. 使用该单例对象做CURD操作时，需要加入同步控制以保证线程安全  
        
        
        d. 能够将用户信息（见201，除了sessionid & token）持久化（插入or更新）到本地数据库中  
        
        e. 能够从本地数据库中读取用户的信息  
        
        
        f. 能够将一篇读书笔记草稿（见102）持久化（插入or更新）到本地数据库中  
        
        g. 能够根据草稿id，获取本地数据库中的某篇草稿  
        
        h. 能够根据草稿id，删除本地数据库中的某篇草稿  
        
        i. 能够按照时间降序，并分页地查出若干篇草稿  
        
        
        j. 能够将一篇自己的已发布读书笔记（见103）持久化（插入or更新）到本地数据库中  
        
        k. 能够根据已发布读书笔记的id，获取本地数据库中的某篇笔记  
        
        l. 能够根据已发布读书笔记的id，删除本地数据库中的某篇笔记  
        
        m. 能够按照时间降序，并分页地查出若干篇自己的已经发布的读书笔记  
        
        
        n. 能够清空本地数据库  
        
        o. 能够将多个已发布的读书笔记一次性批量地插入到本地数据库中  




105.　安卓端浏览自己的草稿笔记  

        a. 总的是按照时间降序，分页地浏览  
        
        b. 每页中的若干篇草稿，也是按照时间降序排列的  
        
        c. 能够向后翻页，向前翻页  
        
        d. 在各种机型上显示效果良好  




106.　安卓端线上阅读时的笔记模板的快速一键生成  

        a. 通过选中一段原文，弹出一个控件，点击它，即跳转到我们的应用上，自动把引用的原文填上  
        
        b. 开一个线程，根据引用的原文，模拟一个请求，发给百度高级搜索，从前5个结果中随机挑一个链接地址作为原文链接  




107.　安卓端线下阅读时的笔记模板的快速一键生成  

        a. 把原文拍照，使用Ocr云识别的SDK，发请求给Ocr云端获取识别结果，作为引用的原文  
        
        b. 发送上述请求后，有个过渡动画  




201.　用户数据的封装  

        a. 包含 :  
            手机号  
            密码的md5加密  
            昵称  
            注册时间戳  
            读书格言  
            sessionid  
            下一次敏感操作的令牌token  
        
        b. 静态单例对象（写法仿照前面的几个单例）  
        
        c. 因为用户数据是存在修改操作的，所以在使用这个单例调用方法时，不管是读还是写，都要进行同步控制  




202.　安卓端的工厂模式下的JsonParser  

        a. 基础的抽象类 JsonParser  
        
            public abstract class JsonParser {  
            
                public void parse( String json, Object obj ){  
                    // 解析json，并把数据记录到obj对象中  
                }  
            }  
        
        b. 举个例子，用来解析登陆的 LoginJsonParser  
        
            public class LoginJsonParser extends JsonParser {  
            
                public void parse( String json, Object obj ){  
                    // 首先解析json  
                    
                    // 强制类型转换（当然调用的时候，实参需要填LoginData对象）  
                    LoginData res = LoginData(obj);  
                    
                    // 把解析后的相关数据记录到该对象中  
                    res.setResult(true);  
                    res.setNick("seven");  
                    res.setTime(1445599887);  
                }  
            }  
        
        c. 工厂类 JsonParserFactory  
        
            public class JsonParserFactory {  
                
                public static JsonParser produce(int action_id){  
                    // 根据 action_id 的值，创建对应的XXXJsonParser，并返回  
                }  
            }  




203.　登陆时的注意事项  

        a. 登陆之前（不管是第一次登陆，还是自动登陆），需要先发送一个请求，来获取公钥  
        
        b. 登陆成功后，要把返回信息记录到单例的用户对象中  
        
        c. 如果是第一次登陆 :  
            c1. 需要把用户信息持久化到本地数据库中  
            c2. 需要紧接着发送同步数据（加载自己所有的读书笔记）的请求（注意事项见于304）  
            c3. 从第二次登陆开始，都是直接读取本地数据库中的信息，然后自动登陆  




301.　发布读书笔记时的注意事项  

        a. 发起发布一篇新的读书笔记的请求的时候，要有个过渡动画  
        
        b. 服务端不仅要保存这篇读书笔记，还要使用Elasticsearch为其做分词和全文索引  
        
        c. 若请求成功 :  
            将这篇读书笔记插入到本地数据库的已发布笔记表中  
            从本地数据库的草稿表中删除这篇笔记（如果有的话）  
        
        d. 若请求失败 :  
            弹出控件，提示用户是否要把这篇读书笔记保存（若原来就有则是更新）到本地数据库的笔记草稿表中  




302.　查看某人的读书笔记列表的注意事项  

        a. 若是查别人的读书笔记列表 :  
            通过发送请求（interface.md中action_id=12的那个）  
        
        b. 若是查自己的读书笔记列表 :  
            客户端直接查本地数据库  
            分页地查询，且页与页之间是按照时间降序的，且每页上的若干篇读书笔记也是按照时间降序的  
        
        c. 可以向前翻页，也可以向后翻页  
        
        d. 在各机型上显示效果良好  




303.　修改读书笔记时的注意事项  

        a. 发起修改一篇读书笔记的请求的时候，要有个过渡动画  
        
        b. 服务端不仅要更新这篇读书笔记，还要使用Elasticsearch重新为其做分词和全文索引  
        
        c. 若请求成功 :  
            将这篇读书笔记更新到本地数据库的已发布笔记表中  
            从本地数据库的草稿表中删除这篇笔记（如果有的话）  
        
        d. 若请求失败 :  
            弹出控件，提示用户是否要把这篇读书笔记保存（若原来就有则是更新）到本地数据库的笔记草稿表中  




304.　同步自己的读书笔记时的注意事项  

        a. 当第一次登陆 且 登陆成功后，需要发送同步读书笔记的请求  
        
        b. 发送请求后，需要有个过渡动画  
        
        c. 请求成功后 :  
            先清空本地数据库中的已发布笔记表  
            再把请求获得的多篇笔记一次性插入到已发布笔记表中  
            再停止过渡动画  




401.　分页浏览所有读书笔记时的注意事项  

        a. 它是首页，并且进首页后默认是请求第一页的数据  
        
        b. 可以向前翻页，也可以向后翻页  
        
        c. 不论向前向后，都是发送请求，即不要暂存以前翻过的页面的数据  
        
        d. 在第一页上，可以下拉刷新，它会刷新第一页的数据  
        
        e. 当请求某页的时候，若发现返回读书笔记的个数为零，则提示已经是最后一页了  
        
        f. 在各机型上显示效果良好  




402.　根据一句话来搜索读书笔记的注意事项  




