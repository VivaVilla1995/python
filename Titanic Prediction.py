#!/usr/bin/env python
# coding: utf-8

# In[1]:


#读入数据
import pandas                                     #提供数据分析和处理功能
titanic = pandas.read_csv('titanic_train.csv')    
print (titanic.describe())
titanic.head(5)


# In[2]:


#对Age列的缺失值进行填充（用均值）  .fillna
titanic['Age'] = titanic['Age'].fillna(titanic['Age'].median())
print (titanic.describe())


# In[3]:


#Sex这一列都是字符特征，要转换成数值形式表达
print (titanic['Sex'].unique())

titanic.loc[titanic['Sex']=='male','Sex']=0
titanic.loc[titanic['Sex']=='female','Sex']=1


# In[4]:


print (titanic['Embarked'].unique())
titanic['Embarked']=titanic['Embarked'].fillna('S')    #用最多的那个值进行填充
titanic.loc[titanic['Embarked']=='S','Embarked']=0
titanic.loc[titanic['Embarked']=='C','Embarked']=1
titanic.loc[titanic['Embarked']=='Q','Embarked']=2


# In[5]:


#运用机器学习算法，先用最简单的：线性回归
from sklearn.linear_model import LinearRegression    #导入线性回归
from sklearn.model_selection import KFold            #交叉验证
import numpy as np

predictors = ['Pclass','Sex','Age','SibSp','Parch','Fare','Embarked']

alg = LinearRegression()
#n_splits：划分为几等份；shuffle：在每次划分时，是否进行洗牌；random_state：随机种子数
kf = KFold(n_splits=3, shuffle=False, random_state=1) 

predictions = []
for train,test in kf.split(titanic):                                   #kf里边有很多train和test
    train_predictors = (titanic[predictors].iloc[train,:])             #拿到train的数据
    train_target = titanic['Survived'].iloc[train]                     #拿到train数据的标签
    alg.fit(train_predictors,train_target)                             #让数据去fit线性回归模型
    test_predictions = alg.predict(titanic[predictors].iloc[test,:])   #测试结果
    predictions.append(test_predictions)


# In[6]:


#最终想要的是分类的结果(获救率)
import numpy as np

predictions = np.concatenate(predictions, axis=0)

predictions[predictions >.5] =1
predictions[predictions <=.5] =0
accuracy =sum(predictions == titanic["Survived"]) /len(predictions)

print(accuracy)


# In[7]:


#逻辑回归，得到概率值
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
 
alg = LogisticRegression(random_state=1)
scores = cross_val_score(alg, titanic[predictors], titanic["Survived"], cv=3)

print(scores.mean())


# In[8]:


#上面得到的结果都是对交叉验证后的验证集来进行分类，在实际结果中，应该使用测试数据集来进行分类
titanic_test = pandas.read_csv("test.csv")
titanic_test["Age"] = titanic_test["Age"].fillna(titanic["Age"].median())
titanic_test["Fare"] = titanic_test["Fare"].fillna(titanic_test["Fare"].median())
titanic_test.loc[titanic_test["Sex"] == "male", "Sex"] = 0
titanic_test.loc[titanic_test["Sex"] == "female", "Sex"] = 1
titanic_test["Embarked"] = titanic_test["Embarked"].fillna("S")
 
titanic_test.loc[titanic_test["Embarked"] == "S", "Embarked"] = 0
titanic_test.loc[titanic_test["Embarked"] == "C", "Embarked"] = 1
titanic_test.loc[titanic_test["Embarked"] == "Q", "Embarked"] = 2


# In[9]:


#使用随机森林
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestClassifier

predictors = ['Pclass','Sex','Age','SibSp','Parch','Fare','Embarked']
alg = RandomForestClassifier(random_state=1,
                             n_estimators=10,           #树的数目
                             min_samples_split=2,       #最小的切分点
                             min_samples_leaf=1)        #最少的叶子节点个数
kf = KFold(n_splits=3, shuffle=False, random_state=1)
scores = cross_val_score(alg, titanic[predictors], titanic["Survived"], cv=kf)

print(scores.mean())


# In[10]:


#对随机森林模型进行优化（调参）
alg = RandomForestClassifier(random_state=1,
                             n_estimators=50,           #树的数目
                             min_samples_split=4,       #最小的切分点
                             min_samples_leaf=2)        #最少的叶子节点个数
kf = KFold(n_splits=3, shuffle=False, random_state=1)
scores = cross_val_score(alg, titanic[predictors], titanic["Survived"], cv=kf)

print(scores.mean())


# In[11]:


#加入一些新的特征
titanic['FamilySize']=titanic['SibSp']+titanic['Parch']

titanic['NameLength']=titanic['Name'].apply(lambda x:len(x))  #名字长度


# In[12]:


import re

def get_title(name):
    title_search = re.search("([A-Za-z]+)\.", name)
    if title_search:
        return title_search.group(1)
    return ''

titles = titanic["Name"].apply(get_title)
print(pandas.value_counts(titles))

title_mapping = {"Mr": 1, "Miss": 2, "Mrs": 3, "Master": 4, "Dr": 5, "Rev": 6, "Major": 7, "Col": 7, "Mlle": 8, "Mme": 8, "Don": 9, "Lady": 10, "Countess": 10, "Jonkheer": 10, "Sir": 9, "Capt": 7, "Ms": 2}
for k,v in title_mapping.items():
    titles[titles == k] = v
    
print (pandas.value_counts(titles))
titanic['Title']=titles


# In[13]:


#随机森林特征重要性分析
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

predictors = ['Pclass','Sex','Age','SibSp','Parch','Fare','Embarked','FamilySize','Title','NameLength']

selector = SelectKBest(f_classif, k=5)
selector.fit(titanic[predictors], titanic["Survived"])
scores = -np.log10(selector.pvalues_)

plt.bar(range(len(predictors)), scores)
plt.xticks(range(len(predictors)), predictors, rotation='vertical')
plt.show()

predictors = ["Pclass", "Sex", "Fare", "Title"]

alg = RandomForestClassifier(random_state=1, 
                             n_estimators=50, 
                             min_samples_split=8, 
                             min_samples_leaf=4)


# In[15]:


#集成算法
from sklearn.ensemble import GradientBoostingClassifier
import numpy as np

algorithms = [             #两个算法：Boosting和LogisticRegression
    [GradientBoostingClassifier(random_state=1, 
                                n_estimators=25, 
                                max_depth=3), ["Pclass", "Sex", "Age", "Fare", "Embarked", "FamilySize", "Title",]],
    [LogisticRegression(random_state=1), ["Pclass", "Sex", "Fare", "FamilySize", "Title", "Age", "Embarked"]]
]

kf = KFold(n_splits=3, shuffle=False, random_state=1) 

predictions = []
for train,test in kf.split(titanic):
    train_target = titanic["Survived"].iloc[train]
    full_test_predictions = []
    for alg, predictors in algorithms:
        alg.fit(titanic[predictors].iloc[train,:], train_target)
        test_predictions = alg.predict_proba(titanic[predictors].iloc[test,:].astype(float))[:,1]
        full_test_predictions.append(test_predictions)
    test_predictions = (full_test_predictions[0] + full_test_predictions[1]) / 2
    test_predictions[test_predictions <= .5] = 0
    test_predictions[test_predictions > .5] = 1
    predictions.append(test_predictions)

predictions = np.concatenate(predictions, axis=0)

accuracy =sum(predictions == titanic["Survived"]) /len(predictions)
print(accuracy)


# In[ ]:




