# 02｜Episode Evidence State Table V1.0（DRAFT）

**Status:** V2_SPECIFICATION_REVIEW_PAUSED  
**Rule:** this is an evidence table, not a Production State register. Only VERIFIED evidence can be copied to Canonical Production State.

## 1. Evidence-status vocabulary

| Status | Meaning | Canonical Production State action |
|---|---|---|
| VERIFIED | Directly located in the authoritative GitHub/Drive source and identity checked | Eligible, subject to normal approval controls |
| INFERRED | Logical conclusion from partial evidence | Do not write automatically |
| UNVERIFIED | Required source was not located or cannot be read | Do not write automatically |
| CONFLICTED | Two authoritative sources disagree | Stop and resolve before write |

## 2. Episode evidence table

| episode_id | evidence item | asserted value | evidence_status | canonical-state action |
|---|---|---|---|---|
| EP01 | Production State | Not retrieved from authoritative source | UNVERIFIED | No automatic write |
| EP01 | Asset Index | Not retrieved from authoritative source | UNVERIFIED | No automatic write |
| EP01 | B1_V2.0 | No authoritative file located | UNVERIFIED | No ownership/state assignment |
| EP01 | A2_V1.1 | No authoritative file located | UNVERIFIED | No ownership/state assignment |
| EP01 | S1 Flow Package | No authoritative file located | UNVERIFIED | No segment or Episode state assignment |
| EP02 | Production State | Not retrieved from authoritative source | UNVERIFIED | No automatic write |
| EP02 | Asset Index | Not retrieved from authoritative source | UNVERIFIED | No automatic write |
| EP02 | B1_V2.0 | No authoritative file located | UNVERIFIED | No ownership/state assignment |
| EP02 | A2_V1.1 | No authoritative file located | UNVERIFIED | No ownership/state assignment |
| EP02 | S1 Flow Package | No authoritative file located | UNVERIFIED | No segment or Episode state assignment |
| EP01/EP02 | REVISION_REQUIRED attribution | No authoritative Production State retrieved | UNVERIFIED | Do not attribute to either Episode |

## 3. Required evidence chain

An Episode state can be verified only when all required records agree:

Episode ID → GitHub Production State → GitHub Asset Index → asset/folder ID → approval or lock record → upstream/downstream dependency check.

A Segment may be READY only as a segment-local fact. It does not imply the Episode is ready, approved, or production-locked. If B1/A2 or any upstream reference changes, all linked Flow packages, outputs, edit manifests, and final-QC evidence require a dependency re-check.

## 4. Resolution protocol

1. Retrieve the exact GitHub paths and commit SHA for Production State, Asset Index, B1_V2.0, A2_V1.1 and S1 Flow Package.
2. Confirm each document’s episode ID and asset IDs.
3. Record conflicting claims as CONFLICTED; do not overwrite historical evidence.
4. After all links are VERIFIED, propose a separate Canonical Production State update for human approval.
