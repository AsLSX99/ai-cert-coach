#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""认证题库监考与模考记账（纯标准库，Python >= 3.9）。

用法：
  python cert.py programs                          # 列出全部轨道（含考试事实）
  python cert.py track <slug>                      # 考试事实 + 领域权重 + 评估与计划
  python cert.py route <slug>                      # 课程路线（required/core、领域映射）
  python cert.py count <mock>                      # 卷面信息（题数/限时/类型）
  python cert.py ask <mock> <n>                    # 只出第 n 题题面与选项（答案封印）
  python cert.py reveal <mock> <n>                 # 作答完成后亮答案/解析/回链
  python cert.py log <slug> --mock mock-01 --correct X --total Y [--timed]
  python cert.py status                            # 各轨模考原始分趋势与排期

<mock> 形如 ccao-f/mock-01 或 mcpa-f/mock-02（在 certifications/*/assessments/ 下解析）
<slug>  形如 ccao-f / ccar-p / mcpa-f（在 certifications/*/tracks/ 下解析）
数据文件：./cert-progress.json
"""
import argparse
import json
import pathlib
import sys
from datetime import datetime, timedelta

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

DATA_FILE = pathlib.Path("cert-progress.json")


# ---------- 进度 ----------

def load():
    if DATA_FILE.exists():
        try:
            data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as e:
            sys.exit("进度文件损坏：%s（修复或删除 %s 后重试）" % (e, DATA_FILE))
        data.setdefault("tracks", {})
        data.setdefault("records", [])
        return data
    return {"tracks": {}, "records": []}


def save(data):
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                         encoding="utf-8")


# ---------- 定位与解析 ----------

def find_root():
    p = pathlib.Path.cwd().resolve()
    for _ in range(5):
        if (p / "certifications").is_dir():
            return p
        if p.parent == p:
            break
        p = p.parent
    return None


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        sys.exit("读取失败 %s：%s" % (path, e))


def track_file(slug):
    root = find_root()
    if not root:
        sys.exit("未找到课程仓库的 certifications/ 目录（先 git clone）")
    for prog in sorted((root / "certifications").iterdir()):
        f = prog / "tracks" / ("%s.json" % slug)
        if f.exists():
            return prog, f
    sys.exit("找不到轨道 %r（可用：python cert.py programs）" % slug)


def mock_file(mock):
    root = find_root()
    if not root:
        sys.exit("未找到课程仓库的 certifications/ 目录")
    if "/" not in mock:
        sys.exit("<mock> 形如 ccao-f/mock-01 或 mcpa-f/mock-02")
    sub, _, name = mock.partition("/")
    for prog in sorted((root / "certifications").iterdir()):
        f = prog / "assessments" / sub / ("%s.json" % name)
        if f.exists():
            return f
    sys.exit("找不到评估卷 %r" % mock)


# ---------- 命令 ----------

def cmd_programs(_args):
    root = find_root()
    if not root:
        sys.exit("未找到课程仓库的 certifications/ 目录")
    found = False
    for prog in sorted((root / "certifications").iterdir()):
        pj = prog / "program.json"
        if not pj.exists():
            continue
        prog_meta = read_json(pj)
        found = True
        print("【%s】%s" % (prog.name, prog_meta.get("name", "")))
        print("  lastVerified: %s" % prog_meta.get("lastVerified", "?"))
        tracks_dir = prog / "tracks"
        track_files = sorted(tracks_dir.glob("*.json")) if tracks_dir.is_dir() else []
        for tf in track_files:
            t = read_json(tf)
            ex = t.get("exam", {})
            print("  %-10s %-46s %s题/%smin/$%s pass=%s" % (
                t.get("slug", tf.stem), (t.get("credential") or "")[:46],
                ex.get("items", "?"), ex.get("timeLimitMinutes", "?"),
                ex.get("feeUsd", "?"), ex.get("passingScaledScore", "未公布")))
        print()
    if not found:
        sys.exit("certifications/ 下没有 program.json")


def cmd_track(args):
    prog, tf = track_file(args.slug)
    t = read_json(tf)
    ex = t.get("exam", {})
    print("%s（%s）· 体系 %s" % (t.get("credential"), t.get("examCode", "-"), prog.name))
    print("受众：%s" % (t.get("audience") or "")[:100])
    print("-" * 70)
    print("题数 %s · 限时 %s min · 费用 $%s · 通过 %s/%s · 有效期 %s 月" % (
        ex.get("items"), ex.get("timeLimitMinutes"), ex.get("feeUsd"),
        ex.get("passingScaledScore", "未公布"),
        ex.get("scoreScale", "-"), ex.get("validityMonths", "?")))
    print("题型 %s · 交付 %s · 指南 %s（%s）" % (
        ex.get("format"), ex.get("delivery"), ex.get("guideVersion"),
        ex.get("effective")))
    print("-" * 70)
    print("领域权重：")
    for d in t.get("domains", []):
        print("  %-38s %3s%%  (%d objectives)" % (
            d.get("id"), d.get("weight"), len(d.get("objectives", []))))
    print("-" * 70)
    print("评估卷：")
    for a in t.get("assessments", []):
        print("  %-12s %-10s %s min  %s" % (
            a.get("kind"), a.get("path", "").split("/")[-1],
            a.get("timeLimitMinutes"), a.get("title")))
    plans = t.get("studyPlans", [])
    if plans:
        print("学习计划：%s" % "、".join(p.get("id", "?") for p in plans))


def cmd_route(args):
    _, tf = track_file(args.slug)
    t = read_json(tf)
    lessons = t.get("lessons", [])
    if not lessons:
        sys.exit("该轨道 JSON 没有 lessons 字段")
    print("%s 路线（%d 课）" % (t.get("examCode", args.slug), len(lessons)))
    for i, l in enumerate(lessons, 1):
        path = l.get("path", "")
        name = path.rstrip("/").split("/")[-1]
        print("%3d. [%-6s %-8s] %-46s → %s" % (
            i, l.get("role", "-"), "必修" if l.get("required") else "选修",
            name[:46], ",".join(l.get("domains", []))[:34]))


def cmd_count(args):
    m = read_json(mock_file(args.mock))
    qs = m.get("questions", [])
    print("%s（%s）" % (m.get("title"), m.get("kind")))
    print("题数 %d · 限时 %s 分钟 · 版本 v%s" % (
        len(qs), m.get("timeLimitMinutes"), m.get("version")))
    types = {}
    domains = {}
    for q in qs:
        types[q.get("type", "?")] = types.get(q.get("type", "?"), 0) + 1
        domains[q.get("domain", "?")] = domains.get(q.get("domain", "?"), 0) + 1
    print("题型：%s" % "、".join("%s×%d" % kv for kv in sorted(types.items())))
    print("领域分布：%s" % "、".join("%s×%d" % kv for kv in sorted(domains.items())))
    print("监考规则：全卷作答完成前不 reveal；到点停笔。")


def cmd_ask(args):
    m = read_json(mock_file(args.mock))
    qs = m.get("questions", [])
    if not (1 <= args.n <= len(qs)):
        sys.exit("题号须在 1..%d" % len(qs))
    q = qs[args.n - 1]
    print("=" * 66)
    print("[%s] 第 %d/%d 题 · %s · domain: %s" % (
        m.get("kind"), args.n, len(qs), q.get("type"), q.get("domain")))
    print("-" * 66)
    print(q.get("prompt", ""))
    print("-" * 66)
    for i, opt in enumerate(q.get("options", [])):
        print("  [%d] %s" % (i, opt))
    print("=" * 66)
    print("（correct/explanation 封印——全卷作答完成后 reveal）")


def cmd_reveal(args):
    m = read_json(mock_file(args.mock))
    qs = m.get("questions", [])
    if not (1 <= args.n <= len(qs)):
        sys.exit("题号须在 1..%d" % len(qs))
    q = qs[args.n - 1]
    print("第 %d 题答案：%s" % (args.n, q.get("correct")))
    print("解析：%s" % q.get("explanation", ""))
    refs = q.get("references", [])
    if refs:
        print("回链：%s" % "、".join(refs))


def cmd_log(args):
    if args.correct < 0 or args.total <= 0 or args.correct > args.total:
        sys.exit("分数不合法（0 <= correct <= total）")
    data = load()
    slug = args.slug
    entry = data["tracks"].setdefault(slug, {"mocks": [], "next_due": None})
    pct = round(100.0 * args.correct / args.total, 1)
    rec = {
        "ts": datetime.now().isoformat(timespec="seconds"),
        "slug": slug,
        "mock": args.mock,
        "correct": args.correct,
        "total": args.total,
        "raw_pct": pct,
        "timed": bool(args.timed),
    }
    data["records"].append(rec)
    entry["mocks"].append(rec)
    entry["last_pct"] = pct
    entry["next_due"] = (datetime.now() + timedelta(days=7)).date().isoformat()
    save(data)
    print("%s · %s 原始分 %s/%s（%s%%%s）" % (
        slug, args.mock, args.correct, args.total, pct,
        "，全真限时" if args.timed else "，非全真"))
    print("⚠️ 原始分 ≠ 官方量表分（100-1000），不能预测官方结果"
          if slug.startswith(("ccao", "ccdv", "ccar")) else
          "⚠️ MCPA 官方通过分未公布，只看趋势")
    print("下次模考排期：%s（+7 天；弱项先回炉）" % entry["next_due"])


def cmd_status(_args):
    data = load()
    tracks, records = data["tracks"], data["records"]
    if not tracks:
        print("没有模考记录。先：python cert.py programs")
        return
    print("模考记录 %d 条 · 覆盖 %d 条轨" % (len(records), len(tracks)))
    print("-" * 64)
    for slug in sorted(tracks):
        e = tracks[slug]
        mocks = e.get("mocks", [])
        trend = " → ".join("%s%%" % m["raw_pct"] for m in mocks[-5:])
        line = "%-10s 最新 %s%% · 历史：%s" % (
            slug, e.get("last_pct", "?"), trend or "无")
        if e.get("next_due"):
            line += " · 下次 %s" % e["next_due"]
        print(line)
    if records:
        print("-" * 64)
        last = records[-1]
        print("最近：%s · %s · %s · %s%%（%s）" % (
            last["ts"][:16], last["slug"], last["mock"], last["raw_pct"],
            "限时" if last.get("timed") else "非限时"))
        print("提醒：原始分只用来找洞，不预测官方结果。")


def main():
    ap = argparse.ArgumentParser(description="认证题库监考与模考记账")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("programs", help="列全部轨道")
    p.set_defaults(func=cmd_programs)

    p = sub.add_parser("track", help="轨道考试事实与领域权重")
    p.add_argument("slug")
    p.set_defaults(func=cmd_track)

    p = sub.add_parser("route", help="课程路线")
    p.add_argument("slug")
    p.set_defaults(func=cmd_route)

    p = sub.add_parser("count", help="卷面信息")
    p.add_argument("mock")
    p.set_defaults(func=cmd_count)

    p = sub.add_parser("ask", help="出题（答案封印）")
    p.add_argument("mock")
    p.add_argument("n", type=int)
    p.set_defaults(func=cmd_ask)

    p = sub.add_parser("reveal", help="作答后亮答案")
    p.add_argument("mock")
    p.add_argument("n", type=int)
    p.set_defaults(func=cmd_reveal)

    p = sub.add_parser("log", help="记模考原始分")
    p.add_argument("slug")
    p.add_argument("--mock", required=True)
    p.add_argument("--correct", type=int, required=True)
    p.add_argument("--total", type=int, required=True)
    p.add_argument("--timed", action="store_true")
    p.set_defaults(func=cmd_log)

    p = sub.add_parser("status", help="总览")
    p.set_defaults(func=cmd_status)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
