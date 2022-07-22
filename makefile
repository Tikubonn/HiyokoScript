	
export LANG=ja_JP.UTF-8 #CP932 cause character corruption when mkdir.

ifeq ($(EXE), 1)
export HIYOKO_SCRIPT_COMMAND=./HiyokoScript.exe
export HIYOKO_SCRIPT_GUI_COMMAND=./HiyokoScriptGUI.exe
export HIYOKO_SCRIPT_EDITOR_COMMAND=./HiyokoScriptEditor.exe
else
export HIYOKO_SCRIPT_COMMAND=pipenv run python HiyokoScript.py
export HIYOKO_SCRIPT_GUI_COMMAND=pipenv run python HiyokoScriptGUI.py
export HIYOKO_SCRIPT_EDITOR_COMMAND=pipenv run python HiyokoScriptEditor.py
endif

.PHONY: release
release:
	make HiyokoScript.zip

.PHONY: setup
setup:
	pip install pipenv
	pip install pip-license-gen
	pipenv install 

.PHONY: test
test: 
	pipenv run python -m unittest
	make test-project -B #always make.
	make Sample -B #always make.

test-project: test-project/assistant-seika

test-project/assistant-seika: test-project/assistant-seika/test-assistant-seika-speaker 

test-project/assistant-seika/test-assistant-seika-speaker: test-project/assistant-seika/test-assistant-seika-speaker/test.exo test-project/assistant-seika/test-assistant-seika-speaker2/test.exo

test-project/assistant-seika/test-assistant-seika-speaker/test.exo: test-project/assistant-seika/test-assistant-seika-speaker/test.txt test-project/assistant-seika/test-assistant-seika-speaker/test.json
	$(HIYOKO_SCRIPT_COMMAND) test-project/assistant-seika/test-assistant-seika-speaker/test.txt --config-file test-project/assistant-seika/test-assistant-seika-speaker/test.json -o test-project/assistant-seika/test-assistant-seika-speaker/test.exo

test-project/assistant-seika/test-assistant-seika-speaker2/test.exo: test-project/assistant-seika/test-assistant-seika-speaker2/test.txt test-project/assistant-seika/test-assistant-seika-speaker2/test.json
	$(HIYOKO_SCRIPT_COMMAND) test-project/assistant-seika/test-assistant-seika-speaker2/test.txt --config-file test-project/assistant-seika/test-assistant-seika-speaker2/test.json -o test-project/assistant-seika/test-assistant-seika-speaker2/test.exo

HiyokoScript.zip: dist 
	cd dist && pipenv run python -m zipfile -c ../HiyokoScript.zip * 

dist: dist/HiyokoScript.exe dist/HiyokoScriptGUI.exe dist/HiyokoScriptEditor.exe dist/config.json dist/language.gui.json dist/language.editor.json dist/README.md dist/README_SYNTAX.md dist/README_CONFIG.md dist/README_ERROR.md dist/LICENSE dist/LICENSE_THIRD_PARTY dist/picture dist/config dist/Sample dist/SampleBackgroundImage dist/SampleBackgroundVideo dist/SampleCharacterGraphic dist/SampleBGM dist/SampleSE

dist/HiyokoScript.exe: HiyokoScript.exe
	mkdir -p dist
	cp HiyokoScript.exe dist/HiyokoScript.exe

dist/HiyokoScriptGUI.exe: HiyokoScriptGUI.exe
	mkdir -p dist
	cp HiyokoScriptGUI.exe dist/HiyokoScriptGUI.exe

dist/HiyokoScriptEditor.exe: HiyokoScriptEditor.exe
	mkdir -p dist
	cp HiyokoScriptEditor.exe dist/HiyokoScriptEditor.exe

HiyokoScript.exe: HiyokoScript.py picture/HiyokoScript.ico
	pipenv run nuitka --onefile --follow-imports --include-package=json5 --enable-plugin=numpy --enable-plugin=tk-inter --windows-icon-from-ico=picture/HiyokoScript.ico HiyokoScript.py

HiyokoScriptGUI.exe: HiyokoScriptGUI.py picture/HiyokoScriptGUI.ico
	pipenv run nuitka --onefile --follow-imports --include-package=json5 --enable-plugin=numpy --enable-plugin=tk-inter --windows-icon-from-ico=picture/HiyokoScriptGUI.ico HiyokoScriptGUI.py

HiyokoScriptEditor.exe: HiyokoScriptEditor.py picture/HiyokoScriptEditor.ico
	pipenv run nuitka --onefile --follow-imports --include-package=json5 --enable-plugin=numpy --enable-plugin=tk-inter --windows-icon-from-ico=picture/HiyokoScriptEditor.ico HiyokoScriptEditor.py

#readme files

dist/README.md: README.md
	cp README.md dist/README.md

dist/README_SYNTAX.md: README_SYNTAX.md
	cp README_SYNTAX.md dist/README_SYNTAX.md

dist/README_CONFIG.md: README_CONFIG.md
	cp README_CONFIG.md dist/README_CONFIG.md

dist/README_ERROR.md: README_ERROR.md
	cp README_ERROR.md dist/README_ERROR.md

#license files 

 dist/LICENSE: LICENSE
	cp LICENSE dist/LICENSE

dist/LICENSE_THIRD_PARTY: LICENSE_THIRD_PARTY
	mkdir -p dist
	cp LICENSE_THIRD_PARTY dist/LICENSE_THIRD_PARTY

LICENSE_THIRD_PARTY: Pipfile Pipfile.lock pip-license-gen.json
	pipenv run pip-license-gen > LICENSE_THIRD_PARTY
	pipenv run pip-license-gen --from-json pip-license-gen.json >> LICENSE_THIRD_PARTY

#config files

dist/config.json: config.json utility/json-editor.py
	mkdir -p dist
	cp config.json dist/config.json
	pipenv run python utility/json-editor.py dist/config.json --set softalk.softalkw_exe_path=\"\" assistant_seika.seika_say2_exe_path=\"\" --delete hiyoko_script

dist/language.gui.json: language.gui.json
	mkdir -p dist
	cp language.gui.json dist/language.gui.json

dist/language.editor.json: language.editor.json
	mkdir -p dist
	cp language.editor.json dist/language.editor.json

#picture

dist/picture: dist/picture/HiyokoScript.ico dist/picture/HiyokoScriptGUI.ico dist/picture/HiyokoScriptEditor.ico dist/picture/HiyokoScriptGUIHeader.png

dist/picture/HiyokoScript.ico: picture/HiyokoScript.ico
	mkdir -p dist/picture
	cp picture/HiyokoScript.ico dist/picture/HiyokoScript.ico

dist/picture/HiyokoScriptGUI.ico: picture/HiyokoScriptGUI.ico
	mkdir -p dist/picture
	cp picture/HiyokoScriptGUI.ico dist/picture/HiyokoScriptGUI.ico

dist/picture/HiyokoScriptEditor.ico: picture/HiyokoScriptEditor.ico
	mkdir -p dist/picture
	cp picture/HiyokoScriptEditor.ico dist/picture/HiyokoScriptEditor.ico

dist/picture/HiyokoScriptGUIHeader.png: picture/HiyokoScriptGUIHeader.png
	mkdir -p dist/picture
	cp picture/HiyokoScriptGUIHeader.png dist/picture/HiyokoScriptGUIHeader.png

#config 

dist/config: config 
	cp -r config dist/config 

#Sample 

dist/Sample: dist/Sample/psdtoolkit-0.2 dist/Sample/psdtoolkit-0.1.3 dist/Sample/AssistantSeika.txt dist/Sample/AssistantSeika.mp4 dist/Sample/BGM.txt dist/Sample/BGM.mp4 dist/Sample/SE.txt dist/Sample/SE.mp4 dist/Sample/SofTalk.txt dist/Sample/SofTalk.mp4 dist/Sample/VOICEVOX.txt dist/Sample/VOICEVOX.mp4 dist/Sample/ぐにゃぐにゃ.txt dist/Sample/ぐにゃぐにゃ.mp4 dist/Sample/ぴょんぴょん.txt dist/Sample/ぴょんぴょん.mp4 dist/Sample/もにゅもにゅ.txt dist/Sample/もにゅもにゅ.mp4 dist/Sample/挨拶.txt dist/Sample/挨拶.mp4 dist/Sample/立ち絵指定.txt dist/Sample/立ち絵指定.mp4 dist/Sample/立ち絵指定2.txt dist/Sample/立ち絵指定2.mp4 dist/Sample/立ち絵指定3.txt dist/Sample/立ち絵指定3.mp4 dist/Sample/背景画像.txt dist/Sample/背景画像.mp4 dist/Sample/背景色.txt dist/Sample/背景色.mp4 dist/Sample/話者指定.txt dist/Sample/話者指定.mp4 dist/Sample/話者指定2.txt dist/Sample/話者指定2.mp4 dist/Sample/背景動画.txt dist/Sample/背景動画.mp4 dist/Sample/字幕.txt dist/Sample/字幕.mp4 dist/Sample/自動ぴょんぴょん.txt dist/Sample/自動ぴょんぴょん.mp4 dist/Sample/自動もにゅもにゅ.txt dist/Sample/自動もにゅもにゅ.mp4

dist/Sample/psdtoolkit-0.2: dist/Sample/psdtoolkit-0.2/坂本あひる dist/Sample/psdtoolkit-0.2/MtU

dist/Sample/psdtoolkit-0.2/坂本あひる: dist/Sample/psdtoolkit-0.2/坂本あひる/ずんだもん.txt dist/Sample/psdtoolkit-0.2/坂本あひる/ずんだもん.mp4 dist/Sample/psdtoolkit-0.2/坂本あひる/四国めたん.txt dist/Sample/psdtoolkit-0.2/坂本あひる/四国めたん.mp4 dist/Sample/psdtoolkit-0.2/坂本あひる/春日部つむぎ.txt dist/Sample/psdtoolkit-0.2/坂本あひる/春日部つむぎ.mp4 dist/Sample/psdtoolkit-0.2/坂本あひる/九州そら.txt dist/Sample/psdtoolkit-0.2/坂本あひる/九州そら.mp4 dist/Sample/psdtoolkit-0.2/坂本あひる/雨晴はう.txt dist/Sample/psdtoolkit-0.2/坂本あひる/雨晴はう.mp4 dist/Sample/psdtoolkit-0.2/坂本あひる/坂本あひる.json

dist/Sample/psdtoolkit-0.2/坂本あひる/ずんだもん.txt: Sample/psdtoolkit-0.2/坂本あひる/ずんだもん.txt 
	mkdir -p dist/Sample/psdtoolkit-0.2/坂本あひる
	cp Sample/psdtoolkit-0.2/坂本あひる/ずんだもん.txt dist/Sample/psdtoolkit-0.2/坂本あひる/ずんだもん.txt

dist/Sample/psdtoolkit-0.2/坂本あひる/ずんだもん.mp4: Sample/psdtoolkit-0.2/坂本あひる/ずんだもん.mp4
	mkdir -p dist/Sample/psdtoolkit-0.2/坂本あひる
	cp Sample/psdtoolkit-0.2/坂本あひる/ずんだもん.mp4 dist/Sample/psdtoolkit-0.2/坂本あひる/ずんだもん.mp4

dist/Sample/psdtoolkit-0.2/坂本あひる/四国めたん.txt: Sample/psdtoolkit-0.2/坂本あひる/四国めたん.txt 
	mkdir -p dist/Sample/psdtoolkit-0.2/坂本あひる
	cp Sample/psdtoolkit-0.2/坂本あひる/四国めたん.txt dist/Sample/psdtoolkit-0.2/坂本あひる/四国めたん.txt

dist/Sample/psdtoolkit-0.2/坂本あひる/四国めたん.mp4: Sample/psdtoolkit-0.2/坂本あひる/四国めたん.mp4
	mkdir -p dist/Sample/psdtoolkit-0.2/坂本あひる
	cp Sample/psdtoolkit-0.2/坂本あひる/四国めたん.mp4 dist/Sample/psdtoolkit-0.2/坂本あひる/四国めたん.mp4

dist/Sample/psdtoolkit-0.2/坂本あひる/春日部つむぎ.txt: Sample/psdtoolkit-0.2/坂本あひる/春日部つむぎ.txt 
	mkdir -p dist/Sample/psdtoolkit-0.2/坂本あひる
	cp Sample/psdtoolkit-0.2/坂本あひる/春日部つむぎ.txt dist/Sample/psdtoolkit-0.2/坂本あひる/春日部つむぎ.txt

dist/Sample/psdtoolkit-0.2/坂本あひる/春日部つむぎ.mp4: Sample/psdtoolkit-0.2/坂本あひる/春日部つむぎ.mp4
	mkdir -p dist/Sample/psdtoolkit-0.2/坂本あひる
	cp Sample/psdtoolkit-0.2/坂本あひる/春日部つむぎ.mp4 dist/Sample/psdtoolkit-0.2/坂本あひる/春日部つむぎ.mp4

dist/Sample/psdtoolkit-0.2/坂本あひる/九州そら.txt: Sample/psdtoolkit-0.2/坂本あひる/九州そら.txt 
	mkdir -p dist/Sample/psdtoolkit-0.2/坂本あひる
	cp Sample/psdtoolkit-0.2/坂本あひる/九州そら.txt dist/Sample/psdtoolkit-0.2/坂本あひる/九州そら.txt

dist/Sample/psdtoolkit-0.2/坂本あひる/九州そら.mp4: Sample/psdtoolkit-0.2/坂本あひる/九州そら.mp4
	mkdir -p dist/Sample/psdtoolkit-0.2/坂本あひる
	cp Sample/psdtoolkit-0.2/坂本あひる/九州そら.mp4 dist/Sample/psdtoolkit-0.2/坂本あひる/九州そら.mp4

dist/Sample/psdtoolkit-0.2/坂本あひる/雨晴はう.txt: Sample/psdtoolkit-0.2/坂本あひる/雨晴はう.txt 
	mkdir -p dist/Sample/psdtoolkit-0.2/坂本あひる
	cp Sample/psdtoolkit-0.2/坂本あひる/雨晴はう.txt dist/Sample/psdtoolkit-0.2/坂本あひる/雨晴はう.txt

dist/Sample/psdtoolkit-0.2/坂本あひる/雨晴はう.mp4: Sample/psdtoolkit-0.2/坂本あひる/雨晴はう.mp4
	mkdir -p dist/Sample/psdtoolkit-0.2/坂本あひる
	cp Sample/psdtoolkit-0.2/坂本あひる/雨晴はう.mp4 dist/Sample/psdtoolkit-0.2/坂本あひる/雨晴はう.mp4

dist/Sample/psdtoolkit-0.2/坂本あひる/坂本あひる.json: Sample/psdtoolkit-0.2/坂本あひる/坂本あひる.json
	mkdir -p dist/Sample/psdtoolkit-0.2/坂本あひる
	cp Sample/psdtoolkit-0.2/坂本あひる/坂本あひる.json dist/Sample/psdtoolkit-0.2/坂本あひる/坂本あひる.json
	pipenv run python utility/json-editor.py dist/Sample/psdtoolkit-0.2/坂本あひる/坂本あひる.json --set search_paths=\[\] 

dist/Sample/psdtoolkit-0.2/MtU: dist/Sample/psdtoolkit-0.2/MtU/結月ゆかり.txt dist/Sample/psdtoolkit-0.2/MtU/結月ゆかり.mp4 dist/Sample/psdtoolkit-0.2/MtU/弦巻マキ.txt dist/Sample/psdtoolkit-0.2/MtU/弦巻マキ.mp4 dist/Sample/psdtoolkit-0.2/MtU/紲星あかり.txt dist/Sample/psdtoolkit-0.2/MtU/紲星あかり.mp4 dist/Sample/psdtoolkit-0.2/MtU/MtU.json

dist/Sample/psdtoolkit-0.2/MtU/結月ゆかり.txt: Sample/psdtoolkit-0.2/MtU/結月ゆかり.txt 
	mkdir -p dist/Sample/psdtoolkit-0.2/MtU
	cp Sample/psdtoolkit-0.2/MtU/結月ゆかり.txt dist/Sample/psdtoolkit-0.2/MtU/結月ゆかり.txt

dist/Sample/psdtoolkit-0.2/MtU/結月ゆかり.mp4: Sample/psdtoolkit-0.2/MtU/結月ゆかり.mp4
	mkdir -p dist/Sample/psdtoolkit-0.2/MtU
	cp Sample/psdtoolkit-0.2/MtU/結月ゆかり.mp4 dist/Sample/psdtoolkit-0.2/MtU/結月ゆかり.mp4

dist/Sample/psdtoolkit-0.2/MtU/弦巻マキ.txt: Sample/psdtoolkit-0.2/MtU/弦巻マキ.txt 
	mkdir -p dist/Sample/psdtoolkit-0.2/MtU
	cp Sample/psdtoolkit-0.2/MtU/弦巻マキ.txt dist/Sample/psdtoolkit-0.2/MtU/弦巻マキ.txt

dist/Sample/psdtoolkit-0.2/MtU/弦巻マキ.mp4: Sample/psdtoolkit-0.2/MtU/弦巻マキ.mp4
	mkdir -p dist/Sample/psdtoolkit-0.2/MtU
	cp Sample/psdtoolkit-0.2/MtU/弦巻マキ.mp4 dist/Sample/psdtoolkit-0.2/MtU/弦巻マキ.mp4

dist/Sample/psdtoolkit-0.2/MtU/紲星あかり.txt: Sample/psdtoolkit-0.2/MtU/紲星あかり.txt 
	mkdir -p dist/Sample/psdtoolkit-0.2/MtU
	cp Sample/psdtoolkit-0.2/MtU/紲星あかり.txt dist/Sample/psdtoolkit-0.2/MtU/紲星あかり.txt

dist/Sample/psdtoolkit-0.2/MtU/紲星あかり.mp4: Sample/psdtoolkit-0.2/MtU/紲星あかり.mp4
	mkdir -p dist/Sample/psdtoolkit-0.2/MtU
	cp Sample/psdtoolkit-0.2/MtU/紲星あかり.mp4 dist/Sample/psdtoolkit-0.2/MtU/紲星あかり.mp4

dist/Sample/psdtoolkit-0.2/MtU/MtU.json: Sample/psdtoolkit-0.2/MtU/MtU.json
	mkdir -p dist/Sample/psdtoolkit-0.2/MtU
	cp Sample/psdtoolkit-0.2/MtU/MtU.json dist/Sample/psdtoolkit-0.2/MtU/MtU.json
	pipenv run python utility/json-editor.py dist/Sample/psdtoolkit-0.2/MtU/MtU.json --set assistant_seika.seika_say2_exe_path=\[\] search_paths=\[\] 

dist/Sample/psdtoolkit-0.1.3: dist/Sample/psdtoolkit-0.1.3/坂本あひる

dist/Sample/psdtoolkit-0.1.3/坂本あひる: dist/Sample/psdtoolkit-0.1.3/坂本あひる/ずんだもん.txt dist/Sample/psdtoolkit-0.1.3/坂本あひる/ずんだもん.mp4 dist/Sample/psdtoolkit-0.1.3/坂本あひる/四国めたん.txt dist/Sample/psdtoolkit-0.1.3/坂本あひる/四国めたん.mp4 dist/Sample/psdtoolkit-0.1.3/坂本あひる/春日部つむぎ.txt dist/Sample/psdtoolkit-0.1.3/坂本あひる/春日部つむぎ.mp4 dist/Sample/psdtoolkit-0.1.3/坂本あひる/坂本あひる.json

dist/Sample/psdtoolkit-0.1.3/坂本あひる/ずんだもん.txt: Sample/psdtoolkit-0.1.3/坂本あひる/ずんだもん.txt
	mkdir -p dist/Sample/psdtoolkit-0.1.3/坂本あひる
	cp Sample/psdtoolkit-0.1.3/坂本あひる/ずんだもん.txt dist/Sample/psdtoolkit-0.1.3/坂本あひる/ずんだもん.txt

dist/Sample/psdtoolkit-0.1.3/坂本あひる/ずんだもん.mp4: Sample/psdtoolkit-0.1.3/坂本あひる/ずんだもん.mp4
	mkdir -p dist/Sample/psdtoolkit-0.1.3/坂本あひる
	cp Sample/psdtoolkit-0.1.3/坂本あひる/ずんだもん.mp4 dist/Sample/psdtoolkit-0.1.3/坂本あひる/ずんだもん.mp4

dist/Sample/psdtoolkit-0.1.3/坂本あひる/四国めたん.txt: Sample/psdtoolkit-0.1.3/坂本あひる/四国めたん.txt
	mkdir -p dist/Sample/psdtoolkit-0.1.3/坂本あひる
	cp Sample/psdtoolkit-0.1.3/坂本あひる/四国めたん.txt dist/Sample/psdtoolkit-0.1.3/坂本あひる/四国めたん.txt

dist/Sample/psdtoolkit-0.1.3/坂本あひる/四国めたん.mp4: Sample/psdtoolkit-0.1.3/坂本あひる/四国めたん.mp4
	mkdir -p dist/Sample/psdtoolkit-0.1.3/坂本あひる
	cp Sample/psdtoolkit-0.1.3/坂本あひる/四国めたん.mp4 dist/Sample/psdtoolkit-0.1.3/坂本あひる/四国めたん.mp4

dist/Sample/psdtoolkit-0.1.3/坂本あひる/春日部つむぎ.txt: Sample/psdtoolkit-0.1.3/坂本あひる/春日部つむぎ.txt
	mkdir -p dist/Sample/psdtoolkit-0.1.3/坂本あひる
	cp Sample/psdtoolkit-0.1.3/坂本あひる/春日部つむぎ.txt dist/Sample/psdtoolkit-0.1.3/坂本あひる/春日部つむぎ.txt

dist/Sample/psdtoolkit-0.1.3/坂本あひる/春日部つむぎ.mp4: Sample/psdtoolkit-0.1.3/坂本あひる/春日部つむぎ.mp4
	mkdir -p dist/Sample/psdtoolkit-0.1.3/坂本あひる
	cp Sample/psdtoolkit-0.1.3/坂本あひる/春日部つむぎ.mp4 dist/Sample/psdtoolkit-0.1.3/坂本あひる/春日部つむぎ.mp4

dist/Sample/psdtoolkit-0.1.3/坂本あひる/坂本あひる.json: Sample/psdtoolkit-0.1.3/坂本あひる/坂本あひる.json
	mkdir -p dist/Sample/psdtoolkit-0.1.3/坂本あひる
	cp Sample/psdtoolkit-0.1.3/坂本あひる/坂本あひる.json dist/Sample/psdtoolkit-0.1.3/坂本あひる/坂本あひる.json

dist/Sample/AssistantSeika.txt: Sample/AssistantSeika.txt
	mkdir -p dist/Sample
	cp Sample/AssistantSeika.txt dist/Sample/AssistantSeika.txt 

dist/Sample/AssistantSeika.mp4: Sample/AssistantSeika.mp4
	mkdir -p dist/Sample
	cp Sample/AssistantSeika.mp4 dist/Sample/AssistantSeika.mp4

dist/Sample/BGM.txt: Sample/BGM.txt
	mkdir -p dist/Sample
	cp Sample/BGM.txt dist/Sample/BGM.txt 

dist/Sample/BGM.mp4: Sample/BGM.mp4
	mkdir -p dist/Sample
	cp Sample/BGM.mp4 dist/Sample/BGM.mp4

dist/Sample/SE.txt: Sample/SE.txt
	mkdir -p dist/Sample
	cp Sample/SE.txt dist/Sample/SE.txt 

dist/Sample/SE.mp4: Sample/SE.mp4
	mkdir -p dist/Sample
	cp Sample/SE.mp4 dist/Sample/SE.mp4

dist/Sample/SofTalk.txt: Sample/SofTalk.txt
	mkdir -p dist/Sample
	cp Sample/SofTalk.txt dist/Sample/SofTalk.txt 

dist/Sample/SofTalk.mp4: Sample/SofTalk.mp4
	mkdir -p dist/Sample
	cp Sample/SofTalk.mp4 dist/Sample/SofTalk.mp4

dist/Sample/VOICEVOX.txt: Sample/VOICEVOX.txt
	mkdir -p dist/Sample
	cp Sample/VOICEVOX.txt dist/Sample/VOICEVOX.txt 

dist/Sample/VOICEVOX.mp4: Sample/VOICEVOX.mp4
	mkdir -p dist/Sample
	cp Sample/VOICEVOX.mp4 dist/Sample/VOICEVOX.mp4

dist/Sample/ぐにゃぐにゃ.txt: Sample/ぐにゃぐにゃ.txt
	mkdir -p dist/Sample
	cp Sample/ぐにゃぐにゃ.txt dist/Sample/ぐにゃぐにゃ.txt 

dist/Sample/ぐにゃぐにゃ.mp4: Sample/ぐにゃぐにゃ.mp4
	mkdir -p dist/Sample
	cp Sample/ぐにゃぐにゃ.mp4 dist/Sample/ぐにゃぐにゃ.mp4

dist/Sample/ぴょんぴょん.txt: Sample/ぴょんぴょん.txt
	mkdir -p dist/Sample
	cp Sample/ぴょんぴょん.txt dist/Sample/ぴょんぴょん.txt 

dist/Sample/ぴょんぴょん.mp4: Sample/ぴょんぴょん.mp4
	mkdir -p dist/Sample
	cp Sample/ぴょんぴょん.mp4 dist/Sample/ぴょんぴょん.mp4

dist/Sample/もにゅもにゅ.txt: Sample/もにゅもにゅ.txt
	mkdir -p dist/Sample
	cp Sample/もにゅもにゅ.txt dist/Sample/もにゅもにゅ.txt 

dist/Sample/もにゅもにゅ.mp4: Sample/もにゅもにゅ.mp4
	mkdir -p dist/Sample
	cp Sample/もにゅもにゅ.mp4 dist/Sample/もにゅもにゅ.mp4

dist/Sample/挨拶.txt: Sample/挨拶.txt
	mkdir -p dist/Sample
	cp Sample/挨拶.txt dist/Sample/挨拶.txt 

dist/Sample/挨拶.mp4: Sample/挨拶.mp4
	mkdir -p dist/Sample
	cp Sample/挨拶.mp4 dist/Sample/挨拶.mp4

dist/Sample/立ち絵指定.txt: Sample/立ち絵指定.txt
	mkdir -p dist/Sample
	cp Sample/立ち絵指定.txt dist/Sample/立ち絵指定.txt 

dist/Sample/立ち絵指定.mp4: Sample/立ち絵指定.mp4
	mkdir -p dist/Sample
	cp Sample/立ち絵指定.mp4 dist/Sample/立ち絵指定.mp4

dist/Sample/立ち絵指定2.txt: Sample/立ち絵指定2.txt
	mkdir -p dist/Sample
	cp Sample/立ち絵指定2.txt dist/Sample/立ち絵指定2.txt 

dist/Sample/立ち絵指定2.mp4: Sample/立ち絵指定2.mp4
	mkdir -p dist/Sample
	cp Sample/立ち絵指定2.mp4 dist/Sample/立ち絵指定2.mp4

dist/Sample/立ち絵指定3.txt: Sample/立ち絵指定3.txt
	mkdir -p dist/Sample
	cp Sample/立ち絵指定3.txt dist/Sample/立ち絵指定3.txt 

dist/Sample/立ち絵指定3.mp4: Sample/立ち絵指定3.mp4
	mkdir -p dist/Sample
	cp Sample/立ち絵指定3.mp4 dist/Sample/立ち絵指定3.mp4

dist/Sample/背景画像.txt: Sample/背景画像.txt
	mkdir -p dist/Sample
	cp Sample/背景画像.txt dist/Sample/背景画像.txt 

dist/Sample/背景画像.mp4: Sample/背景画像.mp4
	mkdir -p dist/Sample
	cp Sample/背景画像.mp4 dist/Sample/背景画像.mp4

dist/Sample/背景色.txt: Sample/背景色.txt
	mkdir -p dist/Sample
	cp Sample/背景色.txt dist/Sample/背景色.txt 

dist/Sample/背景色.mp4: Sample/背景色.mp4
	mkdir -p dist/Sample
	cp Sample/背景色.mp4 dist/Sample/背景色.mp4

dist/Sample/話者指定.txt: Sample/話者指定.txt
	mkdir -p dist/Sample
	cp Sample/話者指定.txt dist/Sample/話者指定.txt 

dist/Sample/話者指定.mp4: Sample/話者指定.mp4
	mkdir -p dist/Sample
	cp Sample/話者指定.mp4 dist/Sample/話者指定.mp4

dist/Sample/話者指定2.txt: Sample/話者指定2.txt
	mkdir -p dist/Sample
	cp Sample/話者指定2.txt dist/Sample/話者指定2.txt 

dist/Sample/話者指定2.mp4: Sample/話者指定2.mp4
	mkdir -p dist/Sample
	cp Sample/話者指定2.mp4 dist/Sample/話者指定2.mp4

dist/Sample/背景動画.txt: Sample/背景動画.txt
	mkdir -p dist/Sample
	cp Sample/背景動画.txt dist/Sample/背景動画.txt 

dist/Sample/背景動画.mp4: Sample/背景動画.mp4
	mkdir -p dist/Sample
	cp Sample/背景動画.mp4 dist/Sample/背景動画.mp4

dist/Sample/字幕.txt: Sample/字幕.txt
	mkdir -p dist/Sample 
	cp Sample/字幕.txt dist/Sample/字幕.txt 

dist/Sample/字幕.mp4: Sample/字幕.mp4
	mkdir -p dist/Sample
	cp Sample/字幕.mp4 dist/Sample/字幕.mp4

dist/Sample/自動ぴょんぴょん.txt: Sample/自動ぴょんぴょん.txt
	mkdir -p dist/Sample 
	cp Sample/自動ぴょんぴょん.txt dist/Sample/自動ぴょんぴょん.txt 

dist/Sample/自動ぴょんぴょん.mp4: Sample/自動ぴょんぴょん.mp4
	mkdir -p dist/Sample
	cp Sample/自動ぴょんぴょん.mp4 dist/Sample/自動ぴょんぴょん.mp4

dist/Sample/自動もにゅもにゅ.txt: Sample/自動もにゅもにゅ.txt
	mkdir -p dist/Sample 
	cp Sample/自動もにゅもにゅ.txt dist/Sample/自動もにゅもにゅ.txt 

dist/Sample/自動もにゅもにゅ.mp4: Sample/自動もにゅもにゅ.mp4
	mkdir -p dist/Sample
	cp Sample/自動もにゅもにゅ.mp4 dist/Sample/自動もにゅもにゅ.mp4

#SampleBackgroundImage

dist/SampleBackgroundImage: dist/SampleBackgroundImage/花.jpg dist/SampleBackgroundImage/秋葉原.jpg dist/SampleBackgroundImage/ヨドバシアキバ.jpg

dist/SampleBackgroundImage/花.jpg: SampleBackgroundImage/花.jpg
	mkdir -p dist/SampleBackgroundImage
	cp SampleBackgroundImage/花.jpg dist/SampleBackgroundImage/花.jpg

dist/SampleBackgroundImage/秋葉原.jpg: SampleBackgroundImage/秋葉原.jpg
	mkdir -p dist/SampleBackgroundImage
	cp SampleBackgroundImage/秋葉原.jpg dist/SampleBackgroundImage/秋葉原.jpg

dist/SampleBackgroundImage/ヨドバシアキバ.jpg: SampleBackgroundImage/ヨドバシアキバ.jpg
	mkdir -p dist/SampleBackgroundImage
	cp SampleBackgroundImage/ヨドバシアキバ.jpg dist/SampleBackgroundImage/ヨドバシアキバ.jpg

#SampleBackgroundVideo

dist/SampleBackgroundVideo: dist/SampleBackgroundVideo/渦巻.mp4 dist/SampleBackgroundVideo/モザイク.mp4 dist/SampleBackgroundVideo/雪.mp4

dist/SampleBackgroundVideo/渦巻.mp4: SampleBackgroundVideo/渦巻.mp4
	mkdir -p dist/SampleBackgroundVideo
	cp SampleBackgroundVideo/渦巻.mp4 dist/SampleBackgroundVideo/渦巻.mp4

dist/SampleBackgroundVideo/モザイク.mp4: SampleBackgroundVideo/モザイク.mp4
	mkdir -p dist/SampleBackgroundVideo
	cp SampleBackgroundVideo/モザイク.mp4 dist/SampleBackgroundVideo/モザイク.mp4

dist/SampleBackgroundVideo/雪.mp4: SampleBackgroundVideo/雪.mp4
	mkdir -p dist/SampleBackgroundVideo
	cp SampleBackgroundVideo/雪.mp4 dist/SampleBackgroundVideo/雪.mp4

#SampleBGM

dist/SampleBGM: dist/SampleBGM/海.wav dist/SampleBGM/戦闘機.wav

dist/SampleBGM/海.wav: SampleBGM/海.wav
	mkdir -p dist/SampleBGM
	cp SampleBGM/海.wav dist/SampleBGM/海.wav

dist/SampleBGM/戦闘機.wav: SampleBGM/戦闘機.wav
	mkdir -p dist/SampleBGM
	cp SampleBGM/戦闘機.wav dist/SampleBGM/戦闘機.wav

#SampleCharacterGraphic

dist/SampleCharacterGraphic: dist/SampleCharacterGraphic/ずんだもん.png dist/SampleCharacterGraphic/ずんだもん喜.png dist/SampleCharacterGraphic/ずんだもん煽.png dist/SampleCharacterGraphic/ずんだもん怒.png dist/SampleCharacterGraphic/ずんだもん悲.png dist/SampleCharacterGraphic/春日部つむぎ.png dist/SampleCharacterGraphic/春日部つむぎ喜.png dist/SampleCharacterGraphic/春日部つむぎ煽.png dist/SampleCharacterGraphic/春日部つむぎ怒.png dist/SampleCharacterGraphic/春日部つむぎ悲.png dist/SampleCharacterGraphic/結月ゆかり.png dist/SampleCharacterGraphic/結月ゆかり喜.png dist/SampleCharacterGraphic/結月ゆかり煽.png dist/SampleCharacterGraphic/結月ゆかり怒.png dist/SampleCharacterGraphic/結月ゆかり悲.png dist/SampleCharacterGraphic/れいむ.png dist/SampleCharacterGraphic/れいむ喜.png dist/SampleCharacterGraphic/れいむ煽.png dist/SampleCharacterGraphic/れいむ怒.png dist/SampleCharacterGraphic/れいむ悲.png 

dist/SampleCharacterGraphic/ずんだもん.png: SampleCharacterGraphic/ずんだもん.png
	mkdir -p dist/SampleCharacterGraphic 
	cp SampleCharacterGraphic/ずんだもん.png dist/SampleCharacterGraphic/ずんだもん.png

dist/SampleCharacterGraphic/ずんだもん喜.png: SampleCharacterGraphic/ずんだもん喜.png
	mkdir -p dist/SampleCharacterGraphic 
	cp SampleCharacterGraphic/ずんだもん喜.png dist/SampleCharacterGraphic/ずんだもん喜.png

dist/SampleCharacterGraphic/ずんだもん煽.png: SampleCharacterGraphic/ずんだもん煽.png
	mkdir -p dist/SampleCharacterGraphic 
	cp SampleCharacterGraphic/ずんだもん煽.png dist/SampleCharacterGraphic/ずんだもん煽.png

dist/SampleCharacterGraphic/ずんだもん怒.png: SampleCharacterGraphic/ずんだもん怒.png
	mkdir -p dist/SampleCharacterGraphic 
	cp SampleCharacterGraphic/ずんだもん怒.png dist/SampleCharacterGraphic/ずんだもん怒.png

dist/SampleCharacterGraphic/ずんだもん悲.png: SampleCharacterGraphic/ずんだもん悲.png
	mkdir -p dist/SampleCharacterGraphic 
	cp SampleCharacterGraphic/ずんだもん悲.png dist/SampleCharacterGraphic/ずんだもん悲.png

dist/SampleCharacterGraphic/春日部つむぎ.png: SampleCharacterGraphic/春日部つむぎ.png
	mkdir -p dist/SampleCharacterGraphic 
	cp SampleCharacterGraphic/春日部つむぎ.png dist/SampleCharacterGraphic/春日部つむぎ.png

dist/SampleCharacterGraphic/春日部つむぎ喜.png: SampleCharacterGraphic/春日部つむぎ喜.png
	mkdir -p dist/SampleCharacterGraphic 
	cp SampleCharacterGraphic/春日部つむぎ喜.png dist/SampleCharacterGraphic/春日部つむぎ喜.png

dist/SampleCharacterGraphic/春日部つむぎ煽.png: SampleCharacterGraphic/春日部つむぎ煽.png
	mkdir -p dist/SampleCharacterGraphic 
	cp SampleCharacterGraphic/春日部つむぎ煽.png dist/SampleCharacterGraphic/春日部つむぎ煽.png

dist/SampleCharacterGraphic/春日部つむぎ怒.png: SampleCharacterGraphic/春日部つむぎ怒.png
	mkdir -p dist/SampleCharacterGraphic 
	cp SampleCharacterGraphic/春日部つむぎ怒.png dist/SampleCharacterGraphic/春日部つむぎ怒.png

dist/SampleCharacterGraphic/春日部つむぎ悲.png: SampleCharacterGraphic/春日部つむぎ悲.png
	mkdir -p dist/SampleCharacterGraphic 
	cp SampleCharacterGraphic/春日部つむぎ悲.png dist/SampleCharacterGraphic/春日部つむぎ悲.png

dist/SampleCharacterGraphic/結月ゆかり.png: SampleCharacterGraphic/結月ゆかり.png
	mkdir -p dist/SampleCharacterGraphic 
	cp SampleCharacterGraphic/結月ゆかり.png dist/SampleCharacterGraphic/結月ゆかり.png

dist/SampleCharacterGraphic/結月ゆかり喜.png: SampleCharacterGraphic/結月ゆかり喜.png
	mkdir -p dist/SampleCharacterGraphic 
	cp SampleCharacterGraphic/結月ゆかり喜.png dist/SampleCharacterGraphic/結月ゆかり喜.png

dist/SampleCharacterGraphic/結月ゆかり煽.png: SampleCharacterGraphic/結月ゆかり煽.png
	mkdir -p dist/SampleCharacterGraphic 
	cp SampleCharacterGraphic/結月ゆかり煽.png dist/SampleCharacterGraphic/結月ゆかり煽.png

dist/SampleCharacterGraphic/結月ゆかり怒.png: SampleCharacterGraphic/結月ゆかり怒.png
	mkdir -p dist/SampleCharacterGraphic 
	cp SampleCharacterGraphic/結月ゆかり怒.png dist/SampleCharacterGraphic/結月ゆかり怒.png

dist/SampleCharacterGraphic/結月ゆかり悲.png: SampleCharacterGraphic/結月ゆかり悲.png
	mkdir -p dist/SampleCharacterGraphic 
	cp SampleCharacterGraphic/結月ゆかり悲.png dist/SampleCharacterGraphic/結月ゆかり悲.png

dist/SampleCharacterGraphic/れいむ.png: SampleCharacterGraphic/れいむ.png
	mkdir -p dist/SampleCharacterGraphic 
	cp SampleCharacterGraphic/れいむ.png dist/SampleCharacterGraphic/れいむ.png

dist/SampleCharacterGraphic/れいむ喜.png: SampleCharacterGraphic/れいむ喜.png
	mkdir -p dist/SampleCharacterGraphic 
	cp SampleCharacterGraphic/れいむ喜.png dist/SampleCharacterGraphic/れいむ喜.png

dist/SampleCharacterGraphic/れいむ煽.png: SampleCharacterGraphic/れいむ煽.png
	mkdir -p dist/SampleCharacterGraphic 
	cp SampleCharacterGraphic/れいむ煽.png dist/SampleCharacterGraphic/れいむ煽.png

dist/SampleCharacterGraphic/れいむ怒.png: SampleCharacterGraphic/れいむ怒.png
	mkdir -p dist/SampleCharacterGraphic 
	cp SampleCharacterGraphic/れいむ怒.png dist/SampleCharacterGraphic/れいむ怒.png

dist/SampleCharacterGraphic/れいむ悲.png: SampleCharacterGraphic/れいむ悲.png
	mkdir -p dist/SampleCharacterGraphic 
	cp SampleCharacterGraphic/れいむ悲.png dist/SampleCharacterGraphic/れいむ悲.png

#SampleSE

dist/SampleSE: dist/SampleSE/もちっ.mp3 dist/SampleSE/もちっ2.mp3 dist/SampleSE/もちっ3.mp3 

dist/SampleSE/もちっ.mp3: SampleSE/もちっ.mp3
	mkdir -p dist/SampleSE
	cp SampleSE/もちっ.mp3 dist/SampleSE/もちっ.mp3

dist/SampleSE/もちっ2.mp3: SampleSE/もちっ2.mp3
	mkdir -p dist/SampleSE
	cp SampleSE/もちっ2.mp3 dist/SampleSE/もちっ2.mp3

dist/SampleSE/もちっ3.mp3: SampleSE/もちっ3.mp3
	mkdir -p dist/SampleSE
	cp SampleSE/もちっ3.mp3 dist/SampleSE/もちっ3.mp3

#Sample 

Sample: Sample/psdtoolkit-0.2 Sample/psdtoolkit-0.1.3 Sample/AssistantSeika.exo Sample/BGM.exo Sample/SE.exo Sample/SofTalk.exo Sample/VOICEVOX.exo Sample/ぐにゃぐにゃ.exo Sample/ぴょんぴょん.exo Sample/もにゅもにゅ.exo Sample/挨拶.exo Sample/背景画像.exo Sample/背景色.exo Sample/立ち絵指定.exo Sample/立ち絵指定2.exo Sample/立ち絵指定3.exo Sample/話者指定.exo Sample/話者指定2.exo Sample/背景動画.exo Sample/字幕.exo Sample/自動ぴょんぴょん.exo Sample/自動もにゅもにゅ.exo

Sample/AssistantSeika.exo: Sample/AssistantSeika.txt config.json
	$(HIYOKO_SCRIPT_COMMAND) Sample/AssistantSeika.txt -o Sample/AssistantSeika.exo

Sample/BGM.exo: Sample/BGM.txt config.json
	$(HIYOKO_SCRIPT_COMMAND) Sample/BGM.txt -o Sample/BGM.exo

Sample/SE.exo: Sample/SE.txt config.json
	$(HIYOKO_SCRIPT_COMMAND) Sample/SE.txt -o Sample/SE.exo

Sample/SofTalk.exo: Sample/SofTalk.txt config.json
	$(HIYOKO_SCRIPT_COMMAND) Sample/SofTalk.txt -o Sample/SofTalk.exo

Sample/VOICEVOX.exo: Sample/VOICEVOX.txt config.json
	$(HIYOKO_SCRIPT_COMMAND) Sample/VOICEVOX.txt -o Sample/VOICEVOX.exo

Sample/ぐにゃぐにゃ.exo: Sample/ぐにゃぐにゃ.txt config.json
	$(HIYOKO_SCRIPT_COMMAND) Sample/ぐにゃぐにゃ.txt -o Sample/ぐにゃぐにゃ.exo

Sample/ぴょんぴょん.exo: Sample/ぴょんぴょん.txt config.json
	$(HIYOKO_SCRIPT_COMMAND) Sample/ぴょんぴょん.txt -o Sample/ぴょんぴょん.exo

Sample/もにゅもにゅ.exo: Sample/もにゅもにゅ.txt config.json
	$(HIYOKO_SCRIPT_COMMAND) Sample/もにゅもにゅ.txt -o Sample/もにゅもにゅ.exo

Sample/挨拶.exo: Sample/挨拶.txt config.json Sample/psdtoolkit-0.2/坂本あひる/坂本あひる.json config/psdtoolkit-0.2/坂本あひる/ずんだもん.json config/psdtoolkit-0.2/坂本あひる/春日部つむぎ.json
	$(HIYOKO_SCRIPT_COMMAND) Sample/挨拶.txt --config-file Sample/psdtoolkit-0.2/坂本あひる/坂本あひる.json -o Sample/挨拶.exo

Sample/背景画像.exo: Sample/背景画像.txt config.json
	$(HIYOKO_SCRIPT_COMMAND) Sample/背景画像.txt -o Sample/背景画像.exo

Sample/背景色.exo: Sample/背景色.txt config.json
	$(HIYOKO_SCRIPT_COMMAND) Sample/背景色.txt -o Sample/背景色.exo

Sample/立ち絵指定.exo: Sample/立ち絵指定.txt config.json
	$(HIYOKO_SCRIPT_COMMAND) Sample/立ち絵指定.txt -o Sample/立ち絵指定.exo

Sample/立ち絵指定2.exo: Sample/立ち絵指定2.txt config.json
	$(HIYOKO_SCRIPT_COMMAND) Sample/立ち絵指定2.txt -o Sample/立ち絵指定2.exo

Sample/立ち絵指定3.exo: Sample/立ち絵指定3.txt config.json
	$(HIYOKO_SCRIPT_COMMAND) Sample/立ち絵指定3.txt -o Sample/立ち絵指定3.exo

Sample/話者指定.exo: Sample/話者指定.txt config.json
	$(HIYOKO_SCRIPT_COMMAND) Sample/話者指定.txt -o Sample/話者指定.exo

Sample/話者指定2.exo: Sample/話者指定2.txt config.json
	$(HIYOKO_SCRIPT_COMMAND) Sample/話者指定2.txt -o Sample/話者指定2.exo

Sample/背景動画.exo: Sample/背景動画.txt config.json
	$(HIYOKO_SCRIPT_COMMAND) Sample/背景動画.txt -o Sample/背景動画.exo

Sample/字幕.exo: Sample/字幕.txt config.json 
	$(HIYOKO_SCRIPT_COMMAND) Sample/字幕.txt -o Sample/字幕.exo

Sample/自動ぴょんぴょん.exo: Sample/自動ぴょんぴょん.txt config.json 
	$(HIYOKO_SCRIPT_COMMAND) Sample/自動ぴょんぴょん.txt -o Sample/自動ぴょんぴょん.exo

Sample/自動もにゅもにゅ.exo: Sample/自動もにゅもにゅ.txt config.json 
	$(HIYOKO_SCRIPT_COMMAND) Sample/自動もにゅもにゅ.txt -o Sample/自動もにゅもにゅ.exo

Sample/psdtoolkit-0.2: Sample/psdtoolkit-0.2/坂本あひる Sample/psdtoolkit-0.2/MtU

Sample/psdtoolkit-0.2/坂本あひる: Sample/psdtoolkit-0.2/坂本あひる/ずんだもん.exo Sample/psdtoolkit-0.2/坂本あひる/四国めたん.exo Sample/psdtoolkit-0.2/坂本あひる/春日部つむぎ.exo Sample/psdtoolkit-0.2/坂本あひる/九州そら.exo Sample/psdtoolkit-0.2/坂本あひる/雨晴はう.exo

Sample/psdtoolkit-0.2/坂本あひる/ずんだもん.exo: Sample/psdtoolkit-0.2/坂本あひる/ずんだもん.txt Sample/psdtoolkit-0.2/坂本あひる/坂本あひる.json config/psdtoolkit-0.2/坂本あひる/ずんだもん.json
	$(HIYOKO_SCRIPT_COMMAND) Sample/psdtoolkit-0.2/坂本あひる/ずんだもん.txt --config-file Sample/psdtoolkit-0.2/坂本あひる/坂本あひる.json -o Sample/psdtoolkit-0.2/坂本あひる/ずんだもん.exo

Sample/psdtoolkit-0.2/坂本あひる/四国めたん.exo: Sample/psdtoolkit-0.2/坂本あひる/四国めたん.txt Sample/psdtoolkit-0.2/坂本あひる/坂本あひる.json config/psdtoolkit-0.2/坂本あひる/四国めたん.json
	$(HIYOKO_SCRIPT_COMMAND) Sample/psdtoolkit-0.2/坂本あひる/四国めたん.txt --config-file Sample/psdtoolkit-0.2/坂本あひる/坂本あひる.json -o Sample/psdtoolkit-0.2/坂本あひる/四国めたん.exo

Sample/psdtoolkit-0.2/坂本あひる/春日部つむぎ.exo: Sample/psdtoolkit-0.2/坂本あひる/春日部つむぎ.txt Sample/psdtoolkit-0.2/坂本あひる/坂本あひる.json config/psdtoolkit-0.2/坂本あひる/春日部つむぎ.json
	$(HIYOKO_SCRIPT_COMMAND) Sample/psdtoolkit-0.2/坂本あひる/春日部つむぎ.txt --config-file Sample/psdtoolkit-0.2/坂本あひる/坂本あひる.json -o Sample/psdtoolkit-0.2/坂本あひる/春日部つむぎ.exo

Sample/psdtoolkit-0.2/坂本あひる/九州そら.exo: Sample/psdtoolkit-0.2/坂本あひる/九州そら.txt Sample/psdtoolkit-0.2/坂本あひる/坂本あひる.json config/psdtoolkit-0.2/坂本あひる/九州そら.json
	$(HIYOKO_SCRIPT_COMMAND) Sample/psdtoolkit-0.2/坂本あひる/九州そら.txt --config-file Sample/psdtoolkit-0.2/坂本あひる/坂本あひる.json -o Sample/psdtoolkit-0.2/坂本あひる/九州そら.exo

Sample/psdtoolkit-0.2/坂本あひる/雨晴はう.exo: Sample/psdtoolkit-0.2/坂本あひる/雨晴はう.txt Sample/psdtoolkit-0.2/坂本あひる/坂本あひる.json config/psdtoolkit-0.2/坂本あひる/雨晴はう.json
	$(HIYOKO_SCRIPT_COMMAND) Sample/psdtoolkit-0.2/坂本あひる/雨晴はう.txt --config-file Sample/psdtoolkit-0.2/坂本あひる/坂本あひる.json -o Sample/psdtoolkit-0.2/坂本あひる/雨晴はう.exo

Sample/psdtoolkit-0.2/MtU: Sample/psdtoolkit-0.2/MtU/結月ゆかり.exo Sample/psdtoolkit-0.2/MtU/弦巻マキ.exo Sample/psdtoolkit-0.2/MtU/紲星あかり.exo

Sample/psdtoolkit-0.2/MtU/結月ゆかり.exo: Sample/psdtoolkit-0.2/MtU/結月ゆかり.txt Sample/psdtoolkit-0.2/MtU/MtU.json config/psdtoolkit-0.2/MtU/結月ゆかり.json
	$(HIYOKO_SCRIPT_COMMAND) Sample/psdtoolkit-0.2/MtU/結月ゆかり.txt --config-file Sample/psdtoolkit-0.2/MtU/MtU.json -o Sample/psdtoolkit-0.2/MtU/結月ゆかり.exo

Sample/psdtoolkit-0.2/MtU/弦巻マキ.exo: Sample/psdtoolkit-0.2/MtU/弦巻マキ.txt Sample/psdtoolkit-0.2/MtU/MtU.json config/psdtoolkit-0.2/MtU/弦巻マキ.json
	$(HIYOKO_SCRIPT_COMMAND) Sample/psdtoolkit-0.2/MtU/弦巻マキ.txt --config-file Sample/psdtoolkit-0.2/MtU/MtU.json -o Sample/psdtoolkit-0.2/MtU/弦巻マキ.exo

Sample/psdtoolkit-0.2/MtU/紲星あかり.exo: Sample/psdtoolkit-0.2/MtU/紲星あかり.txt Sample/psdtoolkit-0.2/MtU/MtU.json config/psdtoolkit-0.2/MtU/紲星あかり.json
	$(HIYOKO_SCRIPT_COMMAND) Sample/psdtoolkit-0.2/MtU/紲星あかり.txt --config-file Sample/psdtoolkit-0.2/MtU/MtU.json -o Sample/psdtoolkit-0.2/MtU/紲星あかり.exo

Sample/psdtoolkit-0.1.3: Sample/psdtoolkit-0.1.3/坂本あひる

Sample/psdtoolkit-0.1.3/坂本あひる: Sample/psdtoolkit-0.1.3/坂本あひる/ずんだもん.exo Sample/psdtoolkit-0.1.3/坂本あひる/四国めたん.exo Sample/psdtoolkit-0.1.3/坂本あひる/春日部つむぎ.exo 

Sample/psdtoolkit-0.1.3/坂本あひる/ずんだもん.exo: Sample/psdtoolkit-0.1.3/坂本あひる/ずんだもん.txt Sample/psdtoolkit-0.1.3/坂本あひる/坂本あひる.json config/psdtoolkit-0.1.3/坂本あひる/ずんだもん.json 
	$(HIYOKO_SCRIPT_COMMAND) Sample/psdtoolkit-0.1.3/坂本あひる/ずんだもん.txt --config-file Sample/psdtoolkit-0.1.3/坂本あひる/坂本あひる.json -o Sample/psdtoolkit-0.1.3/坂本あひる/ずんだもん.exo

Sample/psdtoolkit-0.1.3/坂本あひる/四国めたん.exo: Sample/psdtoolkit-0.1.3/坂本あひる/四国めたん.txt Sample/psdtoolkit-0.1.3/坂本あひる/坂本あひる.json config/psdtoolkit-0.1.3/坂本あひる/四国めたん.json 
	$(HIYOKO_SCRIPT_COMMAND) Sample/psdtoolkit-0.1.3/坂本あひる/四国めたん.txt --config-file Sample/psdtoolkit-0.1.3/坂本あひる/坂本あひる.json -o Sample/psdtoolkit-0.1.3/坂本あひる/四国めたん.exo

Sample/psdtoolkit-0.1.3/坂本あひる/春日部つむぎ.exo: Sample/psdtoolkit-0.1.3/坂本あひる/春日部つむぎ.txt Sample/psdtoolkit-0.1.3/坂本あひる/坂本あひる.json config/psdtoolkit-0.1.3/坂本あひる/春日部つむぎ.json 
	$(HIYOKO_SCRIPT_COMMAND) Sample/psdtoolkit-0.1.3/坂本あひる/春日部つむぎ.txt --config-file Sample/psdtoolkit-0.1.3/坂本あひる/坂本あひる.json -o Sample/psdtoolkit-0.1.3/坂本あひる/春日部つむぎ.exo
