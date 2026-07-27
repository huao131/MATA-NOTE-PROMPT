# QC and Recovery Specification V2.0｜草案

**狀態：DRAFT／NOT LOCKED；QC 不授權覆寫、搬移或刪除正式／Legacy 資產。**

## QC 項目與處置

| QC 面向 | 驗證 | 失敗處置 |
|---|---|---|
| Story Fidelity | Story、旁白、角色登場、節奏與核准版本一致 | `REBUILD_SEGMENT` 或新 Story 版本；recheck 下游 |
| Continuity | Character／Scene／Prop、構圖、光線、首尾影格一致 | `REGENERATE`；保留 rejected 證據 |
| Exact Asset | 原檔 ID、checksum、權利、受控置入 | 禁止替代／重繪；改用原檔後製 |
| Technical／Metadata | Drive ID、checksum、version、Index、Gate、Dependency 完整 | BLOCKED，補回讀資料或人工 reconcile |

QC disposition 僅可為 `APPROVED`、`APPROVED_WITH_EDIT`、`REGENERATE`、`REBUILD_SEGMENT`。Rejected 必須依類型記錄（story、continuity、technical、rights、metadata），隔離於 Rejected／Archive，不可再次作 reference。

## Recovery／Rollback

| 事件 | 復原 |
|---|---|
| Broken Dependency | 標 `DEPENDENCY_RECHECK_REQUIRED`，列出 affected assets/segments/outputs，人工 PASS 前阻塞 Gate。 |
| Missing Drive ID | `STOP_AND_REPORT`；以讀取證據補登錄，絕不猜測或自建替代資料夾。 |
| Lock conflict | 保護原檔；建立新版本與 Register event，禁止原地修正。 |
| Version conflict | 停止；查唯一性後建立唯一新版，不產生同版修正版。 |
| GitHub／Drive metadata conflict | 標 `CONFLICTED`，保全雙方證據並人工 reconcile；不覆蓋任一端。 |

Rollback 是新增受控版本／Register 關聯與重新核准，不是刪除或覆寫。Final 需同時通過 Story Fidelity、Continuity、Exact Asset、metadata、Dependency、Final Asset List 與 `final_approved` Gate。
