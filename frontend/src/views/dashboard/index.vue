<template>
  <div class="dashboard-container">
    <el-image
      style="width: 100%; height: 100%; position: absolute; z-index: -1;"
      :src="url"
    />
    <div id="container" style="width:100%; height: 100%; position: absolute; z-index: 1;" />
  </div>
</template>

<script>
// import { mapGetters } from 'vuex'
import * as echarts from 'echarts'

export default {
  name: 'Dashboard',
  data() {
    return {
      url: require('/src/assets/img/image.jpg')
    }
  },
  mounted() {
    this.getLoadEcharts()
  },
  methods: {
    getLoadEcharts() {
      var chartDom = document.getElementById('container')
      var myChart = echarts.init(chartDom)
      var option
      option = {
        graphic: {
          elements: [
            {
              type: 'text',
              left: 'center',
              top: 'center',
              style: {
                text: '属性级情感分析系统',
                fontSize: 100,
                fontWeight: 'bold',
                lineDash: [0, 200],
                lineDashOffset: 0,
                fill: 'transparent',
                stroke: '#000',
                lineWidth: 2
              },
              keyframeAnimation: {
                duration: 3000,
                loop: true,
                keyframes: [
                  {
                    percent: 0.7,
                    style: {
                      fill: 'transparent',
                      lineDashOffset: 200,
                      lineDash: [200, 0]
                    }
                  },
                  {
                    // Stop for a while.
                    percent: 0.8,
                    style: {
                      fill: 'transparent'
                    }
                  },
                  {
                    percent: 1,
                    style: {
                      fill: 'black'
                    }
                  }
                ]
              }
            }
          ]
        }
      }
      // 绘制图表
      myChart.setOption(option)
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    height:100%;
    width:100%;
    position:fixed;
  }
}
</style>
