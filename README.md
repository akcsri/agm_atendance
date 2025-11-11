# LPAC Attendance System

FY2025 LPAC（Limited Partners Advisory Committee）会議の出席管理システム

## 📋 主な機能

### ユーザー管理
- ✅ ロールベースのアクセス制御（管理者/一般ユーザー）
- ✅ CSVによる一括ユーザーインポート
- ✅ ユーザー作成・削除・パスワードリセット機能

### 参加者管理
- ✅ 参加者情報の登録・更新・削除
- ✅ 出席ステータス管理（対面/オンライン/欠席）
- ✅ CSVによる一括参加者インポート
- ✅ CSV形式での参加者一覧エクスポート

### 管理者機能
- ✅ 全参加者の一覧表示
- ✅ 統計情報（出席者数など）
- ✅ CSVインポート/エクスポート
- ✅ メール通知機能（ログイン、参加者追加/更新/削除時）

### データベース
- ✅ PostgreSQL対応（Render本番環境用）
- ✅ SQLite対応（ローカル開発用）

## 🚀 セットアップ

### ローカル開発環境

1. **リポジトリのクローンと依存関係のインストール**

```bash
git clone <repository-url>
cd lpac_attendance
pip install -r requirements.txt
```

2. **データベースの初期化**

```bash
python init_db.py
```

3. **管理者ユーザーの作成**

```bash
python create_user.py admin password123 --role admin
```

4. **アプリケーションの起動**

```bash
python app.py
```

ブラウザで `http://localhost:5000` にアクセス

### Render本番環境

1. **Renderでの新しいWebサービス作成**
   - GitHub連携でリポジトリを接続
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

2. **PostgreSQLデータベースの追加**
   - Renderダッシュボードで「New PostgreSQL」を作成
   - **Internal Database URL**をコピー（重要）

3. **環境変数の設定**

Renderの環境変数に以下を設定：

```
DATABASE_URL=<PostgreSQLのInternal Database URL>
SECRET_KEY=<ランダムな長い文字列>

# メール通知機能（オプション）
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=<Gmailアドレス>
MAIL_PASSWORD=<Gmailアプリパスワード>
NOTIFICATION_EMAIL=<通知先メールアドレス>
```

4. **デプロイ後の初期設定**

Renderのシェルで：

```bash
python create_user.py admin yourpassword --role admin
```

## 📖 使い方

### ユーザー管理

**ユーザーの作成**
```bash
python create_user.py username password --role user
```

**ユーザー一覧の表示**
```bash
python list_users.py
```

**パスワードのリセット**
```bash
python reset_password.py username newpassword
```

**ユーザーの削除**
```bash
python delete_user.py username
```

### CSVインポート

**ユーザーの一括インポート**

1. CSVファイルを作成（UTF-8 BOM付き）：
```csv
ユーザー名,パスワード,ロール
user1,password1,user
user2,password2,user
admin2,adminpass,admin
```

2. 管理者でログイン
3. 「ユーザーCSVインポート」をクリック
4. CSVファイルを選択してアップロード

**参加者の一括インポート**

1. CSVファイルを作成（UTF-8 BOM付き）：
```csv
ユーザー名,役職,名前,メール,質問,ステータス
user1,部長,山田太郎,yamada@example.com,特になし,出席（対面）
user2,課長,佐藤花子,sato@example.com,駐車場について,出席（オンライン）
```

2. 管理者でログイン
3. 「参加者CSVインポート」をクリック
4. CSVファイルを選択してアップロード

### デバッグ

**ログイン問題のデバッグ**
```bash
python debug_login.py
```

特定ユーザーの詳細チェック：
```bash
python debug_login.py admin
```

## 🔒 セキュリティ

### 推奨事項

1. **SECRET_KEY**: 本番環境では必ず強力なランダムな値を設定
2. **パスワード**: 初回ログイン後、ユーザーに変更を促す
3. **CSVファイル**: パスワードを含むファイルは使用後すぐに削除
4. **HTTPS**: 本番環境では必ずHTTPSを使用（Renderは自動対応）

## 📁 ファイル構造

```
lpac_attendance/
├── app.py                      # メインアプリケーション
├── models.py                   # データベースモデル
├── requirements.txt            # 依存パッケージ
├── .gitignore                 # Git除外設定
├── init_db.py                 # DB初期化
├── create_user.py             # ユーザー作成
├── delete_user.py             # ユーザー削除
├── list_users.py              # ユーザー一覧
├── reset_password.py          # パスワードリセット
├── debug_login.py             # ログインデバッグ
├── participants_template.csv  # 参加者CSVテンプレート
├── users_template.csv         # ユーザーCSVテンプレート
├── templates/                 # HTMLテンプレート
│   ├── login.html
│   ├── index.html
│   ├── user_dashboard.html
│   ├── admin_dashboard.html
│   ├── import_csv.html
│   └── import_users.html
└── static/                    # 静的ファイル
    ├── logo.png
    └── style.css
```

## 🆘 トラブルシューティング

### ログインできない

1. ユーザーが存在するか確認：
```bash
python list_users.py
```

2. パスワードをリセット：
```bash
python reset_password.py username newpassword
```

3. デバッグツールで詳細確認：
```bash
python debug_login.py username
```

### データベース接続エラー

- Renderの場合：
  - **Internal Database URL**を使用しているか確認
  - `DATABASE_URL`環境変数が正しく設定されているか確認

- ローカルの場合：
  - SQLiteファイル（users.db）の権限を確認

### CSVインポートエラー

- エンコーディング：UTF-8（BOM付き）で保存
- ヘッダー行が正しいか確認
- 必須項目がすべて入力されているか確認

## 📧 メール通知

メール通知を有効にするには、以下の環境変数を設定：

```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
NOTIFICATION_EMAIL=admin@example.com
```

**Gmail使用時の注意**：
- Gmailの「アプリパスワード」を使用してください
- 2段階認証を有効にする必要があります

## 📝 ライセンス

このプロジェクトは社内使用のためのものです。

## 🤝 サポート

問題や質問がある場合は、システム管理者に連絡してください。
