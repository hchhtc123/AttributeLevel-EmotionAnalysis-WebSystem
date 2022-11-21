# 基于PaddleNLP的属性级情感分析Web系统

# 一.项目介绍：

  本项目基于PaddleNLP搭建评论观点抽取和属性级情感分析模型，实现细粒度、属性级情感分析。可抽取文本中评论属性和对应观点，并对抽取内容进行细粒度情感倾向分析从而获取评论文本中各个属性所对应的情感分析结果，进而给到企业用户或商家具体有效的建议以及帮助用户高效地从评论获取消费指南。

  为更好进行功能演示，基于前后端分离式架构完成属性级情感分析Web系统搭建，支持输入单条文本进行在线属性级情感分析以及上传Excel文件进行批量文本情感分析。

**技术栈：** 后端：FastAPI + PaddleNLP；前端：Vue+ ElementUI。

**AI Studio项目地址：** [基于PaddleNLP的属性级情感分析Web系统 - 飞桨AI Studio (baidu.com)](https://aistudio.baidu.com/aistudio/projectdetail/5060618)

# 二.项目结构说明：

```
├── 项目说明文档.txt              // 介绍项目环境配置操作，必看！
├── backend                     // 后端API服务模块
│   └── demo.py                 // 模型预测演示demo，用于测试
│   └── main.py                 // API服务启动主程序
│   └── resource                // 存放前端上传的文件资源
├── frontend                    // 情感分析系统前端界面模块
│   └── src/router/index.js     // 定义界面路由
│   └── src/views/              // 搭建的Web界面
```

# 三.项目演示：

**演示视频传送门：**  https://www.bilibili.com/video/BV1H14y1H7Pp/?vd_source=0d95776ba676743c358eea0075f247c4

### **单条文本属性级情感分析：**

![系统_单文本情感分析](https://gitee.com/hchhtc123/picture/raw/master/typora/%E7%B3%BB%E7%BB%9F_%E5%8D%95%E6%96%87%E6%9C%AC%E6%83%85%E6%84%9F%E5%88%86%E6%9E%90.png)

### **批量文本属性级情感分析：**

![系统_批量情感分析](https://gitee.com/hchhtc123/picture/raw/master/typora/%E7%B3%BB%E7%BB%9F_%E6%89%B9%E9%87%8F%E6%83%85%E6%84%9F%E5%88%86%E6%9E%90.png)

# 四.项目反馈：

项目运行过程中遇到问题欢迎提Issue反馈。

联系作者： 若遇到较难解决问题可以添加qq：1075558916 联系作者，注意提供完整报错信息和截图便于定位和解决问题。