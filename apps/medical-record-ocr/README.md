# 病例OCR工具

> Medical Record OCR Tool

---

## 功能说明

- 🏥 病例图片/PDF识别
- 📊 结构化提取（患者信息+诊断+药品+检查结果）
- 🔬 医疗知识库匹配（疾病识别+药品识别）

---

## 技术栈

- Magika：文件类型识别（99%准确率）
- MinerU：PDF解析（表格+公式）
- 家康OS：医疗知识库

---

## 输入支持

- PDF病历
- JPG/PNG病历图片
- DOCX病历文档

---

## 输出格式（JSON）

```json
{
  "patient_info": {
    "name": "患者姓名",
    "age": "年龄",
    "gender": "性别"
  },
  "diagnosis": {
    "disease_name": "疾病名称",
    "doctor": "诊断医生"
  },
  "medications": [
    {
      "name": "药品名称",
      "dosage": "剂量"
    }
  ]
}
```

---

*创建时间：2026-04-17*