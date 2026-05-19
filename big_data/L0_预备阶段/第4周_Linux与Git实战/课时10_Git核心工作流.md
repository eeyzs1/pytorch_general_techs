# 课时10：Git核心工作流

> **课时时长**：3小时
> **教学方式**：讲演 + 团队协作模拟
> **前置要求**：课时1-9完成

---

## 一、教学目标

1. 理解Git三区概念：工作区、暂存区、版本库
2. 熟练掌握Git核心操作：clone、add、commit、push、pull、fetch
3. 掌握分支管理：branch、checkout、merge、rebase
4. 能够解决merge conflict
5. 理解并实践团队协作工作流（Git Flow）

---

## 二、教学内容

### 2.1 Git三区概念（15分钟）

```
┌─────────────────────────────────────────────────┐
│                  Git 三区模型                      │
├──────────────┬──────────────┬───────────────────┤
│   工作区      │    暂存区     │     版本库         │
│  (Workspace) │  (Stage)     │  (Repository)     │
├──────────────┼──────────────┼───────────────────┤
│              │              │                   │
│  git add ───→│              │                   │
│              │  git commit →│                   │
│              │              │                   │
│  实际文件     │  .git/index  │  .git/objects     │
│  你编辑的地方  │  准备提交     │  已提交的历史      │
└──────────────┴──────────────┴───────────────────┘

文件状态流转:
  Untracked → Staged → Committed → Modified → Staged → ...
        ↑        git add    git commit    编辑文件   git add
        └─────────────────────────────────────────────┘
```

**核心概念对照**：

| 操作 | 命令 | 说明 |
|------|------|------|
| 工作区→暂存区 | git add | 暂存修改，准备提交 |
| 暂存区→版本库 | git commit | 正式提交到本地版本库 |
| 版本库→远程 | git push | 推送到远程仓库 |
| 远程→版本库 | git fetch | 拉取远程更新到本地版本库 |
| 远程→工作区 | git pull | fetch + merge（或rebase） |

### 2.2 Git核心操作（30分钟）

```bash
# ========== 初始化与配置 ==========

# 全局配置（只需做一次）
git config --global user.name "你的名字"
git config --global user.email "your.email@example.com"
git config --global core.editor "code --wait"        # VS Code作为编辑器
git config --global init.defaultBranch main           # 默认分支名

# 查看配置
git config --list
git config --global --list

# ========== 创建仓库 ==========

# 方式1: 从零开始
git init my-project
cd my-project

# 方式2: 克隆已有仓库
git clone https://github.com/username/repo.git
git clone git@github.com:username/repo.git    # SSH方式

# ========== 基本工作流 ==========

# 1. 查看状态
git status                    # 查看工作区状态
git status -s                 # 简洁输出

# 2. 暂存文件
git add file.py               # 暂存单个文件
git add file1.py file2.py     # 暂存多个文件
git add .                     # 暂存所有修改
git add -p                    # 交互式暂存（逐个确认）

# 3. 提交
git commit -m "feat: 添加日志解析功能"
git commit -am "fix: 修复数据清洗bug"    # add所有已跟踪文件并commit

# 4. 查看历史
git log                       # 查看提交历史
git log --oneline             # 简洁一行模式
git log --graph --all --decorate  # 图形化分支历史
git log --author="张三"       # 按作者筛选
git log --since="2024-01-01"  # 按日期筛选
git log -p                    # 显示每次修改的具体内容
git log --stat                # 显示每次修改的文件统计

# 5. 差异对比
git diff                      # 工作区 vs 暂存区
git diff --staged             # 暂存区 vs 最新提交
git diff HEAD                 # 工作区 vs 最新提交
git diff branch1..branch2     # 两个分支之间

# ========== 远程操作 ==========

# 查看远程仓库
git remote -v

# 添加远程仓库
git remote add origin https://github.com/user/repo.git

# 推送
git push origin main          # 推送到远程main分支
git push -u origin main       # 首次推送并建立追踪
git push                      # 之后可以简写

# 拉取
git pull origin main          # 拉取远程main分支
git pull                      # 简化写法（需要已建立追踪）
git pull --rebase             # 使用rebase方式拉取（推荐）

# 获取（不合并）
git fetch origin              # 获取所有远程分支的更新
git fetch origin main         # 只获取main分支

# 查看远程分支
git branch -r                 # 查看远程分支
git branch -a                 # 查看所有分支（本地+远程）
```

### 2.3 分支管理与合并（35分钟）

```bash
# ========== 分支基础操作 ==========

# 查看分支
git branch                    # 本地分支列表
git branch -r                 # 远程分支列表
git branch -a                 # 所有分支

# 创建分支
git branch feature-x          # 创建分支（不切换）
git checkout -b feature-x     # 创建并切换到新分支
git switch -c feature-x       # Git 2.23+ 新语法

# 切换分支
git checkout feature-x        # 切换到feature-x
git switch feature-x          # Git 2.23+ 新语法
git checkout -                # 切换到上一个分支

# 删除分支
git branch -d feature-x       # 删除已合并的分支
git branch -D feature-x       # 强制删除（即使未合并）

# 重命名分支
git branch -m old-name new-name

# ========== 合并（Merge）==========

# 基本合并
git checkout main
git merge feature-x           # 将feature-x合并到当前分支(main)

# Fast-Forward合并（默认，无分支分叉时）
# 特点：不产生合并提交，历史呈线性

# --no-ff合并（推荐用于feature分支）
git merge --no-ff feature-x   # 始终产生合并提交，保留分支历史
# 特点：能看到"功能分支"的完整生命周期

# 压缩合并（Squash）
git merge --squash feature-x
git commit -m "feat: 综合合并feature-x的改动"
# 特点：多个commit合并为一个，历史简洁

# 取消合并
git merge --abort             # 合并冲突时取消

# ========== 变基（Rebase）==========

# Rebase vs Merge
# Merge:  "我做了什么 + 别人做了什么 = 合并结果"
# Rebase: "把我的提交重放到别人最新提交之上"

# 基本使用
git checkout feature-x
git rebase main               # 将feature-x的提交移到main最新提交之后

# 交互式Rebase（强大但谨慎使用）
git rebase -i HEAD~3          # 重新整理最近3个提交
# 可以: pick(保留), squash(合并), reword(改消息), drop(删除), edit(修改)

# 解决冲突后继续
git rebase --continue
git rebase --abort            # 放弃rebase

# ========== 分支策略 ==========

# Git Flow（经典策略）
# main:    生产分支（只接受合并，不直接提交）
# develop: 开发分支（集成分支）
# feature/*: 功能分支（从develop分出，合并回develop）
# release/*: 发布分支（从develop分出，合并到main和develop）
# hotfix/*:  热修复分支（从main分出，合并到main和develop）

# GitHub Flow（简化策略）
# main:    可部署的分支
# feature/*: 功能分支（从main分出，通过PR合并回main）

# 常用流程:
# 1. git checkout -b feature/add-login  从main创建功能分支
# 2. 开发、提交...
# 3. git push origin feature/add-login  推送
# 4. 在GitHub上创建Pull Request
# 5. Code Review后合并到main
# 6. 删除功能分支
```

### 2.4 解决Merge Conflict（20分钟）

```bash
# ========== 冲突的产生 ==========
# 当两个分支修改了同一个文件的同一行时，Git无法自动合并

# 模拟冲突场景:
# 分支A: 修改了 app.py 第5行为 "port = 8080"
# 分支B: 修改了 app.py 第5行为 "port = 9090"
# 合并时 → 冲突！

# ========== 冲突标记 ==========
# 文件中的冲突标记:
# <<<<<<< HEAD        (当前分支的内容)
# port = 8080
# =======            (分隔线)
# port = 9090
# >>>>>>> feature-b   (要合并进来的分支)
#
# 解决方式：编辑文件，删除标记，保留正确内容

# ========== 解决冲突流程 ==========

# 1. 查看冲突文件
git status                    # 显示冲突文件
# both modified: app.py

# 2. 手动编辑文件解决冲突
# 删除 <<<<<<<, =======, >>>>>>> 标记
# 保留正确的代码

# 3. 标记为已解决
git add app.py

# 4. 完成合并
git commit                    # 会自动生成合并提交信息
# 或
git merge --continue

# ========== 冲突解决工具 ==========
# VS Code: 内置冲突解决面板（推荐）
# 点击 "Accept Current" / "Accept Incoming" / "Accept Both"

# 命令行工具:
git mergetool                 # 打开配置的合并工具

# ========== 取消合并 ==========
git merge --abort             # 回到合并前的状态

# ========== 查看冲突历史 ==========
git log --merge               # 查看冲突相关的提交
git diff                       # 查看冲突的具体差异
```

### 2.5 其他重要操作（20分钟）

```bash
# ========== 撤销操作 ==========

# 撤销工作区的修改（未add）
git checkout -- file.txt      # 丢弃工作区的修改
git restore file.txt          # Git 2.23+ 新语法

# 取消暂存（已add但未commit）
git reset HEAD file.txt       # 从暂存区移除
git restore --staged file.txt # Git 2.23+ 新语法

# 修改最近的提交信息
git commit --amend -m "new message"   # 修改提交信息

# 修改最近的提交（包含新修改）
git add forgotten_file.txt
git commit --amend --no-edit         # 将新文件加入上次提交

# 回退版本
git reset --soft HEAD~1       # 回退1个commit，保留修改在暂存区
git reset --mixed HEAD~1      # 回退1个commit，保留修改在工作区（默认）
git reset --hard HEAD~1       # 回退1个commit，丢弃所有修改（危险！）

# 安全回退（推荐）
git revert HEAD               # 创建一个新的commit来撤销上次commit
git revert <commit-hash>      # 撤销指定的commit

# ========== 储藏（Stash）==========
# 临时保存未提交的修改，切换到其他分支工作

git stash                     # 储藏当前修改
git stash save "描述信息"      # 储藏并添加描述
git stash list                # 查看所有储藏
git stash pop                 # 恢复最近的储藏并删除记录
git stash apply               # 恢复最近的储藏但保留记录
git stash drop                # 删除最近的储藏
git stash clear               # 清空所有储藏

# ========== Cherry-Pick ==========
# 将指定commit的修改应用到当前分支

git cherry-pick <commit-hash>          # 应用单个commit
git cherry-pick hash1..hash3           # 应用多个commit

# ========== 标签（Tag）==========
# 给特定commit打标签，常用于标记版本号

git tag v1.0.0                         # 轻量标签
git tag -a v1.0.0 -m "首次发布"        # 附注标签
git tag                                # 列出所有标签
git push origin v1.0.0                 # 推送标签
git push origin --tags                 # 推送所有标签
git checkout v1.0.0                    # 切换到标签

# ========== 其他有用操作 ==========

# 查看谁修改了每行代码
git blame file.py
git blame -L 10,20 file.py            # 查看10-20行

# 搜索提交历史中的代码
git log -S "function_name"            # 搜索添加/删除了指定内容的commit
git log -G "regex_pattern"            # 用正则搜索

# 清理未跟踪的文件
git clean -n       # 预览会删除哪些文件
git clean -f       # 删除未跟踪的文件
git clean -fd      # 删除未跟踪的文件和目录

# 查看引用日志（恢复误操作）
git reflog         # 查看所有HEAD的移动记录
# 可以用于恢复被误删的分支和commit
```

### 2.6 团队协作模拟（40分钟）

```bash
# ========== 场景：模拟3人团队协作开发 ==========

# ---- 开发者A：项目初始化 ----
# 1. 创建项目
mkdir big-data-project
cd big-data-project
git init

# 2. 创建初始文件
echo "# Big Data Project" > README.md
echo "print('Starting...')" > main.py

# 3. 提交
git add .
git commit -m "docs: 初始化项目文档和入口文件"

# 4. 推送到GitHub
git remote add origin https://github.com/user/big-data-project.git
git branch -M main
git push -u origin main


# ---- 开发者A：开发日志解析功能 ----
git checkout -b feature/add-log-parser

# 创建 log_parser.py
cat > log_parser.py << 'EOF'
import re

class LogParser:
    """日志解析器"""
    def parse(self, line):
        """解析单行日志"""
        pattern = r'(?P<ip>\S+).*"(?P<method>\S+) (?P<url>\S+).*" (?P<status>\d+)'
        match = re.match(pattern, line)
        return match.groupdict() if match else None

# 测试
if __name__ == "__main__":
    parser = LogParser()
    test = '192.168.1.1 - - [15/Jan/2024:10:30:00 +0800] "GET /index.html HTTP/1.1" 200 5120'
    result = parser.parse(test)
    print(result)
EOF

git add log_parser.py
git commit -m "feat: 实现日志解析器基础功能"
git push origin feature/add-log-parser

# 在GitHub上创建Pull Request: feature/add-log-parser → main


# ---- 开发者B：clone项目并开发CSV清洗功能 ----
# 1. Clone项目
cd /tmp
git clone https://github.com/user/big-data-project.git
cd big-data-project

# 2. 创建功能分支
git checkout -b feature/add-csv-cleaner

# 3. 开发CSV清洗器
cat > csv_cleaner.py << 'EOF'
import csv

class CSVCleaner:
    """CSV数据清洗器"""
    def clean(self, input_file, output_file):
        """清洗CSV文件：去空行、去重复"""
        seen = set()
        cleaned = []
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not any(row.values()):
                    continue
                row_id = row.get('id', '')
                if row_id in seen:
                    continue
                seen.add(row_id)
                cleaned.append({k: v.strip() for k, v in row.items()})

        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=cleaned[0].keys())
            writer.writeheader()
            writer.writerows(cleaned)

        return len(cleaned)
EOF

git add csv_cleaner.py
git commit -m "feat: 实现CSV清洗器"
git push origin feature/add-csv-cleaner


# ---- 开发者A：查看B的工作并更新 ----
git checkout main
git fetch origin
# 查看B推送的分支
git branch -r

# 拉取最新代码
git pull origin main


# ---- 开发者C：clone项目并编辑main.py ----
cd /tmp
git clone https://github.com/user/big-data-project.git
cd big-data-project

# 修改main.py（与A同时在改）
echo "
from log_parser import LogParser
from csv_cleaner import CSVCleaner

def main():
    print('大数据项目启动中...')
    print('模块已加载: LogParser, CSVCleaner')

if __name__ == '__main__':
    main()
" > main.py

git add main.py
git commit -m "chore: 更新main.py入口文件"
git push origin main


# ---- 开发者A：也修改了main.py（制造冲突）----
cd /path/to/big-data-project  # A的本地目录
echo "
import sys
from log_parser import LogParser

def main():
    print('大数据项目 v1.0')
    print(f'Python: {sys.version}')
    parser = LogParser()
    print('LogParser已就绪')

if __name__ == '__main__':
    main()
" > main.py

git add main.py
git commit -m "feat: 添加入口逻辑和版本信息"

# 尝试push → 失败！（远程有更新的版本）
git push origin main
# ! [rejected] main -> main (non-fast-forward)

# 解决方案：先pull再push
git pull origin main
# → CONFLICT! main.py有冲突！

# 查看冲突
git status
# both modified: main.py

# 在VS Code中解决冲突（或手动编辑）
# 保留两边的合理修改

cat main.py
# 解决冲突后:
git add main.py
git commit -m "merge: 解决main.py冲突，合并入口逻辑"
git push origin main


# ---- 开发者B：拉取最新并rebase ----
cd /tmp/big-data-project
git checkout feature/add-csv-cleaner

# 先获取远程最新
git fetch origin

# 将当前分支rebase到最新main上
git rebase origin/main
# 如果有冲突，解决后 git rebase --continue

# 推送（需要force因为改变了历史）
git push origin feature/add-csv-cleaner --force-with-lease


# ========== PR合并流程 ==========
# 在GitHub上:
# 1. 打开 feature/add-csv-cleaner 的PR
# 2. Code Review
# 3. 通过后合并（Squash and merge / Rebase and merge / Create a merge commit）
# 4. 删除远程分支

# 开发者B更新本地:
git checkout main
git pull origin main
git branch -d feature/add-csv-cleaner  # 删除本地分支
```

### 2.7 提交信息规范（10分钟）

```bash
# ========== Conventional Commits 规范 ==========

# 格式: <type>(<scope>): <description>
#
# type类型:
#   feat:     新功能
#   fix:      Bug修复
#   docs:     文档变更
#   style:    代码格式（不影响代码运行）
#   refactor: 重构（不是新功能也不是修复）
#   perf:     性能优化
#   test:     测试相关
#   chore:    构建过程或辅助工具的变动
#   ci:       CI配置变更

# 好的提交信息:
# "feat: 添加Nginx日志解析器"
# "fix: 修复CSV读取时空行导致的索引错误"
# "refactor: 重构ETL基类，提取公共逻辑"
# "docs: 更新README安装说明"
# "perf: 优化正则表达式预编译，提升解析速度30%"
# "test: 添加日志解析器单元测试"

# 不好的提交信息:
# "修改代码"
# "update"
# "fix bug"
# "..."

# ========== 提交信息最佳实践 ==========
# 1. 使用祈使句："添加" 而不是 "添加了"
# 2. 不超过72字符
# 3. 描述做了什么，不是怎么做的
# 4. 用英文更通用，中文也可以但要统一
```

---

## 三、课堂练习（30分钟）

### 练习：两人一组协作模拟

```bash
# ========== 两人一组，按照以下步骤操作 ==========

# 步骤1: A创建仓库并添加B为协作伙伴
# (在GitHub上: Settings → Collaborators)

# 步骤2: 两人都clone仓库
git clone <repo-url>
cd <repo-name>

# 步骤3: A创建功能分支，添加文件并推送
git checkout -b feature/calculator-a
git commit --allow-empty -m "init"
# ... 添加功能代码 ...
git push origin feature/calculator-a

# 步骤4: B创建功能分支，添加文件并推送
git checkout -b feature/calculator-b
# ... 添加功能代码 ...
git push origin feature/calculator-b

# 步骤5: 两人都在main上做修改（制造冲突）
# A:
git checkout main
echo "Version: 1.0-A" > VERSION
git add VERSION
git commit -m "chore: A更新版本号"
git push origin main

# B: (B需要先pull)
git checkout main
git pull origin main    # 先拉取A的修改
echo "Version: 1.0-B" > VERSION
git add VERSION
git commit -m "chore: B更新版本号"
git push origin main    # 这里会失败

# 步骤6: B解决冲突
git pull origin main    # 触发冲突
# 手动解决VERSION文件的冲突
git add VERSION
git commit -m "merge: 解决VERSION冲突"
git push origin main

# 步骤7: 查看完整的分支历史
git log --graph --all --oneline --decorate
```

---

## 四、课后作业（本周核心考核）

### 必做作业

1. **GitHub绿点连续7天**：每天至少一次有效提交
2. **至少产生3次Pull Request**：
   - 可以是对自己仓库的PR（模拟）
   - 至少1次PR包含多个commit
3. **至少解决一次merge conflict**：
   - 在练习中故意制造冲突
   - 截图记录解决过程
4. **使用以下Git操作**：
   - ⬜ branch + checkout
   - ⬜ merge（至少一次有冲突）
   - ⬜ rebase
   - ⬜ stash
   - ⬜ tag
   - ⬜ revert
   - ⬜ cherry-pick
   - ⬜ git log --graph

### 选做作业

**模拟完整的Git Flow工作流**：

```bash
# 1. 在main分支打标签v0.1.0
# 2. 创建develop分支
# 3. 从develop分出feature/user-auth
# 4. 开发user-auth功能（3-5个commit）
# 5. 合并回develop
# 6. 从develop分出release/1.0
# 7. 修复bug并合并到main和develop
# 8. 在main上打标签v1.0.0
```

---

## 五、Git命令速查表

| 操作 | 命令 |
|------|------|
| 初始化 | git init, git clone |
| 暂存 | git add, git add -p |
| 提交 | git commit, git commit --amend |
| 分支 | git branch, git checkout -b, git switch |
| 合并 | git merge, git rebase |
| 远程 | git push, git pull, git fetch |
| 查看 | git status, git log, git diff, git show |
| 撤销 | git reset, git revert, git checkout -- |
| 储藏 | git stash, git stash pop |
| 标签 | git tag, git push --tags |

---

## 六、参考资源

- [Pro Git（中文版）](https://git-scm.com/book/zh/v2)
- [Git官方文档](https://git-scm.com/docs)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow)
- [Learn Git Branching（可视化学习）](https://learngitbranching.js.org/)