const app = getApp();
import Notify from '../../miniprogram_npm/vant-weapp/notify/notify';
Page({

  data: {
    loading:true,
    jobs: false
  },
  onLoad: function (options) {
    this.getJobs();
  },
  getJobs(){
    var that = this;
    wx.request({
      url: app.globalData.automationBase + "/v1/task/getJobs",
      method: 'GET',
      header: {
        "Content-Type": "json"
      },
      success: function (res) {
        var jobs = []
        for (var job in res.data) {
          jobs.push(res.data[job]);
        }
        that.setData({
          jobs: jobs,
          loading: false
        });
      },
      fail: function (error) {
        // fail
        console.log(error)
      }
    })
  },
  toTask: function(event){
    var taskID = event.currentTarget.dataset.id;
    app.globalData.taskID = taskID;
    var timer = setInterval(function () {
      if (app.globalData.taskID == event.currentTarget.dataset.id) {
        wx.switchTab({
          url: '../spiderBatch/spiderBatch',
        })
        clearTimeout(timer);
      }
    }, 500)
  },
  pauseJob(event){
    wx.showNavigationBarLoading();
    var scheduler_id = event.currentTarget.dataset.schedulerid;
    var that = this;
    wx.request({
      url: app.globalData.automationBase + "/v1/task/pauseJob?scheduler_id=" + scheduler_id,
      method: 'GET',
      header: {
        "Content-Type": "json"
      },
      success: function (res) {
        if (res.data.error_code == 0) {
          that.getJobs();
          Notify({
            text: '停止成功',
            backgroundColor: '#24db56'
          });
        } else {
          Notify("停止失败");
        }
        wx.hideNavigationBarLoading();
      },
      fail: function (error) {
        Notify("停止失败");
        wx.hideNavigationBarLoading();
      }
    })
  },
  startJob(event){
    wx.showNavigationBarLoading();
    var scheduler_id = event.currentTarget.dataset.schedulerid;
    var that = this;
    wx.request({
      url: app.globalData.automationBase + "/v1/task/startJob?scheduler_id=" + scheduler_id,
      method: 'GET',
      header: {
        "Content-Type": "json"
      },
      success: function (res) {
        if (res.data.error_code==0){
          that.getJobs();
          Notify({
            text: '启动成功',
            backgroundColor: '#24db56'
          });
        }else{
          Notify("启动失败");
        }
        wx.hideNavigationBarLoading();
      },
      fail: function (error) {
        Notify("启动失败");
        wx.hideNavigationBarLoading();
      }
    })
  }
})