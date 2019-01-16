import * as echarts from '../../ec-canvas/echarts';

const app = getApp();

Page({
  data: {
    ecPie: {
      disableTouch: true,//禁止触摸事件，修复ios无法滑动
      lazyLoad: true
    },
    ecLine: {
      disableTouch: true
    },
    touch:{
      endX:0,
      endY:0,
      startX:0,
      startY:0
    },
    popupShow:false,
    leftIconSlid: true,
    taskData: [],
    taskID: 0
  },
  onLoad: function (options) {
    wx.showNavigationBarLoading();
    var that = this;
    this.pieComponnet = this.selectComponent('#mychart-dom-pie');
    this.lineComponnet = this.selectComponent('#mychart-dom-line');
    this.getTaskData();
    var times = setInterval(function(){
      if (that.data.taskID != 0) {
        that.getReportData(that.data.taskID,that.data.taskName);
        clearTimeout(times);
      }
    },500)

    setInterval(function(){
      that.setData({
        leftIconSlid: !that.data.leftIconSlid
      });
    },3000)
    
  },
  touchStart(e) {
    // console.log(e)
    this.setData({
      "touch.startX": e.changedTouches[0].clientX,
      "touch.startY": e.changedTouches[0].clientY
    });
  },
  touchEnd(e) {
    this.setData({
      "touch.endX": e.changedTouches[0].clientX,
      "touch.endY": e.changedTouches[0].clientY
    });
    var turn = this.slidPage();
    if (turn == "left") {
      this.setData({ popupShow: true });
    }
  },
  //左右滑动屏幕
  slidPage(){
    let turn = "";
    if (this.data.touch.endX - this.data.touch.startX > 40 && Math.abs(this.data.touch.endY - this.data.touch.startY) < 50) {      //右滑
      turn = "right";
    } else if (this.data.touch.endX - this.data.touch.startX < -40 && Math.abs(this.data.touch.endY - this.data.touch.startY) < 50) {   //左滑
      turn = "left";
    }
    return turn;
  },
  onPopupClose(){
    var that = this;
    this.setData({ popupShow: false });
    var times = setInterval(function () {
      if (that.data.popupShow == false) {
        that.pieComponnet = that.selectComponent('#mychart-dom-pie');
        that.lineComponnet = that.selectComponent('#mychart-dom-line');
        that.getReportData(that.data.taskID, that.data.taskName);
        clearTimeout(times);
      }
    }, 500)
  },
  selectTask(event){
    var task = event.currentTarget.dataset.task;
    this.setData({
      taskID : task.id,
      taskName : task.name,
      popupShow: false
    });
    var that = this;
    that.pieComponnet = that.selectComponent('#mychart-dom-pie');
    that.lineComponnet = that.selectComponent('#mychart-dom-line');
    this.getReportData(task.id,task.name);
  },
  getTaskData(){
    var that = this;
    wx.request({
      url: app.globalData.automationBase + "/v1/task/allTask",
      method: 'GET',
      header: {
        "Content-Type": "json"
      },
      success: function (res) {
        that.setData({
          taskData: res.data,
          taskID: res.data[1].id,
          taskName:res.data[1].name
        });
      },
      fail: function (error) {
        // fail
        console.log(error)
      }
    })
  },
  getReportData(taskID,taskName){
    wx.showNavigationBarLoading();
    wx.setNavigationBarTitle({
      title: taskName
    });
    var that = this;
    wx.request({
      url: app.globalData.automationBase + "/v1/task/getReportDate?task_id=" + taskID,
      method: 'GET',
      header: {
        "Content-Type": "json"
      },
      success: function (res) {
        var reportData = res.data;
        var pass_num = 0;
        var fail_num = 0;
        var execute_num = 0;
        var total = 0;
        for (var key in reportData) {
          if (reportData[key]['cicle'] == true) {
            pass_num = reportData[key]['pass_num'];
            fail_num = reportData[key]['fail_num'];
            total = reportData[key]['total'];
            execute_num = reportData[key]['execute_num'];

          }
        }
        var not_excete_num = total - execute_num;
        var circleData = [
          { value: not_excete_num, name: '未执行' },
          { value: pass_num, name: '成功' },
          { value: fail_num, name: '失败' }
        ];
        var lineData = {}
        lineData.pass_probability = [];
        lineData.fail_probability = [];
        lineData.execute_probability = [];
        for (var key in reportData) {
          lineData.pass_probability.push(reportData[key]['pass_probability']);
          lineData.fail_probability.push(reportData[key]['fail_probability']);
          lineData.execute_probability.push(reportData[key]['execute_probability']);
        }
        that.initLine(lineData);
        that.initPie(circleData);
        wx.hideNavigationBarLoading();
      },
      fail: function (error) {
        // fail
        console.log(error)
      }
    })  
  },
  initLine(lineData){
    this.lineComponnet.init((canvas, width, height) => {
      // 初始化图表
      const Chart = echarts.init(canvas, null, {
        width: width,
        height: height
      });
      var option = {
        title: {

        },
        color: ['#67C23A', '#F56C6C','#E6A23C'],
        legend: {
          data: [{
            name: '通过率',
            textStyle: {
              color: '#67C23A'
            }
          }, {
            name: '失败率',
            textStyle: {
              color: '#F56C6C'
            }
          }, {
            name: '执行率',
            textStyle: {
              color: '#E6A23C'
            }
          }],
          top: 30,
          left: 'center',
          textStyle: {
            fontSize: 10
          },
          z: 99
        },
        grid: {
          containLabel: true
        },
        tooltip: {
          show: true,
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
          // show: false
        },
        yAxis: {
          type: 'value',
          axisLabel: {
            formatter: '{value} %'
          },
          max: 100,
          min: 0,
        },
        series: [{
          name: '通过率',
          type: 'line',
          smooth: true,
          data: lineData.pass_probability
        }, {
          name: '失败率',
          type: 'line',
          smooth: true,
            data: lineData.fail_probability
        }, {
          name: '执行率',
          type: 'line',
          smooth: true,
          data: lineData.execute_probability
        }]
      };
      Chart.setOption(option);
      return Chart;
    });
  },
  initPie(circleData){
    this.pieComponnet.init((canvas, width, height) => {
      // 初始化图表
      const Chart = echarts.init(canvas, null, {
        width: width,
        height: height
      });
      var option = {
        title: {
          text: '',
          subtext: '最新记录',
          x: 'center',
          y: 5

        },
        backgroundColor: "#ffffff",
        color: ['#E6A23C', '#67C23A', '#F56C6C'],
        tooltip: {
          trigger: 'item',
          formatter: "{b} : {c} ({d}%)"
        },
        legend: {
          orient: 'vertical',
          left: 'left',
          data: [{
            name: '未执行',
            icon: 'pin',
            textStyle: {
              fontSize: 9,
              color: '#E6A23C'
            }
          }, {
            name: '成功',
            icon: 'pin',
            textStyle: {
              fontSize: 9,
              color: '#67C23A'
            }
          }, {
            name: '失败',
            icon: 'pin',
            textStyle: {
              fontSize: 9,
              color: '#F56C6C'
            }
          }],
          z: 9
        },
        series: [{
          label: {
            normal: {
              fontSize: 12
            }
          },
          type: 'pie',
          center: ['50%', '50%'],
          radius: [0, '60%'],
          data: circleData,
          itemStyle: {
            emphasis: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 2, 2, 0.3)'
            }
          }
        }]
      };
      Chart.setOption(option);
      return Chart;
    });
  }
});