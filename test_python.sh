#!/bin/bash

BASE_FILE="backend/src/tests"
FILE_TO_TEST="/test_001_users.py"


FULL_PATH="${BASE_FILE}${FILE_TO_TEST}"

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

# Execução
echo ""
print_border
print_centered_message
print_border
echo ""

pytest -vvvs --disable-pytest-warnings "${FULL_PATH}"
