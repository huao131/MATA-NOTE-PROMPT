# 19｜Global MASTER SOP V2.0 Draft

**文件狀態：DRAFT／NOT LOCKED**  
**治理層級：唯一 Global MASTER SOP；適用於所有 Series、Episode、Segment 與 Asset。**  
**核心限制：本文件不授權 Lock、Codex Implementation、Flow 操作、CapCut 操作，亦不改寫 Legacy 或任何正式資產。**

## 1. Product Definition 與製片責任

MATA AI ORIGINAL VIDEO STUDIO OS V2 以「原創優先、跨行業、使用者使用自有資源、無額外付費 API 優先」為不可變更核心定位。AI 的角色是受控製片協作：整理需求、產生可審閱候選、維護可追溯交接與提示人工決策；人類擁有創意、權利、核准、Lock、發布與外部工具操作的最終責任。

Codex 可在核准後讀取 Manifest 指定的現行文件，進行受控的規格分析、測試與程式工作；不得直接控制 Flow、CapCut 或任何需帳號／付費點數的外部工具。Gem／ChatGPT 不得將聊天內容取代 Register、Evidence 或正式資產紀錄。

## 2. 繼承與 Chat 邊界

繼承方向固定為 `GLOBAL → SERIES → EPISODE → SEGMENT → ASSET`。Global 規則可被下層引用；Series 與 Episode 的特定設定不得反向升格為全域規則。每支影片必須使用一個獨立 Chat；共享 MASTER SOP，但每集的 Brief、Creative Lock、Story、Visual Bible、資產與狀態完全隔離。Legacy Episode 僅作唯讀證據，不得自動成為 Global Rule。

## 3. New Episode Workflow

1. **Intake**：建立 Episode ID、範圍、目的、平台、時長、CTA、權利與來源證據；缺任一必要資訊即 `BLOCKED`。
2. **Audience Insight 與 Hook Strategy**：先界定受眾、痛點、情境、期望行動與可選 Hook 類型；產出候選但不得自行鎖定。
3. **Creative Lock**：人工核准核心主張、受眾、Hook、CTA、限制與成功標準；未 PASS 不得進入 Story。
4. **Story Development**：建立故事、旁白、腳本、節奏與 Segment 對位；故事變更以新版本處理。
5. **Story／Visual Lock**：以 Visual Bible 與 Storyboard 核對故事、角色、場景、道具、光線及 Exact Asset 使用邊界。
6. **Keyframe Production**：依核准 Storyboard 產出可追溯關鍵影格與 continuity 證據；未通過 `keyframe_lock` 不得送 Flow。
7. **Flow Production Package**：只建立人工可操作的 package（已核准影格、prompt、參數、輸出登錄欄位）；人工在 Flow 完成生成並回寫輸出。Codex 不得操作 Flow。
8. **Editing Handoff**：交付已登錄 Flow Media、Audio、Storyboard、字幕／剪輯需求與 Edit manifest；人工於 CapCut 或指定剪輯工具完成，Codex 不得控制 CapCut。
9. **Final QC 與 Episode Summary**：執行內容、連續性、權利、格式、字幕、音訊、Exact Asset、依賴與交付檢查；建立 Episode Summary、QC evidence、交付清單與 Register event。

## 4. 視覺、資產與 Exact Asset 治理

Character、Scene、Prop、Lighting、服裝與連續性均必須在 Visual Bible 具可追溯定義。Exact Asset（官方 Logo、授權素材、要求一比一保留之檔案）僅可受控引用或後製置入，不得交由生成模型重繪、風格化或以相似圖替代。Rejected 資產必須隔離、保留拒絕理由與 ID，不得作為模型參考、共用素材、剪輯預設輸入或發布候選。

## 5. Gate、Evidence、State 與 Dependency

六個 Gate 固定順序為 `creative_lock`、`story_lock`、`story_visual_lock`、`keyframe_lock`、`production_lock`、`final_approved`。Evidence Status 使用 `VERIFIED`、`INFERRED`、`UNVERIFIED`、`CONFLICTED`；只有 VERIFIED 證據可支撐 Canonical 事實與 Lock Candidate。Production State 與 Lifecycle Status 分欄管理；Segment Ready 不得推升 Episode Ready。

任何上游故事、視覺、關鍵影格、權利、資產版本或 Lock 關係改變，都必須標記受影響下游 `DEPENDENCY_RECHECK_REQUIRED`；完成逐項人工 recheck 前，不得宣告後續 Gate 或交付仍有效。

## 6. Version、Lock、Register 與 Legacy

所有變更採新版本或新資產 ID；`LOCK`、`FINAL`、`MASTER`、`APPROVED` 舊檔不得原地覆寫。Current Effective、supersession、Lock event 與例外處置只記錄於 Version／Lock Register 與 Lock Candidate Manifest；不回寫舊 Draft。Legacy 僅唯讀、不得修改、清理、搬移或刪除。

## 7. GitHub／Drive 責任邊界

GitHub 保存版本化規格、schema、register、state、index、測試與程式；Google Drive 保存受控實體媒體、檔案 ID、資料夾 ID、校驗與交付素材。Drive ID 為實體主鍵，名稱僅為顯示；未驗證 ID 不得宣告 Canonical。不得建立平行目錄規避治理問題。

## 8. 結束條件與禁止事項

Final 僅在所有必要 Gate PASS、Evidence VERIFIED、Dependency PASS、QC evidence 完整、版本關係已登錄且人工批准後成立。本 Draft 僅提供 Lock Review；在 Review 明確通過前，任何人不得執行 Lock、實作、合併 main、操控 Flow／CapCut 或修改 Legacy／正式資產。
