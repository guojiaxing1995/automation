Page({
  data: {
    expect_result: '',
    interface_return: '',
    case_name: ''
  },
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
  }
})