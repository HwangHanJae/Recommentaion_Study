class Model():
  def __init__(self, matrix, num_users, num_items, num_sim_user_top_N, num_item_rec_top_N):
    self.R = matrix
    self.num_users = num_users
    self.num_items = num_items
    self.num_sim_user_top_N = num_sim_user_top_N
    self.num_item_rec_top_N = num_item_rec_top_N
    self.simil_matrix = self._get_simil_matrix()
    

  def _get_I(self, x=None, y=None):
    """
    사용자가 평가한 아이템 집합을 구하는 함수
    """
    I = set()
    #사용자 x,y 모두가 평가한 아이템 집합
    if x != None and y != None:
      for i in range(1, self.num_items+1):
        if self.R[x][i] != None and self.R[y][i] != None:
          I.add(i)
      return I
    #사용자 x가 평가한 아이템집합
    elif x != None and y == None:
      for i in range(1, self.num_items+1):
        if self.R[x][i] != None:
          I.add(i)
      return I
    #사용자 y가 평가한 아이템집합
    elif x == None and y != None:
      for i in range(1, self.num_items+1):
        if self.R[y][i] != None:
          I.add(i)
      return I
    
  def _simil(self, x, y):
      """
      사용자 x, y의 코사인 유사도를 구하는 함수
      """
      Ixy = self._get_I(x, y)
      Ix = self._get_I(x, y=None)
      Iy = self._get_I(x=None, y=y)
      rxi2s = []
      ryi2s = []
      a = 0
      for i in Ixy:
        rxi = self.R[x][i]
        ryi = self.R[y][i]
        a += (rxi * ryi)
      
      for i in Ix:
        rxi = self.R[x][i]
        rxi2s.append(rxi ** 2)
      
      for i in Iy:
        ryi = self.R[y][i]
        ryi2s.append(ryi ** 2)
      
      b = (sum(rxi2s)**0.5) * (sum(ryi2s) ** 0.5)
      
      return (a / b)
    
  def _get_simil_matrix(self):
      """
      코사인 유사도 매트릭스를 구하는 함수
      """
      simil_matrix = {}
      for x in range(1,self.num_users+1):
        simil_matrix[x] = {}
        for y in range(1, self.num_users+1):
          simil_matrix[x][y] = 0

      for x in range(1, self.num_users+1):
        for y in range(1, self.num_users+1):
          if x == y:
            simil_matrix[x][y] = 1
          else:
            try :
              simil_matrix[x][y] = self._simil(x, y)
            except:
              simil_matrix[x][y] = 0
      return simil_matrix
    
  def _get_null_item_idx(self, user_id):
      """
      사용자가 아직 평가하지 않은 아이템의 인덱스 구하는 함수
      """
      indexs = []
      for i in self.R[user_id]:
        if self.R[user_id][i] == None:
          indexs.append(i)
      return indexs
    
  def _get_mean(self,user_id):
      """
      유저의 평균을 구하는 함수
      """
      lst = []
      for i in self.R[user_id]:
        if self.R[user_id][i] != None:
          lst.append(self.R[user_id][i])
      return sum(lst) / len(lst)
  def _get_U(self, user_id):
    sorted_simil_matrix = sorted(self.simil_matrix[user_id].items(), key = lambda x : x[1], reverse=True)
    peergroup = []
    for i in range(1, len(sorted_simil_matrix[:self.num_sim_user_top_N+1])):
      user_id = sorted_simil_matrix[i][0]
      simil = sorted_simil_matrix[i][1]
      peergroup.append(user_id)
    return peergroup
  def _get_k(self, user_id):
    U = self._get_U(user_id)
    k = 0
    try:
      for u_prime in U:
        k += abs(self._simil(user_id, u_prime))
      k = (1 / k)
    except:
      k = 0
    return k, U

  def recommend(self, user_id):
    item_ids = self._get_null_item_idx(user_id)
    k, U = self._get_k(user_id)
    ru = self._get_mean(user_id)
    result = []
    simil = 0
    for u_prime in U:
      simil += self._simil(user_id,u_prime)
    for u_prime in U:
      sum_value = 0
      # 사용자에게 추천해야 하는 아이템들
      for i in item_ids:
        #실제값이 None인 값들 
        if self.R[u_prime][i] == None:
          pass
        #실제값이 None이 아닌 값들
        else:
          result.append([i, ru+(k *simil*(self.R[u_prime][i] - self._get_mean(u_prime)))])
    
    if len(item_ids) < self.num_item_rec_top_N:
      self.num_item_rec_top_N = len(item_ids)

    result_dic = {}
    for item, rating in result:
      result_dic[item] = result_dic.get(item, 0) + rating
    sorted_result = sorted(result_dic.items(), key=lambda x: x[1], reverse=True)[:self.num_item_rec_top_N]
    
    recommendation = [item for item, rating in sorted_result]
    
    return recommendation
    
