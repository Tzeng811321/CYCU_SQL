import pandas as pd
import os
from typing import Tuple, Optional

def HistoryDataSearch(
    base_dir: str = r"D:\CYCU\113_WebCrawler\CODE",
    data_dir: Optional[str] = None,
    format_file: Optional[str] = None,
    index_file: Optional[str] = None,
    price_file: Optional[str] = None,
    output_file: Optional[str] = None
) -> Tuple[Optional[pd.DataFrame], str]:
    """
    處理歷史資料搜尋，比對核價類別和功能類別，產生點數變更記錄。

    Args:
        base_dir (str): 基礎目錄路徑，預設為 D:\CYCU\113_WebCrawler\CODE
        data_dir (Optional[str]): 資料目錄路徑，預設為 base_dir/data
        format_file (Optional[str]): format_clean.csv 的完整路徑
        index_file (Optional[str]): IndexSQL_find.csv 的完整路徑
        price_file (Optional[str]): 價量調查品項108-112.csv 的完整路徑
        output_file (Optional[str]): 輸出檔案 HistoryData.csv 的完整路徑

    Returns:
        Tuple[Optional[pd.DataFrame], str]: (處理後的資料框架, 狀態訊息)
        如果發生錯誤，資料框架會是 None
    """
    # 設定檔案路徑
    data_dir = data_dir or os.path.join(base_dir, "data")
    format_file = format_file or os.path.join(data_dir, "format_clean.csv")
    index_file = index_file or os.path.join(data_dir, "IndexSQL_find.csv")
    price_file = price_file or os.path.join(data_dir, "價量調查品項108-112.csv")
    output_file = output_file or os.path.join(data_dir, "HistoryData.csv")

    try:
        # 1. 讀取三個檔案
        df_format = pd.read_csv(format_file, encoding='utf-8')
        df_index = pd.read_csv(index_file, encoding='utf-8')
        df_price = pd.read_csv(price_file, encoding='utf-8')

        # 檢查必要欄位是否存在
        required_cols = {
            'df_format': ['核價類別'],
            'df_index': ['名稱', '功能類別(前5碼)'],
            'df_price': ['特材代碼前五碼', '核價類別名稱']
        }

        for df_name, cols in required_cols.items():
            df = locals()[df_name]
            missing_cols = [col for col in cols if col not in df.columns]
            if missing_cols:
                raise ValueError(f"{df_name} 缺少以下欄位: {missing_cols}")

        # 2. 在 format_clean 的「核價類別」找出與 IndexSQL_find["名稱"] 相同的列
        format_matches = pd.merge(
            df_format[['核價類別']],
            df_index[['名稱']],
            left_on='核價類別',
            right_on='名稱',
            how='inner'
        )['核價類別'].unique()

        # 3. 在 價量調查品項 的「特材代碼前五碼」找出與 IndexSQL_find["功能類別(前5碼)"] 相同的列
        result = pd.merge(
            df_price,
            df_index[['功能類別(前5碼)']],
            left_on='特材代碼前五碼',
            right_on='功能類別(前5碼)',
            how='inner'
        )

        # 4. 確保所有列都有點數變更記錄值，預設為0
        result['點數變更記錄'] = 0

        # 5. 根據 format_clean 的資料設定點數變更記錄為1
        mask = result['核價類別名稱'].isin(format_matches)
        result.loc[mask, '點數變更記錄'] = 1

        # 6. 確保輸出欄位順序符合要求
        output_columns = [
            '年份', '特材代碼', '特材代碼前五碼', '核價類別名稱', 
            '中英文品名', '產品型號/規格', '單位', '支付點數', 
            '申請者簡稱', '許可證字號', '中文品名', '英文品名', '點數變更記錄'
        ]
        
        result = result[output_columns]

        # 7. 輸出結果前檢查點數變更記錄欄位
        if result['點數變更記錄'].isna().any():
            print("警告：點數變更記錄欄位存在空值，已自動填充為0")
            result['點數變更記錄'] = result['點數變更記錄'].fillna(0)

        # 8. 輸出到CSV
        result.to_csv(output_file, encoding='utf-8', index=False)
        status_msg = (
            f"資料處理完成，共 {len(result)} 筆資料\n"
            f"點數變更記錄為1的筆數: {result['點數變更記錄'].sum()}\n"
            f"已儲存至: {output_file}"
        )
        return result, status_msg

    except FileNotFoundError as e:
        return None, f"找不到檔案: {e}\n請確認檔案是否位於: {data_dir}"
    except ValueError as e:
        return None, f"資料欄位錯誤: {str(e)}"
    except Exception as e:
        error_msg = f"發生錯誤: {str(e)}"
        try:
            error_msg += "\n各檔案欄位清單:\n"
            error_msg += f"format_clean.csv 欄位: {df_format.columns.tolist()}\n"
            error_msg += f"IndexSQL_find.csv 欄位: {df_index.columns.tolist()}\n"
            error_msg += f"價量調查品項108-112.csv 欄位: {df_price.columns.tolist()}"
        except:
            pass
        return None, error_msg

if __name__ == "__main__":
    # 基本用法
    result_df, status = HistoryDataSearch()
    print(status)

    # custom_result, custom_status = HistoryDataSearch(
    #     base_dir=r"D:\CYCU\113_WebCrawler\CODE",
    #     data_dir=r"D:\CYCU\113_WebCrawler\CODE\data",
    #     format_file=r"D:\CYCU\113_WebCrawler\CODE\data\format_clean.csv",
    #     index_file=r"D:\CYCU\113_WebCrawler\DataBase\0407TestData\IndexSQL_find_切片針.csv",
    #     price_file=r"D:\CYCU\113_WebCrawler\CODE\data\價量調查品項108-112.csv",
    #     output_file=r"D:\CYCU\113_WebCrawler\CODE\data\HistoryData.csv"
    # )
    # print(custom_status)        
    # 自訂檔案路徑的用法
    """
    custom_result, custom_status = HistoryDataSearch(
        base_dir=r"D:\其他路徑",
        format_file=r"D:\特定路徑\format_clean.csv",
        output_file=r"D:\輸出路徑\結果.csv"
    )
    print(custom_status)
    
    """
