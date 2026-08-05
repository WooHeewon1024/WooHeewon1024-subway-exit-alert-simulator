# 팀 공유용 배포 안내

이 프로젝트는 GitHub Pages 또는 Render를 이용하면 인터넷에서 열 수 있는 링크로 공유할 수 있습니다.

## 가장 쉬운 방법: GitHub Pages

이 프로젝트의 시뮬레이션은 브라우저 JavaScript에서 동작하므로 GitHub Pages로도 배포할 수 있습니다. 저장소에 코드를 올린 뒤 GitHub 저장소의 **Settings → Pages → Build and deployment → Source**를 **GitHub Actions**로 선택합니다. `main` 브랜치에 올릴 때마다 자동으로 배포되며, 완료 후 표시되는 Pages 주소를 팀원에게 공유하면 됩니다.

각 접속자는 독립된 시뮬레이터 상태를 사용합니다.

## 1. GitHub에 코드 올리기

1. GitHub에서 새 저장소를 만듭니다. (예: `subway-exit-alert-simulator`)
2. 이 프로젝트의 `.venv` 폴더를 제외한 파일을 저장소에 올립니다.
3. `app.py`, `requirements.txt`, `render.yaml`, `templates`, `static` 폴더가 포함되었는지 확인합니다.

## 2. Render 배포

1. [Render](https://render.com/)에 로그인합니다.
2. **New + → Blueprint**를 선택하고 GitHub 저장소를 연결합니다.
3. 저장소를 선택한 뒤 배포를 시작합니다.
4. 완료되면 Render가 만든 `https://...onrender.com` 주소를 팀원에게 공유합니다.

`render.yaml`이 포함되어 있으므로 설치와 실행 명령은 자동으로 설정됩니다.

## 참고

- 링크로 접속한 사람마다 시뮬레이터 상태는 별도로 동작합니다. 한 사람의 조작이 다른 팀원 화면에 영향을 주지 않습니다.
- 로컬 같은 와이파이 공유는 `http://내-PC-IP:5000`으로도 가능합니다.
