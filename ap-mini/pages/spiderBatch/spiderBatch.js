import Notify from '../../miniprogram_npm/vant-weapp/notify/notify';
import Toast from '../../miniprogram_npm/vant-weapp/toast/toast';
import Dialog from '../../miniprogram_npm/vant-weapp/dialog/dialog';
const app = getApp();
Page({
  data: {
    popupShow: false,
    leftIconSlid: true,
    btn_loading:false,
    has_run: false,
    case_reslut: [],
    page: 0,
    pages: 0,
    total: 0,
    loading:false,
    result:{},
    taskData: [],
    task:{},
    taskID: 0,
    touch: {
      endX: 0,
      endY: 0,
      startX: 0,
      startY: 0
    }
  },
  onLoad: function (options) {
    wx.showNavigationBarLoading();
    var that = this;
    this.getTaskData();
    if (app.globalData.taskID){
      console.log("lalala")
      this.setData({
        taskID: app.globalData.taskID
      });
    }else{
      var timer = setInterval(function () {
        if (that.data.taskData.length>0){
          that.setData({
            taskID: that.data.taskData[0].id
          });
          clearTimeout(timer);
        }
      }, 500)
    }
    if (app.globalData.taskID){
      this.getCurrentTask(app.globalData.taskID);
    }else{
      this.getCurrentTask(-1);
    }

  },
  getCurrentTask(TASKID){
    var that = this;
    var timer = setInterval(function () {
      if (that.data.taskID != 0 && that.data.taskData.length > 0) {
        if (TASKID==-1) {
          TASKID = that.data.taskID;
        }
        for (var task in that.data.taskData){
          if (TASKID == that.data.taskData[task].id){
            that.setData({
              task: that.data.taskData[task]
            });
          }
        }
        clearTimeout(timer);
      }
    }, 500)
    wx.hideNavigationBarLoading();
  },
  touchStart(e) {
    // console.log(e)
    this.setData({
      "touch.startX": e.changedTouches[0].clientX,
      "touch.startY": e.changedTouches[0].clientY
    });
  },
  selectTask(event) {
    var task = event.currentTarget.dataset.task;
    this.setData({
      taskID: task.id,
      task:task,
      popupShow: false,
      has_run:false
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
  slidPage() {
    let turn = "";
    if (this.data.touch.endX - this.data.touch.startX > 40 && Math.abs(this.data.touch.endY - this.data.touch.startY) < 50) {      //右滑
      turn = "right";
    } else if (this.data.touch.endX - this.data.touch.startX < -40 && Math.abs(this.data.touch.endY - this.data.touch.startY) < 50) {   //左滑
      turn = "left";
    } else if (Math.abs(this.data.touch.endX - this.data.touch.startX) < Math.abs(this.data.touch.endY - this.data.touch.startY) && (this.data.touch.endY - this.data.touch.startY) <- 50){
      turn = "up";
    }
    console.log(turn);
    return turn;
  },
  getTaskData() {
    var that = this;
    wx.request({
      url: app.globalData.automationBase + "/v1/task/allTask",
      method: 'GET',
      header: {
        "Content-Type": "json"
      },
      success: function (res) {
        that.setData({
          taskData: res.data
        });
      },
      fail: function (error) {
        // fail
        console.log(error)
      }
    })
  },
  onPopupClose() {
    var that = this;
    this.setData({ popupShow: false });
  },
  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    var that = this;
    setInterval(function () {
      that.setData({
        leftIconSlid: !that.data.leftIconSlid
      });
    }, 3000)

    var that = this;
    if (app.globalData.taskID) {
      this.getCurrentTask(app.globalData.taskID);
      this.setData({
        has_run: false,
        taskID: app.globalData.taskID
      });
    } else {
      // this.getCurrentTask(-1);
      // this.setData({
      //   has_run: false,
      //   taskID: this.data.taskData[0].id
      // });
    }
  },
  run: function(event){
    app.globalData.taskID = false;
    this.setData({
      loading: true,
      btn_loading:true,
      has_run:false
    });
    var that = this;
    wx.request({
      url: app.globalData.automationBase + "/v1/interface/spider/batch",
      method: 'POST',
      data:{
        task_id: that.data.taskID
      },
      header: {
        "Content-Type": "application/json"
      },
      success: function (res) {
        if(res.data.error_code){
           Notify('用例数据错误请前往PC端编辑');

          that.setData({
            loading: false,
            btn_loading: false
          });
        }else{
          that.setData({
            result: res.data
          });
          var _self = that;
          wx.request({
            url: app.globalData.automationBase + "/v1/interface/searchCase",
            method: 'POST',
            data: {
              task_id: that.data.taskID
            },
            header: {
              "Content-Type": "application/json"
            },
            success: function (res) {
              var case_reslut = [];
              for(var c in res.data.data){
                case_reslut.push(res.data.data[c]);
              }
                _self.setData({
                  case_reslut: case_reslut,
                  page: res.data.page,
                  pages: res.data.pages,
                  total: res.data.total,
                  btn_loading: false,
                  has_run: true,
                  loading:false
                });
            },
            fail: function (error) {
              // fail
              console.log(error)
            }
        
          })
        }
      },
      fail: function (error) {
        // fail
        console.log(error)
      }

    })
  },
  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {
    app.globalData.taskID = false;
    console.log(app.globalData.taskID);
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {
    if(this.data.has_run){
      if(this.data.page==this.data.pages){
        Toast('没有更多啦~');
        const toast = Toast({
          duration: 1000,   
          message: '没有更多啦~',
          position:'bottom',
        });
      }else{
        var that = this;
        wx.request({
          url: app.globalData.automationBase + "/v1/interface/searchCase",
          method: 'POST',
          data: {
            task_id: that.data.taskID,
            page: that.data.page+1,
          },
          header: {
            "Content-Type": "application/json"
          },
          success: function (res) {
            var case_reslut = [];
            for (var c in res.data.data) {
              case_reslut.push(res.data.data[c]);
            }
            case_reslut = that.data.case_reslut.concat(case_reslut);
            that.setData({
              case_reslut: case_reslut,
              page: res.data.page,
              pages: res.data.pages,
              total: res.data.total,
            });
          },
          fail: function (error) {
            // fail
            console.log(error)
          }

        })
      }
    }
  },
  caseDetail(event){
    var case_id = event.currentTarget.dataset.caseid
    wx.navigateTo({
      url: '../searchCase/caseDetail/caseDetail?case_id=' + case_id,
    })
  },
  toResult(event){
    var c = event.currentTarget.dataset.c
    wx.navigateTo({
      url: 'result/result?expect_result=' + c.expect_result + '&interface_return=' + c.interface_return+'&case_name='+c.case_name,
    })
  }
})