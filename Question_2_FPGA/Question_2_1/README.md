# 交通號誌控制系統設計 (Traffic Light FSM)

本專案使用 **VHDL** 語言設計一個基於有限狀態機（FSM）的交通號誌控制器。

## 1. 專案介紹
本設計模擬標準十字路口的紅綠燈循環邏輯。系統透過一個內部計數器來精確控制每個燈號狀態的持續時間。

### 規格要求：
* **綠燈 (Green)**：持續 8 個時脈週期 (Clock Cycles)。
* **黃燈 (Yellow)**：持續 2 個時脈週期 (Clock Cycles)。
* **紅燈 (Red)**：持續 10 個時脈週期 (Clock Cycles)。
* **循環順序**：綠燈 -> 黃燈 -> 紅燈 -> 綠燈。

---

## 2. 邏輯流程圖 (Flowchart)

```mermaid
flowchart TD
    Start((開始)) --> Reset{Reset?}
    Reset -- "Yes" --> G[進入 S_GREEN <br/>計數器清零]
    Reset -- "No" --> Edge(等待時脈負緣)
    Edge --> State{當前狀態?}
    
    State -- "S_Green" --> G_Limit{計數 = 7?}
    G_Limit -- "No" --> G_Inc[計數 + 1]
    G_Limit -- "Yes" --> Y[轉入 S_YELLOW <br/>計數器清零]
    
    State -- "S_Yellow" --> Y_Limit{計數 = 1?}
    Y_Limit -- "No" --> Y_Inc[計數 + 1]
    Y_Limit -- "Yes" --> R[轉入 S_RED <br/>計數器清零]
    
    State -- "S_Red" --> R_Limit{計數 = 9?}
    R_Limit -- "No" --> R_Inc[計數 + 1]
    R_Limit -- "Yes" --> G

    classDef g_style fill:#d4edda,stroke:#28a745,stroke-width:2px
    classDef y_style fill:#fff3cd,stroke:#ffc107,stroke-width:2px
    classDef r_style fill:#f8d7da,stroke:#dc3545,stroke-width:2px
    class G g_style
    class Y y_style
    class R r_style

    linkStyle 0,2,3,4,7,10 stroke:#333,stroke-width:2px
    linkStyle 1,12 stroke:#28a745,stroke-width:5px
    linkStyle 6 stroke:#ffc107,stroke-width:5px
    linkStyle 9 stroke:#dc3545,stroke-width:5px
    linkStyle 5,8,11 stroke:#888,stroke-width:2px,stroke-dasharray:5
```

---

## 3.狀態轉移圖

```mermaid
stateDiagram-v2
    direction TB
    [*] --> S_GREEN : rst_n = 0
    
    S_GREEN --> S_YELLOW : timer = 7 (8 clks)
    S_YELLOW --> S_RED : timer = 1 (2 clks)
    S_RED --> S_GREEN : timer = 9 (10 clks)

    state S_GREEN {
        direction LR
        [*] --> 綠燈運作中
    }
    state S_YELLOW {
        direction LR
        [*] --> 黃燈運作中
    }
    state S_RED {
        direction LR
        [*] --> 紅燈運作中
    }
```

---

## 3. 硬體架構 (Architecture)

本系統由兩個主要部分組成：
1.  **時序邏輯 (Sequential Logic)**：處理時脈正邊緣觸發與重置訊號。
2.  **狀態轉換邏輯 (Next State Logic)**：判斷 `timer` 是否達到設定上限（如綠燈 8 clks）。

### 狀態編碼表：
| 狀態名稱 | 燈號輸出 (R, Y, G) | 持續時間 |
| :--- | :--- | :--- |
| S_GREEN | 001 | 8 Clks |
| S_YELLOW | 010 | 2 Clks |
| S_RED | 100 | 10 Clks |

---

## 4. 模擬成果 (Results)

透過 VHDL Testbench 進行功能驗證，下圖展示了時序波形的模擬結果：

![成果展示](./img/成果展示.png)


### 模擬現象觀察：
1.  **Reset 階段**：當 `rst_n` 為低電位時，輸出立即回到 `S_GREEN`。
   
   ![RESET](./img/RESET.png)

2.  **自動循環**：
    * 在時脈第 1 到 8 個週期顯示綠燈。
    * 第 9 到 10 個週期轉換為黃燈。
    * 第 11 到 20 個週期轉換為紅燈，隨後回到綠燈完成循環。

---


