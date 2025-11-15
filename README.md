# CYCU_SQL

HistoryData.csv,endcoding=UTF-8
header格式:[年份,特材代碼,特材代碼前五碼,核價類別名稱,中英文品名,產品型號/規格,單位,支付點數,申請者簡稱,許可證字號,中文品名,英文品名,點數變更記錄]
HistoryData.csv["點數變更記錄"]，該列資料來源為format_clean 值為1，其他的值都為0

PowerBI網址:
https://officecycu-my.sharepoint.com/:u:/g/personal/11120436_o365st_cycu_edu_tw/EaRWj6oVhVZEicXQFH_xRwEBGqebEm_kosZCHbuSFC3C9A?e=Yg5jXS

```mermaid
flowchart TD
    A[開始] --> B(讀取 CSV 並建立 SQLite 資料庫<br>load_data_to_db);
    B --> C(建立資料庫索引<br>create_index);
    C --> D{使用者輸入產品名稱或關鍵字};
    D --> E(進行模糊搜尋<br>fuzzy_search_product);
    E --> F{有找到直接匹配結果?};

    %% Branch 1: Direct Match Found
    F -- 是 --> G(取得匹配產品);
    G --> H(查詢相同功能類別產品<br>query_products_by_function);
    H --> I(將結果分組[大小類]，輸出結果');
    I --> J(將結果存入 CSV 檔案<br>IndexSQL_find.csv);
    J --> K[結束];

    %% Branch 2: No Direct Match
    F -- 否 --> L(進行模糊搜尋<br>fuzzywuzzy 模組);
    L --> M{有找到模糊匹配結果?};

    %% Branch 2a: Fuzzy Match Found
    M -- 是 --> H;  %% 流程回到 H

    %% Branch 2b: No Fuzzy Match
    M -- 否 --> Q(顯示「找不到產品」訊息);
    Q --> K; %% 結束
