# Asset Index and Identity Schema V2.1｜草案

**狀態：DRAFT／NOT LOCKED**  
**Folder 參照必須完整符合 `07_FOLDER_REGISTRY_V2.1_DRAFT.md`，不得以名稱或路徑代替 Drive ID。**

## 受控欄位

- `evidence_status`：只允許 `VERIFIED`、`INFERRED`、`UNVERIFIED`、`CONFLICTED`。
- `lifecycle_status`：只允許 `DRAFT`、`REVIEW`、`APPROVED`、`LOCKED`、`SUPERSEDED`、`ARCHIVED`、`REJECTED`。
- `qc_status` 是獨立欄位；`QC_PENDING` 不得寫入 `lifecycle_status`。

## Asset Index 必填欄位

| 欄位 | 要求 |
|---|---|
| `asset_id`、`asset_type`、`scope_type`、`scope_id`、`version` | 不可變身分與版本。 |
| `folder_ref.stable_folder_code`、`folder_ref.display_name_zh_TW`、`folder_ref.google_drive_folder_id`、`folder_ref.parent_folder_id` | 必須與唯一 Folder Registry 記錄完全相符。 |
| `google_drive_file_id`、`checksum`、`mime_type`、`file_size_bytes` | 實體檔案定位與完整性。 |
| `evidence_status`、`lifecycle_status`、`qc_status`、`approval_ref`、`lock_ref` | 證據、生命週期、品質與治理分離。 |
| `source_asset_ids`、`dependency_check_status` | 上游與依賴結果。 |
| `exact_asset` | 見下列 Exact Asset 欄位。 |

## Exact Asset

`exact_asset=true` 時，必須記錄 `exact_asset_id`、`approved_original_drive_file_id`、`checksum`、`approved_version`、`usage_locations`、`crop_or_scale_allowed`。禁止生成式 AI 重繪、仿製或替代；只可受控引用或後製置入。

## Rejected 與 Dependency

`REJECTED` 資產不可成為 Character、Scene、Prop、Flow Reference 或任何下游 Generation Dependency，也不得出現在 Final Asset List；僅可位於 Rejected／Archive 作歷史與教學紀錄。上游被新版本取代時，建立 `DEPENDENCY_RECHECK_REQUIRED`，必填 `affected_assets`、`affected_segments`、`affected_outputs`、`recheck_owner`、`recheck_result`。GitHub 保存此 Index、State、Approval、Lock 與證據；Google Drive 保存媒體，File ID 與 Metadata 回寫本 Index。
