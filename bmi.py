with tab1:
    if calc_button:
        # --- ここからボタンが押された時の処理 ---
        
        # 1. 計算ロジック
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        ideal_weight = 22 * (height_m ** 2)
        diff_weight = weight_kg - ideal_weight
        min_target, max_target = get_target_bmi_range(age)

        # 2. データの保存
        df_history = save_data(weight_kg, bmi)
        st.toast("データを記録しました！", icon="💾") 

        # 3. 結果表示
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("あなたのBMI", f"{bmi:.1f}")
        with col2:
            st.metric("適正体重 (BMI 22)", f"{ideal_weight:.1f}kg", f"{diff_weight:+.1f}kg", delta_color="inverse")
        with col3:
            st.metric("年齢別の目標範囲", f"{min_target} - {max_target}")

        st.divider()

        # 4. メーター表示
        bar_value = max(0.0, min(1.0, (bmi - 10) / 30))
        st.subheader("現在のポジション")
        st.progress(bar_value)
        st.caption("10 (痩せ) ............ 18.5 (普通) ............ 25 (肥満) ............ 40")

        # 5. 詳細な判定結果の表示（書き換えた部分）
        # ★重要：ここのインデントがズレるとエラーになります
        st.subheader("診断結果")
        
        if bmi < min_target:
            st.warning(f"【痩せすぎ】です。目標範囲（{min_target}以上）を下回っています。ご高齢の場合は筋肉量の減少に注意が必要です。")
        elif min_target <= bmi <= max_target:
            st.success(f"【適正範囲】です！ 年齢（{age}歳）に適した素晴らしい体型です。")
        else:
            st.error(f"【肥満気味】です。目標範囲（{max_target}以下）を上回っています。生活習慣を見直してみましょう。")
            
        # --- ボタン処理ここまで ---

    else:
        # ボタンが押されていない時の表示
        st.info("サイドバーで数値を入力し「診断・記録する」ボタンを押してください。")