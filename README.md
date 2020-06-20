# DataMining - NKUST CSIE Course
## HW List
- HW1. Apriori Algorithm
- HW2. Regular Expression
- HW3. K-means Algorithm
- HW4. DBScan Algorithm
- HW5. FP-Tree
- HW6. ID3 Algorithm
## HW1 Description
```
請參考投影片與論文，使用「能在教室電腦上運行」的程式語言，完成本次作業。
作業Data可使用壓縮檔內的來測試。

最後結果請顯示：
    1.請將L詳細結果存入電腦txt檔，如下：
        1:2154
        2:9547
        1,2:1073
    2.請在cmd視窗中顯示L所獲得的總數，也就是將 L1總數 + L2總數 + ... 的結果。
        (總數是指L的itemset 的種類數量)
    3.請紀錄程式開始到結束的時間，顯示為毫秒。
```
## HW2 Description
```
請參考老師課堂所教，使用爬蟲至 http://www.csie.kuas.edu.tw/teacher.php 、
http://www.csie.kuas.edu.tw/index.php 中，將該頁面的Email與電話全數撈出，
例如：
    jc.chen@nkust.edu.tw
    changwl@nkust.edu.tw
    ...
    wychung@nkust.edu.tw

最後結果請顯示：
    1.所有頁面中的Email與電話
    2.總計列出了多少筆Email與多少筆電話資料
```
## HW3 Description
```
請參考投影片，完成K-means演算法，Data請使用Jpg或Bmp圖片並且可以設定要分幾群(K值)。

圖片使用方法：
    請使用每個pixel的RGB當成座標，以此三圍座標當作計算距離的依據，
    並且依照演算法進行分群，
    最後請將該群的RGB平均值重新寫回對應位置的pixel。

最後結果請顯示：
    重新上色過的圖片
```
## HW4 Description
```
請參考投影片，完成DBSCAN演算法，測試Data請使用壓縮檔案內附的Bmp圖片並且可以設定距離與雜訊過濾的基準值。

圖片使用方法：
    請使用每個pixel在圖中的位置當成座標，以此二圍座標當作計算距離的依據，
    並且顏色為黑色代表有點存在，而白色就代表沒有點存在，請依照演算法進行分群，
    最後請將同群的任意寫入同一顏色。

最後結果請顯示：
    1.重新上色過的圖片
    2.總共分了幾群
```
## HW5 Description
```
請使用company.csv(公司資料)、disaster.csv(受傷紀錄)、insurance.csv(保險資料)此三個檔案作為依據，
撰寫一隻能夠產生資料表與將三個.csv匯入資料的程式，這將使用教室內電腦MySql來做為database。

請注意資料表之間的關聯性設定，以下列出相關聯的資料；
company:公司編號 = insurance:公司編號
insurance:人員編號 = disaster:人員編號

第一階段: 提供Demo專用的data，請在1個半小時內匯入完畢。
第二階段: 提供所需要分析出的目標資料，使用自行設計SQL的code，並將運行的結果記錄起來，完成全部題目後請助教檢查。

最後結果請顯示：
    1.使用的SQL Code
    2.計算出結果，如數量、平均值、最大值等等
```
## HW6 Description
```
請參考投影片，完成本次作業。
作業Data可使用壓縮檔內的來測試。

最後結果請顯示：
    完整樹狀圖，可使用套件轉換成圖片，或利用文字，可以參考下面的結構。
        項目(一)
        ├─(結果1)──	Yes
        ├─(結果2)──	No
        └─(結果3)──	項目(二)
                ├─(結果4)──	No
                └─(結果5)──	Yes
```