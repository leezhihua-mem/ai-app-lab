// pages/index/index.js

Page({
  data: {
    // 进度数据
    showProgress: false,
    progress: 0,
    remainingTime: 15,
    
    // 结果数据
    showResult: false,
    documentType: '化验单',
    hospital: '北京协和医院',
    date: '2026-04-18',
    
    // 异常指标
    alertItems: [
      {
        name: '血糖',
        value: '7.2',
        unit: 'mmol/L',
        status: '偏高',
        riskLevel: '红色预警',
        normalRange: '3.9-6.1 mmol/L'
      }
    ],
    
    // 正常指标
    normalItems: [
      {
        name: '血压',
        value: '120/80',
        unit: 'mmHg'
      },
      {
        name: '血脂',
        value: '4.5',
        unit: 'mmol/L'
      }
    ],
    
    // 家康OS集成模块
    integrations: [
      {
        icon: '⚠️',
        text: '健康预警模块（25个医学预警模型）'
      },
      {
        icon: '💊',
        text: '用药提醒模块（慢病用药管理）'
      },
      {
        icon: '📅',
        text: '随访管理模块（复诊提醒+随访记录）'
      },
      {
        icon: '👨‍👩‍👧‍👦',
        text: '家庭档案模块（多人健康管理）'
      },
      {
        icon: '🤖',
        text: 'AI问诊模块（辅助诊断建议）'
      }
    ]
  },
  
  // 选择图片
  chooseImage() {
    wx.chooseImage({
      count: 1,
      sizeType: ['compressed'],
      sourceType: ['album', 'camera'],
      success: (res) => {
        // 显示进度
        this.setData({
          showProgress: true,
          progress: 0
        });
        
        // 模拟OCR处理
        this.simulateOCR();
      }
    });
  },
  
  // 选择文件
  chooseFile() {
    wx.chooseMessageFile({
      count: 1,
      type: 'file',
      extension: ['pdf', 'jpg', 'png', 'jpeg'],
      success: (res) => {
        // 显示进度
        this.setData({
          showProgress: true,
          progress: 0
        });
        
        // 模拟OCR处理
        this.simulateOCR();
      }
    });
  },
  
  // 拍照上传
  takePhoto() {
    wx.chooseImage({
      count: 1,
      sizeType: ['compressed'],
      sourceType: ['camera'],
      success: (res) => {
        // 显示进度
        this.setData({
          showProgress: true,
          progress: 0
        });
        
        // 模拟OCR处理
        this.simulateOCR();
      }
    });
  },
  
  // 模拟OCR处理
  simulateOCR() {
    let progress = 0;
    
    const timer = setInterval(() => {
      progress += 10;
      
      this.setData({
        progress: progress,
        remainingTime: Math.floor((100 - progress) / 10)
      });
      
      if (progress >= 100) {
        clearInterval(timer);
        
        // 显示结果
        this.setData({
          showProgress: false,
          showResult: true
        });
        
        wx.showToast({
          title: 'OCR识别完成',
          icon: 'success'
        });
      }
    }, 500);
  },
  
  // 重新识别
  retryOCR() {
    this.setData({
      showResult: false,
      showProgress: false,
      progress: 0
    });
    
    wx.showToast({
      title: '请重新上传',
      icon: 'none'
    });
  },
  
  // 保存结果
  saveResult() {
    // 调用家康OS集成保存数据
    wx.showToast({
      title: '已保存到健康档案',
      icon: 'success'
    });
    
    // 跳转到档案页
    wx.navigateTo({
      url: '/pages/archive/archive'
    });
  }
});