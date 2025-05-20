# math-arithmetic-test

## 專案簡介

本專案是一個以 Tkinter 製作的數學四則運算練習程式，支援自訂倒數秒數與題目難度，適合學生或一般使用者進行心算訓練。

## 預覽畫面 | Screenshot

![四則運算練習器預覽圖](math-arithmetic-test/images/screenshot.png)  
_▲ 程式主畫面：可隨機生成四則運算題目_

## 安裝方式

1. 下載或 clone 此專案。
2. 確認已安裝 Python 3（建議 3.7 以上）。
3. Tkinter 為 Python 內建套件，通常無需額外安裝。

## 執行方式

進入 `src` 資料夾後執行：

```bash
python math_arithmetic_test.py
```

## 功能說明

- 題目類型：加法、減法、乘法、除法，四則運算平均隨機出現。
- 數字長度：每題數字為 3~5 位數，機率均等。
- 倒數計時：可自訂 30~99 秒，預設 90 秒。
- 每題最多可答 3 次，錯 3 次會顯示正確答案。
- 支援一鍵重刷題目與重新計時。

## 需求
- Python 3
- Tkinter（Python 內建）

## 進階自訂
- 秒數可於介面上直接輸入（30~99）。
- 題目難度可調整 `src/math_arithmetic_test.py` 內 `generate_number` 或 `generate_question` 相關邏輯。

## 題目與答案範圍
- 題目數字與所有答案（加減乘的和/差/積、除法的商、分子、分母）都會控制在 3~5 位數（100~99999），確保難度適中且適合心算練習。 
