
# エラーが発生したら

ひよこすくりぷとは、間違った使いかたをしてしまったり、プログラムに含まれるバグなどによってエラーが発生することがあります。
もし運悪くエラーに遭遇してしまったときは、焦らずに出てきたエラー文を、よく読んでみましょう。
もしかしたら問題解決のヒントがあるかもしれません。

こちらのページでは、数あるエラーの中から遭遇しやすそうなものを、開発者の負担にならない程度に紹介しています。

* [対象のコンピューターによって拒否されたため、接続できませんでした。](#対象のコンピューターによって拒否されたため接続できませんでした)
* [KeyError: 'キャラクター名'](#keyerror-キャラクター名)
* [Could not find voice name by XXX in XXX ](#could-not-find-voice-name-by-xxx-in-xxx)
* [Could not find speaker name by XXX in XXX ](#could-not-find-speaker-name-by-xxx-in-xxx)
* [Could not change layer XXX visibility, because layer's name startswith '!' ](#could-not-change-layer-xxx-visibility-because-layers-name-startswith)
* [Could not change layer XXX to invisible, because layer's name startswith '\*' ](#could-not-change-layer-xxx-to-invisible-because-layers-name-startswith)
* [Could not find layer XXX in XXX ](#could-not-find-layer-xxx-in-xxx)

## 対象のコンピューターによって拒否されたため、接続できませんでした。

接続先のサーバが見つからなかったときに発生するエラーです。

多くの場合、ひよこすくりぷと実行時にVOICEVOXが起動していないことが原因だと思われます。
ひよこすくりぷととVOICEVOXを連携させるには、あらかじめVOICEVOXを起動している必要があります。

VOICEVOXが起動しているにも関わらず同じようなエラーが発生するならば、
VOICEVOXのサーバ設定と、ひよこすくりぷとの連携部分の設定があっているかを一度ご確認ください。

## KeyError: 'キャラクター名'

キャラクター名が合成音声ソフトのキャラクターならば、
AssistantSeikaが起動していない、もしくは、製品スキャンが行われていない可能性があります。
もし起動していなければ、AssistantSeikaを起動し、製品スキャンを行う必要があります。

## Could not find voice name by XXX in XXX 

`#声設定名`で存在しない声設定を呼び出そうとすると発生するエラーです。

## Could not find speaker name by XXX in XXX 

`@人物名`で存在しない人物名を呼び出そうとすると発生するエラーです。

## Could not change layer XXX visibility, because layer's name startswith '!' 

PSDToolKitの立ち絵で、`!`から始まるレイヤーを変更したときに発生するエラーです。

## Could not change layer XXX to invisible, because layer's name startswith '\*' 

PSDToolKitの立ち絵で、`*`から始まるレイヤーを非表示にしようとしたときに発生するエラーです。

## Could not find layer XXX in XXX 

PSDToolKitの立ち絵で存在しないレイヤーを変更しようとしたときに発生するエラーです。

## Couldn't find ffmpeg or avconv - defaulting to ffmpeg, but may not work

ひよこすくりぷとに ffmpeg が導入されていないときに表示される警告文です。
WAV形式以外の音声ファイルを取り扱わないのであれば無視していただいても問題ありません。
