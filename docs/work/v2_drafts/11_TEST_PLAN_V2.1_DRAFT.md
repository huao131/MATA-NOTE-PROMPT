# Test and Acceptance Plan V2.1｜第三批草案

**狀態：DRAFT／NOT LOCKED；測試預設使用唯讀檢查或獨立 `TEST_` scope，絕不寫入正式 Production State。**

| test_id | precondition | input | expected_result | failure_condition | recovery_action | evidence_required | automation_candidate |
|---|---|---|---|---|---|---|---|
| STR-01 | 使用者 Mapping 存在 | 五大 root 清單 | 每個 stable code 僅一個 root | 重複／缺少 root | 停止、列出 ID，不自動修正 | 父ID、子項清單、時間 | YES |
| STR-02 | Registry 可讀 | stable code 與中文名稱 | 兩欄分離、名稱非主鍵 | 以名稱作 ID 或 code 改寫 | 停止並報告 Mapping 差異 | Registry record | YES |
| STR-03 | Drive 可讀 | Folder ID／Parent ID | ID、父ID、MIME type 完全匹配 | ID不存在／父層不符 | STOP_AND_REPORT | read-back 證據 | YES |
| STR-04 | root 清單可讀 | `00_GLOBAL_OS`／`01_SERIES`／`02_EPISODES` | 不存在平行架構 | 發現平行或同用途 folder | 隔離報告，不搬移刪除 | 子項清單 | YES |
| EVD-01 | State record 候選 | `INFERRED`／`UNVERIFIED` | 不寫入 Canonical State | Canonical 欄有事實主張 | 移除候選寫入、保留證據 | State diff、source ref | YES |
| EVD-02 | Segment 與 Episode state | `segment_status=READY` | Episode 不自動 READY | Episode 被自動推升 | 還原為 NOT_EVALUATED／人工審核 | Gate／dependency records | YES |
| EVD-03 | Gate record | 缺 basis 或非 VERIFIED | Gate 不得 PASS | PASS 無完整證據 | 標 BLOCKED，補證據 | Gate entry、source ref | YES |
| EVD-04 | State record | `CONFLICTED` evidence | 所有相關 Gate／State 阻塞 | 仍可 PASS 或發布 | STOP_AND_REPORT、reconcile | conflict report | YES |
| VLK-01 | Protected artifact | 寫入 LOCK／FINAL／MASTER／APPROVED 原檔 | 操作被攔截 | 原檔內容／名稱／位置改變 | 新版＋外部 Register event | git/Drive before-after | YES |
| VLK-02 | Register 有既有版 | 相同 scope+artifact+version | 重複版號被拒 | 產生第二份同版 | 停止，建立唯一新版 | Register query | YES |
| VLK-03 | Supersession 情境 | 對 protected 舊檔標 SUPERSEDED | 僅外部 Register 記錄 | 回寫舊檔 metadata／名稱 | 還原原檔、追加 register event | old file checksum + register | YES |
| VLK-04 | 上游新版已登錄 | MAJOR 或取代關係 | 下游標 `DEPENDENCY_RECHECK_REQUIRED` | Gate 仍 PASS／無重查 | 阻塞受影響 Gate、建立 queue | impact list、recheck record | YES |
| AST-01 | Asset Index 有 Rejected | 將 Rejected 指為 reference | 驗證失敗 | Rejected 進入 Reference／Flow | 隔離、更新清單 | Index entry | YES |
| AST-02 | Exact Asset record | 生成式替代資產 | 驗證失敗 | 缺原檔 ID/checksum 或 AI 版本 | 改用原檔受控引用 | rights + checksum | PARTIAL |
| AST-03 | Asset candidate | 缺 Drive File ID 或 checksum | 不得 Approved／Locked／Final | 狀態升級成功 | BLOCKED，補登錄與回讀 | file metadata | YES |
| AST-04 | Final Asset List | 含 REJECTED | Final Gate 失敗 | Rejected 出現於 final | 移除候選並重新 QC | final list + QC | YES |
| REC-01 | Registry request | 不存在 Drive ID | 停止且不寫入 | 自建替代資料夾 | 回報預期／實際與讀取證據 | error + registry | YES |
| REC-02 | 已登錄 Asset | Drive 檔案遺失 | 依賴／Gate 阻塞 | 仍作為可用輸入 | 標遺失、從受控新版／備份復原 | Drive read failure + Index | PARTIAL |
| REC-03 | GitHub／Drive 都有紀錄 | ID、checksum、版本衝突 | `CONFLICTED` 並阻塞 | 任一端覆蓋另一端 | 保留雙方證據、人工 reconcile | Git SHA + Drive metadata | PARTIAL |
| REC-04 | Lock Register + State | Register／State 不一致 | 阻塞進度與發布 | 仍 Gate PASS | 人工比對後新增受控事件 | both records | YES |
| REC-05 | 上游已變更 | recheck 未完成 | 受影響 Gate 不得 PASS | 發布／final 通過 | 維持 BLOCKED 至 PASS recheck | impact/recheck evidence | YES |

## 驗收規則

所有 `YES` 候選僅代表可在未來由已核准的實作評估自動化；在 Codex Implementation 核准前一律以人工或唯讀檢查處理。任何測試失敗不得以刪除、覆寫、搬移 Legacy／正式資產或消耗 Flow 點數作為修復。測試通過也不解除 Repository Publication Gate，亦不構成 SYSTEM SPECIFICATION LOCK V2.0。
