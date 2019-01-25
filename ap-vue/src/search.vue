<template>
    <div id="app">
        <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect" background-color="#545c64" text-color="#fff" active-text-color="#ffd04b">
            <el-menu-item index="1">
                <v-link href="/">
                    <div style="width: 100%">接口测试</div>
                </v-link>
            </el-menu-item>
            <el-menu-item index="2">
                <v-link href="/spiderBatch">
                    <div style="width: 100%">批量执行</div>
                </v-link>
            </el-menu-item>
            <el-menu-item index="3">
                <v-link href="/scheduler">
                    <div style="width: 100%">定时任务</div>
                </v-link>
            </el-menu-item>
            <el-menu-item index="4">
                <v-link href="/report">
                    <div style="width: 100%">执行报告</div>
                </v-link>
            </el-menu-item>
            <el-menu-item index="5">
                <v-link href="/search">
                    <div style="width: 100%">记录查询</div>
                </v-link>
            </el-menu-item>
            <el-menu-item index="6" disabled>消息中心</el-menu-item>
        </el-menu>

        <el-form ref="searchForm" :model="searchForm" label-width="80px">
            <el-row :gutter="10">
                <el-col :span="7" :offset="1">
                    <el-form-item label="URL:" style="font-weight:600">
                        <el-input v-model="searchForm.url" size="large" placeholder="请输入url"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="4">
                    <el-form-item label="用例名称:" style="font-weight:600">
                        <el-input v-model="searchForm.case_name" size="large" placeholder="请输入用例名称"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="4">
                    <el-form-item label="任务名称:" style="font-weight:600">
                        <el-input v-model="searchForm.task_name" size="large" placeholder="请输入任务名称"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="3">
                    <el-form-item label="执行结果:" :value="searchForm.result" style="font-weight:600">
                        <el-select v-model="searchForm.result">
                            <el-option label="全部" value=-1 selected="selected"></el-option>
                            <el-option label="成功" value=1></el-option>
                            <el-option label="失败" value=0></el-option>
                        </el-select>
                    </el-form-item>
                </el-col>
                <el-col :span="4">
                    <el-form-item label="执行人:" style="font-weight:600">
                        <el-input v-model="searchForm.user_name" size="large" placeholder="请输入执行人"></el-input>
                    </el-form-item>
                </el-col>
            </el-row>

            <el-row :gutter="10">

                <el-col :span="7" offset="1">
                    <el-form-item label="执行时间:" style="font-weight:600">
                        <el-date-picker v-model="searchForm.sendDate" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" value-format="yyyy-MM-dd">
                        </el-date-picker>

                    </el-form-item>

                </el-col>
                <el-col :span="4">
                    <el-form-item label="记录类型:" :value="searchForm.is_new" style="font-weight:600">
                        <el-select v-model="searchForm.is_new">
                            <el-option label="全部" value=-1 selected="selected"></el-option>
                            <el-option label="最新记录" value=1></el-option>
                        </el-select>
                    </el-form-item>
                </el-col>

                <el-col :span="2" offset="9">
                    <el-button type="primary" size="medium" @click="handleCurrentChange(1)" icon="el-icon-search"> 搜索</el-button>
                </el-col>

            </el-row>

        </el-form>
        <el-row>
                <div class="grid-content"></div>
        </el-row>
        <div style="text-align: center">
            <div id="table">
                <el-table @row-click="showCaseDetail" :header-cell-style="{background:'#409EFF',color:'#FFFFFF',align:'center'}" v-loading="loading" :row-style="rowStyle" element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading" element-loading-background="rgba(143, 188, 143, 0.8)" :data="tableData" height="485" stripe border style="width: 100%">
                    <el-table-column type="index" label="序号" width="80" align="center">
                    </el-table-column>
                    <el-table-column prop="case_id" label="用例编号" width="140" :show-overflow-tooltip="true" align="center">
                    </el-table-column>
                    <el-table-column prop="case_name" label="用例名称" width="190" :show-overflow-tooltip="true" align="left">
                    </el-table-column>
                    <el-table-column prop="url" label="URL" width="350" :show-overflow-tooltip="true" align="left">
                    </el-table-column>
                    <el-table-column prop="method" label="请求方法" width="140" align="center">
                    </el-table-column>
                    <el-table-column prop="dependent_case" label="依赖用例" width="200" :show-overflow-tooltip="true" align="center">
                    </el-table-column>
                    <el-table-column prop="is_run" label="是否执行" width="80" :show-overflow-tooltip="true" align="center">
                        <template slot-scope="scope">
                            <span v-if="scope.row.is_run">是</span>
                            <span v-else>否</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="actual_result" label="实际结果" width="135" :filters="[{ text: '失败', value: '0' }, { text: '通过', value: '1' }]" :filter-method="filterTag" filter-placement="bottom-end" align="center">
                        <template slot-scope="scope">
                            <el-tag v-if="scope.row.actual_result === '0'" type="danger" size="medium " disable-transitions>失败</el-tag>
                            <el-tag v-if="scope.row.actual_result === '1'" type="success" size="medium " disable-transitions>通过</el-tag>
                        </template>
                    </el-table-column>

                </el-table>

            </div>
        </div>
        <el-row>
            <el-col :span="4" :offset="16">
                <div class="block">
                    <el-pagination @current-change="handleCurrentChange" :page-size="8" layout="total,prev, pager, next, jumper" :total="pagination.total" :current-page="pagination.page">
                    </el-pagination>
                </div>
            </el-col>
        </el-row>

        <div class='popContainer' v-show="this.detailTab">
            <el-scrollbar style="height: 100%;">
                <div class="detailTable" @mouseleave="closeTab" style="overflow:hidden">

                    <div style="margin-top: 25px;margin-bottom:15px;font-size: large">用例详情</div>
                    <table style="table-layout:fixed;word-break: break-all; word-wrap: break-word;">
                        <tr>
                            <td class="td1" style="text-align: right">用例编号:</td>
                            <td style="text-align: left;color: #5b4080;">{{detail.case_id}}</td>
                            <td class="td1" style="text-align: right">用例名称:</td>
                            <td style="text-align: left;color: #5b4080;">{{detail.case_name}}</td>
                            <td class="td1" style="text-align: right">任务名称:</td>
                            <td style="text-align: left;color: #5b4080;">{{detail.task_name}}</td>
                            <td class="td1" style="text-align: right">执行结果:</td>
                            <td style="text-align: left;color: #5b4080;" width="70px">{{detail.actual_result}}</td>
                        </tr>
                        <tr>
                            <td class="td1" style="text-align: right">请求方法:</td>
                            <td style="text-align: left;color: #5b4080;">{{detail.method}}</td>
                            <td class="td1" style="text-align: right">URL:</td>
                            <td style="text-align: left;color: #5b4080;" colspan="5">{{detail.url}}</td>
                        </tr>
                        <tr>
                            <td class="td1" style="text-align: right">是否执行:</td>
                            <td style="text-align: left;color: #5b4080;">{{detail.is_run}}</td>
                            <td class="td1" style="text-align: right">依赖用例:</td>
                            <td style="text-align: left;color: #5b4080;" colspan="3">{{detail.dependent_case}}</td>
                            <td class="td1" style="text-align: right">执行人:</td>
                            <td style="text-align: left;color: #5b4080;">{{detail.user_name}}</td>
                        </tr>
                        <tr>
                            <td class="td1" style="text-align: right;">后置处理:</td>
                            <td style="text-align: left;color: #5b4080;">{{detail.deal_method}}</td>
                            <td class="td1" style="text-align: right">处理语句:</td>
                            <td style="text-align: left;color: #5b4080;" colspan="3">{{detail.need_position}}</td>
                            <td class="td1" style="text-align: right">最新记录:</td>
                            <td style="text-align: left;color: #5b4080;">{{detail.is_new}}</td>
                        </tr>
                        <tr style="height: 20px;">
                            <td>提交方式</td>
                            <td colspan="2">header</td>
                            <td colspan="5">data</td>
                        </tr>
                        <tr>
                            <td rowspan="2" style="color: #5b4080;">{{detail.submission}}</td>
                            <td rowspan="2" colspan="2" style="color: #5b4080;">
                                <el-scrollbar style="height: 100%">
                                    <div style="height: 70px;">{{detail.header}}</div>
                                </el-scrollbar>
                            </td>
                            <td rowspan="2" colspan="5" style="color: #5b4080;">
                                <el-scrollbar style="height: 100%">
                                    <div style="width: 96%;height: 70px;">{{detail.data}}</div>
                                </el-scrollbar>
                            </td>
                        </tr>
                        <tr>
                        </tr>
                        <tr style="height: 20px;">
                            <td colspan="3">预期结果</td>
                            <td colspan="5">接口返回</td>
                        </tr>
                        <tr>
                            <td rowspan="3" colspan="3" style="color: #5b4080;">{{detail.expect_result}}</td>
                            <td rowspan="3" colspan="5" style="color: #5b4080;">
                                <el-scrollbar style="height: 100%">
                                    <div style="width: 96%;height: 70px;">{{detail.interface_return}}</div>
                                </el-scrollbar>
                            </td>
                        </tr>

                    </table>
                </div>
            </el-scrollbar>
        </div>

        <div id="footer_min" v-if="minWindow">
          <span>© 2018-2019 automation created by 郭家兴 | 晋ICP备18013433号</span>
        </div>
        <div id="footer" v-else>
          <span>© 2018-2019 automation created by 郭家兴 | 晋ICP备18013433号</span>
        </div>
    </div>
</template>
<script>
import VLink from "./VLink.vue";
export default {
  components: {
    VLink
  },
    mounted() {
    const that = this;
        window.onresize = () => {
            return (() => {
                that.screenHeight = window.innerHeight;
            })()
        }
  },
  watch: {
    screenHeight(val){
      if(this.screenHeight<=745){
          this.minWindow = true;
      }else{
          this.minWindow = false;
      }
      
    }
  },
  data() {
    return {
      minWindow: true,
      screenHeight: window.innerHeight,
      activeIndex: "5",
      detailTab: false,
      detail: {
        actual_result: "",
        case_id: "",
        case_name: "",
        data: "",
        deal_method: "",
        dependent_case: "",
        expect_result: "",
        header: "",
        interface_return: "",
        is_new: "",
        is_run: "",
        method: "",
        need_position: "",
        submission: "",
        task_name: "",
        url: "",
        user_name: ""
      },
      pagination: {
        page: 1,
        pages: 0,
        total: 0
      },
      searchForm: {
        case_name: "",
        url: "",
        result: "-1",
        sendDate: ["2019-02-01", "2019-03-31"],
        is_new: "-1",
        user_name: "",
        task_name: ""
      },
      tableData: []
    };
  },
  mounted: function() {},
  methods: {
    closeTab: function() {
      this.detailTab = false;
    },
    handleCurrentChange(currentPage) {
      const _self = this;
      if (this.searchForm.sendDate[1].indexOf("23:59:59") == -1) {
        this.searchForm.sendDate[1] += " 23:59:59";
      }
      if (this.searchForm.sendDate[0].indexOf("00:00:00") == -1) {
        this.searchForm.sendDate[0] += " 00:00:00";
      }
      this.sendParams = {
        case_name: this.searchForm.case_name,
        page: currentPage,
        user_name: this.searchForm.user_name,
        task_name: this.searchForm.task_name,
        url: this.searchForm.url,
        is_new: this.searchForm.is_new,
        result: this.searchForm.result,
        startDate: this.searchForm.sendDate[0],
        endDate: this.searchForm.sendDate[1]
      };
      $.ajax({
        type: "POST",
        url: window.URL + "/v1/interface/searchCase",
        contentType: "application/json",
        data: JSON.stringify(this.sendParams),
        success: function(r) {
          _self.tableData = r.data;
          _self.pagination.page = r.page;
          _self.pagination.pages = r.pages;
          _self.pagination.total = r.total;
        },
        error: function(r) {}
      });
    },
    showCaseDetail: function(row, event) {
      const loading = this.$loading({
        lock: true,
        text: "Loading",
        spinner: "el-icon-loading",
        background: "rgba(0, 0, 0, 0.7)",
        target: document.querySelector("#app")
      });
      const _self = this;
      $.ajax({
        type: "GET",
        url: window.URL + "/v1/interface/getCaseDetail?id=" + row.id,
        contentType: "application/json",
        success: function(r) {
          _self.detail = r;
          if (r.actual_result == "1") {
            _self.detail.actual_result = "通过";
          } else {
            _self.detail.actual_result = "失败";
          }
          if (r.deal_method == "0") {
            _self.detail.deal_method = "不做处理";
          } else if (r.deal_method == "1") {
            _self.detail.deal_method = "默认处理";
          } else if (r.deal_method == "2") {
            _self.detail.deal_method = "获取key值存储";
          } else {
            _self.detail.deal_method = "正则表达式";
          }
          if (r.is_new == true) {
            _self.detail.is_new = "是";
          } else {
            _self.detail.is_new = "否";
          }
          if (r.is_run == true) {
            _self.detail.is_run = "是";
          } else {
            _self.detail.is_run = "否";
          }
          if (r.submission == "0") {
            _self.detail.submission = "表单提交";
          } else {
            _self.detail.submission = "json提交";
          }
          try {
            if (r.interface_return) {
              _self.detail.interface_return = JSON.stringify(
                JSON.parse(r.interface_return),
                null,
                2
              );
            }
          } catch (e) {}
          if (r.data) {
            _self.detail.data = JSON.stringify(JSON.parse(r.data), null, 2);
          }
          if (r.header) {
            _self.detail.header = JSON.stringify(JSON.parse(r.header), null, 2);
          }

          loading.close();
        },
        error: function(r) {
          if (r.responseJSON.error_code) {
            loading.close();
            _self.openError("未查询到明细");
          }
        }
      });

      this.detailTab = true;
    },
    filterTag(value, row) {
      return row.actual_result === value;
    },
    rowStyle(val) {
        return "cursor: pointer";
      },
    openFullScreen() {
      const loading = this.$loading({
        lock: true,
        text: "Loading",
        spinner: "el-icon-loading",
        background: "rgba(0, 0, 0, 0.7)"
      });
      setTimeout(() => {
        loading.close();
      }, 5000);
    }
  }
};
</script>

<style scoped>
#app {
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB",
    "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
  text-align: center;
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
}
#table {
  display: inline-block;
  margin-top: 15px;
}
.elbtn {
  margin: 0;
}
.el-scrollbar__wrap {
  overflow-x: hidden;
}

.el-row {
  padding-top: 15px;
  margin-left: 0 !important ;
  margin-right: 0 !important ;
}

.grid-content {
  border-radius: 4px;
  min-height: 3px;
  background: #99a9bf;
  width: 94%;
  margin: 0 auto;
}

.box {
  border-radius: 4px;
  background-color: #409eff;
  text-align: center;
  color: #fff;
  box-sizing: border-box;
}

.el-radio-group {
  width: 66.5%;
}

#footer {
  color: #9a9b9c;
  font-weight: 400;
  position: absolute;
  bottom: 4%;
  width: 97%;
  display: flex;
  justify-content: center;
}
#footer_min {
  color: #9a9b9c;
  font-weight: 400;
  margin-top: 15px;
  margin-bottom: 15px;
  margin-bottom: 15px;
  width: 97%;
  display: flex;
  justify-content: center;
}
.elbtn {
  margin: 0;
}
[v-cloak] {
  display: none;
}
.el-col {
  height: 40px;
}
div.popContainer {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
}
div.popContainer2 {
  position: fixed;
  top: 143px;
  left: 0;
  right: 1200px;
  bottom: 70px;
  background: rgba(255, 255, 255, 0.9);
}
.caseForm {
  width: 55%;
  height: 70%;
  overflow: auto;
  margin: auto;
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  background: #ffffff;
}
.taskForm {
  width: 30%;
  height: 45%;
  overflow: auto;
  margin: auto;
  position: absolute;
  top: 0;
  left: 0;
  bottom: 25%;
  right: 0;
  background: #ffffff;
}
.detailTable {
  width: 60%;
  height: 75%;
  overflow: auto;
  margin: auto;
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  background: #ffffff;
}

.active {
  background: rgba(1, 144, 254, 0.51);
  color: #fff;
}
.select {
  background: rgb(1, 144, 254);
  color: #fff;
}
.el-table th {
  -moz-user-select: none;
  text-align: center !important;
}
.el-table__column-filter-trigger i {
  color: #f2f6fc;
}
.el-table th > .cell.highlight {
  color: #ffbd40;
}
.el-table__column-filter-trigger {
  display: inline-block;
  line-height: 23px;
  cursor: pointer;
}
.detailTable table,
th,
td {
  border: 1px solid #ebeef5;
  border-collapse: collapse;
}
.detailTable table {
  width: 85%;
  height: 80%;
  margin: auto;
}
.td1 {
  border-right-style: none;
  width: 85px;
}
.closebtn {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 0;
  background: 0 0;
  border: none;
  outline: 0;
  cursor: pointer;
  font-size: 16px;
}
</style>
