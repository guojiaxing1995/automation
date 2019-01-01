const app = getApp();
Page({
  data: {
    noresult: false,
    loading: true,
    detail:false
  },
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
          that.setData({
            detail: false,
            noresult: true,
            loading:false
          });
        }else{
        that.setData({
          caseDetail: res.data,
          detail: true,
          noresult: false,
          loading: false
        });
        }
        wx.setNavigationBarTitle({
          title: res.data.case_id,
        })
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
          caseDetail: res.data,
          detail: true,
          noresult: false,
          loading: false
        });
        wx.setNavigationBarTitle({
          title: res.data.case_id,
        })
      },
      fail: function (error) {
        console.log(error)
      }
    })
  }
})