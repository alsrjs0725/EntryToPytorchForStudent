#!/usr/bin/env bash
# 시작할 때 러너를 저장소에 등록하고, 컨테이너가 멈추면 등록을 해제합니다.
set -euo pipefail
: "${GITHUB_REPOSITORY:?GITHUB_REPOSITORY가 필요합니다 (예: alsrjs0725/EntryToPytorchForStudent)}"
: "${ACCESS_TOKEN:?ACCESS_TOKEN이 필요합니다 (.env 참고)}"

api="https://api.github.com/repos/${GITHUB_REPOSITORY}/actions/runners"
token() {
    curl -fsSL -X POST \
        -H "Authorization: Bearer ${ACCESS_TOKEN}" \
        -H "Accept: application/vnd.github+json" \
        "${api}/$1" | jq -r .token
}

cd /home/runner/actions-runner
if [ ! -f .runner ]; then
    ./config.sh --unattended --replace \
        --url "https://github.com/${GITHUB_REPOSITORY}" \
        --token "$(token registration-token)" \
        --name "${RUNNER_NAME:-homeserver-manim}" \
        --labels "${RUNNER_LABELS:-manim}" \
        --work /home/runner/_work
fi

cleanup() {
    echo "러너 등록 해제 중..."
    ./config.sh remove --token "$(token remove-token)" || true
}
trap 'kill -INT "$pid" 2>/dev/null; wait "$pid" || true; cleanup; exit 0' TERM INT

./run.sh &
pid=$!
wait "$pid"
