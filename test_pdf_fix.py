#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试PDF转换修复功能
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.services.pdf_converter import clean_cell_content

def test_clean_cell_content():
    """测试音标字符清理功能"""
    test_cases = [
        # 原始音标 -> 期望结果
        ("eco-friendly [ˌiː.kəʊˈfrendli]", "eco-friendly [i.ku.frendli]"),
        ("atmosphere [ˈætməsfɪə]", "atmosphere [ætməsfɪə]"),
        ("hydrosphere [haɪˈdrɒsfɪə]", "hydrosphere [haɪ.drɒsfɪə]"),
        ("biosphere [ˈbaɪəsfɪə]", "biosphere [baɪəsfɪə]"),
        ("lithosphere [ˈlɪθəsfɪə]", "lithosphere [lɪθəsfɪə]"),
        ("普通的中文内容", "普通的中文内容"),
        ("simple english words", "simple english words"),
    ]
    
    print("🧪 测试音标字符清理功能:")
    print("=" * 50)
    
    for i, (input_text, expected) in enumerate(test_cases, 1):
        result = clean_cell_content(input_text)
        status = "✅ PASS" if result == expected or expected in result else "❌ FAIL"
        print(f"测试 {i}: {status}")
        print(f"  输入: {input_text}")
        print(f"  输出: {result}")
        print()

if __name__ == "__main__":
    test_clean_cell_content()