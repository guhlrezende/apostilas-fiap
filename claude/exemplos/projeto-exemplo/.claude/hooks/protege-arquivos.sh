#!/bin/bash
# Hook PreToolUse: bloqueia edição de arquivos sensíveis (adaptado da documentação oficial).
# O Claude Code manda um JSON no stdin; sair com código 2 bloqueia a ação,
# e o que for escrito no stderr vira o motivo que o Claude lê.

ENTRADA=$(cat)
ARQUIVO=$(echo "$ENTRADA" | jq -r '.tool_input.file_path // empty')
ARQUIVO="${ARQUIVO//\\//}"   # normaliza barras do Windows

PROTEGIDOS=(".env" "package-lock.json" ".git/")

for padrao in "${PROTEGIDOS[@]}"; do
  if [[ "$ARQUIVO" == *"$padrao"* ]]; then
    echo "Bloqueado: $ARQUIVO bate com o padrão protegido '$padrao'" >&2
    exit 2
  fi
done

exit 0
