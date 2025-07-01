# 湖南大学广东省招生数据分析系统

> 基于湖南大学官方API的广东省招生数据可视化分析系统

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1.1-green.svg)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📊 项目概览

本项目是一个完整的招生数据分析系统，专门分析湖南大学在广东省2020-2025年的招生情况。通过多维度的数据可视化，帮助用户深入了解专业设置、招生趋势和学院分布。

### 🎯 数据概况

- **📅 时间范围**: 2020-2025年（6年完整数据）
- **📈 数据规模**: 353条记录，80个专业，29个学院
- **👥 总招生数**: 6年累计1606人
- **🔍 数据来源**: 湖南大学官方招生API

### 🌟 核心功能

| 功能模块 | 描述 | 特色 |
|---------|------|------|
| 📊 **总览分析** | 年度趋势与专业分布 | 交互式图表，关键词筛选 |
| 🎓 **专业统计** | 单专业历年详细数据 | 折线图趋势，详细表格 |
| 🏫 **学院分析** | 按学院维度分析招生 | 折叠式展示，专业设置 |
| 📈 **专业对比** | 横向对比表格 | 多排序方式，CSV导出 |

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Flask 3.1.1
- pandas 2.2.3
- requests 2.32.4

### 安装步骤

```bash
# 1. 克隆项目
git clone https://github.com/XiaoDcs/hnu_analysis.git
cd hnu_analysis

# 2. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 运行应用
python app.py
```

### 访问应用

启动后访问以下地址：

- 🏠 **总览页面**: http://127.0.0.1:5000
- 🎓 **专业统计**: http://127.0.0.1:5000/guangdong  
- 🏫 **学院分析**: http://127.0.0.1:5000/departments
- 📈 **专业对比**: http://127.0.0.1:5000/comparison

## 📖 功能详解

### 1. 总览分析页面 (/)

**主要功能：**
- 📈 年度招生总人数趋势图
- 📊 专业招生分布（横向柱状图）
- 🔍 专业关键词筛选
- 📋 数据统计卡片

**使用示例：**
- 输入"计算机"筛选相关专业
- 切换年份查看不同年度的专业分布
- 查看6年总招生趋势变化

### 2. 专业统计页面 (/guangdong)

**主要功能：**
- 📋 80个专业下拉选择
- 📊 专业历年招生趋势图
- 📝 详细数据表格（按年份展示）
- 📈 6年总计统计

**热门专业示例：**

| 专业 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 总计 |
|------|------|------|------|------|------|------|------|
| 电气工程及其自动化 | 11 | 12 | 12 | 12 | 16 | 20 | **83** |
| 金融学 | 15 | 15 | 13 | 12 | 9 | 8 | **72** |
| 计算机科学与技术 | 3 | 4 | 5 | 6 | 10 | 15 | **43** |

### 3. 学院分析页面 (/departments)

**主要功能：**
- 🏫 29个学院按招生数排序
- 📅 年份筛选功能
- 📂 折叠式展示各学院详情
- 🎯 展示每年的专业设置和招生计划

**TOP5学院（按总招生数）：**
1. **信息科学与工程学院**: 172人
2. **电气与信息工程学院**: 147人  
3. **机械与运载工程学院**: 136人
4. **金融与统计学院**: 114人
5. **土木工程学院**: 108人

### 4. 专业对比页面 (/comparison)

**主要功能：**
- 📊 80个专业的横向对比表格
- 🔍 关键词筛选（如"计算机"、"工程"）
- 🔄 多种排序方式：总数/最新年份/专业名称
- 💾 CSV数据导出功能
- 🎨 数据可视化（最高值高亮显示）

**对比维度：**
- 各年份招生人数
- 6年总计数
- 年均招生数
- 最高/最低年份数据

## 🛠 技术架构

### 后端技术栈

- **🐍 Python**: 核心开发语言
- **🌶 Flask**: Web框架
- **🐼 pandas**: 数据处理与分析
- **📡 requests**: HTTP请求处理

### 前端技术栈

- **🎨 HTML5 + CSS3**: 响应式UI设计
- **📊 Chart.js**: 交互式图表库
- **⚡ 原生JavaScript**: 前端交互逻辑

### 数据处理

```python
# 核心数据处理流程
def load_guangdong_dataset():
    """加载广东省数据并转换为DataFrame"""
    with open(GUANGDONG_DATA_FILE, 'r', encoding='utf-8') as f:
        guangdong_data = json.load(f)
    
    # 数据标准化处理
    rows = []
    for year_str, year_data in guangdong_data.items():
        year = int(year_str)
        for item in year_data:
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
    
    return pd.DataFrame(rows)
```

## 📡 API 接口文档

### 数据统计 API
```http
GET /api/stats
```
**响应示例：**
```json
{
  "total_records": 353,
  "total_majors": 80,
  "total_students": 1606,
  "years_covered": [2020, 2021, 2022, 2023, 2024, 2025],
  "sample_majors": ["产品设计", "人工智能", "会计学", ...]
}
```

### 专业列表 API
```http
GET /api/guangdong_majors
```

### 专业趋势 API
```http
GET /api/guangdong_major_trend?major=信息安全
```

### 学院分析 API
```http
GET /api/department_analysis?year=2025
```

### 专业对比 API
```http
GET /api/major_comparison?keyword=计算机&sort_by=total
```

## 📁 项目结构

```
hnu_analysis/
├── app.py                          # Flask主应用
├── requirements.txt                # 依赖包列表
├── download_data_fixed.py          # 数据下载脚本
├── guangdong_data_fixed.json       # 主数据文件
├── sample.json                     # 样本数据
├── README.md                       # 项目文档
├── .gitignore                      # Git忽略文件
└── templates/                      # 前端模板
    ├── index_guangdong.html        # 总览页面
    ├── guangdong.html              # 专业统计页面
    ├── departments.html            # 学院分析页面
    └── comparison.html             # 专业对比页面
```

## 🔧 开发指南

### 添加新功能

1. **新增API端点**：在`app.py`中添加路由
2. **创建前端页面**：在`templates/`目录添加HTML模板
3. **更新导航**：在各页面模板中添加导航链接

### 数据更新

使用数据下载脚本更新数据：

```bash
python download_data_fixed.py
```

### 本地开发

```bash
# 启动开发服务器
python app.py

# 访问开发环境
http://127.0.0.1:5000
```

## 📊 数据源说明

**数据来源**: 湖南大学招生网官方API
- **API地址**: `https://admi2.hnu.edu.cn/lnzsjhSearch`
- **数据完整性**: 2020-2025年完整覆盖
- **数据准确性**: 直接来源于官方系统，确保准确性

**请求头配置**:
```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Referer': 'https://admi2.hnu.edu.cn/'
}
```

## 🤝 贡献指南

1. Fork 本仓库
2. 创建你的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的改动 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 📄 许可证

本项目使用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- 湖南大学招生办公室提供的数据支持
- Chart.js 提供的优秀图表库
- Flask 社区的技术支持

## 📞 联系方式

- **项目地址**: https://github.com/XiaoDcs/hnu_analysis
- **问题反馈**: [Issues](https://github.com/XiaoDcs/hnu_analysis/issues)

---

<div align="center">

**🎓 为湖南大学招生数据分析而生**

Made with ❤️ by [XiaoDcs](https://github.com/XiaoDcs)

</div>

## 🌐 在线部署

### 部署到Render

1. **Fork仓库**到你的GitHub账号
2. **登录Render**: https://render.com
3. **创建新的Web Service**
   - 连接你的GitHub仓库
   - 选择`hnu_analysis`项目
4. **配置部署**:
   ```
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn --bind 0.0.0.0:$PORT app:app
   ```
5. **环境变量**（可选）:
   - `PYTHON_VERSION`: 3.8.10

### 一键部署按钮

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/XiaoDcs/hnu_analysis)

部署完成后，你将获得一个类似 `https://your-app.onrender.com` 的在线地址。

### 部署说明

- **启动时间**: 首次访问可能需要30-60秒冷启动
- **免费套餐**: Render免费套餐完全支持本项目
- **自动部署**: 推送到main分支将自动触发重新部署

## 🔧 开发指南 