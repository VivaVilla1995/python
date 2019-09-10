#!/usr/bin/env python
# coding: utf-8

# In[1]:


#数据分析的三大件
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


import os 
path = 'LogiReg_data.txt'
pdData = pd.read_csv(path,header=None,names=['Exam 1','Exam 2','Admitted'])
pdData.head()


# In[3]:


pdData.shape


# In[4]:


positive = pdData[pdData['Admitted']==1]
negative = pdData[pdData['Admitted']==0]

fig, ax = plt.subplots(figsize=(10,5))
ax.scatter(positive['Exam 1'], positive['Exam 2'], s=30, c='b', marker='o', label='Admitted')
ax.scatter(negative['Exam 1'], negative['Exam 2'], s=30, c='r', marker='x', label='Not Admitted')
ax.legend()
ax.set_xlabel('Exam 1 Score')
ax.set_ylabel('Exam 2 Score')


# In[5]:


#sigmoid函数：映射到概率
def sigmoid(z):
    return 1/(1+np.exp(-z))


# In[6]:


#展示sigmoid函数
nums = np.arange(-10,10,step=1)
fig,ax = plt.subplots(figsize=(12,4))
ax.plot(nums,sigmoid(nums),'r')


# In[7]:


#插入一列（1），把原来的数值运算转换成矩阵运算
def model(X,theta):
    return sigmoid(np.dot(X,theta.T))

pdData.insert(0,'Ones',1)
orig_data = pdData.as_matrix()
cols = orig_data.shape[1]
X = orig_data[:,0:cols-1]
y = orig_data[:,cols-1:cols]

theta = np.zeros([1,3])    #占位


# In[8]:


X[:5]


# In[9]:


y[:5]


# In[10]:


theta


# In[11]:


X.shape, y.shape, theta.shape


# In[12]:


#计算损失函数
def cost(X,y,theta):
    left = np.multiply(-y,np.log(model(X,theta)))
    right = np.multiply(1-y,np.log(1-model(X,theta)))
    return np.sum(left-right)/len(X)


# In[13]:


cost (X,y,theta)


# In[14]:


#计算梯度
def gradient(X, y, theta):
    grad = np.zeros(theta.shape)
    error = (model(X, theta)- y).ravel()
    for j in range(len(theta.ravel())): #for each parmeter
        term = np.multiply(error, X[:,j])
        grad[0, j] = np.sum(term) / len(X)
    
    return grad


# In[15]:


#比较三种不同梯度下降方法(停止策略)
STOP_ITER = 0
STOP_COST = 1
STOP_GRAD = 2

def stopCriterion(type, value, threshold):
    #设定三种不同的停止策略
    if type == STOP_ITER:        
        return value > threshold
    elif type == STOP_COST:      
        return abs(value[-1]-value[-2]) < threshold
    elif type == STOP_GRAD:      
        return np.linalg.norm(value) < threshold


# In[16]:


#洗牌打乱顺序再重新指定X和y
def shuffleData(data):
    np.random.shuffle(data)
    cols = data.shape[1]
    X = data[:, 0:cols-1]
    y = data[:, cols-1:]
    return X, y


# In[17]:


#时间计算的影响
import time

def descent(data, theta, batchSize, stopType, thresh, alpha):
    #梯度下降求解
    
    init_time = time.time()
    i = 0 # 迭代次数
    k = 0 # batch
    X, y = shuffleData(data)
    grad = np.zeros(theta.shape) # 计算的梯度
    costs = [cost(X, y, theta)] # 损失值

    
    while True:
        grad = gradient(X[k:k+batchSize], y[k:k+batchSize], theta)
        k += batchSize #取batch数量个数据
        if k >= n: 
            k = 0 
            X, y = shuffleData(data) #重新洗牌
        theta = theta - alpha*grad # 参数更新
        costs.append(cost(X, y, theta)) # 计算新的损失
        i += 1 

        if stopType == STOP_ITER:       value = i
        elif stopType == STOP_COST:     value = costs
        elif stopType == STOP_GRAD:     value = grad
        if stopCriterion(stopType, value, thresh): break
    
    return theta, i-1, costs, grad, time.time() - init_time


# In[18]:


#画图显示
def runExpe(data, theta, batchSize, stopType, thresh, alpha):
    #核心代码
    theta, iter, costs, grad, dur = descent(data, theta, batchSize, stopType, thresh, alpha)
    name = "Original" if (data[:,1]>2).sum() > 1 else "Scaled"
    name += " data - learning rate: {} - ".format(alpha)
    if batchSize==n: strDescType = "Gradient"
    elif batchSize==1:  strDescType = "Stochastic"
    else: strDescType = "Mini-batch ({})".format(batchSize)
    name += strDescType + " descent - Stop: "
    if stopType == STOP_ITER: strStop = "{} iterations".format(thresh)
    elif stopType == STOP_COST: strStop = "costs change < {}".format(thresh)
    else: strStop = "gradient norm < {}".format(thresh)
    name += strStop
    
    print ("***{}\nTheta: {} - Iter: {} - Last cost: {:03.2f} - Duration: {:03.2f}s".format(
        name, theta, iter, costs[-1], dur))
    fig, ax = plt.subplots(figsize=(12,4))
    ax.plot(np.arange(len(costs)), costs, 'r')
    ax.set_xlabel('Iterations')
    ax.set_ylabel('Cost')
    ax.set_title(name.upper() + ' - Error vs. Iteration')
    return theta


# In[19]:


#选择的梯度下降方法是基于所有样本的
n=100    #对所有样本进行梯度下降
runExpe(orig_data, theta, n, STOP_ITER, thresh=5000, alpha=0.000001)  #学习率为0.000001


# In[20]:


runExpe(orig_data, theta, n, STOP_COST, thresh=0.000001, alpha=0.001)   #改变策略


# In[21]:


runExpe(orig_data, theta, n, STOP_COST, thresh=0.000001, alpha=0.001)  #学习率为0.000001


# In[22]:


#对比不同的梯度下降方法
runExpe(orig_data, theta, 1, STOP_ITER, thresh=5000, alpha=0.001)  #只迭代一个样本
#非常不稳定，模型不收敛


# In[23]:


runExpe(orig_data, theta, 1, STOP_ITER, thresh=15000, alpha=0.000002)


# In[24]:


runExpe(orig_data, theta, 16, STOP_ITER, thresh=15000, alpha=0.001)  #mini-batch descent


# In[25]:


#进行数据标准化
from sklearn import preprocessing as pp

scaled_data = orig_data.copy()
scaled_data[:, 1:3] = pp.scale(orig_data[:, 1:3])

runExpe(scaled_data, theta, n, STOP_ITER, thresh=5000, alpha=0.001)


# In[33]:


runExpe(scaled_data, theta, n, STOP_GRAD, thresh=0.02, alpha=0.001)
#说明Mini-batch模型是比较合适的


# In[34]:


theta = runExpe(scaled_data, theta, 1, STOP_GRAD, thresh=0.002/5, alpha=0.001)


# In[35]:


runExpe(scaled_data, theta, 16, STOP_GRAD, thresh=0.002*2, alpha=0.001)


# In[36]:


#设定阈值（0.5）
def predict(X, theta):
    return [1 if x >= 0.5 else 0 for x in model(X, theta)]


# In[37]:


scaled_X = scaled_data[:, :3]
y = scaled_data[:, 3]
predictions = predict(scaled_X, theta)
correct = [1 if ((a == 1 and b == 1) or (a == 0 and b == 0)) else 0 for (a, b) in zip(predictions, y)]
accuracy = (sum(map(int, correct)) % len(correct))
print ('accuracy = {0}%'.format(accuracy))


# In[ ]:




