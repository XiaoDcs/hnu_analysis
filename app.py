from flask import Flask, jsonify, render_template, request
import pandas as pd
import json
import os
from functools import lru_cache

app = Flask(__name__)

# ---------------------------
# Configuration
# ---------------------------
YEARS = list(range(2020, 2026))  # 2020-2025 inclusive
GUANGDONG_DATA_FILE = "guangdong_data_fixed.json"

# ---------------------------
# Data loading
# ---------------------------
@lru_cache(maxsize=1)
def load_guangdong_dataset():
    """加载广东省数据"""
    if not os.path.exists(GUANGDONG_DATA_FILE):
        print(f"错误: 找不到数据文件 {GUANGDONG_DATA_FILE}")
        return pd.DataFrame()
    
    with open(GUANGDONG_DATA_FILE, 'r', encoding='utf-8') as f:
        guangdong_data = json.load(f)
    
    print(f"✓ 加载广东省数据: {len(guangdong_data)} 年份")
    
    # 转换为DataFrame
    rows = []
    for year_str, year_data in guangdong_data.items():
        year = int(year_str)
        for item in year_data:
            try:
                rows.append({
                    "year": year,
                    "province": "广东",
                    "major": item.get("zymc", ""),
                    "department": item.get("yxmc", ""),
                    "exam_category": item.get("kl", ""),
                    "plan_type": item.get("jhlbmc", ""),
                    "duration": item.get("xz", ""),
                    "count": int(item.get("zsrs", 0))
                })
            except ValueError:
                pass
    
    df = pd.DataFrame(rows)
    print(f"✓ DataFrame: {len(df)} 条记录, {len(df['major'].unique())} 个专业")
    return df

# ---------------------------
# API Endpoints
# ---------------------------
@app.route("/api/guangdong_majors")
def api_guangdong_majors():
    """返回广东省所有专业列表"""
    df = load_guangdong_dataset()
    majors = sorted(df["major"].unique())
    majors = [m for m in majors if m.strip()]  # 移除空字符串
    return jsonify({"majors": majors})

@app.route("/api/guangdong_major_trend")
def api_guangdong_major_trend():
    """返回广东省特定专业的历年数据
    
    Query params:
        major (required): 专业名称
    """
    major = request.args.get("major", "").strip()
    if not major:
        return jsonify({"error": "需要指定专业名称"}), 400
    
    df = load_guangdong_dataset()
    filtered_df = df[df["major"] == major]
    
    if filtered_df.empty:
        return jsonify({"error": f"未找到专业 '{major}' 的数据"}), 404
    
    # 按年份聚合数据
    yearly_data = []
    for year in YEARS:
        year_df = filtered_df[filtered_df["year"] == year]
        total_count = int(year_df["count"].sum())
        
        # 获取详细信息
        details = []
        for _, row in year_df.iterrows():
            details.append({
                "department": str(row["department"]),
                "exam_category": str(row["exam_category"]),
                "plan_type": str(row["plan_type"]),
                "duration": str(row["duration"]),
                "count": int(row["count"])
            })
        
        yearly_data.append({
            "year": int(year),
            "total_count": total_count,
            "details": details
        })
    
    return jsonify({
        "major": str(major),
        "province": "广东",
        "yearly_data": yearly_data
    })

@app.route("/api/analysis")
def api_analysis():
    """返回聚合统计数据 (仅限广东省)"""
    df = load_guangdong_dataset()

    # 关键词过滤
    keyword = request.args.get("keyword", "").strip()
    if keyword:
        df = df[df["major"].str.contains(keyword, na=False)]

    # 年度总计
    year_totals = (
        df.groupby("year")["count"]
        .sum()
        .sort_index()
        .apply(lambda x: int(x))  # 转换为Python int
        .to_dict()
    )

    # 所选年份的专业分布
    try:
        selected_year = int(request.args.get("year", max(YEARS)))
    except ValueError:
        selected_year = max(YEARS)
    
    major_totals = (
        df[df["year"] == selected_year]
        .groupby("major")["count"]
        .sum()
        .sort_values(ascending=False)
        .apply(lambda x: int(x))  # 转换为Python int
        .to_dict()
    )

    return jsonify({
        "year_totals": year_totals,
        "major_totals": major_totals,  # 改为专业分布而不是省份
        "selected_year": selected_year,
    })

@app.route("/api/stats")
def api_stats():
    """返回数据统计信息"""
    df = load_guangdong_dataset()
    
    stats = {
        "total_records": int(len(df)),
        "total_majors": int(len(df["major"].unique())),
        "total_students": int(df["count"].sum()),
        "years_covered": [int(year) for year in sorted(df["year"].unique())],
        "sample_majors": sorted(df["major"].unique())[:10]
    }
    
    return jsonify(stats)

@app.route("/api/department_analysis")
def api_department_analysis():
    """分析各学院的招生情况
    
    Query params:
        year (optional): 指定年份分析 (默认所有年份)
    """
    df = load_guangdong_dataset()
    
    # 过滤掉学院字段为空的记录
    df = df[df["department"].str.strip() != ""]
    
    year = request.args.get("year")
    if year:
        try:
            year = int(year)
            df = df[df["year"] == year]
        except ValueError:
            pass
    
    # 按学院和年份统计
    dept_year_stats = []
    
    departments = sorted(df["department"].unique())
    years = sorted(df["year"].unique())
    
    for dept in departments:
        dept_df = df[df["department"] == dept]
        
        dept_info = {
            "department": dept,
            "total_students": int(dept_df["count"].sum()),
            "years_data": []
        }
        
        for year in years:
            year_df = dept_df[dept_df["year"] == year]
            
            if not year_df.empty:
                majors_info = []
                for _, row in year_df.iterrows():
                    majors_info.append({
                        "major": str(row["major"]),
                        "count": int(row["count"]),
                        "plan_type": str(row["plan_type"]),
                        "exam_category": str(row["exam_category"])
                    })
                
                dept_info["years_data"].append({
                    "year": int(year),
                    "total_count": int(year_df["count"].sum()),
                    "major_count": len(year_df),
                    "majors": majors_info
                })
        
        if dept_info["years_data"]:  # 只返回有数据的学院
            dept_year_stats.append(dept_info)
    
    return jsonify({
        "departments": dept_year_stats,
        "summary": {
            "total_departments": len(dept_year_stats),
            "years_covered": [int(y) for y in years],
            "filtered_records": int(len(df))
        }
    })

@app.route("/api/major_comparison")
def api_major_comparison():
    """专业横向比较表格数据
    
    Query params:
        keyword (optional): 专业名称关键词筛选
        sort_by (optional): 排序方式 ('total'|'latest'|'name')
    """
    df = load_guangdong_dataset()
    
    # 关键词筛选
    keyword = request.args.get("keyword", "").strip()
    if keyword:
        df = df[df["major"].str.contains(keyword, na=False)]
    
    # 构建专业对比表格
    majors = sorted(df["major"].unique())
    years = sorted(df["year"].unique())
    
    comparison_data = []
    
    for major in majors:
        major_df = df[df["major"] == major]
        
        row_data = {
            "major": major,
            "years": {},
            "total": 0
        }
        
        for year in years:
            year_count = int(major_df[major_df["year"] == year]["count"].sum())
            row_data["years"][str(year)] = year_count
            row_data["total"] += year_count
        
        # 添加一些统计信息
        year_counts = [row_data["years"][str(y)] for y in years]
        row_data["latest"] = year_counts[-1] if year_counts else 0
        row_data["average"] = round(row_data["total"] / len(years), 1)
        row_data["max_year"] = max(year_counts) if year_counts else 0
        row_data["min_year"] = min(year_counts) if year_counts else 0
        
        comparison_data.append(row_data)
    
    # 排序
    sort_by = request.args.get("sort_by", "total")
    if sort_by == "total":
        comparison_data.sort(key=lambda x: x["total"], reverse=True)
    elif sort_by == "latest":
        comparison_data.sort(key=lambda x: x["latest"], reverse=True)
    elif sort_by == "name":
        comparison_data.sort(key=lambda x: x["major"])
    
    return jsonify({
        "comparison_data": comparison_data,
        "years": [int(y) for y in years],
        "summary": {
            "total_majors": len(comparison_data),
            "total_students": sum(row["total"] for row in comparison_data),
            "years_covered": [int(y) for y in years]
        }
    })

# ---------------------------
# Front-end routes
# ---------------------------
@app.route("/")
def index():
    return render_template("index_guangdong.html", years=YEARS)

@app.route("/guangdong")
def guangdong():
    return render_template("guangdong.html", years=YEARS)

@app.route("/departments")
def departments():
    return render_template("departments.html", years=YEARS)

@app.route("/comparison")
def comparison():
    return render_template("comparison.html", years=YEARS)

if __name__ == "__main__":
    import os
    
    # 获取端口号，优先使用环境变量，默认为5000
    port = int(os.environ.get('PORT', 5000))
    
    # 在生产环境中监听所有接口，在开发环境中只监听本地
    host = '0.0.0.0' if os.environ.get('PORT') else '127.0.0.1'
    
    print(f"🚀 启动湖南大学广东省招生数据分析系统...")
    print(f"📡 服务器地址: http://{host}:{port}")
    print(f"📊 数据覆盖: 2020-2025年，353条记录")
    
    app.run(host=host, port=port, debug=not os.environ.get('PORT')) 