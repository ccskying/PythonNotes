# python3中有6个标准数据类型：数字，字符串，列表，元组，集合，字典
# python3 has 6 variables: number, string, list, tuple, set, dictionary
# 数字分int float bool complex
# 在python中，bool是一个单独的数据类型

# python 的 print 在结束时会自动换行，不需要多写一个 \n,除非希望获得一个空行

# 赋值
a = b = 1
a, b, c = 2, 2, 'char'
# b = 3 , d = 5 这样是不行的
b = 3
d = 5

#########################################
# 数字类型的计算
print("数字\n")
# 除法与c++不同
# 产生浮点数的商
print(d / b)
# 产生整数的商
print(d // b)
# 取余与c++相同
print(d % b)
# 乘法与c++相同
print(d * b)
# 多了一个乘方
print(d ** b)

# python加入了复数运算，复数的实部和虚部都是浮点类型
e = 3 + 3.14j
print(e)
print(e + d)


###################################
# python中的字符串，部分操作与c++类似
print("\n\n字符串\n")
# 与 C 字符串不同的是，Python 字符串不能被改变。向一个索引位置赋值，比如word[0] = 'm'会导致错误
# 0表示第一个字符，-1表示倒数第1个字符
st = 'Runoob'

print(st)  # 输出字符串
print(st[0:-1])  # 输出第1个之后，到倒数第1个之前，的所有字符
print(st[-1:])  # 输出倒数第1个之后，的字符
print(st[0])  # 输出字符串第一个字符
print(st[2:5])  # 输出从第三个开始到第五个的字符
print(st[2:])  # 输出从第三个开始的后的所有字符
print(st * 2)  # 输出字符串两次
print(st + "TEST")  # 连接字符串

# Python 使用反斜杠(\)转义特殊字符，可以在字符串前面添加一个 r，表示原始字符串

print('Ru\noob')
print(r'Ru\noob')

# 反斜杠可以作为续行符，表示下一行是这一行的延续，不能直接用在print中
strtest = 'hello'\
    'world'
print(strtest)

print(strtest[0], strtest[5])
print(strtest[-1], strtest[-6])


#####################################
# List（列表） 是 Python 中使用最频繁的数据类型。
print("\n\nlist\n")
# 列表可以完成大多数集合类的数据结构实现。列表中元素的类型可以不相同，它支持数字，字符串甚至可以包含列表（所谓嵌套）。
# 列表是写在方括号 [] 之间、用逗号分隔开的元素列表。
# 和字符串一样，列表同样可以被索引和截取，列表被截取后返回一个包含所需元素的新列表。
# 直接用print输出列表，会打印包括[],''在内的所有分隔符

lst = ['abcd', 786, 2.23, 'runoob', 70.2]
tinylist = [123, 'runoob']
#create a lista = [1,2]
lista = []
lista.append(2)

print(lst)  # 输出完整列表
print(lst[0])  # 输出列表第一个元素
print(lst[1:3])  # 从第二个开始输出到第三个元素
print(lst[2:])  # 输出从第三个元素开始的所有元素
print(tinylist * 2)  # 输出两次列表
print(lst + tinylist)  # 连接列表

# 与 字符串 不一样的是，列表中的元素是可以改变的：

lst_a = [1, 2, 3, 4, 5, 6]
print("lst_a = ")
print(lst_a)
lst_a[0] = 9
lst_a[2:5] = [13, 14, 15]
print(lst_a)

############################################
# 元组（tuple）与列表类似，不同之处在于元组的元素不能修改。元组写在小括号(())里，元素之间用逗号隔开。
print("\n\ntuple\n")
# 元组中的元素类型也可以不相同
# 元组与字符串类似，可以被索引且下标索引从0开始，-1 为从末尾开始的位置。也可以进行截取
# 其实，可以把字符串看作一种特殊的元组。

tuple = ('abcd', 786, 2.23, 'runoob', 70.2)
tinytuple = (123, 'runoob')

print(tuple)  # 输出完整元组
print(tuple[0])  # 输出元组的第一个元素
print(tuple[1:3])  # 输出从第二个元素开始到第三个元素
print(tuple[2:])  # 输出从第三个元素开始的所有元素
print(tinytuple * 2)  # 输出两次元组
print(tuple + tinytuple)  # 连接元组


##################################
# 集合（set）是一个无序不重复元素的序列。
print("\n\nset\n")
# 基本功能是进行成员关系测试和删除重复元素。
# 可以使用大括号 { } 或者 set() 函数创建集合
# 注意：创建一个空集合必须用 set() 而不是 { }，因为 { } 是用来创建一个空字典。

# 空集合示例
NullSet = set()
print(NullSet)
print(type(NullSet))

student = {'Tom', 'Jim', 'Mary', 'Tom', 'Jack', 'Rose'}

print(student)  # 输出集合，重复的元素被自动去掉

# 成员测试
if ('Rose' in student):
    print('Rose 在集合中')
else:
    print('Rose 不在集合中')

# set可以进行集合运算
set_a = set('abracadabra')
set_b = set('alacazam')

print(set_a)

print(set_a - set_b)  # a和b的差集

print(set_a | set_b)  # a和b的并集

print(set_a & set_b)  # a和b的交集

print(set_a ^ set_b)  # a和b中不同时存在的元素











