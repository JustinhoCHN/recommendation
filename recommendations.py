
from math import sqrt

#以下是数据集
critics = {
'Lisa Rose':{
			'Lady in the Water' : 2.5,
			'Snake on a Plane' : 3.5,
			'Just My Luck' : 3.0,
			'Superman Returns' : 3.5,
			'You, Me and Dupree' : 2.5,
			'The Night Listener' : 3.0
			} ,
'Gene Seymour' : {
				'Lady in the Water' : 3.0
				'Snake on a Plane' : 3.5,
				'Just My Luck' : 1.5,
				'Superman Returns' : 5.0,
				'The Night Listener' : 3.0,
				'You, Me and Dupree' : 3.5
					},
'Michael Phillips':{
				'Lady in the Water' : 2.5,
				'Snake on a Plane' : 3.0,
				'Superman Returns' : 3.5,
				'The Night Listener' : 4.0
				},		
'Claudia Puig':{
				'Snake on a Plane' : 3.5,
				'Just My Luck' : 3.0,
				'The Night Listener' : 4.5,
				'Superman Returns' : 4.0,
				'You, Me and Dupree' : 2.5
				},
'Mick LaSalle':{
				'Lady in the Water' : 3.0,
				'Snake on a Plane' : 4.0,
				'Just My Luck' : 2.0,
				'Superman Returns' : 3.0,
				'The Night Listener' : 3.0,
				'You, Me and Dupree' : 2.0
				},
'Jack Matthews':{
				'Lady in the Water' : 3.0,
				'Snake on a Plane' : 4.0,
				'The Night Listener' : 3.0,
				'Superman Returns' : 5.0,
				'You, Me and Dupree' : 3.5
				},
'Toby':{
		'Snake on a Plane' : 4.5,
		'You, Me and Dupree' : 1.0,
		'Superman Returns' : 4.0
		}			
}

#基于欧几里得距离的相似度评价函数，计算两用户间的相似度
def sim_distance(prefs, person1, person2):
	#得到shared_items的列表
	si = {} #"si" = "Share Items"
	#若用户1中的物品也出现在用户2的物品列表中，则返回1
	for item in prefs[person1]:
		if item in prefs[person2]:
			si[item] = 1
	#若两者无共同之处，返回0
	if len(si) == 0: return 0
	
	#计算所有差值的平方和，用欧几里得距离公式求出在两个用户的共有物品内，两两物品间的相似度，
	#然后求总和，即为此两名用户间的相似度。
	sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item],2)] 
							for item in prefs[person1] if item in prefs[person2])
	return 1 / (1 + sqrt(sum_of_squares))

#皮尔逊相关系数，计算两用户间的相似度
def sim_pearson(prefs,p1,p2):
  # Get the list of mutually rated items
  si={}
  for item in prefs[p1]: 
    if item in prefs[p2]: si[item]=1

  # if they are no ratings in common, return 0
  if len(si)==0: return 0

  # Sum calculations
  n=len(si)
  
  # Sums of all the preferences
  sum1=sum([prefs[p1][it] for it in si])
  sum2=sum([prefs[p2][it] for it in si])
  
  # Sums of the squares
  sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
  sum2Sq=sum([pow(prefs[p2][it],2) for it in si])	
  
  # Sum of the products
  pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])
  
  # Calculate r (Pearson score)
  num=pSum-(sum1*sum2/n)
  den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
  if den==0: return 0

  r=num/den

  return r	
	
#返回用户最佳匹配，匹配结果数量n和相似度函数similarity函数为可选项，可用欧几里得相似度函数
#或者皮尔逊相关系数函数。
def topMatches(prefs,person,n=5,similarity=sim_pearson):
  scores=[(similarity(prefs,person,other),other) #求出该名用户与其他用户间的相似度，储存在列表中
                  for other in prefs if other!=person]
  scores.sort() 
  scores.reverse() #对该用户与其它用户的相似度列表进行倒序排名
  return scores[0:n] #返回相似对最高的前n个用户，格式为：[(相似度，用户1)，...]

#基于用户的协同过滤算法来推荐物品
def getRecommendations(prefs, person, similarity = sim_pearson):
	totals = {} #建立一个字典，用于存放每部电影的评分总计值
	simSums = {} #建立一个字典，用于存放该用户与其他人的相似度总和
	for other in prefs:
		if other == person : #跟除自己以外的人比较
			continue
		sim = similarity(prefs, person, other)#用相似度函数计算与其他用户的相似度
		
		if sim <= 0 : continue #忽略相似度低于等于0的用户
		for item in prefs(other) :
			#只计算该用户还未看过的电影分数（有可能是不在用户评分的列表中，或者在列表中评分为0的项目）
			if item not in prefs[person] or prefs[person][item] == 0;
				#计算（该用户与其他人的相似度sim）乘以（对应用户评分）
				totals.setdefault(item, 0)#在totals字典内生成item key
				totals[item] += prefs[person][item] * sim 
				#计算该用户对所有人的相似度总和
				simSums.setdefault(item, 0)#在simSums字典内生成item key
				simSums += sim
	
	#总计值除以总相似度，返回一个列表，格式：[(总计值除以总相似度,物品名1），...]
	rankings = [((total)/simSums[item],item) for item, total in totals.items()]
	
	#返回一个经排序的列表，总计值除以总相似度，实际上是预测该用户可能对这部电影的评分
	rankings.sort()
	rankings.reverse()
	return rankings

#用户和物品的转换
def transformPrefs(prefs):
  result={}
  for person in prefs:
    for item in prefs[person]:
      result.setdefault(item,{})
      
      # Flip item and person
      result[item][person]=prefs[person][item]
  return result

	
#基于物品的协同过滤算法#
def calculateSimilarItems(prefs,n=10):
	result = {}#给出与该物品最为相似的其它物品的字典，格式为：[(物品名，相似度)]
	#以物品为中心对偏好矩阵实施倒置处理
	itemPrefs = transformPrefs(prefs)#调用transformPrefs函数
	c = 0 
	for item in itemPrefs:
		c += 1
		if c % 100 == 0 :
			print("%d / %d " % (c, len(itemPrefs)))
		scores = topMatches(itemPrefs, item, n = n, similarity = sim_distance)
		result[item] = scores
	return result

#对该名用户提供基于物品的推荐
def getRecommendedItems(prefs, itemMatch, user):
	userRatings = prefs[user]#读取出该用户的评分列表
	scores = {}#字典格式：{item1:val1,item2:val2,...}
	totalSim = {}#字典格式同上
	
	for (item,rating) in userRatings.items():
		
		for (similarity, item2) in itemMatch[item] :#itemMatch为item与其它物品间的相似度similarity的字典
			#格式为：{item1:[(sim1,other),...],item2:[(sim1,other),...]，...}，相当于上面的返回的result。
			
			#忽略已评分的项目
			if item2 in userRatings: continue
			
			#计算两物品间的加权分值：sim * rating，保存于scores字典中
			scores.setdefault(item2, 0)
			scores[item2] += similarity * rating
			
			totalSim.setdefault(item2, 0)
			totalSim[item2] += similarity
		
	rankings = [(score/totalSim[item],item) for item,score in scores.items()]
	#对该用户返回一个排序的推荐列表，格式为[(预测评分值，物品名字)，...]
	rankings.sort()
	rankings.reverse()
	return rankings

#以下为获取movielens数据集
def loadMovieLens(path='/data/movielens'):
  # Get movie titles
  movies={}
  for line in open(path+'/u.item'):
    (id,title)=line.split('|')[0:2]
    movies[id]=title
  
  # Load data
  prefs={}
  for line in open(path+'/u.data'):
    (user,movieid,rating,ts)=line.split('\t')
    prefs.setdefault(user,{})
    prefs[user][movies[movieid]]=float(rating)
  return prefs






















	
	
	
	
	
	
