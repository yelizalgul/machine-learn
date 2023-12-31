#special_data_analysis.ipynb

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
df = sns.load_dataset("titanic")

def check_df(dataframe, head=5):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head(head))
    print("##################### Tail #####################")
    print(dataframe.tail(head))
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.describe([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(df)

#Kategorik Değişken Analizi (Analysis of Categorical Variables)

df["survived"].value_counts()

df["sex"].unique()

df["class"].nunique()

cat_cols=[col for col in df.columns if str(df[col].dtypes) in ["category","object","bool"]]

cat_cols

num_but_cat=[col for col in df.columns if df[col].nunique()<10 and df[col].dtypes in ["int","float"]]

num_but_cat

cat_but_car=[col for col in df.columns if df[col].nunique()>20 and str(df[col].dtypes) in ["category", "object"]]

cat_but_car

cat_cols = cat_cols + num_but_cat

cat_cols

cat_cols=[col for col in cat_cols if col not in cat_but_car]

df[cat_cols].nunique()

[col for col in df.columns if col not in cat_cols]

# Sayısal Değişken Analizi (Analysis of Numerical Variables)

num_cols=[col for col in df.columns if df[col].dtypes in ["int","float"]]

num_cols

num_cols = [col for col in num_cols if col not in cat_cols]

num_cols

def catch_col(dataframe, cat_th=10 , car_th=20):
  """
  Veri Seti içindeki kategorik, nümerik ve varsa kardinal değişkenleri ayıklar

  Parameters
  -------------------------

  dataframe: değişkenlerin bylunduğu data

  cat_th: int, float
          nümerik fakat kategorik değişkenler için eşik değer
  car_th: int ,float
          kategorik fakat kardinal değişkenler için eşik değer

  Returns
  ----------------------------

  cat_cols:

  num_cols:

  cat_but_car:

  note
  --------------------------
  toplam değişken sayısı= cat_cols + num_cols + cat_but_car.

  """


  cat_cols = [col for col in dataframe.columns if str(dataframe[col].dtypes) in ["category", "object", "bool"]]

  num_but_cat = [col for col in dataframe.columns if dataframe[col].nunique() < 10 and dataframe[col].dtypes in ["int", "float"]]

  cat_but_car = [col for col in dataframe.columns if dataframe[col].nunique() > 20 and str(dataframe[col].dtypes) in ["category", "object"]]

  cat_cols = cat_cols + num_but_cat
  cat_cols = [col for col in cat_cols if col not in cat_but_car]

  num_cols = [col for col in dataframe.columns if dataframe[col].dtypes in ["int", "float"]]
  num_cols = [col for col in num_cols if col not in cat_cols]


  print(f"Observations: {dataframe.shape[0]}")
  print(f"Variables: {dataframe.shape[1]}")
  print(f'cat_cols: {len(cat_cols)}')
  print(f'num_cols: {len(num_cols)}')
  print(f'cat_but_car: {len(cat_but_car)}')
  print(f'num_but_cat: {len(num_but_cat)}')

  return cat_cols, num_cols, cat_but_car

cat_cols,num_cols,cat_but_car=catch_col(df)

df = sns.load_dataset("titanic")

for col in df.columns:
    if df[col].dtypes == "bool":
        df[col] = df[col].astype(int)

cat_cols, num_cols, cat_but_car = catch_col(df)

def summary(dataframe, col_name, plot=False):
  print(pd.DataFrame({col_name:dataframe[col_name].value_counts(),
                      "Ratio":100*dataframe[col_name].value_counts()/len(dataframe)}))
  print('--------------------------------------------------------------')

  if plot:
    sns.countplot(x=dataframe[col_name], data=dataframe)
    plt.show(block=True)

summary(df, "survived")

summary(df,"survived", plot=True)

def target_summary_cat(dataframe, target, categorical_col):
    print(pd.DataFrame({"TARGET_MEAN": dataframe.groupby(categorical_col)[target].mean()}), end="\n\n\n")

target_summary_cat(df, "survived", "pclass")

for col in cat_cols:
  target_summary_cat(df,"survived",col)

def target_summary_num(dataframe, target, numerical_col):
    print(dataframe.groupby(target).agg({numerical_col: "mean"}), end="\n\n\n")

for col in num_cols:
    target_summary_num(df, "survived", col)

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
df = pd.read_csv("breast_cancer.csv")
df = df.iloc[:, 1:-1]
df.head()

num_cols = [col for col in df.columns if df[col].dtype in [int, float]]

corr = df[num_cols].corr()

sns.set(rc={'figure.figsize': (12, 12)})
sns.heatmap(corr, cmap="RdBu")
plt.show()

cor_matrix = df.corr().abs()

upper_triangle_matrix = cor_matrix.where(np.triu(np.ones(cor_matrix.shape), k=1).astype(bool))

upper_triangle_matrix

drop_list = [col for col in upper_triangle_matrix.columns if any(upper_triangle_matrix[col]>0.90) ]

drop_list

cor_matrix[drop_list]

def correlated_cols(dataframe, plot=False, corr_th=0.90):
    corr = dataframe.corr()
    cor_matrix = corr.abs()
    upper_triangle_matrix = cor_matrix.where(np.triu(np.ones(cor_matrix.shape), k=1).astype(bool))
    drop_list = [col for col in upper_triangle_matrix.columns if any(upper_triangle_matrix[col] > corr_th)]
    if plot:
        import seaborn as sns
        import matplotlib.pyplot as plt
        sns.set(rc={'figure.figsize': (15, 15)})
        sns.heatmap(corr, cmap="RdBu")
        plt.show()
    return drop_list

correlated_cols(df)

drop_list = correlated_cols(df, plot=True)

# df = pd.read_csv("fraud_train_transaction.csv") 600mb 300 den fazla değişken var.
