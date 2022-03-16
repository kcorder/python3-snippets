import glob
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np 
import argparse

parser = argparse.ArgumentParser() 
parser.add_argument("--file-glob", required=True, type=str)
parser.add_argument("--fig-name", type=str)
parser.add_argument("--ylabel", type=str, required=True)
args = parser.parse_args()

sns.set()


csvs = glob.glob(args.file_glob)
dfs = [pd.read_csv(csv_name).Value for csv_name in csvs]


X_MIN = 0
X_MAX = int(1e6)

concat_df = pd.concat(dfs, axis=1)
agg_df = concat_df.agg([np.mean, np.std, np.quantile], axis=1)
num_points = len(agg_df['mean'])
xaxis = np.linspace(X_MIN, X_MAX, num_points)
means = agg_df['mean'].to_numpy()
stdvs = agg_df['std'].to_numpy()

concat_df['steps'] = xaxis
concat_df = concat_df.set_index('steps')
sns.lineplot(data=concat_df)
# plt.plot(xaxis, means, color='b')
# plt.fill_between(xaxis, np.clip(means-stdvs,0,1), np.clip(means+stdvs,0,1), color='b', alpha=0.2)
# plt.xticks([int(100000)*i for i in range(11)])
plt.xlabel('Steps')
plt.ylabel(args.ylabel)

if args.fig_name is not None:
    plt.savefig(args.fig_name, bbox_inches='tight')
else:
    plt.show() 

if __name__ == '__main__':
    pass