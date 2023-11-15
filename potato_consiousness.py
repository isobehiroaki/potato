import matplotlib.pyplot as plt
import numpy as np

#パラメータ
# ポテトへの意識の初期値
C0 = 85.0
# ポテトの本数
pmax = 80.0
# シミュレーションの繰り返し回数
Nmax = 640
# 食べたポテト量の刻み値
dp = pmax / Nmax

# 飽きによる意識の減少項
fed_up1 = -3.0
fed_up2 = -5.0

# 残り本数による意識の上昇項
nokori_amp = 50.0 # 振幅
pnokori_th = pmax - 20.0 #発動のしきい値

# バーガー食べるなど途中のインタラプションによる上昇項1
bg1_pth = pmax * 0.25  # ポテトを25%食べた時に発動すると仮定
bg1_ppk = bg1_pth + 4.0 # インタラプション効果のピークの位置
bg1_psg = 2.0 # 継続時間に相当するポテト本数（ガウシアンの幅）
bg1_amp = 15.0

# バーガー食べるなど途中のインタラプションによる上昇項2
bg2_pth = pmax * 0.60  # ポテトを60%食べた時に発動すると仮定
bg2_ppk = bg2_pth + 3.0 # インタラプション効果のピークの位置
bg2_psg = 1.0 # 継続時間に相当するポテト本数（ガウシアンの幅）
bg2_amp = 20.0

e_p = [0]
c_p = [C0]

e_p_b = 0
c_p_b = C0
for n in range(1,Nmax):
  #eの更新
  e_p_n = e_p_b + dp
  e_p.append(e_p_n)

  #pの更新

  # 飽きの効果
  fed_up = fed_up2 + (fed_up1 - fed_up2) * (pmax - e_p_b)/pmax

  # 残り本数による効果の項の計算
  if e_p_b > pnokori_th:
    nokori = nokori_amp
  else:
    nokori = 0

  # バーガー食べるなど途中のインタラプション効果1
  bg1=0
  if e_p_b >=bg1_pth:
    bg1 = bg1_amp * np.exp(- (e_p_b - bg1_ppk)**2 / bg1_psg**2)

  bg2=0
  if e_p_b >=bg2_pth:
    bg2 = bg2_amp * np.exp(- (e_p_b - bg2_ppk)**2 / bg2_psg**2)

  dc = (fed_up + bg1 + bg2 + nokori/(pmax - e_p_b)**0.8)*dp

  #100に近づいたときの理性の抗力
  if c_p_b >= 90:
    if dc >= 0:
      dc = dc * ((100-c_p_b)/10.0)**2
  c_p_n = c_p_b + dc

  # 意識は0以下にならない
  if c_p_n < 0:
    c_p_n = 0.0


  c_p.append(c_p_n)

  #更新
  e_p_b = e_p_n
  c_p_b = c_p_n

# グラフ描画
fig, ax = plt.subplots()
ax.plot(e_p, c_p)
ax.set_xlabel('Number of eaten potato')
ax.set_ylabel('Consiousness of potato (%)')
plt.show()
