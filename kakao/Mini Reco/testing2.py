import os
from evaluation import ndcg
from solution import UserBaseCF
from Case import DataFrame_Matrix
import pandas as pd
number = str(4)
testcase = DataFrame_Matrix(number)
matrix = testcase.matrix
num_users = testcase.num_users
num_items = testcase.num_items
num_sim_user_top_N = testcase.num_sim_user_top_N
num_item_rec_top_N = testcase.num_item_rec_top_N
active_users = testcase.active_users
gts = testcase.gts
#solve
model =UserBaseCF(matrix, num_users, num_items, num_sim_user_top_N, num_item_rec_top_N)
scores = []
for i in range(len(active_users)):
  rec = model.recommend(active_users[i])
  gt = gts[i]
  scores.append(ndcg(gt, rec))

print(f"ndcg 평균 : {(sum(scores) / len(scores))}")