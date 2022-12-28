import os
import pandas as pd
class TestCase():
  def __init__(self, number, type_='Dict'):
    number = str(number)
    base_input_path = os.getcwd()+'\\kakao\Mini Reco\\testcase\input'
    base_output_path = os.getcwd()+'\\kakao\Mini Reco\\testcase\output'
    input_file = f'input00{number}.txt'
    output_file = f'output00{number}.txt'

    #input
    input_path = os.path.join(base_input_path, input_file)
    f = open(input_path, 'r')
    lines = f.readlines()
    self.num_sim_user_top_N = int(lines[0].strip())
    self.num_item_rec_top_N = int(lines[1].strip())
    self.num_users = int(lines[2].strip())
    self.num_items = int(lines[3].strip())
    num_rows  = int(lines[4].strip())

    #matrix 초기화
    if type_ == 'Dict':
      self.matrix = {}
      for u in range(1,self.num_users+1):
        self.matrix[u] = {}
        for i in range(1, self.num_items+1):
          self.matrix[u][i] = None

      for line in lines[5:num_rows+5]:
        data = line.strip().split()
        u = int(data[0])
        i = int(data[1])
        rating = float(data[2])
        self.matrix[u][i] = rating
    elif type_ == 'DataFrame':
      self.matrix = pd.DataFrame()
  
      for line in lines[5:num_rows+5]:
        data = line.strip().split()
        u = int(data[0])
        i = int(data[1])
        rating = float(data[2])
        self.matrix.loc[u, i] = rating

    for line in lines[5:num_rows+5]:
      data = line.strip().split()
      u = int(data[0])
      i = int(data[1])
      rating = float(data[2])
      self.matrix[u][i] = rating
      
    num_reco_users = lines[num_rows+5]
    self.active_users = []
    for line in lines[num_rows+6:]:
      user = int(line.strip())
      self.active_users.append(user)
      
    f.close()
    # output
    output_path = os.path.join(base_output_path, output_file)
    f = open(output_path, 'r')
    lines = f.readlines()
    self.gts = []
    for line in lines:
      gt = list(map(int,line.strip().split()))
      self.gts.append(gt)
    f.close()