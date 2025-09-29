#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LeetCode 中文站爬虫脚本

功能：
- 获取题目列表（中文标题、难度、是否会员、题号、slug 等）
- 可选：按 slug 获取题目详情（中文描述、标签、代码模版等）

用法示例：
  仅获取列表并保存：
    python crawl.py --output problems_zh_simple.json

  获取列表 + 前 50 道题详情：
    python crawl.py --details --limit 50 --output problems_zh_with_details.json

说明：
- 数据来源：
  列表： https://leetcode.cn/api/problems/algorithms/
  详情(GraphQL)： https://leetcode.cn/graphql
- 该脚本未使用账号登录接口，属于公开信息抓取；若接口策略更改，可能需要添加 Cookie。
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import os
from typing import Any, Dict, List, Optional
import dotenv

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

dotenv.load_dotenv(dotenv.find_dotenv(raise_error_if_not_found=True))
LEETCODE_CN_BASE = "https://leetcode.cn"
PROBLEMS_API = f"{LEETCODE_CN_BASE}/api/problems/algorithms/"
GRAPHQL_API = f"{LEETCODE_CN_BASE}/graphql"


def _build_session() -> requests.Session:
    """Create a requests session with sane retries and headers."""
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST"],
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retries, pool_maxsize=10)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    session.headers.update(
        {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "application/json, text/plain, */*",
            "Referer": f"{LEETCODE_CN_BASE}/problemset/all/",
            "Origin": LEETCODE_CN_BASE,
        }
    )
    return session


def get_leetcode_questions_simple(session: Optional[requests.Session] = None) -> List[Dict[str, Any]]:
    """获取题目列表（基础信息）。

    返回字段示例：
    [
      {
        "question_id": 1,
        "frontend_id": "1",
        "title_cn": "两数之和",
        "title": "Two Sum",
        "title_slug": "two-sum",
        "difficulty": "Easy",
        "paid_only": False,
        "status": None
      }, ...
    ]
    """

    s = session or _build_session()
    resp = s.get(PROBLEMS_API, timeout=20)
    resp.raise_for_status()
    data = resp.json()

    results: List[Dict[str, Any]] = []
    for item in data.get("stat_status_pairs", []):
        stat = item.get("stat", {})
        difficulty_level = item.get("difficulty", {}).get("level", 0)
        difficulty = {1: "Easy", 2: "Medium", 3: "Hard"}.get(difficulty_level, "Unknown")

        results.append(
            {
                "question_id": stat.get("question_id"),
                "frontend_id": stat.get("frontend_question_id"),
                "title_cn": stat.get("question__title_cn"),
                "title": stat.get("question__title"),
                "title_slug": stat.get("question__title_slug"),
                "difficulty": difficulty,
                "paid_only": bool(item.get("paid_only")),
                "status": item.get("status"),
            }
        )

    return results


def get_question_detail(title_slug: str, session: Optional[requests.Session] = None) -> Dict[str, Any]:
    """按 slug 获取题目详情（包含中文翻译字段）。"""
    s = session or _build_session()

    graphql_query = {
        "operationName": "questionData",
        "variables": {"titleSlug": title_slug},
        "query": (
            "query questionData($titleSlug: String!) {\n"
            "  question(titleSlug: $titleSlug) {\n"
            "    questionId\n"
            "    questionFrontendId\n"
            "    title\n"
            "    titleSlug\n"
            "    translatedTitle\n"
            "    translatedContent\n"
            "    content\n"
            "    difficulty\n"
            "    likes\n"
            "    dislikes\n"
            "    topicTags { name slug translatedName }\n"
            "    codeSnippets { lang langSlug code }\n"
            "    hints\n"
            "    similarQuestions\n"
            "  }\n"
            "}"
        ),
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Referer": f"{LEETCODE_CN_BASE}/problems/{title_slug}/",
        "Origin": LEETCODE_CN_BASE,
    }

    # 轻度速率控制，避免触发反爬
    time.sleep(0.3)
    r = s.post(GRAPHQL_API, headers=headers, json=graphql_query, timeout=30)
    r.raise_for_status()
    payload = r.json()

    q = (payload or {}).get("data", {}).get("question")
    if not q:
        return {"titleSlug": title_slug, "error": payload}
    return q


def save_json(data: Any, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ----------------------------- Feishu Bitable ----------------------------- #

class FeishuBitableClient:
    """飞书多维表格（Bitable）客户端，支持获取租户 token、增/改记录。

    参考文档：
    - 认证: https://open.feishu.cn/document/server-docs/authentication-management/access-token/tenant_access_token_internal
    - Bitable 记录: https://open.feishu.cn/document/server-docs/docs/bitable-v1/record/create
    """

    def __init__(
        self,
        app_id: str,
        app_secret: str,
        app_token: str,
        table_id: str,
        base_url: str = "https://open.feishu.cn",
        session: Optional[requests.Session] = None,
    ) -> None:
        self.app_id = app_id
        self.app_secret = app_secret
        self.app_token = app_token  # Bitable Base 的 app_token（也叫 app_id/app_token）
        self.table_id = table_id
        self.base_url = base_url.rstrip("/")
        self.s = session or _build_session()
        self._tenant_token: Optional[str] = None

    def _request(self, method: str, url: str, **kwargs) -> requests.Response:
        """统一请求并在出错时打印可读信息（含响应体）。"""
        try:
            resp = self.s.request(method=method, url=url, timeout=kwargs.pop("timeout", 20), **kwargs)
            resp.raise_for_status()
            return resp
        except requests.HTTPError as e:
            text = getattr(e.response, "text", "")
            try:
                data = e.response.json()
            except Exception:
                data = None
            msg = f"HTTP {e.response.status_code} error for {url}: {text or data}"
            raise requests.HTTPError(msg) from e

    def tenant_access_token(self) -> str:
        if self._tenant_token:
            return self._tenant_token
        url = f"{self.base_url}/open-apis/auth/v3/tenant_access_token/internal"
        r = self._request("POST", url, json={"app_id": self.app_id, "app_secret": self.app_secret})
        data = r.json()
        if data.get("code") != 0:
            raise RuntimeError(f"get tenant token failed: {data}")
        self._tenant_token = data["tenant_access_token"]
        return self._tenant_token

    def _auth_headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.tenant_access_token()}"}

    def list_records(self, filter_formula: Optional[str] = None, page_size: int = 1) -> Dict[str, Any]:
        url = f"{self.base_url}/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/records"
        params: Dict[str, Any] = {"page_size": page_size}
        if filter_formula:
            params["filter"] = filter_formula
        r = self._request("GET", url, params=params, headers=self._auth_headers())
        return r.json()

    def create_record(self, fields: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/records"
        payload = {"fields": fields}
        r = self._request("POST", url, headers=self._auth_headers(), json=payload)
        return r.json()

    def update_record(self, record_id: str, fields: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/records/{record_id}"
        payload = {"fields": fields}
        r = self._request("PUT", url, headers=self._auth_headers(), json=payload)
        return r.json()

    def verify_access(self) -> None:
        """预检：尝试拉取一条记录，检查表可访问性和权限。抛错时包含详细信息。"""
        url = f"{self.base_url}/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/records"
        _ = self._request("GET", url, params={"page_size": 1}, headers=self._auth_headers())


def _build_bitable_fields(q: Dict[str, Any]) -> Dict[str, Any]:
    """将题目字典映射为 Bitable 的 fields 映射。字段名可在飞书表中自行创建对应列名。

    默认字段：
    - frontend_id, title_cn, title, title_slug, difficulty, paid_only, status
    - translatedTitle, translatedContent, likes, dislikes, questionFrontendId
    - tags (逗号分隔)，updated_at（时间戳）
    """
    tags = q.get("topicTags") or []
    tag_names = [t.get("translatedName") or t.get("name") for t in tags if isinstance(t, dict)]
    fields = {
        "frontend_id": q.get("frontend_id") or q.get("questionFrontendId"),
        "title_cn": q.get("title_cn") or q.get("translatedTitle"),
        "title": q.get("title"),
        "title_slug": q.get("title_slug") or q.get("titleSlug"),
        "difficulty": q.get("difficulty") or q.get("difficulty"),
        "paid_only": q.get("paid_only"),
        "status": q.get("status"),
        "translatedTitle": q.get("translatedTitle"),
        "translatedContent": q.get("translatedContent"),
        "likes": q.get("likes"),
        "dislikes": q.get("dislikes"),
        "questionFrontendId": q.get("questionFrontendId") or q.get("frontend_id"),
        "tags": ", ".join([x for x in tag_names if x]),
        "updated_at": int(time.time()),
    }
    # 过滤 None
    return {k: v for k, v in fields.items() if v is not None}


def _feishu_upsert_question(
    client: FeishuBitableClient,
    q: Dict[str, Any],
    unique_field: str = "title_slug",
) -> str:
    """按唯一字段在 Bitable 中增量写入：存在则更新，不存在则创建。

    返回记录的 record_id。
    """
    fields = _build_bitable_fields(q)

    # 从原始 q 中取唯一键值（优先 detail 字段名）
    value = (
        q.get(unique_field)
        or q.get("titleSlug")
        or q.get("title_slug")
        or q.get("frontend_id")
        or q.get("questionFrontendId")
    )
    if value is None:
        raise ValueError(f"unique_field '{unique_field}' not found in question: {q.keys()}")

    # 构造 filter 公式：字符串需双引号包裹
    if isinstance(value, (int, float)):
        filter_formula = f"CurrentValue.{unique_field} = {value}"
    else:
        # 转义引号
        val = str(value).replace('"', '\\"')
        filter_formula = f"CurrentValue.{unique_field} = \"{val}\""

    data = client.list_records(filter_formula=filter_formula, page_size=1)
    items = (data or {}).get("data", {}).get("items", [])
    if items:
        record_id = items[0].get("record_id")
        client.update_record(record_id, fields)
        return record_id
    else:
        created = client.create_record(fields)
        return (created or {}).get("data", {}).get("record", {}).get("record_id", "")


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="LeetCode 中文题目爬虫")
    parser.add_argument(
        "--output",
        default="problems_zh_simple.json",
        help="输出 JSON 文件名（默认：problems_zh_simple.json）",
    )
    parser.add_argument(
        "--details",
        action="store_true",
        help="是否抓取题目详情（会逐题访问 GraphQL，较慢）",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="限制抓取题目的数量（0 表示不限制）",
    )
    parser.add_argument(
        "--start-index",
        type=int,
        default=0,
        help="从列表的某个索引开始抓取（用于断点续抓）",
    )
    # Feishu Bitable 相关参数：可用环境变量兜底
    parser.add_argument("--feishu", action="store_true", help="是否将数据增量写入飞书多维表格（Bitable）")
    parser.add_argument("--feishu-app-id", default=os.getenv("FEISHU_APP_ID", ""))
    parser.add_argument("--feishu-app-secret", default=os.getenv("FEISHU_APP_SECRET", ""))
    parser.add_argument("--feishu-base-id", default=os.getenv("FEISHU_BASE_APP_TOKEN", ""), help="Bitable 的 app_token")
    parser.add_argument("--feishu-table-id", default=os.getenv("FEISHU_TABLE_ID", ""))
    parser.add_argument(
        "--feishu-unique-field",
        default=os.getenv("FEISHU_UNIQUE_FIELD", "title_slug"),
        help="用于增量去重的唯一字段（默认为 title_slug）",
    )

    args = parser.parse_args(argv)
    args.limit = 1
    args.details = True
    args.feishu = True
    session = _build_session()

    print("[INFO] 获取题目列表...")
    questions = get_leetcode_questions_simple(session)
    print(f"[INFO] 共获取到 {len(questions)} 道题目")

    # 根据 limit 和 start-index 截取
    start = max(0, args.start_index)
    if args.limit and args.limit > 0:
        subset = questions[start : start + args.limit]
    else:
        subset = questions[start:]

    # 若未开启飞书写入，仅保存 JSON 或继续抓详情
    if not args.details and not args.feishu:
        print(f"[INFO] 仅保存列表：{args.output}")
        save_json(questions, args.output)
        return 0

    print(f"[INFO] 开始抓取详情（共 {len(subset)} 道）...")
    enriched: List[Dict[str, Any]] = []
    feishu_client: Optional[FeishuBitableClient] = None
    if args.feishu:
        missing = [
            name
            for name, val in [
                ("--feishu-app-id", args.feishu_app_id),
                ("--feishu-app-secret", args.feishu_app_secret),
                ("--feishu-base-id", args.feishu_base_id),
                ("--feishu-table-id", args.feishu_table_id),
            ]
            if not val
        ]
        if missing:
            print(f"[ERROR] 缺少飞书参数: {', '.join(missing)}；将仅输出 JSON 文件")
        else:
            feishu_client = FeishuBitableClient(
                app_id=args.feishu_app_id,
                app_secret=args.feishu_app_secret,
                app_token=args.feishu_base_id,
                table_id=args.feishu_table_id,
                session=session,
            )
            try:
                feishu_client.verify_access()
                print("[INFO] 飞书预检通过：表可访问且权限正常")
            except Exception as e:
                print(f"[ERROR] 飞书预检失败：{e}\n[HINT] 请检查：\n- 应用是否具有 bitable:record:read, bitable:record:write 权限\n- 应用是否已安装到你的租户（企业自建应用需在企业内上架/安装）\n- 目标多维表格是否已将应用添加为协作者（在表的共享设置中添加应用，并授予可读写权限）\n- app_token 与 table_id 是否对应同一个 Base\n- 环境变量/参数是否正确（区分中国区 open.feishu.cn 与海外域名）")

    for idx, q in enumerate(subset, 1):
        merged = dict(q)
        slug = q.get("title_slug")
        if args.details:
            try:
                detail = get_question_detail(slug, session=session)
                merged = {**q, **detail}
            except Exception as e:
                print(f"[WARN] 获取详情失败 {slug}: {e}")
                merged = {**q, "detail_error": str(e)}

        enriched.append(merged)

        # 增量写入飞书
        if feishu_client:
            try:
                _feishu_upsert_question(feishu_client, merged, unique_field=args.feishu_unique_field)
            except Exception as e:
                print(f"[WARN] 写入飞书失败 {slug}: {e}")

        if idx % 20 == 0:
            print(f"[INFO] 已处理 {idx}/{len(subset)} 题...（中间保存 JSON 一次）")
            save_json(enriched, args.output)

    print(f"[INFO] 保存结果到：{args.output}")
    save_json(enriched, args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())

