# Vercel 部署事故复盘 — 共享 GitHub 仓库导致站点覆盖

**事故时间线**：2026-02-25

## 事故描述

1. 生成 `evolutionary-psychology-workshop`（进化心理学），成功部署
2. 生成 `design-aesthetics-workshop`（设计美学），成功部署
3. 用户发现 **word.qiaomu.ai**（原词根词缀网站）显示的是进化心理学内容
4. 检查发现 `word-root-workshop` 项目的 Git 仓库被进化心理学内容覆盖

## 根本原因分析

```bash
# 事故前的状态
evolutionary-psychology-workshop → origin: https://github.com/joeseesun/word-root-workshop.git
word-root-workshop              → origin: https://github.com/joeseesun/word-root-workshop.git
                                   ↑↑↑ 两个项目共享同一个 GitHub 仓库
```

## 为什么会发生

- 旧版 skill 使用 `cp -r word-root-workshop` 复制模板
- 复制时连 `.git/` 目录也一起复制了（包含远程仓库配置）
- 部署时 Vercel 检测到 Git 远程仓库，自动关联
- 多个项目关联同一个 GitHub 仓库，后部署的覆盖先部署的

## 损害范围

- ⛔ word.qiaomu.ai（生产域名）显示错误内容
- ⛔ word-root-workshop 的 Git 历史被污染
- ⛔ 用户体验受损，需要紧急修复

## 紧急修复步骤

```bash
# 1. 恢复 word-root-workshop 到原始状态
cd $BASE_DIR/word-root-workshop
git log --oneline  # 找到原始提交
git reset --hard 14cc7b0  # 恢复到原始词根词缀内容

# 2. 修复 vercel.json 配置冲突
# 移除不兼容的 routes 配置

# 3. 重新部署
vercel --prod --yes

# 4. 验证恢复
curl -sL https://word.qiaomu.ai/ | grep "词根词缀记忆工坊"

# 5. 清理其他项目的 Git 远程仓库
cd $BASE_DIR/evolutionary-psychology-workshop
git remote remove origin
```

## 彻底解决方案（已在 SKILL.md Step 6 实施）

1. **强制前置检查**：部署前自动移除所有 Git 远程仓库
2. **强制后置验证**：部署后检查 projectId 唯一性
3. **冲突自动检测**：遍历所有项目，发现相同 projectId 立即报错
4. **完整日志记录**：所有部署操作记录到 /tmp/
5. **零容忍策略**：任何检测到的冲突都不允许继续

## 教训总结

> "Copy + Paste 是万恶之源。模板驱动看似高效，实则埋下了隐患。只有从零生成（设计系统驱动），才能确保每个项目真正独立。"

## 影响

- 促使 skill 从"模板驱动"彻底重构为"设计系统驱动"
- 确立了"零模板依赖"的核心原则
- 建立了完善的部署安全检查机制
- gen-html.py 从源头消除了 sed 替换导致的语义残留
