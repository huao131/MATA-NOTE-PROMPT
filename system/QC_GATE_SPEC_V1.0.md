# QC Gate Spec V1.0

After every generated image, set runtime_state to QC_WAITING and output only:

1｜確認：修改指定問題並重生，不儲存正式版本。
2｜OK：核准使用，更新紀錄，停留目前節點。
3｜PASS／通過：正式鎖定並實際上傳 Drive，寫入 File ID。
4｜APPROVED：完成本張並進入下一個合法 Keyframe。
3+4：PASS 成功後再 APPROVED；上傳失敗時不得執行 4。
