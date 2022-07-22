
# ひよこすくりぷと(試験版)

![](https://img.shields.io/badge/version-0.1.0-gray)
![](https://img.shields.io/badge/python-3.10-blue)
![](https://img.shields.io/github/license/tikubonn/HiyokoScript)

https://user-images.githubusercontent.com/7812951/173231979-f917317e-220c-4940-b47f-5a1c1b0e96ba.mp4

ひよこすくりぷとは動画編集の補助を目的に開発されたスクリプト言語です。
このスクリプト言語は脚本ライクな構文から「音声」「字幕」「立ち絵」などを含むエクスポートファイルを生成します。
生成されたエクスポートファイルは、AviUtlにインポートすることで動画として出力することができます。

```txt
--この文章は読み上げられません

$背景画像=花.jpg
@ずんだもん&つむぎちゃん

#ずん 皆様はじめまして、投稿者代理のずんだもんと
#つむにこ 春日部つむぎちゃんです
#つむ 突然ですが、テキストから音声字幕などを自動生成してくれるスクリプト言語をつくりました
まだまだ試作段階ですが、興味があれば使ってみてください
#ずんにこ&つむにこ それでは、ご視聴ありがとうございました
```

## 対応しているAviUtl環境

* AviUtl version 1.10: http://spring-fragrance.mints.ne.jp/aviutl/
* 拡張編集 version 0.92: http://spring-fragrance.mints.ne.jp/aviutl/
* PSDToolKit v0.1.3: https://github.com/oov/aviutl_psdtoolkit
* PSDToolKit v0.2.0beta60: https://github.com/oov/aviutl_psdtoolkit

## 対応している音声合成ソフト

* VOICEVOX 0.11.4: https://voicevox.hiroshiba.jp/
* SofTalk 1.93.28: https://w.atwiki.jp/softalk/
* AssistantSeika 20220504/u: https://hgotoh.jp/wiki/doku.php/documents/voiceroid/assistantseika/assistantseika-000

## つかいかた

**まず、本ソフトウェアの実行前に、登場させるキャラクターの合成音声ソフトを起動してください。**
例えば、ずんだもんを会話に登場させるならば、本ソフトの実行前にVOCEVOXを立ちあげる必要があります。

```txt
#ずん ずんだもん可愛いって言って？
#つむ ｽﾞﾝﾀﾞﾓﾝｶﾜｲｲﾔｯﾀｰ
```

合成音声ソフトの起動が終わったら、試しにこちらの文章を変換してみましょう。
まずはメモ帳でもなんでもよいので、こちらの文章を適当なファイルに保存してください。

保存が終わったら、ダウンロードした`HiyokoScriptGUI.exe`を起動します。
起動すると、小さな画面が表示されますので、その中にある**入力ファイル**の項目から、先ほど保存したファイルを指定します。

ファイルの指定が終わったら、最後に**実行する**ボタンを押し保存先のファイルを指定してください。
すると変換処理が開始されるので、あとは待つだけです。

### さらに詳細なつかいかた

ひよこすくりぷとの文法や、設定ファイルの詳細について知りたい方は、
関連する情報を別ページにまとめましたのでこれらのページをご参照ください。
特に、新しいキャラクターをひよこすくりぷとに追加する際に、設定ファイルの知識が必要になります。

* [ひよこすくりぷとの文法説明書](./README_SYNTAX.md)
* [ひよこすくりぷとの設定ファイル説明書](./README_CONFIG.md)
* [エラーが出たら](./README_ERROR.md)

## 免責事項

本ソフトウェアは無保証で提供されます。
よって、使用者が本ソフトウェアを使用したことによって何かしらの損害を被ったとしても、本ソフトウェアの開発者は一切の責任を負いません。
これに同意できない方は本ソフトウェアの使用をしないでください。

## インストール

本ソフトウェアはダウンロードしてすぐに使用することができます。
ただし、いくつかの機能を有効化するためには、前もって設定ファイルの編集が必要になる場合がございます。

具体的な例

* [VOICEVOXを使った音声合成](./README_CONFIG.md#voicevoxとの連携を設定する)
* [AssistantSeika(VOICEROID/CeVIO)を使った音声合成](./README_CONFIG.md#assistantseikaとの連携を設定する)
* [SofTalkを使った音声合成](./README_CONFIG.md#softalkとの連携を設定する)
* [PSDToolKitを使った立ち絵](./README_CONFIG.md#人物に立ち絵を設定する)
* [MP3/OGG形式への対応](#mp3ogg形式への対応)

### MP3/OGG形式への対応

ひよこすくりぷとは単体でMP3/OGG形式の音声ファイルに対応していません。
そのため、それらの音声ファイルに対応するためには、別途FFmpegという外部ソフトウェアが必要になります。
なお、導入にあたり、新たにソフトウェアをインストールする必要はありません。

https://ffmpeg.org/

ひよこすくりぷとにFFmpegを導入するには、まず上記のウェブサイトから実行ファイルをダウンロードしてください。
ダウンロードが終わったら、そのファイルを解凍し、中に入っている実行ファイル`ffmpeg.exe`・`ffplay.exe`・`ffprobe.exe`を`HiyokoScript.exe`と同じフォルダにコピーしてください。
最後に`HiyokoScriptGUI.exe`を起動し、問題なく動作していれば導入は完了です。

## エラーが出たら

まずは、設定ファイルやスクリプトが正しく書かれているかを確認しましょう。
同梱されているサンプルファイル集`Sample`には、動作確認済みのスクリプトがたくさんあります。
そちらと見比べてみるのもよいかもしれません。

ひよこすくりぷとの設定ファイルのなかには、未設定のままでは動作しないものもあります。
詳細はこちらのページをご確認ください。

* [ひよこすくりぷとの設定ファイル説明書](./README_CONFIG.md)

## Build

ひよこすくりぷとは v0.2.0 からパッケージ管理に [pipenv](https://pipenv-ja.readthedocs.io/ja/translate-ja/) を使用するようになりました。
ひよこすくりぷとをビルドするにはこれらのコマンドを実行してください。

```cmd
chcp 65001
make setup 
make release
```

### Author's environments 

著者の開発環境はこのようになってます。参考までに。

* Microsoft Windows 10 Home 
* Intel(R) Core(TM) i7-8700 CPU @ 3.20GHz、3192 Mhz、6 個のコア、12 個のロジカル プロセッサ 
* RAM 8.00 GB
* Python 3.10.1 
* GNU Make 4.3 Built for x86_64-pc-cygwin 

## Package requirements 

* exolib: https://github.com/tikubonn/exolib
* json5: https://github.com/dpranke/pyjson5
* Nuitka: https://nuitka.net
* opencv-python: https://github.com/skvark/opencv-python
* psdtoolkit-util: https://github.com/tikubonn/psdtoolkit-util
* pydub: http://pydub.com
* requests: https://requests.readthedocs.io
* tkinterdnd2: https://github.com/Eliav2/tkinterdnd2
* ordered-set: https://github.com/rspeer/ordered-set <!-- added manually -->

## License

HiyokoScript released under [The GNU General Public License v3.0](./LICENSE).<br>
HiyokoScript's icon released under [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/).<br>
Pictures and videos in SampleBackgroundImage, SampleBackgroundVideo, SampleCharacterGraphic released under the [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).<br>

* aggdraw: [Python (MIT style)](./LICENSE_THIRD_PARTY)
* attrs: [MIT](./LICENSE_THIRD_PARTY)
* certifi: [MPL-2.0](./LICENSE_THIRD_PARTY)
* charset-normalizer: [MIT](./LICENSE_THIRD_PARTY)
* docopt: [MIT](./LICENSE_THIRD_PARTY)
* exofile: [MIT](./LICENSE_THIRD_PARTY)
* exolib: [MIT](./LICENSE_THIRD_PARTY)
* idna: [BSD-3-Clause](./LICENSE_THIRD_PARTY)
* imageio: [BSD-2-Clause](./LICENSE_THIRD_PARTY)
* json5: [Apache](./LICENSE_THIRD_PARTY)
* Nuitka: [Apache License, Version 2.0](./LICENSE_THIRD_PARTY)
* numpy: [BSD](./LICENSE_THIRD_PARTY)
* opencv-python: [MIT](./LICENSE_THIRD_PARTY)
* packaging: [BSD-2-Clause or Apache-2.0](./LICENSE_THIRD_PARTY)
* Pillow: [HPND](./LICENSE_THIRD_PARTY)
* psd-tools: [MIT License](./LICENSE_THIRD_PARTY)
* psdtoolkit-util: [MIT](./LICENSE_THIRD_PARTY)
* pydub: [MIT](./LICENSE_THIRD_PARTY)
* PyWavelets: [MIT](./LICENSE_THIRD_PARTY)
* requests: [Apache 2.0](./LICENSE_THIRD_PARTY)
* scikit-image: [Modified BSD](./LICENSE_THIRD_PARTY)
* scipy: [BSD](./LICENSE_THIRD_PARTY)
* tifffile: [BSD](./LICENSE_THIRD_PARTY)
* urllib3: [MIT](./LICENSE_THIRD_PARTY)
* networkx: [the 3-clause BSD license](./LICENSE_THIRD_PARTY) <!-- added manually ref from https://github.com/networkx/networkx -->
* ordered-set: [MIT license](./LICENSE_THIRD_PARTY) <!-- added manually ref from https://github.com/rspeer/ordered-set -->
* pyparsing: [MIT license](./LICENSE_THIRD_PARTY) <!-- added manually ref from https://github.com/pyparsing/pyparsing -->
* tkinterdnd2: [MIT license](./LICENSE_THIRD_PARTY) <!-- added manually ref from https://github.com/Eliav2/tkinterdnd2 -->
* Python: [Python Software Foundation License](./LICENSE_THIRD_PARTY) <!-- added manually ref from https://github.com/python/cpython -->
