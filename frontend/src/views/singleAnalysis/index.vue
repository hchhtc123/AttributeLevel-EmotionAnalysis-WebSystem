<template>
  <div class="app-container">
    <el-card class="box-card">
      <div class="tip">
        请输入要进行属性级情感分析的文本:
      </div>
      <el-input v-model="textarea" type="textarea" :disabled="stage" :rows="6" placeholder="请输入要进行属性级情感分析的文本" clearable />
    </el-card>
    <div style="text-align: center; padding-top:20px; padding-bottom:20px;">
      <el-button type="info" round @click="clear()">清空内容</el-button>
      <el-button type="primary" round @click="emotionAnalysis()">情感分析</el-button>
    </div>
    <el-card v-show="visible" class="box-card">
      <div v-show="visible" class="tip">
        属性级情感分析结果:
      </div>
      <!-- <el-input v-show="visible" v-model="result" type="textarea" :rows="13" /> -->
      <el-table
        :data="analysisResult"
        height="290"
        border
        style="width: 100%"
      >
        <el-table-column
          prop="aspect"
          label="属性"
          width="180"
        />
        <el-table-column
          prop="opinions"
          label="观点"
        />
        <el-table-column
          prop="sentiment"
          label="情感倾向"
          width="180"
        />
      </el-table>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      textarea: '', // 用户输入框内输入内容
      analysisResult: '', // 情感分析结果
      stage: false,
      visible: false // 设置情感分析结果的可见性
    }
  },
  methods: {
    clear() {
      var that = this
      that.textarea = ''
      that.analysisResult = ''
      that.visible = false
      that.$message({
        showClose: true,
        message: '文本内容已清空！',
        type: 'success'
      })
    },
    emotionAnalysis() {
      var that = this
      // 获取用户输入框输入的要进行情感分析的文本
      var context = that.textarea
      if (context === '') {
        this.$message({
          showClose: true,
          message: '输入文本内容不能为空',
          type: 'warning'
        })
        that.analysisResult = ''
        that.visible = false
      } else {
        // 请求后端单文本情感分析接口，请求方法为POST，请求体格式为JSON，字段text为要进行情感分析的文本
        axios.post('http://127.0.0.1:8000/v1/singleEmotionAnalysis', {
          text: that.textarea
        }).then((response) => {
          console.log(response.data)
          // 获取接口返回的情感分析预测结果并更新界面数据
          that.analysisResult = response.data.singleAnalysisResult
          that.visible = true
          that.$message({
            showClose: true,
            message: '属性级情感分析完成！',
            type: 'success'
          })
        }).catch((error) => {
          // 捕获异常并弹窗提示
          console.log(error)
          that.analysisResult = ''
          that.visible = false
          that.$message({
            showClose: true,
            message: '请求异常，请检查后端服务模块！',
            type: 'error'
          })
        })
      }
    }
  }
}
</script>

<style scoped>
  .tip {
    font-family: 宋体;
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 10px;
  }
</style>
