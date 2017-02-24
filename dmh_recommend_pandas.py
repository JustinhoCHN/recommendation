import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances

# 建立pandas矩阵，x_index为item名字，y_index为用户ID
# 用户阅读列表格式假设为：all_user_items = {user1:{item1:1, item2:1, ...}, user2:{item1:1, item2:1, ...}, ...}
# item的value为1，表示是该用户阅读过这篇文章，但未阅读过的文章不在字典内。

all_user_items = {'alice': {'A': 1, 'B': 1},
                  'bob': {'A': 1, 'C': 1, 'D': 1},
                  'cindy': {'B': 1, 'E': 1, 'F': 1},
                  'danny': {'A': 1, 'D': 1},
                  'evens': {'C': 1, 'D': 1, 'E': 1},
                  'fancy': {'A': 1, 'C': 1, 'E': 1},
                  'gary': {'F': 1, 'G': 1}
                  }


# 生成物品列表item_list
def create_item_list(items):
    i_list = []
    for user in items:
        for item in items[user]:
            if item not in i_list:
                i_list.append(item)
    return i_list


# 生成用户列表user_list
def create_user_list(items):
    u_list = []
    for user in items:
        u_list.append(user)
    return u_list


# 建立用户-物品矩阵(user_item_matrix，缩写为uim）
def create_uim(items, num_users, num_items, u_list, i_list):
    uim = pd.DataFrame(np.zeros((num_users, num_items)), index=u_list, columns=i_list)
    for user in items:
        for item in items[user]:
            uim.loc[user, item] = 1
    return uim


# 预测某一用户会喜欢相似度最大的前k个物品
def create_data(username, num_items, i_list, items):
    item_vector = pd.DataFrame(np.zeros((1, num_items), dtype=int), index=[username], columns=i_list)
    for item in items[username]:
        item_vector.loc[:, item] = 1
    return item_vector


def predict(data, similarity, k):  # k为推荐物品数量
    pred = data.dot(similarity) / np.array([np.abs(similarity).sum(axis=1)])
    p = pred.sort_index(axis=1, ascending=False)
    return p.T[0:k]

# 生成用户列表、文章列表
user_list = create_user_list(all_user_items)
item_list = create_item_list(all_user_items)
print('User list is %s' % user_list)
print('\r\n')
print('Item list is %s' % item_list)
print('\r\n')

# 计算用户数量、文章数量
n_users = len(user_list)
n_items = len(item_list)
print('Number of users is %s' % n_users)
print('Number of items is %s' % n_items)
print('\r\n')

# 生成用户-文章矩阵
user_item_matrix = create_uim(all_user_items, n_users, n_items, user_list, item_list)
print('User_Item_matrix is generated')
print('\r\n')

# 使用sklearn库计算用户-文章矩阵的余弦相似度
item_similarity = pd.DataFrame(pairwise_distances(user_item_matrix.T, metric='cosine'),
                               index=item_list, columns=item_list)
print('Item similarity is calculated')
print('\r\n')
print(item_similarity)
print('\r\n')

# 为alice推荐文章
udata = create_data('alice', n_items, item_list, all_user_items)
recommend = predict(udata, item_similarity.T, 3)
print('The recommend item list is : %s' % recommend)
