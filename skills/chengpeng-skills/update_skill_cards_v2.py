"""Update skill_card.md files: Group field + add GitHub path field"""
import os, glob, re

NEW_GROUP = "程鹏211125120093、诸葛梦豪221125120224、施贵峰221125120167"

bases = [
    r"C:\Users\17588\.openclaw\workspace\skills",
    r"C:\Users\17588\.openclaw\workspace\skills_en"
]

count = 0
for base in bases:
    for fpath in glob.glob(os.path.join(base, "chengpeng-*", "skill_card.md")):
        folder_name = os.path.basename(os.path.dirname(fpath))
        github_path = f"skills/{folder_name}/"
        
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        changes = []
        
        # 1. Update Group line
        old_group = None
        for g in re.findall(r'^\| Group \| .+ \|$', content, re.MULTILINE):
            old_group = g
        if old_group:
            content = content.replace(old_group, f"| Group | {NEW_GROUP} |")
            changes.append("Group")
        
        # 2. Add GitHub 路径 after Target Users line
        target_line = None
        for t in re.findall(r'^\| Target Users \| .+ \|$', content, re.MULTILINE):
            target_line = t
        if target_line:
            # Find the position after Target Users line
            github_line = f"| GitHub 路径 | {github_path} |"
            if github_line not in content:
                content = content.replace(target_line, target_line + "\n" + github_line)
                changes.append("GitHub 路径")
        
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f'  [OK] {folder_name}: {", ".join(changes)}')
        count += 1

print(f'\nDone! Updated {count} files')
