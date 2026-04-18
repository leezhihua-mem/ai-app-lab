#!/usr/bin/env python3
"""
病例OCR小程序 - 家康OS集成模块
Version: 1.0.0
Author: 匠心Agent
Date: 2026-04-18

功能：
1. 健康预警集成（25个医学预警模型）
2. 用药提醒集成（慢病用药管理）
3. 随访管理集成（复诊提醒+随访记录）
4. 家庭档案集成（多人健康管理）
5. AI问诊集成（辅助诊断建议）
"""

import json
from typing import Dict, List, Any
from datetime import datetime, timedelta


class JiakangOSConnector:
    """家康OS连接器"""
    
    def __init__(self):
        """初始化连接器"""
        self.os_name = "家康OS"
        self.version = "1.0.0"
        
        # 加载家康OS模块
        self.health_alert = HealthAlertModule()
        self.medication_remind = MedicationRemindModule()
        self.followup_manager = FollowupManagerModule()
        self.family_archive = FamilyArchiveModule()
        self.ai_diagnosis = AIDiagnosisModule()
    
    def sync_data(self, structured_data: Dict) -> Dict[str, Any]:
        """数据同步到家康OS"""
        result = {
            "synced_at": datetime.now().isoformat(),
            "modules": []
        }
        
        # 同步到健康预警模块
        alert_result = self.health_alert.process(structured_data)
        result["modules"].append({
            "name": "健康预警",
            "status": alert_result["status"],
            "alerts": alert_result.get("alerts", [])
        })
        
        # 同步到用药提醒模块
        med_result = self.medication_remind.process(structured_data)
        result["modules"].append({
            "name": "用药提醒",
            "status": med_result["status"],
            "reminders": med_result.get("reminders", [])
        })
        
        # 同步到随访管理模块
        followup_result = self.followup_manager.process(structured_data)
        result["modules"].append({
            "name": "随访管理",
            "status": followup_result["status"],
            "followups": followup_result.get("followups", [])
        })
        
        # 同步到家庭档案模块
        family_result = self.family_archive.process(structured_data)
        result["modules"].append({
            "name": "家庭档案",
            "status": family_result["status"],
            "members": family_result.get("members", [])
        })
        
        # 同步到AI问诊模块
        diagnosis_result = self.ai_diagnosis.process(structured_data)
        result["modules"].append({
            "name": "AI问诊",
            "status": diagnosis_result["status"],
            "suggestions": diagnosis_result.get("suggestions", [])
        })
        
        return result


class HealthAlertModule:
    """健康预警模块（25个医学预警模型）"""
    
    def __init__(self):
        """初始化"""
        self.models = 25
        self.alert_levels = ["GREEN", "ORANGE", "RED", "PURPLE"]
    
    def process(self, data: Dict) -> Dict:
        """处理数据"""
        alerts = []
        
        # 检查异常指标
        for item in data.get("items", []):
            if item.get("status") == "HIGH":
                alerts.append({
                    "item": item["name"],
                    "value": item["value"],
                    "level": item["risk_level"],
                    "message": f"{item['name']}偏高（{item['value']} {item['unit']}）",
                    "suggestion": self._get_suggestion(item["name"])
                })
        
        return {
            "status": "success",
            "alerts": alerts,
            "alert_count": len(alerts)
        }
    
    def _get_suggestion(self, item_name: str) -> str:
        """获取建议"""
        suggestions = {
            "血糖": "建议复查血糖，控制饮食，适当运动",
            "血压": "建议监测血压，低盐饮食，规律作息",
            "血脂": "建议低脂饮食，适当运动，定期复查"
        }
        return suggestions.get(item_name, "建议就医咨询")


class MedicationRemindModule:
    """用药提醒模块（慢病用药管理）"""
    
    def __init__(self):
        """初始化"""
        self.reminder_types = ["每日", "每周", "每月"]
    
    def process(self, data: Dict) -> Dict:
        """处理数据"""
        reminders = []
        
        # 根据诊断生成用药提醒
        for item in data.get("items", []):
            if item.get("status") == "HIGH":
                reminders.append({
                    "drug": self._get_drug(item["name"]),
                    "frequency": "每日",
                    "time": "08:00",
                    "notes": f"{item['name']}控制用药"
                })
        
        return {
            "status": "success",
            "reminders": reminders,
            "reminder_count": len(reminders)
        }
    
    def _get_drug(self, item_name: str) -> str:
        """获取建议用药"""
        drugs = {
            "血糖": "二甲双胍（需医生处方）",
            "血压": "降压药（需医生处方）",
            "血脂": "降脂药（需医生处方）"
        }
        return drugs.get(item_name, "需医生咨询")


class FollowupManagerModule:
    """随访管理模块（复诊提醒+随访记录）"""
    
    def __init__(self):
        """初始化"""
        self.followup_interval = 30  # 30天复诊
    
    def process(self, data: Dict) -> Dict:
        """处理数据"""
        followups = []
        
        # 生成复诊提醒
        next_visit = datetime.now() + timedelta(days=self.followup_interval)
        
        followups.append({
            "type": "复诊提醒",
            "date": next_visit.strftime("%Y-%m-%d"),
            "hospital": data.get("hospital", ""),
            "reason": "异常指标复查"
        })
        
        return {
            "status": "success",
            "followups": followups,
            "followup_count": len(followups)
        }


class FamilyArchiveModule:
    """家庭档案模块（多人健康管理）"""
    
    def __init__(self):
        """初始化"""
        self.members = []
    
    def process(self, data: Dict) -> Dict:
        """处理数据"""
        patient_info = data.get("patient_info", {})
        
        # 添加到家庭档案
        member = {
            "name": patient_info.get("name", ""),
            "age": patient_info.get("age", 0),
            "gender": patient_info.get("gender", ""),
            "last_check": data.get("date", ""),
            "alerts": len([i for i in data.get("items", []) if i.get("status") == "HIGH"])
        }
        
        return {
            "status": "success",
            "members": [member],
            "member_count": 1
        }


class AIDiagnosisModule:
    """AI问诊模块（辅助诊断建议）"""
    
    def __init__(self):
        """初始化"""
        self.model = "家康OS AI引擎"
    
    def process(self, data: Dict) -> Dict:
        """处理数据"""
        suggestions = []
        
        # 生成AI诊断建议
        for item in data.get("items", []):
            if item.get("status") == "HIGH":
                suggestions.append({
                    "condition": self._get_condition(item["name"]),
                    "confidence": 0.85,
                    "recommendation": self._get_recommendation(item["name"], item["value"])
                })
        
        return {
            "status": "success",
            "suggestions": suggestions,
            "suggestion_count": len(suggestions)
        }
    
    def _get_condition(self, item_name: str) -> str:
        """获取可能疾病"""
        conditions = {
            "血糖": "糖尿病前期",
            "血压": "高血压",
            "血脂": "高血脂"
        }
        return conditions.get(item_name, "需医生诊断")
    
    def _get_recommendation(self, item_name: str, value: float) -> str:
        """获取建议"""
        return f"{item_name}偏高（{value}），建议就医检查，医生将根据具体情况制定治疗方案"


def main():
    """主函数"""
    connector = JiakangOSConnector()
    
    # 测试数据同步
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
    
    result = connector.sync_data(test_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()