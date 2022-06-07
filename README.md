## 第6回
### オリジナルゲームの作成
#### 3,4,5限：オリジナルゲーム作成
- ゲーム概要：
    - final kadai/Rex.pyを実行すると900X500のスクリーンに空が表示されて飛行機を右から来る障害物をよける横スクロールゲーム
    - クリアなどはなく飛行機と障害物が当たるまで続く、障害物と5回衝突した際にゲームオーバーとなり終了する
- 操作方法：スペースキーのみで操作する、キーを押し続けると飛行機は上昇し離すと下降する
 - 上矢印キーでも操作可能に変更(武田)
- プログラムの説明
    - グローバル変数として障害物の確率のリスト、雲の描画のリスト、体力の初期値をキャラの移動範囲を設定している。
    - Rex.pyを実行するとpygameの初期化 、main関数の順に処理が進む
    - ScreenClassではウィンドウに関するものを行っている
    - Planeclassでは飛行機の描画とキャラ操作に関する処理を行っている
    - Bulletclassでは障害物に関する描画と動作に関する処理を行っている
    - Cloudclassでは雲の描画と動作に関する処理を行っている
    - Scoreclassではスコア計算に関する処理を行っているまた表示に関するも処理を行っている
    - main関数が実行されるとず各クラスが呼出される
    - main関数内で飛行機と障害物に関するクラスをスプライトグループにする
    - 障害物を複数呼出せるように空のコンテナを作る
    - またwhile内で常にrandintを回し続けグループ変数内での一定の数値になると雲と障害物を発生させる
    - またplaneクラスとBulletクラスをsprite.guroupcolideを用いて当たり判定を行い衝突したらHPを-10するといった処理を行いＨＰ=0となるとプログラムは
    終了する
    - HPクラスはプレイヤーのHＰを表している障害物に当たるごとに２０マイナスされる０になるとプログラムが終了になる

