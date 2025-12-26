import streamlit as st
import pandas as pd
import datetime
import os

# ページ設定
st.set_page_config(
    page_title="高機能BMIアプリ", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 定数・設定 ---
CSV_FILE = "bmi_log.csv"

# --- 関数群 ---
def get_target_bmi_range(age):
    """年齢別の目標BMI範囲を返す"""
    if age < 18:
        return 18.5, 25.0
    elif 18 <= age < 50:
        return 18.5, 24.9
    elif 50 <= age < 65:
        return 20.0, 24.9
    else:
        return 21.5, 24.9

def load_data():
    """CSVファイルから過去のデータを読み込む"""
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["日付", "体重", "BMI"])

def save_data(weight, bmi):
    """データをCSVに追記保存する"""
    today = datetime.date.today()
    new_data = pd.DataFrame({
        "日付": [today],
        "体重": [weight],
        "BMI": [bmi]
    })
    
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        df = df[df["日付"] != str(today)]
        df = pd.concat([df, new_data], ignore_index=True)
    else:
        df = new_data
        
    df.to_csv(CSV_FILE, index=False)
    return df

# --- サイドバー ---
st.sidebar.header("📝 ユーザー情報入力")
gender = st.sidebar.radio("性別", ["男性", "女性"])
age = st.sidebar.number_input("年齢", min_value=18, max_value=100, value=22)
height_cm = st.sidebar.number_input("身長 (cm)", min_value=50.0, value=170.0)
weight_kg = st.sidebar.number_input("体重 (kg)", min_value=10.0, value=60.0)
calc_button = st.sidebar.button("診断・記録する")

# --- メイン画面 ---
st.title("📊 健康管理ダッシュボード")

# データの読み込み
df_history = load_data()

# ★ここが重要！タブを作る命令
tab1, tab2 = st.tabs(["今回の診断", "📈 体重の推移グラフ"])

# タブ1：診断画面
with tab1:
    if calc_button:
        # 計算
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        ideal_weight = 22 * (height_m ** 2)
        diff_weight = weight_kg - ideal_weight
        min_target, max_target = get_target_bmi_range(age)

        # 保存
        save_data(weight_kg, bmi)
        st.toast("データを記録しました！", icon="💾")

        # 表示
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("あなたのBMI", f"{bmi:.1f}")
        with col2:
            st.metric("適正体重 (BMI 22)", f"{ideal_weight:.1f}kg", f"{diff_weight:+.1f}kg", delta_color="inverse")
        with col3:
            st.metric("年齢別の目標範囲", f"{min_target} - {max_target}")

        st.divider()

        # メーター
        bar_value = max(0.0, min(1.0, (bmi - 10) / 30))
        st.subheader("現在のポジション")
        st.progress(bar_value)
        st.caption("10 (痩せ) ............ 18.5 (普通) ............ 25 (肥満) ............ 40")

        # 判定
        st.subheader("診断結果")
        if bmi < min_target:
            st.warning(f"【痩せすぎ】です。目標範囲（{min_target}以上）を下回っています。")
        elif min_target <= bmi <= max_target:
            st.success(f"【適正範囲】です！ 年齢（{age}歳）に適した素晴らしい体型です。")
        else:
            st.error(f"【肥満気味】です。目標範囲（{max_target}以下）を上回っています。")
    else:
        st.info("サイドバーで数値を入力し「診断・記録する」ボタンを押してください。")

# タブ2：グラフ画面
with tab2:
    st.subheader("体重の変化記録")
    if not df_history.empty:
        st.line_chart(df_history, x="日付", y="体重")
        with st.expander("詳細データを見る"):
            st.dataframe(df_history)
    else:
        st.write("まだ記録データがありません。")
        
