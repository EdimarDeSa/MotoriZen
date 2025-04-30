#!/bin/bash

BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE_FILE="${BASE_DIR}/backend/src/"
TEST_MODULE="tests/"
GENERATE_FILE="utils/generate_fake_data.py"
CLEANER_MODULE="tests.utils.cleaner"
FILE_TO_TEST="test_004*.py"


FULL_PATH="${TEST_MODULE}${FILE_TO_TEST}"

MESSAGE="Iniciando testes ${FILE_TO_TEST}"
LINE_WIDTH=80
BORDER_CHAR="="
SIDE_BORDER="###"

# Função para imprimir uma linha de borda
print_border() {
  printf "${SIDE_BORDER}"
  printf "%${LINE_WIDTH}s" | tr ' ' "${BORDER_CHAR}"
  printf "${SIDE_BORDER}\n"
}

print_frame() {
  printf "${SIDE_BORDER}"
  printf "%${LINE_WIDTH}s" | tr ' ' " "
  printf "${SIDE_BORDER}\n"
}

# Função para imprimir a linha central com a mensagem centralizada
print_centered_message() {
  local total_inner_width=$((LINE_WIDTH))
  local message_length=${#MESSAGE}
  local padding=$(( (total_inner_width - message_length) / 2 ))
  local extra=$(( total_inner_width - message_length - padding ))
  printf "${SIDE_BORDER}"
  printf "%*s%s%*s" "$padding" "" "$MESSAGE" "$extra" ""
  printf "${SIDE_BORDER}\n"
}

clear

# Execução
echo ""
print_border
print_frame
print_centered_message
print_frame
print_border
echo ""

cd "${BASE_FILE}"
python "${TEST_MODULE}${GENERATE_FILE}"
pytest -vvvs --disable-warnings -p no:warnings --durations=0 ${FULL_PATH}

echo "Limpando dados..."
python -m ${CLEANER_MODULE} > /dev/null

echo "Done!"