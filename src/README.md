# 원본 조각 파일

`index.html`은 여기 있는 조각들을 합쳐 만들어집니다. 직접 고치지 말고 이쪽을 고치세요.

| 파일 | 무엇 |
|---|---|
| `build.py` | 표지·디자인·자바스크립트가 들어 있고, 네 권을 합쳐 `index.html`을 만듭니다 |
| `v1.html` ~ `v4.html` | 각 권의 본문 |
| `logo.svg` / `logo-dark.svg` | 로고 — 밝은판과 어두운판. 벡터입니다 |
| `logo.b64` / `logo-dark.b64` | 위 두 SVG의 base64. `build.py`가 이걸 읽어 갑니다 |
| `logo-text.png` | 로고의 '최수빈' 글자만 잘라 둔 그림 (원본) |
| `make_logo.py` | 로고를 다시 만드는 도구 — `python3 src/make_logo.py` |
| `logo.png` | 옛 로고. `logo-text.png`를 여기서 떠 왔습니다. 지금은 쓰이지 않습니다 |

## 로고

심벌 「해와 글줄」은 `make_logo.py` 안에 좌표로 들어 있습니다 —
`~/Documents/Bluesky/자료/표식/01_심볼만/책곁_심볼_저녁.svg` 와 같은 도형입니다.
색은 밝은 곳에서 먹 `#3B2317`, 어두운 곳에서 반전 `#F6EEE1`, 해는 양쪽 모두 금 `#D39A2B`.

심벌이나 색을 바꾸려면 `make_logo.py` 위쪽의 값만 고치고 다시 돌리면 됩니다.
글자 '최수빈'은 `logo-text.png` 그대로 씁니다 — 글자꼴은 건드리지 않습니다.

## 고치고 올리는 순서

```bash
cd ~/Documents/chaekgyeot
python3 src/build.py          # index.html 다시 만들기
git add -A && git commit -m "무엇을 고쳤는지"
git push
```

1~2분 뒤 사이트에 반영됩니다.
