#-*- coding: utf-8 -*-

import sys, random, math
from operator import itemgetter

random.seed(0)



class ItemBasedCF():
	
	def __init__(self, transet, cvset, testset, n_sim_movie, n_rec_movie, \
	             movie_sim_mat, movie_popular, movie_count):
		self.trainset = {}
		self.testset = {}
		
		self.n_sim_movie = {}
		self.n_rec_movie = {}
		
		self.movie_sim_mat = {}
		self.movie_popular = {}
		self.movie_count = 0
		
		print("Similar movie number = %d" %(self.n_sim_movie),file=sys.stderr)
		print("Recommended movie number = %d" %(self.n_rec_movie),file=sys.stderr)
	
	
	def loadfile(filename):
		fp = open(filename, 'r')
		for i, line in enumerate(fp):
			yield line.strip('\r\n')
			if i % 100000 == 0 :
				print("Loading %s(%s)"%(filename,i),file = sys.stderr)
		fp.close()
		print("load %s success" %(filename),file = sys.stderr)
	
	
	def generate_dataset(self, filename, p1 = 0.6 , p2 = 0.8):
		trainset_len = 0
		cvset_len = 0 
		testset_len = 0
		
		user, movie, rating, _ = line.split('::')#把列表每行数据以：：分割，并储存
												 #到user, movie, rating, _这四个变量当中	
		for line in self.loadfile(filename) :
			if (random.random() < p1):
				self.trainset.setdefault(user,{})#在字典的每个元素里生成一个字典？
                self.trainset[user][movie] = int(rating)#user是大字典trainset的key，
				                                        #同时user也是一个字典，其字典
														#内部的key是movie，把value赋值
														#为int（rating）
                trainset_len += 1

    def calc_movie_sim(self):#检测每部电影一共有多少人评分，字典的key为电影名字，value为评分人数
        ''' calculate movie similarity matrix '''
        print >> sys.stderr, 'counting movies number and popularity...'

        for user, movies in self.trainset.iteritems():
            for movie in movies:
                # count item popularity 
                if movie not in self.movie_popular:
                    self.movie_popular[movie] = 0
                self.movie_popular[movie] += 1  #如果对应movie有人打分，每次累加1

				print >> sys.stderr, 'count movies number and popularity succ'

		# save the total number of movies
		self.movie_count = len(self.movie_popular)
		print >> sys.stderr, 'total movie number = %d' % self.movie_count

        # count co-rated users between items
        itemsim_mat = self.movie_sim_mat
        print >> sys.stderr, 'building co-rated users matrix...'

        for user, movies in self.trainset.iteritems():#生成共现物品矩阵
            for m1 in movies:
                for m2 in movies:#m1,m2均是movies列表里面的电影
                    if m1 == m2: continue #忽略相同项
                    itemsim_mat.setdefault(m1,{})#查找m1，没有的话就返回一个空字典
                    itemsim_mat[m1].setdefault(m2,0)#在m1字典里查找m2，如果没有就返回0
                    itemsim_mat[m1][m2] += 1#在字典m1中的key：m2，其value加1

        print >> sys.stderr, 'build co-rated users matrix succ'

        # calculate similarity matrix 
        print >> sys.stderr, 'calculating movie similarity matrix...'
        simfactor_count = 0
        PRINT_STEP = 2000000
        #计算共现矩阵C的物品余弦相似度
        for m1, related_movies in itemsim_mat.iteritems():
            for m2, count in related_movies.iteritems():#count为m2的value
                itemsim_mat[m1][m2] = count / math.sqrt(
                        self.movie_popular[m1] * self.movie_popular[m2])#计算余弦相似度，相似度公式为：对两部电影都喜欢的人数count除以分别喜欢这两部电影的人数之和；
						#movie_popular[m1]和movie_popular[m2]分别为电影m1、m2的打分人数
						#重新赋值给itemsim_mat
                simfactor_count += 1
                if simfactor_count % PRINT_STEP == 0:#如果计算完20万次相似度计算
                    print >> sys.stderr, 'calculating movie similarity factor(%d)' % simfactor_count

        print >> sys.stderr, 'calculate movie similarity matrix(similarity factor) succ'
        print >> sys.stderr, 'Total similarity factor number = %d' %simfactor_count







	def SplitData(data, M, k, seed):
		test = []
		train = []
		cvset = []
		random.seed(seed)
		for user , itemgetter in data :
			if random.append(0, M) == k :
				test.append([user, item])
			else :
				train.append([user, item])
		return train, test
		
		

		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		