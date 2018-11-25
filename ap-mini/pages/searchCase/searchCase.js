// pages/searchCase/searchCase.js
const app = getApp();
Page({

  /**
   * 页面的初始数据
   */
  data: {
    mainActiveIndex: 0,
    activeId:0,
    items: []
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.getTaskData();
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
  onSearch(event){
    var case_id = event.detail
    wx.navigateTo({
      url: 'caseDetail/caseDetail?case_id=' + case_id,
    }) 
  },
  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },
  onClickNav(event) {
    this.setData({
      mainActiveIndex: event.detail.index || 0
    });

  },
  getTaskData() {
    var that = this;
    wx.request({
      url: app.globalData.automationBase + "/v1/task/TaskCaseItemsMini",
      method: 'GET',
      header: {
        "Content-Type": "json"
      },
      success: function (res) {
        that.setData({
          items:res.data
        });
      },
      fail: function (error) {
        // fail
        console.log(error)
      }
    })
  },
  onClickItem(event) {
    this.setData({
      activeId: event.detail.id
    });
    var id = event.detail.id;
    wx.navigateTo({
      url: 'caseDetail/caseDetail?id='+id,
    }) 
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})