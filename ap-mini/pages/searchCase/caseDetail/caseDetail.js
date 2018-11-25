// pages/searchCase/caseDetail/caseDetail.js
const app = getApp();
Page({

  /**
   * 页面的初始数据
   */
  data: {
    noresult: false,
    loading: false
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var id = options.id;
    var case_id = options.case_id;
    if (options.id){
    this.getCaseDetailById(id);
    } else if(options.case_id){
      this.getCaseDetailByCaseId(case_id);
    }
  },
  getCaseDetailByCaseId(case_id) {
    var that = this;
    wx.request({
      url: app.globalData.automationBase + "/v1/task/getCaseById?case_id=" + case_id,
      method: 'GET',
      header: {
        "Content-Type": "json"
      },
      success: function (res) {
        if(res.data.error_code){
          console.log(res.data)
        }else{
        that.setData({
          caseDetail: res.data
        });
        }
      },
      fail: function (error) {
        // fail
        console.log(error)
      }
    })
  },
  getCaseDetailById(id) {
    var that = this;
    wx.request({
      url: app.globalData.automationBase + "/v1/task/getCaseById?id=" + id,
      method: 'GET',
      header: {
        "Content-Type": "json"
      },
      success: function (res) {
        that.setData({
          caseDetail: res.data
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

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})