"""Update Group field in all skill_card.md files from 课程项目 to 程鹏、诸葛梦豪、施贵峰"""
import os, glob

bases = [
    r"C:\Users\17588\.openclaw\workspace\skills",
    r"C:\Users\17588\.openclaw\workspace\skills_en"
]

count = 0
for base in bases:
    for fpath in glob.glob(os.path.join(base, "*", "skill_card.md")):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        if '课程项目' in content:
            content = content.replace('课程项目', '程鹏、诸葛梦豪、施贵峰')
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'  [OK] {fpath}')
            count += 1
        else:
            print(f'  [SKIP] {os.path.basename(os.path.dirname(fpath))} (no match)')

print(f'\nDone! Updated {count} files')
