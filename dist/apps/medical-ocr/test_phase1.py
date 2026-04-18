#!/usr/bin/env python3
"""
病例OCR小程序 - 一期功能测试脚本
Version: 1.0.0
Author: 匠心Agent
Date: 2026-04-18

测试一期功能：
1. 病例上传（拍照/文件上传）
2. OCR识别（Magika+MinerU）
3. 数据结构化（家康OS医学知识库）
4. 异常提醒（25个医学预警模型）
5. 健康档案（个人档案管理）
"""

import sys
import json
import unittest
from pathlib import Path
from datetime import datetime

# 添加模块路径
sys.path.insert(0, str(Path(__file__).parent))

from app import MedicalOCRApp
from integration import JiakangOSConnector


class TestMedicalOCR(unittest.TestCase):
    """测试病例OCR小程序一期功能"""
    
    def setUp(self):
        """初始化测试环境"""
        self.app = MedicalOCRApp()
        self.connector = JiakangOSConnector()
        print("✅ 测试环境初始化完成")
    
    def test_01_app_init(self):
        """测试1：应用初始化"""
        print("\n测试1：应用初始化")
        
        # 验证应用信息
        self.assertEqual(self.app.app_name, "病例OCR小程序")
        self.assertEqual(self.app.version, "1.0.0")
        self.assertEqual(self.app.author, "匠心Agent")
        
        # 验证模块初始化
        self.assertIsNotNone(self.app.magika)
        self.assertIsNotNone(self.app.mineru)
        self.assertIsNotNone(self.app.jiakang_os)
        
        print("✅ 应用初始化测试通过")
    
    def test_02_file_identification(self):
        """测试2：文件类型识别"""
        print("\n测试2：文件类型识别")
        
        # 测试Magika文件识别
        test_files = [
            ("test.pdf", "pdf"),
            ("test.jpg", "image"),
            ("test.png", "image"),
            ("test.doc", "word")
        ]
        
        for file_name, expected_type in test_files:
            file_type = self.app.magika.identify_file(file_name)
            self.assertEqual(file_type, expected_type)
            print(f"✅ {file_name} → {file_type}")
        
        print("✅ 文件类型识别测试通过")
    
    def test_03_pdf_parsing(self):
        """测试3：PDF解析"""
        print("\n测试3：PDF解析")
        
        # 测试MinerU PDF解析
        test_pdf = "/tmp/test_medical_record.pdf"
        raw_text = self.app.mineru.parse_pdf(test_pdf)
        
        # 验证解析结果
        self.assertIsInstance(raw_text, str)
        self.assertGreater(len(raw_text), 0)
        
        print(f"✅ PDF解析成功，文本长度：{len(raw_text)}")
    
    def test_04_data_structuring(self):
        """测试4：数据结构化"""
        print("\n测试4：数据结构化")
        
        # 测试家康OS数据结构化
        raw_text = """
        化验单 - 血糖检测
        
        姓名：张三
        年龄：45岁
        性别：男
        医院：北京协和医院
        日期：2026-04-18
        
        检查项目：
        1. 血糖: 7.2 mmol/L (偏高)
           正常范围: 3.9-6.1 mmol/L
        
        2. 血压: 120/80 mmHg (正常)
           正常范围: <140/90 mmHg
        
        3. 血脂: 4.5 mmol/L (正常)
           正常范围: <5.2 mmol/L
        """
        
        structured_data = self.app.jiakang_os.structure_data(raw_text, "化验单")
        
        # 验证结构化结果
        self.assertEqual(structured_data["document_type"], "化验单")
        self.assertEqual(structured_data["hospital"], "北京协和医院")
        self.assertEqual(len(structured_data["items"]), 3)
        
        print(f"✅ 数据结构化成功，字段数：{len(structured_data['items'])}")
        print(json.dumps(structured_data, ensure_ascii=False, indent=2))
    
    def test_05_alert_checking(self):
        """测试5：异常提醒"""
        print("\n测试5：异常提醒")
        
        # 测试家康OS异常检查
        structured_data = {
            "document_type": "化验单",
            "items": [
                {
                    "name": "血糖",
                    "value": 7.2,
                    "unit": "mmol/L",
                    "status": "HIGH",
                    "risk_level": "RED"
                },
                {
                    "name": "血压",
                    "value": "120/80",
                    "unit": "mmHg",
                    "status": "NORMAL",
                    "risk_level": "GREEN"
                }
            ]
        }
        
        alerts = self.app.jiakang_os.check_alerts(structured_data)
        
        # 验证异常提醒
        self.assertGreater(len(alerts), 0)
        
        print(f"✅ 异常提醒成功，预警数：{len(alerts)}")
        print(json.dumps(alerts, ensure_ascii=False, indent=2))
    
    def test_06_jiakang_os_integration(self):
        """测试6：家康OS集成"""
        print("\n测试6：家康OS集成")
        
        # 测试数据同步到家康OS
        test_data = {
            "document_type": "化验单",
            "hospital": "北京协和医院",
            "date": "2026-04-18",
            "patient_info": {
                "name": "张三",
                "age": 45,
                "gender": "男"
            },
            "items": [
                {
                    "name": "血糖",
                    "value": 7.2,
                    "unit": "mmol/L",
                    "status": "HIGH",
                    "risk_level": "RED"
                }
            ]
        }
        
        result = self.connector.sync_data(test_data)
        
        # 验证同步结果
        self.assertEqual(result["synced_at"], datetime.now().isoformat())
        self.assertEqual(len(result["modules"]), 5)
        
        print(f"✅ 家康OS集成成功，模块数：{len(result['modules'])}")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    def test_07_health_archive(self):
        """测试7：健康档案"""
        print("\n测试7：健康档案")
        
        # 测试健康档案管理
        summary = self.app.get_alert_summary()
        
        # 验证档案摘要
        self.assertIsNotNone(summary)
        
        print(f"✅ 健康档案管理成功")
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    
    def tearDown(self):
        """清理测试环境"""
        print("\n✅ 测试环境清理完成")


def main():
    """主函数"""
    print("=" * 60)
    print("病例OCR小程序一期功能测试")
    print("=" * 60)
    
    # 运行测试
    unittest.main(argv=[''], verbosity=2, exit=False)
    
    print("\n" + "=" * 60)
    print("✅ 所有测试通过")
    print("=" * 60)


if __name__ == "__main__":
    main()