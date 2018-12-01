// pages/spiderBatch/result/result.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    expect_result: '',
    interface_return: '',
    case_name: ''
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var expect_result = options.expect_result;
    var interface_return = options.interface_return;
    var case_name = options.case_name;
    this.setData({
      expect_result: expect_result,
      interface_return: interface_return,
      case_name: case_name
    });
    wx.setNavigationBarTitle({
      title: this.data.case_name,
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