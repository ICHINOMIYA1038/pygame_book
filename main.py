import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():
    # 1. データ生成
    np.random.seed(42)
    months = np.array([f'{i}' for i in range(1, 13)])  # 1月から12月
    sales_data = np.random.randint(100, 500, size=(12, 3))  # 100~500のランダムな整数

    # 2. DataFrameの作成
    df = pd.DataFrame(sales_data, columns=['A', 'B', 'C'])
    df['Month'] = months

    # 3. 基本統計量の確認
    summary = df.describe()

    # 4. 可視化（売上の推移）
    plt.figure(figsize=(10, 6))
    for product in ['A', 'B', 'C']:
        plt.plot(df['Month'], df[product], marker='o', label=product)

    plt.title('Monthly Sales Data')
    plt.xlabel('Month')
    plt.ylabel('Sales Amount')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__=="__main__":
    main()