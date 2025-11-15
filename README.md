# CYCU_SQL

HistoryData.csv,endcoding=UTF-8
header格式:[年份,特材代碼,特材代碼前五碼,核價類別名稱,中英文品名,產品型號/規格,單位,支付點數,申請者簡稱,許可證字號,中文品名,英文品名,點數變更記錄]
HistoryData.csv["點數變更記錄"]，該列資料來源為format_clean 值為1，其他的值都為0

PowerBI網址:
https://officecycu-my.sharepoint.com/:u:/g/personal/11120436_o365st_cycu_edu_tw/EaRWj6oVhVZEicXQFH_xRwEBGqebEm_kosZCHbuSFC3C9A?e=Yg5jXS

```markdown
```mermaid
flowchart TD
    A[開始] --> B(讀<br>load_data_to_db);
    B --> C(建<br>create_index);
    C --> D{使用者輸入};
    D --> E(模糊搜尋<br>fuzzy_search_product);
    E --> F{有直接匹配?};

    F -->|是| G(取得匹配產品);
    G --> H(查詢相同功能產品<br>query_products_by_function);
    H --> I(分組並輸出);
    I --> J(存入 CSV<br>IndexSQL_find.csv);
    J --> K[結束];

    F -->|否| L(進階模糊搜尋<br>fuzzywuzzy);
    L --> M{有模糊匹配?};

    M -->|是| H;  %% 流程回到 H
    M -->|否| Q(顯示「找不到產品」);
    Q --> K; %% 結束
```
