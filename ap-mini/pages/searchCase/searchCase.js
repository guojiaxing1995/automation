const app = getApp();
Page({
  data: {
    mainActiveIndex: 0,
    activeId:0,
    items: []
  },
  onLoad: function (options) {
    this.getTaskData();
  },
  onPullDownRefresh: function (options) {
    this.getTaskData();
    wx.stopPullDownRefresh();
  },
  onSearch(event){
    var case_id = event.detail
    wx.navigateTo({
      url: 'caseDetail/caseDetail?case_id=' + case_id,
    }) 
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
  }
})