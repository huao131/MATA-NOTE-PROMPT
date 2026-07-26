# Codex Implementation Backlog V2.1｜第三批草案

**狀態：DRAFT／NOT LOCKED。此為需求 Backlog，不含程式碼，也不授權實作。**  
**共同禁止：不得控制 Flow／CapCut、不得消耗 Flow 點數、不得異動 Legacy 或受保護資產；外部 API 一律非預設且需另行核准。**

| 任務ID | 優先級 | 輸入規格 | 輸出 | 依賴 | 驗收條件 | 禁止行為 | 外部 API | 預估風險 |
|---|---|---|---|---|---|---|---|---|
| P0-01 | P0 | D05、D11 | Schema validation report | 發布後 repo 結構 | 非法 evidence／lifecycle／gate 值阻塞 | 猜測或修補資料 | 否 | Schema 與既有 Legacy 不相容 |
| P0-02 | P0 | D07 Registry | Folder Registry read-only resolver | 已驗證 Mapping | 僅以 ID+stable code 解析；不符停止 | 依名稱定位或自建資料夾 | 否 | Mapping 漂移 |
| P0-03 | P0 | D08 Index schema | Asset Index read/write proposal | Schema validation | 必填 ID／checksum／狀態缺失阻塞 | 寫入未驗證 Canonical State | 否 | 舊資料缺欄位 |
| P0-04 | P0 | D05、D11 | Version／Lock protection checks | Register 模型 | Protected 原檔不可改、版號唯一 | 覆寫或回寫 SUPERSEDED | 否 | 保護規則誤攔正常新版本 |
| P0-05 | P0 | D01、D02、D05 | Evidence status validator | Evidence source | 非 VERIFIED 不可 Canonical；CONFLICTED 阻塞 | 以聊天推定證據 | 否 | 證據來源格式不一致 |
| P0-06 | P0 | D05、D08 | Dependency recheck queue | 上下游關係 | 新版上游觸發受影響範圍重查 | 跳過 recheck 或推升 Gate | 否 | 間接依賴遺漏 |
| P1-01 | P1 | D04、D10 | New Episode initialization plan | P0、發布 Gate解除 | 新 Episode／TEST scope 隔離 | 觸碰 Legacy 或正式 State | 否 | 範本污染 |
| P1-02 | P1 | D05 | Production State update workflow | P0-01、P0-05 | Gate 順序與 Evidence 規則成立 | Segment Ready 推升 Episode | 否 | 人工審批遺失 |
| P1-03 | P1 | D05、D11 | Gate Register operations | P1-02 | 六 Gate 完整稽核欄位 | 用布林取代 Gate record | 否 | Gate 定義改版 |
| P1-04 | P1 | D08 | Segment／Asset status handling | P0-03 | Rejected 與 status 隔離 | 把 Rejected 放入下游 | 否 | 狀態混用 |
| P1-05 | P1 | D04、D08 | Prompt Library metadata model | D04 GAP解除 | Prompt 可追溯到 approved inputs | 將 Prompt 視為 Flow 控制 | 否 | Workflow Schema 未完成 |
| P1-06 | P1 | D08、D09 | Storyboard／Flow handoff manifest | D08 GAP解除 | 只產出交接資料與驗證缺口 | 自動呼叫 Flow | 否 | 外部工具格式變動 |
| P2-01 | P2 | D07、D10 | Drive ID mapping validation | P0-02 | 帳號隔離、ID/父ID核對 | 沿用 Mata ID、重複建資料夾 | 可選；預設否 | Drive 權限／API變更 |
| P2-02 | P2 | D08 | Physical asset registration workflow | P2-01 | File ID、checksum、metadata 完整 | 假造 Drive 證據 | 可選；預設否 | 雜湊取得成本 |
| P2-03 | P2 | D08 | Exact Asset validation | P2-02 | 原檔 ID／checksum／權利存在 | AI 替代或重繪 | 否 | 原始權利證據不足 |
| P2-04 | P2 | D08、D09 | CapCut Editing Manifest | D08 GAP解除 | 只交接 manifest，不控制 CapCut | 自動編輯或發布 | 否 | CapCut 格式未定 |
| P2-05 | P2 | D08、D09 | SRT／Voiceover handoff manifest | D08 GAP解除 | 對位、來源、版本可追溯 | 自動生成或上傳外部檔 | 否 | 工具格式未定 |
| P3-01 | P3 | D08、D11 | Rejected quarantine check | P0-03 | Rejected 不在 reference／final 清單 | 刪除 Rejected 證據 | 否 | 歷史資料混放 |
| P3-02 | P3 | D05、D08 | Broken dependency detection | P0-06 | 上游變更必標重查 | 自動判 PASS | 否 | 依賴圖不完整 |
| P3-03 | P3 | D05、D11 | Lock violation interceptor | P0-04 | 保護檔寫入被阻截 | 修改原檔作修復 | 否 | 誤判檔案標記 |
| P3-04 | P3 | D05、D11 | Duplicate version interceptor | P0-04 | 重複版號停止回報 | 另建同版修正版 | 否 | 登錄並行衝突 |
| P3-05 | P3 | D07、D11 | Missing Drive ID stop control | P2-01 | 缺／錯 ID 無法進入下游 | 自動猜測 ID | 否 | 離線情境 |
| P3-06 | P3 | D09、D11 | Rollback／Recovery runbook support | D09 GAP解除 | 保留證據、外部 Register 新事件 | 刪除／覆寫／平行重建 | 否 | Recovery 規格未完成 |

**啟動條件：** 先完成 FULL SYSTEM INTEGRATION REVIEW、補齊或正式豁免 Crosswalk GAP、解除 Repository Publication Gate 並驗證 remote SHA，才可另行審議 SYSTEM SPECIFICATION LOCK V2.0 與實作授權。
