// pages/schedule/schedule.js
const app = getApp();
import Notify from '../../miniprogram_npm/vant-weapp/notify/notify';
Page({

  /**
   * 页面的初始数据
   */
  data: {
    loading:true,
    jobs: false
  },

  /**
   * 生命周期函数--监听页面加载
   */
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
  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

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
  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

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
  },
  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})