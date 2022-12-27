import os
from evaluation import ndcg
from solution import UserBaseCF
import pandas as pd
number = str(4)
base_input_path = os.getcwd()+'\\kakao\Mini Reco\\testcase\input'
base_output_path = os.getcwd()+'\\kakao\Mini Reco\\testcase\output'
input_file = f'input00{number}.txt'
output_file = f'output00{number}.txt'

#input
input_path = os.path.join(base_input_path, input_file)
f = open(input_path, 'r')
lines = f.readlines()
num_sim_user_top_N = int(lines[0].strip())
num_item_rec_top_N = int(lines[1].strip())
num_users = int(lines[2].strip())
num_items = int(lines[3].strip())
num_rows  = int(lines[4].strip())

#matrix 초기화
matrix = pd.DataFrame()

for line in lines[5:num_rows+5]:
  data = line.strip().split()
  u = int(data[0])
  i = int(data[1])
  rating = float(data[2])
  matrix.loc[u, i] = rating
  
num_reco_users = lines[num_rows+5]
active_users = []
for line in lines[num_rows+6:]:
  user = int(line.strip())
  active_users.append(user)
  
f.close()
# output
output_path = os.path.join(base_output_path, output_file)
f = open(output_path, 'r')
lines = f.readlines()
gts = []
for line in lines:
  gt = list(map(int,line.strip().split()))
  gts.append(gt)
f.close()

#solve
model =UserBaseCF(matrix, num_users, num_items, num_sim_user_top_N, num_item_rec_top_N)
scores = []
for i in range(len(active_users)):
  rec = model.recommend(active_users[i])
  gt = gts[i]
  scores.append(ndcg(gt, rec))

print(f"ndcg 평균 : {(sum(scores) / len(scores))}")