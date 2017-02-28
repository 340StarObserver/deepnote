## python规范 ##
<br/>


### 缩进 & 空行 ###

> 统一使用4个空格，而不是tab，来缩进  

> 比较长的一行代码，使用行延续 \ 来分成多行，短行符应在操作符之前，且分行后要缩进，例如：  

            if num is 1 or num is 2 \
                or num is 3 \
                or num is 4:
                dosomething()
            else:
                doother()

> 类与类之间，全局函数与类之间，全局函数与全局函数之间，用两个空行来分离  

> 类内的成员函数用一个空行分离  

> 类声明与第一个成员函数or第一个成员变量之间用一个空行分离  

> 在函数内使用空行时，最好仅用于表示相对独立的一个代码段  

<br/>


### 命名 ###

> 模块名用小写  

> 常量用大写，多单词用下划线连接，若是全局常量以下划线开头  

> 变量用小写，多单词用下划线连接  

> 类中的私有变量，用两个下划线开头  

> 函数名的命名规范与变量相同  

<br/>


### import ###

> import语句放在文件开头，位于模块注释和文件注释之后，位于该文件内的全局变量和常量之前  

> 每个import独占一行，即不要出现 import module1,module2 的写法  

> import的顺序最好按照　标准库导入 -> 第三方库导入 -> 自己的库导入　的顺序，三者之间用空行隔开  

<br/>


### 代码语句 ###

> 在二元运算符的两边各放置一个空格，例如： = , == , < , > , is , in , and , or , not。例如：  
>> x = 1  
>> i += 1  
>> c = (a + b) * (c + d)  
>> 注意，一般函数的参数列表里的多个参数之间，不要加空格  

> 等值比较最好用 is , is not 来做，例如 if xxx is None， if xxx is not True  

> 不要在循环中用 + 或 += 来连接字符串，这样会多出很多临时对象
>> 应将各子串加入列表，在循环结束后用join来连接列表  

> 使用字符串格式化来代替字符串拼接  

> 执行主程序之前检查 if __name__=='__main__'  

<br/>


### 注释 ###

> 修改代码后，不要忘记修改对应的注释  

> 注释用英文书写，推荐用完整的句子或易于理解的短语  

> 注释以 # 和一个空格开头  

> 慎用行内注释，所谓行内注释是代码和注释位于同一行，例如  i += 1  # increase i  

> 为公共模块，函数，类方法编写文档字符串  
>> 如果是函数或类方法的文档字符串，位于def的下一行  
>> 文档字符串的第一行是概括性的描述，然后是一个空行，接着是详细描述，例如：  

            def help():
                """
                print the usage of this command and the format of command(总述)
                
                detail information(详述)
                """
                print "xxxx"

> 

<br/>


### 文件开头规范示例 ###

    #!/usr/bin/python
    # -*- coding:utf-8 -*-
    
    # Author           : Lv Yang
    # Created          : 17 July 2016
    # Last Modified    : 17 July 2016
    # Version          : 1.0
    
    """
    introduction of this script file
    """
    
    import 标准库
    
    import 第三方库
    
    import 自己的库

<br/>
