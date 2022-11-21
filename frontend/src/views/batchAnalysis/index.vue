<template>
  <div class="app-container">
    <el-card class="box-card">
      <div class="tip">
        请上传要进行批量分析的Excel文件
      </div>
      <el-upload
        class="upload-demo"
        drag
        action=""
        :limit="1"
        :http-request="uploadFile"
        accept=".xls,.xlsx"
        style="text-align: center; padding-top:10px;padding-bottom:10px;"
      >
        <i class="el-icon-upload" />
        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
      </el-upload>
    </el-card>
    <el-row style="text-align: center; padding-top:20px;padding-bottom:20px;">
      <el-button type="primary" round @click="batchEmotionAnalysis()">情感分析</el-button>
      <el-button type="success" round @click="saveResult()">保存结果</el-button>
    </el-row>
    <el-card v-show="visible" class="box-card">
      <div v-show="visible" class="tip">
        批量情感分析结果：
      </div>
      <el-table
        id="excel"
        :data="analysisResults"
        height="290"
        border
        style="width: 100%"
      >
        <el-table-column
          prop="text"
          label="文本"
        />
        <el-table-column
          prop="result"
          label="情感分析结果"
          width="480"
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
      fileData: '',
      analysisResults: '',
      visible: false
    }
  },
  methods: {
    // 上传文件，获取上传文件内容并弹窗提示
    uploadFile(file) {
      this.fileData = file.file
      console.log(file.file)
      this.$message({
        showClose: true,
        message: '文件上传成功！',
        type: 'success'
      })
    },
    // 保存纠错结果
    saveResult() {
      var tempData = this.analysisResults
      if (tempData === '') {
        this.$message({
          showClose: true,
          message: '情感分析结果内容为空！',
          type: 'warning'
        })
      } else {
        // 第一个参数是导出文件的名称，第二个参数是需要导出的表格标签的id
        this.Excels.exportExcel('批量情感分析结果.xlsx', '#excel')
        this.$message({
          showClose: true,
          message: '情感分析结果保存成功！',
          type: 'success'
        })
      }
    },
    // 批量情感分析
    batchEmotionAnalysis() {
      var that = this
      // 判断用户是否已经选择要上传的文件
      if (that.fileData === '') {
        this.$message({
          showClose: true,
          message: '请先选择要进行批量情感分析的Excel文件！',
          type: 'warning'
        })
        that.analysisResults = ''
        that.visible = false
        return
      }
      that.visible = true
      that.$message({
        showClose: true,
        message: '批量情感分析完成！',
        type: 'success'
      })
      // 请求后端批量情感分析接口，请求方法为POST，请求体格式为form-data，字段为file，类型也为file
      var config = {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
      var form = new FormData()
      form.append('file', that.fileData)
      axios.post('http://127.0.0.1:8000/v1/batchEmotionAnalysis', form, config).then((response) => {
        // 获取接口返回的情感分析预测结果并更新界面数据
        that.analysisResults = response.data.batchAnalysisResults
        that.visible = true
        that.$message({
          showClose: true,
          message: '批量情感分析完成！',
          type: 'success'
        })
      }).catch((error) => {
        console.log(error)
        that.analysisResults = ''
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
</script>

<style scoped>
  .tip {
    font-family: 宋体;
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 20px;
    margin-bottom: 10px;
    text-align: left;
  }
</style>
