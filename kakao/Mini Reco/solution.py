class Model():
  def __init__(self, matrix, num_users, num_items, num_sim_user_top_N, num_item_rec_top_N):
    self.R = matrix
    self.num_users = num_users
    self.num_items = num_items
    self.num_sim_user_top_N = num_sim_user_top_N
    self.num_item_rec_top_N = num_item_rec_top_N
    self.simil_matrix = self._get_simil_matrix()
    self.null_item_matrix = self._get_null_item_matrix()
    self.mean_matrix = self._get_mean_matrix()
    self.U = self._get_U()
    self.user_rating_items = self._get_rating_item_matrix()

  def _get_Ixy(self, x, y):
    """
    사용자 x, y 모두가 평가한 아이템 집합을 구하는 함수
    """

    Ixy = set()
    for i in range(1, self.num_items+1):
      if self.R[x][i] != None and self.R[y][i] != None:
        Ixy.add(i)
    return Ixy
  
  def _get_I(self, u):
    """
    사용자(u)가 평가한 아이템 집합을 구하는 함수
    """
    I = set()
    for i in range(1, self.num_items+1):
      if self.R[u][i] != None:
        I.add(i)
    return I

  def _simil(self, x, y):
      """
      사용자 x, y의 코사인 유사도를 구하는 함수
      """
      Ixy = self._get_Ixy(x, y)
      Ix = self._get_I(x)
      Iy = self._get_I(y)

      rxi2s = []
      ryi2s = []
      numerator = []
      for i in Ixy:
        rxi = self.R[x][i]
        ryi = self.R[y][i]
        numerator.append((rxi*ryi))
      
      for i in Ix:
        rxi = self.R[x][i]
        rxi2s.append((rxi ** 2))
      
      for i in Iy:
        ryi = self.R[y][i]
        ryi2s.append((ryi ** 2))
      
      numerator = sum(numerator)
      denominator = (sum(rxi2s)**0.5) * (sum(ryi2s) ** 0.5)
      #Cosine similarity 계산이 정의되지 않는 경우
      #zero division error가 나올때
      if denominator == 0:
        return 0
      else:
        return (numerator / denominator)
    
  def _get_simil_matrix(self):
      """
      코사인 유사도 매트릭스를 구하는 함수
      """
      simil_matrix = {}
      for x in range(1,self.num_users+1):
        simil_matrix[x] = {}
        for y in range(1, self.num_users+1):
          simil_matrix[x][y] = None

      for x in range(1, self.num_users+1):
        for y in range(1, self.num_users+1):
          if x == y:
            simil_matrix[x][y] = 1
          else:
            simil_matrix[x][y] = self._simil(x, y)
      return simil_matrix
  def _get_rating_item_matrix(self):
    """
    사용자가 평가한 아이템 매트릭스를 구하는 함수

    """
    matrix = {}
    for u in range(1, self.num_users+1):
      matrix[u] = None
    for u in range(1, self.num_users+1):
      items = set()
      for i in range(1, self.num_items+1):
        if self.R[u][i] != None:
          items.add(i)
      matrix[u] = items
    return matrix

  def _get_null_item_matrix(self):
      """
      사용자가 아직 평가하지 않은 아이템 매트릭스를 구하는 함수
      """
      matrix = {}
      
      for u in range(1,self.num_users+1):
        matrix[u] = None
      
      for u in range(1, self.num_users+1):
        items = set()
        for i in range(1, self.num_items+1):
          if self.R[u][i] == None:
            items.add(i)
        matrix[u] = items
      return matrix
    
  def _get_mean_matrix(self):
      """
      유저의 평균 매트릭스를 구하는 함수
      """
      matrix = {}
      for u in range(1, self.num_users+1):
        values = []
        for i in range(1, self.num_items+1):
          if self.R[u][i] == None:
            pass
          else:
            values.append(self.R[u][i])
        mean = sum(values) / len(values)
        matrix[u] = mean
      return matrix

  def _get_U(self):
    """
    아이템  i 를 평가한 사용자 u와 가장 유사한 상위 N명의 사용자 집합(피어그룹) U 매트릭스를 구하는 함수
    """
    matrix = {}
    
    for u in range(1, self.num_users+1):
      peergroup = []
      sorted_simil_matrix = sorted(self.simil_matrix[u].items(), key = lambda x : x[1], reverse=True)
      for i in range(1, len(sorted_simil_matrix)):
        user = sorted_simil_matrix[i][0]
        peergroup.append(user)
      matrix[u] = peergroup[:self.num_sim_user_top_N]

    return matrix
  def _get_k(self, u):
    sum_value = 0
    for u_prime in self.U[u]:
      sum_value += abs(self.simil_matrix[u][u_prime])
    #식 (1)에서 normalizing factor  k  값이 정의되지 않은 경우에는 0으로 정의
    #zero division error가 나올때
    if sum_value == 0:
      return 0
    else:
      return (1 / sum_value)

  def _get_rui(self, u, i):
    ru = self.mean_matrix[u]
    k = self._get_k(u)

    sum_value = 0
    for u_prime in self.U[u]:
      r_uprime_i = self.R[u_prime][i]
      r_uprime_bar = self.mean_matrix[u_prime] 
      if r_uprime_i == None:
        sum_value += 0
      else:
        sum_value += self.simil_matrix[u][u_prime] * (r_uprime_i - r_uprime_bar)

    return ru + (k * sum_value)
  
  def recommend(self,u):
    null_items = self.null_item_matrix[u]
    u_prime_rating_items = set()
    recommendation = []
    for u_prime in self.U[u]:
      u_prime_rating_items = u_prime_rating_items.union(self.user_rating_items[u_prime])
    recom_items = null_items.intersection(u_prime_rating_items)
    
    result = []
    for i in recom_items:
      rui = self._get_rui(u, i)
      result.append([i, rui])

    result.sort(key=lambda x : x[1], reverse=True)

    for i in range(len(result)):
      item = result[i][0]
      recommendation.append(item)
    if len(recommendation) < self.num_item_rec_top_N:
      self.num_item_rec_top_N = len(recommendation) 
    return recommendation[:self.num_item_rec_top_N]

