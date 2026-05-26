import akshare as ak
import requests
import datetime
import pandas as pd
import os

# ====================== 【配置说明】 ======================
# 方式一（推荐）：设置环境变量 WECHAT_WEBHOOK_URL（用于 GitHub Actions 等自动化场景）
# 方式二：直接修改下方 WEBHOOK_URL 的值（本地运行）
# ========================================================
WEBHOOK_URL = os.environ.get(
    "WECHAT_WEBHOOK_URL",
    "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=3ae74635-56f1-404b-9c5c-1a873e0a2169"
)
# ========================================================


def get_money_fund_7day_median():
    """
    获取货币基金7日年化收益率中位数
    数据来源：东方财富-货币基金排行榜（https://fund.eastmoney.com/data/hbxfundranking.html）
    覆盖约540只主流货币基金（东方财富展示的活跃基金）
    """
    print("正在获取货币基金数据...")
    # 1. 获取货币基金排行榜数据
    df = ak.fund_money_rank_em()
    
    # 打印数据概况
    print(f"获取到 {len(df)} 只货币基金数据")
    
    # 2. 7日年化收益率列名
    target_col = "年化收益率7日"
    
    # 3. 数据清洗：过滤空值
    df = df.dropna(subset=[target_col])
    
    # 4. 计算中位数
    median_rate = df[target_col].median()
    count = len(df)
    print(f"货币基金7日年化收益率中位数：{median_rate:.2f}%")
    
    # 5. 获取日期（取第一条记录的日期）
    date_str = df["日期"].iloc[0] if "日期" in df.columns else datetime.date.today().strftime("%Y-%m-%d")
    
    # 返回字典，包含 send_to_wechat 需要的所有字段
    return {
        "median": median_rate,
        "count": count,
        "date": date_str
    }
def send_to_wechat(data):
    """
    发送到企业微信群机器人
    """
    msg = f"""📊 货币基金7日年化收益率（前一日）
统计日期：{data['date']}
基金数量：{data['count']} 只
中位数收益率：{data['median']:.4f}%"""

    payload = {
        "msgtype": "text",
        "text": {"content": msg}
    }

    r = requests.post(WEBHOOK_URL, json=payload)
    print("发送结果：", r.json())

if __name__ == "__main__":
    fund_data = get_money_fund_7day_median()
    send_to_wechat(fund_data)
