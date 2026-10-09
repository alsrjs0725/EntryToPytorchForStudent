# 00-01 Colab 시작하기

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alsrjs0725/EntryToPytorchForStudent/blob/main/notebooks/00-시작하기/01-colab-시작하기.ipynb)

이 튜토리얼의 모든 실습은 Google Colab에서 해요. 설치 없이 브라우저만 있으면 무료 GPU로 PyTorch를 쓸 수 있어요. 이 문서를 마치면 Colab 노트북을 열고, GPU를 켜고, 첫 셀을 실행할 수 있어요.

**사전 지식:** Google 계정, 파이썬 기초 문법

## 1. 3단계로 시작하기

1. **Colab 열기:** 문서 맨 위의 **Open in Colab** 배지를 누르면 이 문서의 노트북이 Colab에서 열려요.
2. **GPU 켜기:** 메뉴에서 **런타임 → 런타임 유형 변경 → T4 GPU**를 고르고 저장해요.
3. **첫 셀 실행:** 첫 셀을 클릭하고 `Shift + Enter`를 눌러요.

처음 실행하면 "이 노트북은 Google에서 작성하지 않았습니다"라는 경고가 떠요. **무시하고 계속**을 누르면 돼요.

!!! tip "노트북을 저장하려면"
    Open in Colab으로 연 노트북은 고쳐도 원본에 저장되지 않아요. 고친 내용을 남기려면 **파일 → Drive에 사본 저장**을 눌러요.

## 2. 첫 셀: GPU 확인과 device 설정

모든 노트북의 첫 셀은 이 코드로 시작해요. GPU를 쓸 수 있는지 확인하고, 텐서를 둘 장치 이름을 `device`에 담아요. `torch.manual_seed(0)`은 무작위 값을 매번 같게 만들어요. 자세한 내용은 00-02에서 봐요.

```python
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
torch.manual_seed(0)
print("PyTorch 버전:", torch.__version__)
print("device:", device)
```

GPU를 켰다면 `device: cuda`가 출력돼요. `cuda`는 NVIDIA GPU를 뜻해요. `device: cpu`가 나오면 2단계(GPU 켜기)를 다시 확인해요.

GPU 이름도 확인할 수 있어요. 무료 Colab에서는 보통 `Tesla T4`가 나와요.

```python
if torch.cuda.is_available():
    print(torch.cuda.get_device_name(0))
else:
    print("GPU가 없어요. 런타임 유형을 GPU로 바꿨는지 확인하세요.")
```

!!! note "이 사이트의 출력 결과"
    이 사이트의 문서에 적힌 출력은 GPU가 없는 환경(CPU)에서 실행한 결과예요. Colab GPU에서는 `device: cuda`가 나와요. 무작위 값과 학습 결과도 문서와 조금 다를 수 있어요.

### GPU 상태 자세히 보기 (`!nvidia-smi`)

`!`로 시작하는 줄은 파이썬이 아니라 터미널 명령으로 실행돼요. `!nvidia-smi`로 GPU 이름과 메모리 사용량을 볼 수 있어요. GPU를 켜지 않았다면 `command not found`가 나와요.

```python
!nvidia-smi
```

## 3. 셀끼리 변수 공유하기

한 셀에서 만든 변수는 다른 셀에서도 쓸 수 있어요. 그래서 **위에서부터 순서대로** 실행해야 해요.

```python
message = "앞 셀에서 만든 변수"
```

```python
print(message)
```

```
앞 셀에서 만든 변수
```

## 자주 묻는 질문

??? question "`NameError: name 'torch' is not defined`가 나요"
    위쪽 셀을 실행하기 전에 아래 셀을 실행하면 이 오류가 나요. **런타임 → 이전 셀 모두 실행**을 눌러요.

??? question "런타임 유형에 GPU가 없거나 'GPU를 사용할 수 없음'이 떠요"
    무료 Colab은 GPU 사용량에 한도가 있어요. 한도를 넘으면 잠시 GPU를 쓸 수 없어요. 시간이 지난 뒤 다시 시도하거나, 그동안 CPU로 실행해요. 챕터 00~04는 CPU로도 돌아가요.

??? question "한참 뒤에 돌아왔더니 변수가 다 사라졌어요"
    오래 쓰지 않으면 Colab이 연결을 끊고 런타임을 초기화해요. 첫 셀부터 다시 실행해요.

## 정리

- 실습은 Colab에서 "열기 → GPU 켜기 → 첫 셀 실행" 3단계로 시작해요.
- 첫 셀의 `device`가 `cuda`인지 확인해요.
- 셀은 위에서부터 순서대로 실행해요.

**다음 문서:** [00-02 텐서 기초](02-텐서-기초.md)
