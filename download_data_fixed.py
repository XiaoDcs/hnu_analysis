#!/usr/bin/env python3
"""
湖南大学招生数据下载脚本 (修复版)
使用正确的请求头获取中文数据
"""

import requests
import json
import urllib.parse
import time
import os

def download_guangdong_data_fixed():
    """下载广东省2020-2025年的招生数据 (修复版)"""
    
    years = list(range(2020, 2026))  # 2020-2025
    province = "广东"
    all_data = {}
    
    # 设置正确的请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': 'https://admi2.hnu.edu.cn/'
    }
    
    print(f"开始下载广东省 {years[0]}-{years[-1]} 年招生数据 (修复版)...")
    
    for year in years:
        print(f"\n正在下载 {year} 年数据...")
        
        # 构建URL
        url = f"https://admi2.hnu.edu.cn/lnzsjhSearch?year={year}&sf={urllib.parse.quote(province)}"
        
        try:
            resp = requests.get(url, headers=headers, timeout=15)
            resp.raise_for_status()
            
            # 手动解码为UTF-8
            content = resp.content
            text = content.decode('utf-8')
            data = json.loads(text)
            
            all_data[str(year)] = data
            print(f"✓ {year}年: {len(data)} 条记录")
            
            # 显示一些专业示例
            if data:
                majors = set(item.get('zymc', '') for item in data if item.get('zymc'))
                majors = [m for m in majors if m.strip()]
                if majors:
                    print(f"  专业示例: {', '.join(sorted(majors)[:5])}")
            
            # 避免请求过快
            time.sleep(1)
            
        except Exception as e:
            print(f"✗ {year}年: 下载失败 - {e}")
            all_data[str(year)] = []
    
    # 保存数据
    output_file = "guangdong_data_fixed.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n数据已保存到: {output_file}")
    
    # 统计信息
    total_records = sum(len(data) for data in all_data.values())
    all_majors = set()
    total_students = 0
    
    for year_data in all_data.values():
        for item in year_data:
            if item.get('zymc'):
                all_majors.add(item['zymc'])
            try:
                total_students += int(item.get('zsrs', 0))
            except:
                pass
    
    print(f"\n=== 数据统计 ===")
    print(f"总记录数: {total_records}")
    print(f"专业数量: {len(all_majors)}")
    print(f"总招生人数: {total_students}")
    print(f"年份范围: {min(years)}-{max(years)}")
    
    # 显示所有专业
    print(f"\n=== 所有专业 ===")
    for i, major in enumerate(sorted(all_majors), 1):
        print(f"{i:2d}. {major}")
    
    return all_data

if __name__ == "__main__":
    download_guangdong_data_fixed() 