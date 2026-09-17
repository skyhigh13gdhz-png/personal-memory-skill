#!/usr/bin/env bash
set -euo pipefail

SOURCE_DIR="${SOURCE_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
INSTALL_DIR="${INSTALL_DIR:-/opt/personal-memory-skill}"
ENV_FILE="${ENV_FILE:-/etc/personal-memory-skill.env}"
SERVICE_NAME="personal-memory-mcp"
RUN_USER="${SUDO_USER:-${USER}}"

if [[ $EUID -ne 0 ]]; then
  echo "[✗] 请使用 sudo 运行：sudo bash scripts/install-mcp-adapter.sh"
  exit 1
fi

if [[ ! -f "$ENV_FILE" ]]; then
  echo "[✗] 缺少 $ENV_FILE"
  echo "    请先创建该文件，并至少设置 MEMORY_GATEWAY_TOKEN。"
  exit 1
fi

if ! grep -q '^MEMORY_GATEWAY_TOKEN=.' "$ENV_FILE"; then
  echo "[✗] $ENV_FILE 中未设置 MEMORY_GATEWAY_TOKEN"
  exit 1
fi

install -d -m 0755 "$INSTALL_DIR"
cp "$SOURCE_DIR/mcp_server.py" "$SOURCE_DIR/requirements.txt" "$INSTALL_DIR/"
python3 -m venv "$INSTALL_DIR/.venv"
"$INSTALL_DIR/.venv/bin/pip" install -q --upgrade pip
"$INSTALL_DIR/.venv/bin/pip" install -q -r "$INSTALL_DIR/requirements.txt"
chmod 600 "$ENV_FILE"

cat > "/etc/systemd/system/${SERVICE_NAME}.service" <<EOF
[Unit]
Description=Personal Memory MCP Adapter
After=network-online.target memory-gateway.service
Wants=network-online.target

[Service]
Type=simple
User=${RUN_USER}
WorkingDirectory=${INSTALL_DIR}
EnvironmentFile=${ENV_FILE}
ExecStart=${INSTALL_DIR}/.venv/bin/python ${INSTALL_DIR}/mcp_server.py
Restart=on-failure
RestartSec=2

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now "$SERVICE_NAME"
sleep 1

if systemctl is-active --quiet "$SERVICE_NAME"; then
  echo "[✓] Personal Memory MCP Adapter 已启动"
  echo "[✓] 默认仅监听本机 127.0.0.1:8000，MCP endpoint：/mcp"
  echo "[→] 下一步：先做本机 MCP 验收，再决定 Secure MCP Tunnel 或 HTTPS/OAuth 接入。"
else
  echo "[✗] MCP Adapter 启动失败"
  journalctl -u "$SERVICE_NAME" -n 50 --no-pager
  exit 1
fi
