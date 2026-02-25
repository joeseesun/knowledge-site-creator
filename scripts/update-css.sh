#!/bin/bash
#
# 批量更新所有 workshop 的 CSS 样式
# 用途：当 skill 的 CSS 有 bug 修复或样式改进时，一键更新所有已部署的网站
#
# 使用方法：
#   bash scripts/update-css.sh [--dry-run]
#
# 选项：
#   --dry-run    仅列出将要更新的项目，不实际执行
#

set -e  # 遇到错误立即退出

DRY_RUN=false
if [ "$1" = "--dry-run" ]; then
  DRY_RUN=true
  echo "🔍 演练模式（不会实际更新）"
  echo ""
fi

# CSS 源文件位置（需要先准备好最新的 CSS）
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CSS_SOURCE="$SKILL_DIR/templates/minimal.css"

if [ ! -f "$CSS_SOURCE" ]; then
  echo "❌ 错误：未找到 CSS 源文件：$CSS_SOURCE"
  echo "   请先创建或复制最新的 CSS 文件到 templates/ 目录"
  exit 1
fi

echo "📁 CSS 源文件：$CSS_SOURCE"
echo "📊 文件大小：$(wc -c < "$CSS_SOURCE") bytes"
echo ""

# 查找所有 workshop 项目
WORKSHOPS_DIR="/Users/joe/Dropbox/code"
UPDATED_COUNT=0
SKIPPED_COUNT=0
FAILED_COUNT=0

echo "🔍 扫描 workshop 项目..."
echo ""

for dir in "$WORKSHOPS_DIR"/*-workshop; do
  if [ ! -d "$dir" ]; then
    continue
  fi

  PROJECT_NAME=$(basename "$dir")
  CSS_TARGET="$dir/css/minimal.css"

  echo "================================================"
  echo "📦 项目：$PROJECT_NAME"

  # 检查是否有 CSS 文件
  if [ ! -f "$CSS_TARGET" ]; then
    echo "⚠️  跳过：未找到 css/minimal.css"
    SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
    echo ""
    continue
  fi

  # 检查 CSS 是否相同（避免不必要的更新）
  if cmp -s "$CSS_SOURCE" "$CSS_TARGET"; then
    echo "✓ 跳过：CSS 已是最新版本"
    SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
    echo ""
    continue
  fi

  if [ "$DRY_RUN" = true ]; then
    echo "📝 将更新：$CSS_TARGET"
    echo "📝 将重新部署到 Vercel"
    UPDATED_COUNT=$((UPDATED_COUNT + 1))
    echo ""
    continue
  fi

  # 备份旧 CSS
  cp "$CSS_TARGET" "$CSS_TARGET.backup"
  echo "💾 已备份旧 CSS：$CSS_TARGET.backup"

  # 复制新 CSS
  cp "$CSS_SOURCE" "$CSS_TARGET"
  echo "✓ 已更新 CSS"

  # Git 提交
  cd "$dir"
  git add css/minimal.css
  git commit -m "chore: update CSS from skill template" || echo "⚠️  无 Git 变更"

  # 重新部署
  echo "🚀 重新部署到 Vercel..."
  if vercel --prod --yes > /dev/null 2>&1; then
    echo "✅ 部署成功"
    UPDATED_COUNT=$((UPDATED_COUNT + 1))
  else
    echo "❌ 部署失败"
    FAILED_COUNT=$((FAILED_COUNT + 1))
    # 恢复备份
    cp "$CSS_TARGET.backup" "$CSS_TARGET"
    echo "↩️  已恢复备份"
  fi

  echo ""
done

echo "================================================"
echo "📊 更新总结"
echo ""
echo "  ✅ 成功更新：$UPDATED_COUNT 个项目"
echo "  ⚠️  跳过：$SKIPPED_COUNT 个项目"
if [ $FAILED_COUNT -gt 0 ]; then
  echo "  ❌ 失败：$FAILED_COUNT 个项目"
fi
echo ""

if [ "$DRY_RUN" = true ]; then
  echo "💡 这是演练模式，没有实际执行任何操作"
  echo "   要实际执行，请运行：bash scripts/update-css.sh"
fi
