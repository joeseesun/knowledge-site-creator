# 批量更新机制 🔄

当 skill 的设计系统有更新（如 CSS bug 修复、样式改进）时，需要将更新同步到所有已部署的 workshop 项目。

## 典型场景

- CSS 样式修复：修复了响应式布局问题
- 设计改进：优化了卡片阴影、间距、配色
- 功能增强：添加了新的交互动效
- 安全更新：修复了 XSS 漏洞或其他安全问题
- HTML 模板更新：修改 gen-html.py 后需要重新生成所有站点的 HTML

## 更新脚本

### CSS 更新

`scripts/update-css.sh` — 批量更新所有已部署站点的 CSS 文件

```bash
# 演练模式
bash scripts/update-css.sh --dry-run

# 执行更新
bash scripts/update-css.sh
```

脚本自动执行：扫描项目 → 智能对比 → 安全备份 → Git 提交 → 重新部署 → 失败回滚 → 统计报告

### HTML 重新生成

`scripts/gen-html.py` — 当 gen-html.py 本身有更新时，对每个已部署项目重新运行：

```bash
for dir in $BASE_DIR/*-workshop; do
  if [ -f "$dir/js/siteConfig.js" ]; then
    echo "Regenerating: $(basename $dir)"
    python "$SKILL_DIR/scripts/gen-html.py" "$dir"
    cd "$dir"; vercel --prod --yes
  fi
done
```

## 安全特性

1. **智能跳过**：自动跳过已是最新版本的项目
2. **自动备份**：更新前备份旧 CSS 为 `.backup` 文件
3. **失败回滚**：部署失败时自动恢复备份
4. **Git 记录**：所有更新都有 Git commit，可追溯历史
5. **演练模式**：`--dry-run` 模式让你先看看会更新什么

## 注意事项

- 确保 `templates/minimal.css` 已经过测试
- 使用 `--dry-run` 先预览将更新的项目
- 脚本完成后，随机抽查 2-3 个项目的网站
- 失败的项目不影响其他项目的更新

## 扩展性

当前脚本仅支持 CSS 更新，但同样的机制可以扩展到：
- JavaScript 文件更新（`js/storage.js` 等）
- HTML 模板更新（如修复 meta 标签缺失）
- 配置文件更新（`vercel.json` 等）
- 批量迁移（如数据结构变更）
