# AGENTS.md

이 저장소는 **파이썬은 익숙하지만 머신러닝은 처음인 컴퓨터 분야 대학교 2학년**을 위한 PyTorch 튜토리얼입니다.
글쓰기는 에이전트가 맡고, 사람(관리자)은 카테고리와 큰 흐름만 조정합니다.

## 1. 먼저 읽을 것

모든 에이전트는 작업 전에 다음 두 문서를 읽습니다.

- [agents/curriculum.md](agents/curriculum.md): 카테고리와 문서 목록. **관리자가 직접 수정하는 유일한 기준 문서**입니다.
- [agents/style-guide.md](agents/style-guide.md): 독자, 용어, 문체, 코드 규칙

## 2. 역할에 맞는 문서로 이동

| 역할 | 언제 | 문서 |
| --- | --- | --- |
| 기획 (Planner) | 새 문서를 시작할 때. 문서 유형과 목표를 정함 | [agents/planner.md](agents/planner.md) |
| 작성 (Writer) | 기획서를 바탕으로 초안을 쓸 때 | [agents/writer.md](agents/writer.md) |
| 구조 검토 (Structure Reviewer) | 초안의 목차, 흐름, 제목을 검토할 때 | [agents/structure-reviewer.md](agents/structure-reviewer.md) |
| 문장 교정 (Sentence Editor) | 구조가 확정된 뒤 문장을 다듬을 때 | [agents/sentence-editor.md](agents/sentence-editor.md) |
| 코드 검증 (Code Reviewer) | 문서 속 예제 코드를 실행하고 확인할 때 | [agents/code-reviewer.md](agents/code-reviewer.md) |
| 영상 제작 (Animator) | 개념을 Manim 애니메이션으로 보여줄 때 | [agents/animator.md](agents/animator.md) |

역할이 지정되지 않았다면 요청 내용을 보고 위 표에서 고릅니다. 애매하면 **기획**부터 시작합니다.

## 3. 기본 작업 순서

```
기획 → 작성 → 구조 검토 → (수정) → 코드 검증 → 문장 교정 → 관리자 확인
             └→ 영상 제작 (작성과 함께 진행)
```

- 한 단계는 한 역할만 맡습니다. 여러 역할을 한 번에 섞지 않습니다.
- 각 단계의 결과물 형식은 역할 문서의 "출력" 절을 따릅니다.
- 관리자 판단이 필요한 것(카테고리 변경, 문서 분리/통합, 학습 순서 변경)은 직접 바꾸지 말고 질문으로 남깁니다.

## 4. 파일 위치

- 튜토리얼 본문: `docs/<카테고리 번호>-<카테고리>/<문서 번호>-<제목>.md`
- 실습 노트북: `notebooks/<카테고리 번호>-<카테고리>/<문서 번호>-<제목>.ipynb` (Colab에서 바로 열 수 있게 문서 첫머리에 "Open in Colab" 링크를 둡니다)
- 애니메이션 원본: `animations/<카테고리 번호>-<카테고리>/<장면>.py` (렌더링 결과는 `docs/videos/` 같은 경로에 `.mp4`로 저장)
- 기획서와 검토 기록: PR 설명이나 PR 코멘트에 남깁니다. 저장소에 별도 파일로 두지 않습니다.

## 참고

역할 문서의 검토 원칙은 [토스 테크니컬 라이팅 가이드의 AI 리뷰 프롬프트](https://technical-writing.dev/tutorial/review-prompt.html)를 이 프로젝트에 맞게 옮긴 것입니다.
