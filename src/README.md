# 원본 조각 파일

`index.html`은 여기 있는 조각들을 합쳐 만들어집니다. 직접 고치지 말고 이쪽을 고치세요.

| 파일 | 무엇 |
|---|---|
| `build.py` | 표지·디자인·자바스크립트가 들어 있고, 네 권을 합쳐 `index.html`을 만듭니다 |
| `v1.html` ~ `v4.html` | 각 권의 본문 |
| `logo.png` / `logo.b64` | 로고 (배경을 지우고 잘라 둔 것) |
| `make_logo.py` | 로고를 다시 만들 때 쓰는 도구 |

## 고치고 올리는 순서

```bash
cd ~/Documents/chaekgyeot
python3 src/build.py          # index.html 다시 만들기
git add -A && git commit -m "무엇을 고쳤는지"
git push
```

1~2분 뒤 사이트에 반영됩니다.
