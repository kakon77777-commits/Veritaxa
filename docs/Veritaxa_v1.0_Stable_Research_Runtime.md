# Veritaxa v1.0：可驗證研究編譯與攜帶式審計封裝

v1.0將前面版本的搜尋、Evidence IR、Evidence Span、Claim Review、MRASG、失效傳播與重新編譯固定為第一個穩定契約。

## 五個穩定物

1. 穩定研究Runtime API；
2. 穩定研究編譯Schema；
3. 穩定失效與依賴傳播語義；
4. 穩定人類治理邊界；
5. 穩定、可攜、可雜湊驗證的Research Bundle。

## Bundle不是備份壓縮檔

Bundle是研究狀態的最小可審計投影。它同時保存當前編譯、Evidence、Review事件、Invalidation、Impact、Conflict、Conclusion與Audit，並用Manifest鎖定每個檔案。

## 不可變原則

```text
Machine output cannot self-authorize.
Evidence loss must propagate.
Conflict closure must be attributed.
Recompilation must return to review.
Tampered bundles must fail validation.
```

v1.0因此不是功能終點，而是後續v1.x可以可靠擴充的第一個相容基線。
