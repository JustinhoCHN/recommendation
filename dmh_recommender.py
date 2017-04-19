from math import sqrt
#提取txt内客户阅读内容标签信息，格式为字典，user_tag_train = {users:{tags:times},...}
user_tag_train = {}
#生成物品矩阵
itemsim_mat = {}
item_dict = {}
def itemmat(user_tag_train):
	for user, tags in user_tag_train.items():
		for tag in tags:
# count item popularity 
			if tag not in item_dict:
			item_dict[tag] = 0
			item_dict[tag] += 1

	num_of_tags = len(item_dict)

	print('Number of tags is %s'%(num_of_tags))
	print('标签总数为：%s'%(num_of_tags)+ '\r\n' + '\r\n')		

	
#生成共现矩阵
def commonmat(user_tag_train，item_dict,simfactor_count = 1):
	for user, tags in user_tag_train.items():#生成共现物品矩阵
		for t1 in tags:
			for t2 in tags:#t1，t2均是tags列表里面的标签
				if t1 == t2: continue #忽略相同项
				itemsim_mat.setdefault(t1,{})#查找t1，没有的话就返回一个空字典
				itemsim_mat[t1].setdefault(t2,0)#在t1字典里查找t2，如果没有就返回0
				itemsim_mat[t1][t2] += 1#对字典t1中的key：t2，其value加1
	print('Itemsim_mat is generated')
	print('已生成物品共现矩阵' + '\r\n' + '\r\n')
	
	#计算物品相似度（用余弦相似度）
	for t1, related_movies in itemsim_mat.items():
		for t2, count in related_movies.items():#count为m2的value
			itemsim_mat[t1][t2] = count / math.sqrt(item_dict[t1] * item_dict[t2])
			#计算余弦相似度，相似度公式为：对两个物品都喜欢的人数count除以分别喜欢这两个物品的人数之和；
			#item_dict[t1]和item_dict[t2]分别为喜欢物品t1、t2的人数
			#重新赋值给itemsim_mat
			simfactor_count += 1
	print('Calculate item similarity completed.Simfactor_count is %s'%(simfactor_count))
	print('计算余弦相似度完成，物品相似对数为%s对'%(simfactor_count) + '\r\n' + '\r\n')


#获得推荐
def recommend(user,k,n):
	#k为与每个物品相似的物品数
	#n为给每个用户推荐的物品数
	rank = {}
	user_tag = user_tag_train[user]

	for tag in user_tag:
		for related_tag, sim in sorted(itemsim_mat[tag].items(),
			key=itemgetter(1), reverse = True)[:k]:
			if related_tag in user_tag : continue
			rank.setdefault(related_movie, 0)
			rank[related_movie] += sim
        # return the N best movies
	
	print('The top N best recommended items are : ')
	print('推荐给用户前N个最可能感兴趣的物品为：')
	return sorted(rank.items(), key=itemgetter(1), reverse = True)[:n]
	

user_tag_train = 
item_dict = itemmat(user_tag_train)
itemsim_mat = commonmat(user_tag_train，item_dict,simfactor_count = 1)
recommend_list = recommend(user, k, n)
