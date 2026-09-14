# Antigravity Hands-On

Google Antigravity を活用したエージェント開発ハンズオンの教材リポジトリです。
座学資料・受講者配布用スターターキット・講師用の模範解答をワークショップ単位でまとめています。

## ワークショップ一覧

| ディレクトリ | 対象 | 所要時間 | 概要 |
| --- | --- | --- | --- |
| [`workshops/gemini-enterprise-admin`](workshops/gemini-enterprise-admin/) | Gemini Enterprise 管理者 | 3 時間 | ハーネス（AGENTS.md / Skill / Hook）によるエージェント制御、Stop フックによる秘密情報直書きの阻止と自己修正、受入評価（Eval）、Agent Runtime デプロイ、Gemini Enterprise 登録までを体験する |
| [`workshops/antigravity-cloud-workstations`](workshops/antigravity-cloud-workstations/) | 社内エンジニア / 環境構築担当 | 1 時間程度 | Cloud Workstations 上に Antigravity 環境を構築する手順 |

## ディレクトリ構成

```
.
├── README.md
└── workshops/
    ├── gemini-enterprise-admin/
    │   ├── README.md
    │   ├── docs/          # 講師向け設計書・受講者向け事前準備
    │   ├── starter-kit/   # 受講者に配布する資材（意図的な欠陥入り）
    │   ├── answers/       # 講師用の模範解答（受講者には配布しない）
    │   └── governance/    # Model Armor / Agent Gateway の設定サンプル
    └── antigravity-cloud-workstations/
        ├── README.md
        └── docs/
```

## 使い方

1. 開催するワークショップのディレクトリに移動する
2. `README.md` を読み、`docs/` の設計書と事前準備チェックリストを確認する
3. 受講者には `starter-kit/` のみを配布する（`answers/` は講師用）

> [!WARNING]
> `answers/` 配下は模範解答です。受講者に事前共有すると演習が成立しません。